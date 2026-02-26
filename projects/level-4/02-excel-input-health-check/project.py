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
    """Guess the CSV delimiter by counting candidate characters.

    We check comma, tab, semicolon, and pipe across the first few lines.
    The character with the most consistent count wins.
    """
    # WHY these four candidates? -- They cover 99% of real-world CSV dialects.
    # Comma is the default fallback if no clear winner emerges.
    candidates = [",", "\t", ";", "|"]
    best = ","
    best_score = -1

    for char in candidates:
        counts = [line.count(char) for line in sample_lines if line.strip()]
        if not counts:
            continue
        # WHY use min(counts) as the score? -- A real delimiter appears the
        # same number of times in every row. The minimum count across rows
        # filters out characters that appear inconsistently (e.g., commas
        # inside free-text fields).
        if min(counts) > 0 and min(counts) >= best_score:
            best_score = min(counts)
            best = char

    return best


def check_encoding(path: Path) -> dict:
    """Try reading the file as UTF-8; report success or failure."""
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

    # WHY normalize before duplicate check? -- "Name" and "name" would cause
    # subtle bugs when used as dictionary keys, so we treat them as duplicates.
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

    # WHY start=2? -- Row 1 is the header; data rows start at 2
    # so error messages match what users see in their spreadsheet.
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

    # 1. Encoding check
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

    delimiter = detect_delimiter(raw_lines[:10])
    report["detected_delimiter"] = repr(delimiter)

    # 3. Parse as CSV with detected delimiter
    reader = csv.reader(raw_lines, delimiter=delimiter)
    rows = list(reader)

    # 4. Header check
    report["headers"] = check_headers(rows)

    # 5. Row completeness
    report["completeness"] = check_row_completeness(rows)

    # 6. Empty columns
    report["empty_columns"] = check_empty_columns(rows)

    # WHY a three-tier status (OK/WARN/FAIL)? -- FAIL means the file is
    # unreadable; WARN means it loads but has quality issues; OK means clean.
    # This lets downstream tools decide whether to proceed or stop.
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
