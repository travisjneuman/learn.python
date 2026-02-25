"""Level 4 / Project 03 — Robust CSV Ingestor.

Ingests CSV files with error recovery: bad rows are quarantined to a
separate file instead of crashing the pipeline. Good rows are written
to a clean output CSV. A summary report tracks what happened.
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

# ---------- ingestion logic ----------


def validate_row(row: list[str], expected_columns: int, row_num: int) -> str | None:
    """Validate a single CSV row. Returns an error message or None if valid.

    Checks:
    1. Correct number of columns.
    2. No completely empty rows.
    3. No rows where every field is blank.
    """
    if len(row) != expected_columns:
        return f"row {row_num}: expected {expected_columns} columns, got {len(row)}"

    if all(cell.strip() == "" for cell in row):
        return f"row {row_num}: all fields are empty"

    return None


def ingest_csv(
    input_path: Path,
    good_path: Path,
    quarantine_path: Path,
) -> dict:
    """Read a CSV, separate good rows from bad, write both to separate files.

    Returns a summary dict with counts and error details.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    text = input_path.read_text(encoding="utf-8")
    reader = csv.reader(text.splitlines())
    rows = list(reader)

    if not rows:
        return {"total_rows": 0, "good": 0, "quarantined": 0, "errors": []}

    headers = rows[0]
    expected_columns = len(headers)

    good_rows: list[list[str]] = []
    bad_rows: list[list[str]] = []
    errors: list[str] = []

    for idx, row in enumerate(rows[1:], start=2):
        error = validate_row(row, expected_columns, idx)
        if error:
            errors.append(error)
            bad_rows.append([str(idx)] + row)  # prepend row number for traceability
            logging.warning("Quarantined: %s", error)
        else:
            good_rows.append(row)

    # Write clean output
    good_path.parent.mkdir(parents=True, exist_ok=True)
    with good_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(good_rows)

    # Write quarantine file
    quarantine_path.parent.mkdir(parents=True, exist_ok=True)
    with quarantine_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["original_row_num"] + headers)
        writer.writerows(bad_rows)

    summary = {
        "total_rows": len(rows) - 1,  # exclude header
        "good": len(good_rows),
        "quarantined": len(bad_rows),
        "errors": errors,
    }
    return summary


def run(
    input_path: Path,
    output_dir: Path,
) -> dict:
    """Full ingestion run: ingest, quarantine bad rows, write report."""
    good_path = output_dir / "clean_data.csv"
    quarantine_path = output_dir / "quarantined_rows.csv"
    report_path = output_dir / "ingestion_report.json"

    summary = ingest_csv(input_path, good_path, quarantine_path)

    report_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info(
        "Ingestion complete — %d good, %d quarantined",
        summary["good"],
        summary["quarantined"],
    )
    return summary

# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest CSV with error recovery")
    parser.add_argument("--input", default="data/sample_input.csv")
    parser.add_argument("--output-dir", default="data/output")
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    summary = run(Path(args.input), Path(args.output_dir))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
