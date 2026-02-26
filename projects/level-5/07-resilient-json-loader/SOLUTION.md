# Resilient JSON Loader — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Level 5 / Project 07 — Resilient JSON Loader.

Loads JSON files with fallbacks, retries, and partial recovery.
Handles: malformed JSON, missing files, encoding issues, and
truncated files.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

# ---------- logging ----------

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- load helpers ----------

def read_text_safe(path: Path) -> tuple[str | None, str | None]:
    """Read file text, trying UTF-8 first then Latin-1 as fallback."""
    if not path.exists():
        return None, f"file not found: {path}"
    try:
        return path.read_text(encoding="utf-8"), None
    except UnicodeDecodeError:
        pass
    # WHY Latin-1 fallback? -- Latin-1 never raises UnicodeDecodeError
    # because it maps every byte (0x00-0xFF) to a character. The decoded
    # text may have garbled characters, but at least the JSON parser can
    # attempt recovery.
    try:
        text = path.read_text(encoding="latin-1")
        logging.warning("Fell back to latin-1 encoding for %s", path)
        return text, None
    except OSError as exc:
        return None, f"read error: {exc}"


def try_load_json(path: Path) -> tuple[object | None, str | None]:
    """Try to load a JSON file. Returns (data, error_message).

    WHY return a tuple instead of raising? -- The caller needs to try
    multiple sources (primary, fallbacks, repair). Exceptions would
    require nested try/except blocks. Tuples let the caller check
    success with a simple `if data is not None`.
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
# Lines (one object per line) instead of a proper array.

TRAILING_COMMA_PATTERNS: list[tuple[str, str]] = [
    (",]", "]"),
    (",}", "}"),
    (",\n]", "\n]"),
    (",\n}", "\n}"),
    (",\r\n]", "\r\n]"),
    (",\r\n}", "\r\n}"),
]


def try_repair_json(text: str) -> object | None:
    """Attempt to repair common JSON issues and return parsed data."""
    # Strategy 1 — remove trailing commas (the most common mistake)
    cleaned = text
    for old, new in TRAILING_COMMA_PATTERNS:
        cleaned = cleaned.replace(old, new)
    try:
        data = json.loads(cleaned)
        logging.info("Repair succeeded: removed trailing commas")
        return data
    except json.JSONDecodeError:
        pass

    # Strategy 2 — parse as JSON Lines (one JSON object per line)
    # WHY: Some tools (log aggregators, streaming APIs) output one JSON
    # object per line instead of wrapping them in an array.
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

    WHY this order? -- The primary file is the freshest data. Fallbacks
    are stale but valid. Repair is a last resort because repaired data
    may have lost information (e.g., a truncated final record).
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

    # All strategies exhausted — return empty list rather than crashing
    return [], {"source": None, "method": "none", "error": "all sources failed"}

# ---------- pipeline ----------

def run(
    primary_path: Path,
    output_path: Path,
    fallback_paths: list[Path] | None = None,
) -> dict:
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
    parser = argparse.ArgumentParser(description="Load JSON with fallbacks and repair")
    parser.add_argument("--input", default="data/primary.json")
    parser.add_argument("--fallback", default="data/backup.json")
    parser.add_argument("--output", default="data/loaded_data.json")
    return parser.parse_args()

def main() -> None:
    configure_logging()
    args = parse_args()
    fallbacks = [Path(args.fallback)] if args.fallback else []
    report = run(Path(args.input), Path(args.output), fallbacks)
    print(json.dumps(report["load_status"], indent=2))

if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Return `(data, error)` tuples instead of raising | The caller tries multiple sources in sequence. Tuples make success/failure checks simple (`if data is not None`) without nested try/except blocks. |
| Fallback chain order: primary -> backup -> repair | The primary file has the freshest data. Backups are stale but structurally valid. Repair is last because it may lose or corrupt partial records. |
| Latin-1 encoding fallback | Latin-1 maps every single byte to a character, so it never raises `UnicodeDecodeError`. The text may be garbled, but at least JSON parsing can be attempted. |
| Return empty list on total failure | Returning `[]` instead of raising lets downstream code handle "no data" gracefully. The status dict records the failure for operator review. |

## Alternative Approaches

### Using exception chaining for richer error context

```python
def load_json_strict(path: Path) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise
    except UnicodeDecodeError as e:
        raise ValueError(f"Encoding error in {path}") from e
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}") from e
```

Exception chaining (the `from e` syntax) preserves the original error while wrapping it in a more descriptive message. This is cleaner when you do not need a fallback chain and want errors to propagate up immediately.

## Common Pitfalls

1. **Trailing commas are valid in JavaScript but not JSON** — Many developers add trailing commas from habit. `[1, 2, 3,]` is invalid JSON. The repair heuristic strips these, but the best fix is to validate upstream data.
2. **Assuming UTF-8 everywhere** — Files from legacy systems or Windows tools often use Latin-1, Windows-1252, or other encodings. Without the encoding fallback, `read_text(encoding="utf-8")` raises `UnicodeDecodeError` and the entire load fails.
3. **Repairing corrupted data silently** — If repair succeeds, the loaded data may be subtly wrong (e.g., a truncated final record is missing). Always log when repair is used so operators know the data quality is degraded.
