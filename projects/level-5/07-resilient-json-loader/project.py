"""Level 5 / Project 07 — Resilient JSON Loader.

Loads JSON files with fallbacks, retries, and partial recovery.
Handles: malformed JSON, missing files, encoding issues, and
truncated files.  Falls back to backup files when primary fails.

Concepts practiced:
- Graceful error recovery with multiple fallback strategies
- JSON repair heuristics (trailing commas, JSON Lines)
- Encoding detection and fallback (UTF-8 -> Latin-1)
- Structured status reporting for load operations
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path


# ---------- logging ----------

def configure_logging() -> None:
    """Set up logging so every load attempt is traceable."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


# ---------- load helpers ----------

def read_text_safe(path: Path) -> tuple[str | None, str | None]:
    """Read file text, trying UTF-8 first then Latin-1 as fallback.

    Returns (text, error_message).  On success error_message is None.
    """
    if not path.exists():
        return None, f"file not found: {path}"
    try:
        return path.read_text(encoding="utf-8"), None
    except UnicodeDecodeError:
        pass
    # WHY Latin-1 fallback? -- Latin-1 never raises UnicodeDecodeError
    # because it maps every single byte (0x00-0xFF) to a character.
    # The decoded text may contain garbled characters, but at least
    # the file loads so the JSON parser can attempt recovery.
    try:
        text = path.read_text(encoding="latin-1")
        logging.warning("Fell back to latin-1 encoding for %s", path)
        return text, None
    except OSError as exc:
        return None, f"read error: {exc}"


def try_load_json(path: Path) -> tuple[object | None, str | None]:
    """Try to load a JSON file.  Returns (data, error_message).

    Attempts UTF-8 first, falls back to Latin-1 for encoding, then
    parses the text as JSON.
    """
    text, err = read_text_safe(path)
    if text is None:
        return None, err
    try:
        return json.loads(text), None
    except json.JSONDecodeError as exc:
        return None, f"JSON parse error in {path}: {exc}"


# ---------- repair heuristics ----------

# WHY repair heuristics? -- In real pipelines, upstream systems often
# produce slightly invalid JSON: editors add trailing commas, truncated
# network transfers cut files mid-value, and some tools output JSON
# Lines (one object per line) instead of a proper array. Fixing these
# automatically saves hours of manual debugging.

TRAILING_COMMA_PATTERNS: list[tuple[str, str]] = [
    (",]", "]"),
    (",}", "}"),
    (",\n]", "\n]"),
    (",\n}", "\n}"),
    (",\r\n]", "\r\n]"),
    (",\r\n}", "\r\n}"),
]


def try_repair_json(text: str) -> object | None:
    """Attempt to repair common JSON issues and return parsed data.

    Strategy 1: Remove trailing commas (the most common mistake).
    Strategy 2: Parse as JSON Lines (one JSON object per line).
    Returns None if all repair strategies fail.
    """
    # Strategy 1 — trailing commas
    cleaned = text
    for old, new in TRAILING_COMMA_PATTERNS:
        cleaned = cleaned.replace(old, new)
    try:
        data = json.loads(cleaned)
        logging.info("Repair succeeded: removed trailing commas")
        return data
    except json.JSONDecodeError:
        pass

    # Strategy 2 — JSON Lines
    entries: list[object] = []
    for line_num, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            logging.debug("JSON Lines: skipped unparseable line %d", line_num)
            continue

    if entries:
        logging.info("Repair succeeded: parsed %d JSON Lines entries", len(entries))
        return entries

    return None


# ---------- fallback loading ----------


def load_with_fallbacks(
    primary: Path,
    fallbacks: list[Path],
) -> tuple[object, dict]:
    """Try primary, then each fallback, then repair.

    Returns (data, status_dict) where status_dict records which
    source and method succeeded (or that all sources failed).
    """
    # 1. Try primary file as-is
    data, err = try_load_json(primary)
    if data is not None:
        return data, {"source": str(primary), "method": "primary", "error": None}
    logging.warning("Primary load failed: %s", err)

    # 2. Try each fallback file in order
    for fb_path in fallbacks:
        data, fb_err = try_load_json(fb_path)
        if data is not None:
            logging.info("Loaded from fallback: %s", fb_path)
            return data, {"source": str(fb_path), "method": "fallback", "error": None}
        logging.warning("Fallback %s also failed: %s", fb_path, fb_err)

    # 3. Try repairing the primary file
    if primary.exists():
        text, _ = read_text_safe(primary)
        if text is not None:
            repaired = try_repair_json(text)
            if repaired is not None:
                return repaired, {"source": str(primary), "method": "repair", "error": None}

    # All strategies exhausted
    return [], {"source": None, "method": "none", "error": "all sources failed"}


# ---------- pipeline ----------


def run(
    primary_path: Path,
    output_path: Path,
    fallback_paths: list[Path] | None = None,
) -> dict:
    """Full load pipeline: try primary, fallbacks, repair, then write output."""
    data, status = load_with_fallbacks(primary_path, fallback_paths or [])
    record_count = len(data) if isinstance(data, list) else 1

    report = {
        "records_loaded": record_count,
        "load_status": status,
        "data": data,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info("Loaded %d records via %s", record_count, status["method"])
    return report


# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the resilient loader."""
    parser = argparse.ArgumentParser(
        description="Load JSON with fallbacks and repair",
    )
    parser.add_argument("--input", default="data/primary.json", help="Primary JSON file")
    parser.add_argument("--fallback", default="data/backup.json", help="Fallback JSON file")
    parser.add_argument("--output", default="data/loaded_data.json", help="Output path")
    return parser.parse_args()


def main() -> None:
    """Entry point: configure logging, parse args, run the loader."""
    configure_logging()
    args = parse_args()
    fallbacks = [Path(args.fallback)] if args.fallback else []
    report = run(Path(args.input), Path(args.output), fallbacks)
    print(json.dumps(report["load_status"], indent=2))


if __name__ == "__main__":
    main()
