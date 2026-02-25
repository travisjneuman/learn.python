"""Level 5 / Project 08 — Cross-File Joiner.

Joins records across multiple CSV/JSON files by a shared key field.
Supports inner join, left join, and full outer join strategies.

Concepts practiced:
- Dictionary-based indexing for fast lookups
- Multiple join strategies (inner, left, full outer)
- Loading heterogeneous file formats (CSV and JSON)
- Handling missing keys and duplicate records
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path


# ---------- logging ----------

def configure_logging() -> None:
    """Set up logging so every join operation is traceable."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


# ---------- file loading ----------


def load_file(path: Path) -> list[dict]:
    """Load a CSV or JSON file into a list of dicts based on extension.

    CSV files are parsed with DictReader (first row = headers).
    JSON files must contain a top-level array of objects.
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if path.suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError(f"JSON file must contain an array: {path}")
        return data

    # Default: treat as CSV
    text = path.read_text(encoding="utf-8")
    return list(csv.DictReader(text.splitlines()))


def validate_key_exists(records: list[dict], key: str, source_name: str) -> None:
    """Verify that at least one record contains the join key.

    Raises ValueError with a helpful message if the key is missing
    from all records, so the user knows which file is the problem.
    """
    if records and not any(key in r for r in records):
        available = sorted(records[0].keys()) if records else []
        raise ValueError(
            f"Join key '{key}' not found in {source_name}. "
            f"Available columns: {available}"
        )


# ---------- indexing ----------


def index_by_key(records: list[dict], key: str) -> dict[str, dict]:
    """Build a lookup dictionary indexed by the value of *key*.

    If duplicate key values exist, the last record wins.  Empty key
    values are skipped with a warning.
    """
    index: dict[str, dict] = {}
    duplicates = 0

    for record in records:
        key_value = str(record.get(key, "")).strip()
        if not key_value:
            continue
        if key_value in index:
            duplicates += 1
        index[key_value] = record

    if duplicates:
        logging.warning("Found %d duplicate key values (last-wins policy)", duplicates)

    return index


# ---------- join strategies ----------


def join_inner(left: dict[str, dict], right: dict[str, dict]) -> list[dict]:
    """Inner join: only keys present in both sides are included."""
    result: list[dict] = []
    for key in left:
        if key in right:
            result.append({**left[key], **right[key]})
    return result


def join_left(left: dict[str, dict], right: dict[str, dict]) -> list[dict]:
    """Left join: all records from left, matched fields from right.

    Unmatched right-side fields are omitted (the row only has left data).
    """
    result: list[dict] = []
    for key, row in left.items():
        if key in right:
            result.append({**row, **right[key]})
        else:
            result.append(dict(row))
    return result


def join_full(left: dict[str, dict], right: dict[str, dict]) -> list[dict]:
    """Full outer join: all records from both sides.

    Keys present in only one side appear with that side's data only.
    """
    all_keys = sorted(set(left.keys()) | set(right.keys()))
    result: list[dict] = []
    for key in all_keys:
        merged: dict = {}
        if key in left:
            merged.update(left[key])
        if key in right:
            merged.update(right[key])
        result.append(merged)
    return result


# Map strategy names to functions for clean dispatch.
JOIN_STRATEGIES: dict[str, callable] = {
    "inner": join_inner,
    "left": join_left,
    "full": join_full,
}


# ---------- pipeline ----------


def run(
    left_path: Path,
    right_path: Path,
    output_path: Path,
    key: str,
    strategy: str = "inner",
) -> dict:
    """Load both files, index by key, join, and write the result."""
    left_data = load_file(left_path)
    right_data = load_file(right_path)

    validate_key_exists(left_data, key, str(left_path))
    validate_key_exists(right_data, key, str(right_path))

    left_idx = index_by_key(left_data, key)
    right_idx = index_by_key(right_data, key)

    join_func = JOIN_STRATEGIES.get(strategy, join_inner)
    joined = join_func(left_idx, right_idx)

    # Build a summary that includes match statistics.
    matched_keys = set(left_idx.keys()) & set(right_idx.keys())
    left_only = set(left_idx.keys()) - set(right_idx.keys())
    right_only = set(right_idx.keys()) - set(left_idx.keys())

    report = {
        "left_records": len(left_data),
        "right_records": len(right_data),
        "joined_records": len(joined),
        "strategy": strategy,
        "matched_keys": len(matched_keys),
        "left_only_keys": len(left_only),
        "right_only_keys": len(right_only),
        "data": joined,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info(
        "%s join: %d matched rows on key '%s'",
        strategy.capitalize(),
        len(joined),
        key,
    )
    return report


# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the cross-file joiner."""
    parser = argparse.ArgumentParser(
        description="Join records across files by a shared key",
    )
    parser.add_argument("--left", default="data/employees.csv", help="Left-side file")
    parser.add_argument("--right", default="data/departments.csv", help="Right-side file")
    parser.add_argument("--output", default="data/joined.json", help="Output path")
    parser.add_argument("--key", default="dept_id", help="Join key column name")
    parser.add_argument(
        "--join",
        choices=["inner", "left", "full"],
        default="inner",
        help="Join strategy",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point: configure logging, parse args, run the joiner."""
    configure_logging()
    args = parse_args()
    report = run(Path(args.left), Path(args.right), Path(args.output), args.key, args.join)
    print(f"{args.join.capitalize()} join: {report['joined_records']} matched rows on key '{args.key}'")


if __name__ == "__main__":
    main()
