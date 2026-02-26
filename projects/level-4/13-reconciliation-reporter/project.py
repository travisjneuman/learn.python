"""Level 4 / Project 13 — Reconciliation Reporter.

Compares two datasets (source vs target) by a key field and reports
differences: records only in source, only in target, and records
present in both but with differing values.
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

# ---------- comparison logic ----------


def load_csv_as_dict(path: Path, key_field: str) -> dict[str, dict]:
    """Load a CSV into a dict keyed by the specified field.

    WHY key by a field? -- Indexing rows by a unique key (like "id") lets
    us look up matching records in O(1) instead of scanning the entire
    list for each comparison. This is what makes reconciliation fast.

    Raises ValueError if key_field is not in the CSV headers.
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    text = path.read_text(encoding="utf-8")
    reader = csv.DictReader(text.splitlines())
    headers = reader.fieldnames or []

    if key_field not in headers:
        raise ValueError(f"Key field '{key_field}' not found in headers: {headers}")

    result: dict[str, dict] = {}
    for row in reader:
        key_value = row[key_field]
        if key_value in result:
            logging.warning("Duplicate key '%s' in %s — last row wins", key_value, path)
        result[key_value] = dict(row)

    return result


def reconcile(
    source: dict[str, dict],
    target: dict[str, dict],
    compare_fields: list[str] | None = None,
) -> dict:
    """Compare source and target datasets by key.

    Returns:
        {
            "only_in_source": [keys],
            "only_in_target": [keys],
            "mismatches": [{"key": str, "differences": {field: {"source": v, "target": v}}}],
            "matched": int
        }
    """
    # WHY set operations? -- Set difference and intersection are the natural
    # way to express "only in A," "only in B," and "in both." Python's set
    # operators (-, &) make this intent clear and run in O(n) time.
    source_keys = set(source.keys())
    target_keys = set(target.keys())

    only_source = sorted(source_keys - target_keys)
    only_target = sorted(target_keys - source_keys)
    common = source_keys & target_keys

    mismatches: list[dict] = []
    matched = 0

    for key in sorted(common):
        src_row = source[key]
        tgt_row = target[key]

        # Determine which fields to compare
        fields = compare_fields or [
            f for f in src_row.keys() if f in tgt_row
        ]

        diffs: dict[str, dict] = {}
        for field in fields:
            src_val = src_row.get(field, "")
            tgt_val = tgt_row.get(field, "")
            if src_val != tgt_val:
                diffs[field] = {"source": src_val, "target": tgt_val}

        if diffs:
            mismatches.append({"key": key, "differences": diffs})
        else:
            matched += 1

    return {
        "only_in_source": only_source,
        "only_in_target": only_target,
        "mismatches": mismatches,
        "matched": matched,
    }

# ---------- runner ----------


def run(
    source_path: Path,
    target_path: Path,
    output_path: Path,
    key_field: str,
    compare_fields: list[str] | None = None,
) -> dict:
    """Full reconciliation: load both files, compare, write report."""
    source = load_csv_as_dict(source_path, key_field)
    target = load_csv_as_dict(target_path, key_field)
    report = reconcile(source, target, compare_fields)

    report["summary"] = {
        "source_records": len(source),
        "target_records": len(target),
        "only_in_source": len(report["only_in_source"]),
        "only_in_target": len(report["only_in_target"]),
        "mismatches": len(report["mismatches"]),
        "matched": report["matched"],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info(
        "Reconciliation: %d matched, %d mismatches, %d source-only, %d target-only",
        report["matched"], len(report["mismatches"]),
        len(report["only_in_source"]), len(report["only_in_target"]),
    )
    return report

# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two datasets and report differences")
    parser.add_argument("--source", default="data/source.csv")
    parser.add_argument("--target", default="data/target.csv")
    parser.add_argument("--output", default="data/reconciliation_report.json")
    parser.add_argument("--key", default="id", help="Key field for matching records")
    parser.add_argument("--fields", default="", help="Comma-separated fields to compare (empty = all)")
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    compare_fields = [f.strip() for f in args.fields.split(",") if f.strip()] or None
    report = run(Path(args.source), Path(args.target), Path(args.output), args.key, compare_fields)
    print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__":
    main()
