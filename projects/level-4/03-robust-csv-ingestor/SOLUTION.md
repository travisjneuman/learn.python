# Robust CSV Ingestor — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
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
    """Validate a single CSV row. Returns an error message or None if valid."""
    # WHY: Column count is the most fundamental check — if a row has the
    # wrong number of fields, the data is structurally broken and cannot
    # be reliably mapped to headers.
    if len(row) != expected_columns:
        return f"row {row_num}: expected {expected_columns} columns, got {len(row)}"

    # WHY: All-empty rows are usually blank lines in the source file.
    # They carry no data and would create misleading records downstream.
    if all(cell.strip() == "" for cell in row):
        return f"row {row_num}: all fields are empty"

    return None


def ingest_csv(
    input_path: Path,
    good_path: Path,
    quarantine_path: Path,
) -> dict:
    """Read a CSV, separate good rows from bad, write both to separate files."""
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

    # WHY: start=2 so row numbers match what a human sees in a spreadsheet
    # (row 1 = header, row 2 = first data row).
    for idx, row in enumerate(rows[1:], start=2):
        error = validate_row(row, expected_columns, idx)
        if error:
            errors.append(error)
            # WHY: Prepend the original row number so humans reviewing
            # the quarantine file can trace bad rows back to the source
            # without manually recounting lines.
            bad_rows.append([str(idx)] + row)
            logging.warning("Quarantined: %s", error)
        else:
            good_rows.append(row)

    # WHY: Write clean and quarantine as separate files so the clean output
    # can feed directly into the next pipeline stage while bad rows get
    # independent manual review.
    good_path.parent.mkdir(parents=True, exist_ok=True)
    with good_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(good_rows)

    quarantine_path.parent.mkdir(parents=True, exist_ok=True)
    with quarantine_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # WHY: Add "original_row_num" as the first column header so the
        # quarantine file is self-documenting.
        writer.writerow(["original_row_num"] + headers)
        writer.writerows(bad_rows)

    summary = {
        "total_rows": len(rows) - 1,  # exclude header
        "good": len(good_rows),
        "quarantined": len(bad_rows),
        "errors": errors,
    }
    return summary


def run(input_path: Path, output_dir: Path) -> dict:
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
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Quarantine bad rows instead of skipping or crashing | Skipping loses data silently. Crashing stops the entire pipeline. Quarantining preserves the bad data for review while letting good data flow through. |
| Prepend original row number to quarantined rows | Traceability — when a human reviews the quarantine file, they need to find the problem in the original file without recounting lines. |
| Write the quarantine file even if it is empty | Downstream tools can rely on the file always existing. Checking "does the quarantine file exist?" vs "is it empty?" are different questions with different answers. |
| Return error strings instead of raising exceptions | Lets the caller accumulate all errors across all rows and decide what to do (log, abort, retry). Exceptions would stop at the first bad row. |

## Alternative Approaches

### Using `csv.DictReader` instead of `csv.reader`

```python
def ingest_with_dictreader(input_path: Path) -> tuple[list[dict], list[dict]]:
    text = input_path.read_text(encoding="utf-8")
    reader = csv.DictReader(text.splitlines())
    good, bad = [], []
    for i, row in enumerate(reader, start=2):
        if any(v is None for v in row.values()):
            bad.append({"row": i, "data": row})
        else:
            good.append(row)
    return good, bad
```

**Trade-off:** `DictReader` automatically maps columns to header names, which is more convenient for downstream code. However, it handles column count mismatches by setting extra values to `None` or grouping them into a `restkey`, which can silently mask structural problems. The raw `csv.reader` approach gives you explicit control over how mismatches are detected and reported.

## Common Pitfalls

1. **Using `newline=""` when opening CSV files for writing** — Without this, Python on Windows may add extra blank lines between rows. The `newline=""` parameter tells Python to let the `csv.writer` handle line endings.
2. **Counting rows from 0 instead of 2** — Users see row 1 as the header in their spreadsheet. If you report "row 0 has an error," they will look at the wrong line. Using `start=2` in `enumerate` matches human expectations.
3. **Not handling the empty-file case** — If the CSV has zero lines, `rows[0]` will raise an `IndexError`. Always check `if not rows` before accessing the header.
