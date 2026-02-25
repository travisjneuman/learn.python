"""Level 4 / Project 11 — Audit Log Enhancer.

Reads raw audit log entries (JSON lines), enriches them with context
(correlation IDs, timing, severity classification), and writes enhanced
logs. Demonstrates structured logging patterns for traceability.
"""

from __future__ import annotations

import argparse
import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path

# ---------- logging ----------

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- enrichment functions ----------


def generate_correlation_id() -> str:
    """Create a unique correlation ID for linking related log entries."""
    return str(uuid.uuid4())[:8]


def classify_severity(event_type: str) -> str:
    """Map event types to severity levels.

    This is a simple keyword-based classifier. In production you would
    use a more sophisticated approach.
    """
    event_lower = event_type.lower()
    if any(w in event_lower for w in ("error", "fail", "crash", "critical")):
        return "HIGH"
    if any(w in event_lower for w in ("warn", "timeout", "retry", "slow")):
        return "MEDIUM"
    return "LOW"


def compute_duration_ms(start: str | None, end: str | None) -> int | None:
    """Calculate duration between two ISO timestamps in milliseconds.

    Returns None if either timestamp is missing or unparseable.
    """
    if not start or not end:
        return None
    try:
        t_start = datetime.fromisoformat(start)
        t_end = datetime.fromisoformat(end)
        delta = t_end - t_start
        return int(delta.total_seconds() * 1000)
    except (ValueError, TypeError):
        return None


def enrich_entry(entry: dict, correlation_id: str) -> dict:
    """Add enrichment fields to a single audit log entry.

    Adds: correlation_id, severity, duration_ms, enriched_at timestamp.
    """
    enriched = dict(entry)  # shallow copy — don't mutate the original

    enriched["correlation_id"] = correlation_id
    enriched["severity"] = classify_severity(entry.get("event_type", ""))
    enriched["duration_ms"] = compute_duration_ms(
        entry.get("start_time"), entry.get("end_time")
    )
    enriched["enriched_at"] = datetime.now(timezone.utc).isoformat()

    return enriched

# ---------- pipeline ----------


def load_log_entries(path: Path) -> list[dict]:
    """Load JSON-lines formatted audit log (one JSON object per line)."""
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")

    entries: list[dict] = []
    for line_num, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            logging.warning("Skipping malformed JSON at line %d", line_num)

    return entries


def enrich_log(entries: list[dict]) -> list[dict]:
    """Enrich all entries, grouping by session_id for correlation."""
    # Group entries by session_id (if present) for shared correlation IDs
    session_correlations: dict[str, str] = {}
    enriched: list[dict] = []

    for entry in entries:
        session = entry.get("session_id", "")
        if session and session not in session_correlations:
            session_correlations[session] = generate_correlation_id()

        corr_id = session_correlations.get(session, generate_correlation_id())
        enriched.append(enrich_entry(entry, corr_id))

    return enriched

# ---------- runner ----------


def run(input_path: Path, output_path: Path) -> dict:
    """Full enrichment run: load raw logs, enrich, write enhanced logs."""
    entries = load_log_entries(input_path)
    enriched = enrich_log(entries)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    # Write as JSON lines (one per line) for streaming compatibility
    with output_path.open("w", encoding="utf-8") as f:
        for entry in enriched:
            f.write(json.dumps(entry) + "\n")

    summary = {
        "total_entries": len(entries),
        "enriched": len(enriched),
        "severity_counts": {},
    }
    for e in enriched:
        sev = e.get("severity", "UNKNOWN")
        summary["severity_counts"][sev] = summary["severity_counts"].get(sev, 0) + 1

    logging.info("Enriched %d log entries", len(enriched))
    return summary

# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Enrich audit logs with context and timing")
    parser.add_argument("--input", default="data/sample_input.jsonl")
    parser.add_argument("--output", default="data/enriched_logs.jsonl")
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    summary = run(Path(args.input), Path(args.output))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
