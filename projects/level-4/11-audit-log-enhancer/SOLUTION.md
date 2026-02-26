# Audit Log Enhancer — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
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
    """Create a unique correlation ID for linking related log entries.

    WHY only 8 characters? A full UUID is 36 chars and clutters log output.
    The first 8 hex digits give ~4 billion unique values, which is more
    than enough for correlating entries within a single run.
    """
    return str(uuid.uuid4())[:8]


def classify_severity(event_type: str) -> str:
    """Map event types to severity levels.

    WHY keyword-based classification? It is simple, transparent, and covers
    the most common patterns. In production you might use a configurable
    mapping or machine learning, but keyword matching is the right starting
    point.
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
    # WHY: Return None rather than 0 for missing/invalid timestamps.
    # None signals "unknown" to downstream code, while 0 would falsely
    # suggest the operation was instantaneous.
    if not start or not end:
        return None
    try:
        t_start = datetime.fromisoformat(start)
        t_end = datetime.fromisoformat(end)
        delta = t_end - t_start
        # WHY: total_seconds() returns a float with microsecond precision.
        # Multiplying by 1000 converts to milliseconds, the standard unit
        # for operation durations in logging.
        return int(delta.total_seconds() * 1000)
    except (ValueError, TypeError):
        return None


def enrich_entry(entry: dict, correlation_id: str) -> dict:
    """Add enrichment fields to a single audit log entry."""
    # WHY: Shallow copy adds new keys but does not modify existing values.
    # Mutating the original would break callers that compare before/after
    # or need to retry enrichment.
    enriched = dict(entry)

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
            # WHY: Skip malformed lines instead of crashing. Real log files
            # often contain partial writes from crashed processes. Logging
            # the warning preserves visibility into the problem.
            logging.warning("Skipping malformed JSON at line %d", line_num)

    return entries


def enrich_log(entries: list[dict]) -> list[dict]:
    """Enrich all entries, grouping by session_id for correlation."""
    # WHY: Entries with the same session_id share a correlation ID so you
    # can trace an entire user session across multiple log entries.
    session_correlations: dict[str, str] = {}
    enriched: list[dict] = []

    for entry in entries:
        session = entry.get("session_id", "")
        if session and session not in session_correlations:
            session_correlations[session] = generate_correlation_id()

        # WHY: If there is no session_id, generate a unique correlation
        # ID per entry. This ensures every entry has a correlation ID
        # for consistent downstream processing.
        corr_id = session_correlations.get(session, generate_correlation_id())
        enriched.append(enrich_entry(entry, corr_id))

    return enriched

# ---------- runner ----------


def run(input_path: Path, output_path: Path) -> dict:
    """Full enrichment run: load raw logs, enrich, write enhanced logs."""
    entries = load_log_entries(input_path)
    enriched = enrich_log(entries)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    # WHY: JSON Lines instead of a JSON array. JSONL lets you append new
    # entries without reading the entire file, and tools like jq, grep, and
    # streaming processors can handle one line at a time.
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
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Correlation IDs grouped by session_id | Lets you trace all actions within a user session as a single unit. Without correlation, debugging a "user reports slow page" requires manually matching timestamps and user IDs across thousands of log entries. |
| Truncated UUID (8 chars) instead of full UUID | Reduces log line clutter without sacrificing practical uniqueness. 8 hex characters = 4 billion possible values, which vastly exceeds the number of sessions in any single pipeline run. |
| JSON Lines format for output | JSONL supports append-only writes, streaming processing, and line-by-line tools (grep, jq). A JSON array requires reading and re-serializing the entire file to add one entry. |
| Shallow copy in `enrich_entry` | Preserves the original entry for comparison, retry, or audit purposes. If enrichment fails, the original data is still intact. |

## Alternative Approaches

### Using Python's `logging` module with custom formatters

```python
import logging

class AuditFormatter(logging.Formatter):
    def format(self, record):
        entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "correlation_id": getattr(record, "correlation_id", ""),
        }
        return json.dumps(entry)
```

**Trade-off:** Using Python's built-in logging infrastructure gives you free rotation, handlers, and log levels. However, it conflates application logging with audit log processing. The solution's approach treats audit logs as data to be processed, not as program output, which is the right abstraction for a data pipeline.

### Using `collections.Counter` for severity counting

```python
from collections import Counter

severity_counts = Counter(e["severity"] for e in enriched)
```

**Trade-off:** `Counter` is cleaner and more Pythonic than manual dictionary counting. It is a better choice in production code. The manual approach in the solution is used to demonstrate how counting works at the dict level, which is the pedagogical goal at this level.

## Common Pitfalls

1. **Assuming all timestamps have timezone info** — `datetime.fromisoformat("2025-01-15T10:30:00")` produces a naive datetime (no timezone). Subtracting a naive from an aware datetime raises a `TypeError`. Handle timezone-naive timestamps by assuming UTC or catching the error.
2. **Using `json.load()` instead of line-by-line `json.loads()`** — JSON Lines is NOT valid JSON. `json.load()` expects a single JSON value (object or array), not one JSON object per line. You must read line by line and parse each line separately.
3. **Not handling entries without session_id** — If `session_id` is missing, `entry.get("session_id", "")` returns an empty string. Using `""` as a dictionary key would group all session-less entries under one correlation ID, which is wrong. The solution checks for empty strings and generates unique IDs for those entries.
