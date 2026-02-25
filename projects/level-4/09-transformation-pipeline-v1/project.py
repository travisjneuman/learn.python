"""Level 4 / Project 09 — Transformation Pipeline V1.

Chains data transformations in sequence, with logging at each step.
Each transform is a pure function that takes records and returns records.
The pipeline tracks what changed at each step for auditability.
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

# ---------- transform functions ----------
# Each takes a list of record dicts and returns a new list.
# This functional style keeps transforms composable and testable.


def transform_strip_whitespace(records: list[dict]) -> list[dict]:
    """Strip leading/trailing whitespace from all string values."""
    return [
        {k: v.strip() if isinstance(v, str) else v for k, v in row.items()}
        for row in records
    ]


def transform_lowercase_keys(records: list[dict]) -> list[dict]:
    """Normalize all dictionary keys to lowercase."""
    return [
        {k.lower(): v for k, v in row.items()}
        for row in records
    ]


def transform_add_row_id(records: list[dict]) -> list[dict]:
    """Add a sequential row_id field to each record."""
    return [
        {**row, "row_id": idx}
        for idx, row in enumerate(records, start=1)
    ]


def transform_filter_empty_rows(records: list[dict]) -> list[dict]:
    """Remove records where all values are empty strings."""
    return [
        row for row in records
        if any(str(v).strip() for v in row.values())
    ]


def transform_coerce_numbers(records: list[dict]) -> list[dict]:
    """Try to convert string values that look numeric into int or float."""
    result = []
    for row in records:
        new_row = {}
        for k, v in row.items():
            if isinstance(v, str):
                # Try int first, then float
                try:
                    new_row[k] = int(v)
                    continue
                except ValueError:
                    pass
                try:
                    new_row[k] = float(v)
                    continue
                except ValueError:
                    pass
            new_row[k] = v
        result.append(new_row)
    return result

# ---------- pipeline engine ----------

# Registry of available transforms by name
TRANSFORMS: dict[str, callable] = {
    "strip_whitespace": transform_strip_whitespace,
    "lowercase_keys": transform_lowercase_keys,
    "add_row_id": transform_add_row_id,
    "filter_empty_rows": transform_filter_empty_rows,
    "coerce_numbers": transform_coerce_numbers,
}


def run_pipeline(
    records: list[dict],
    steps: list[str],
) -> tuple[list[dict], list[dict]]:
    """Execute a sequence of named transforms, logging each step.

    Returns (final_records, step_log) where step_log tracks
    the record count after each transform.
    """
    step_log: list[dict] = []
    current = records

    for step_name in steps:
        func = TRANSFORMS.get(step_name)
        if func is None:
            logging.error("Unknown transform: %s — skipping", step_name)
            step_log.append({"step": step_name, "status": "skipped", "reason": "unknown"})
            continue

        before_count = len(current)
        current = func(current)
        after_count = len(current)

        step_log.append({
            "step": step_name,
            "status": "ok",
            "records_before": before_count,
            "records_after": after_count,
        })
        logging.info("Step '%s': %d -> %d records", step_name, before_count, after_count)

    return current, step_log

# ---------- I/O ----------


def load_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Input not found: {path}")
    text = path.read_text(encoding="utf-8")
    return list(csv.DictReader(text.splitlines()))


def run(input_path: Path, output_path: Path, steps: list[str]) -> dict:
    """Load data, run pipeline, write results."""
    records = load_csv(input_path)
    result, step_log = run_pipeline(records, steps)

    report = {
        "input_records": len(records),
        "output_records": len(result),
        "steps": step_log,
        "data": result,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info("Pipeline complete: %d -> %d records", len(records), len(result))
    return report

# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a data transformation pipeline")
    parser.add_argument("--input", default="data/sample_input.csv")
    parser.add_argument("--output", default="data/pipeline_output.json")
    parser.add_argument(
        "--steps",
        default="strip_whitespace,lowercase_keys,filter_empty_rows,coerce_numbers,add_row_id",
        help="Comma-separated transform names",
    )
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    steps = [s.strip() for s in args.steps.split(",")]
    report = run(Path(args.input), Path(args.output), steps)
    print(json.dumps({"steps": report["steps"], "output_records": report["output_records"]}, indent=2))


if __name__ == "__main__":
    main()
