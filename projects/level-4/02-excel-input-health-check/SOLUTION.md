# Excel Input Health Check — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 4 / Project 02 — Excel Input Health Check.

Analyzes CSV/data files for common quality issues: encoding problems,
delimiter inconsistencies, missing headers, empty columns, and row
completeness. Produces a structured health report.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path

# ---------- logging ----------

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- detection helpers ----------


def detect_delimiter(sample_lines: list[str]) -> str:
    """Guess the CSV delimiter by counting candidate characters."""
    # WHY: These four candidates cover 99% of real-world CSV dialects.
    # Comma is the default fallback if no clear winner emerges.
    candidates = [",", "\t", ";", "|"]
    best = ","
    best_score = -1

    for char in candidates:
        counts = [line.count(char) for line in sample_lines if line.strip()]
        if not counts:
            continue
        # WHY: min(counts) filters out characters that appear inconsistently.
        # A real delimiter shows up the same number of times in every row.
        # A comma inside free-text might appear in some rows but not others,
        # so its minimum count across rows would be low or zero.
        if min(counts) > 0 and min(counts) >= best_score:
            best_score = min(counts)
            best = char

    return best


def check_encoding(path: Path) -> dict:
    """Try reading the file as UTF-8; report success or failure."""
    # WHY: Encoding issues are the most common reason CSV processing fails.
    # Checking it first prevents confusing UnicodeDecodeError messages later.
    try:
        path.read_text(encoding="utf-8")
        return {"encoding": "utf-8", "readable": True}
    except UnicodeDecodeError:
        return {"encoding": "unknown", "readable": False}


def check_headers(rows: list[list[str]]) -> dict:
    """Verify the header row has no blanks and no duplicates."""
    if not rows:
        return {"present": False, "issues": ["file is empty"]}

    headers = rows[0]
    issues: list[str] = []

    blanks = [i for i, h in enumerate(headers) if not h.strip()]
    if blanks:
        issues.append(f"blank header(s) at column index(es): {blanks}")

    # WHY: Normalize before duplicate check because "Name" and "name" would
    # cause subtle bugs when used as dictionary keys later.
    seen: set[str] = set()
    for h in headers:
        normalized = h.strip().lower()
        if normalized in seen:
            issues.append(f"duplicate header: '{h.strip()}'")
        seen.add(normalized)

    return {"present": True, "column_count": len(headers), "issues": issues}


def check_row_completeness(rows: list[list[str]]) -> dict:
    """Check whether every data row has the same number of fields as the header."""
    if len(rows) < 2:
        return {"data_rows": 0, "short_rows": [], "long_rows": []}

    expected = len(rows[0])
    short: list[int] = []
    long: list[int] = []

    # WHY: start=2 because row 1 is the header; data rows start at 2 so
    # error messages match what users see in their spreadsheet.
    for idx, row in enumerate(rows[1:], start=2):
        if len(row) < expected:
            short.append(idx)
        elif len(row) > expected:
            long.append(idx)

    return {
        "data_rows": len(rows) - 1,
        "expected_columns": expected,
        "short_rows": short,
        "long_rows": long,
    }


def check_empty_columns(rows: list[list[str]]) -> list[int]:
    """Return column indexes that are entirely empty across all data rows."""
    if len(rows) < 2:
        return []

    col_count = len(rows[0])
    empty_cols: list[int] = []

    # WHY: Check col_idx >= len(row) to handle short rows without crashing.
    for col_idx in range(col_count):
        all_empty = all(
            col_idx >= len(row) or not row[col_idx].strip()
            for row in rows[1:]
        )
        if all_empty:
            empty_cols.append(col_idx)

    return empty_cols

# ---------- main pipeline ----------


def health_check(path: Path) -> dict:
    """Run all health checks on a CSV file and return a combined report."""
    report: dict = {"file": str(path)}

    # 1. Encoding check — gate everything else behind this
    enc = check_encoding(path)
    report["encoding"] = enc
    if not enc["readable"]:
        report["status"] = "FAIL"
        return report

    # 2. Read raw lines for delimiter detection
    raw_lines = path.read_text(encoding="utf-8").splitlines()
    if not raw_lines:
        report["status"] = "FAIL"
        report["reason"] = "file is empty"
        return report

    # WHY: Only sample first 10 lines for delimiter detection — enough to
    # be accurate without reading the entire file.
    delimiter = detect_delimiter(raw_lines[:10])
    report["detected_delimiter"] = repr(delimiter)

    # 3. Parse as CSV with detected delimiter
    reader = csv.reader(raw_lines, delimiter=delimiter)
    rows = list(reader)

    # 4-6. Run all quality checks
    report["headers"] = check_headers(rows)
    report["completeness"] = check_row_completeness(rows)
    report["empty_columns"] = check_empty_columns(rows)

    # WHY: Three-tier status (OK/WARN/FAIL) lets downstream tools decide
    # whether to proceed. FAIL = unreadable. WARN = loads but has issues.
    has_issues = (
        report["headers"].get("issues", [])
        or report["completeness"].get("short_rows", [])
        or report["completeness"].get("long_rows", [])
        or report["empty_columns"]
    )
    report["status"] = "WARN" if has_issues else "OK"

    return report


def run(input_path: Path, output_path: Path) -> dict:
    """Execute health check and persist the report."""
    report = health_check(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info("Health check complete — status=%s", report["status"])
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check CSV/data file health")
    parser.add_argument("--input", default="data/sample_input.csv")
    parser.add_argument("--output", default="data/health_report.json")
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    report = run(Path(args.input), Path(args.output))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Check encoding before anything else | If the file is not UTF-8 readable, all other checks will crash. Fail fast with a clear status instead. |
| Use `min(counts)` for delimiter detection | A real delimiter appears consistently in every row. The minimum count filters out characters that appear only in some rows (like commas inside text fields). |
| Separate header checks from row completeness | Headers are structural metadata (column names), while row completeness is data quality. They have different implications and different fixes. |
| Three-tier status: OK / WARN / FAIL | Gives downstream tools a simple decision point. FAIL means "do not use this file." WARN means "usable but review issues." OK means "clean." |

## Alternative Approaches

### Using Python's `csv.Sniffer` for delimiter detection

```python
import csv

def detect_delimiter_sniffer(sample: str) -> str:
    try:
        dialect = csv.Sniffer().sniff(sample)
        return dialect.delimiter
    except csv.Error:
        return ","  # fallback
```

**Trade-off:** `csv.Sniffer` is built-in and handles more edge cases (like quoted fields containing delimiters), but it can fail on very short samples or unusual files. The manual counting approach in the main solution is more transparent and predictable — you can see exactly why it chose a particular delimiter.

### Using `chardet` for encoding detection

```python
import chardet

def detect_encoding(path: Path) -> str:
    raw = path.read_bytes()
    result = chardet.detect(raw)
    return result["encoding"] or "utf-8"
```

**Trade-off:** `chardet` can identify dozens of encodings (Latin-1, Shift-JIS, etc.) and auto-convert, but it adds an external dependency. The simple UTF-8-or-fail approach works for most modern data pipelines where UTF-8 is the expected standard.

## Common Pitfalls

1. **Using `average` instead of `min` for delimiter scoring** — Averages can be misleading when one row has many commas inside a text field. The minimum count is a better signal for consistency.
2. **Forgetting to handle empty files** — An empty file has no lines, no headers, no rows. Every function must check for `len(rows) < 1` or `len(rows) < 2` before accessing indexes.
3. **Not normalizing headers before duplicate detection** — "Name" and "name" look different as strings but will collide as dictionary keys, causing silent data loss when you use `csv.DictReader`.
