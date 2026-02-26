# Cross-File Joiner — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 5 / Project 08 — Cross-File Joiner.

Joins records across multiple CSV/JSON files by a shared key field.
Supports inner join, left join, and full outer join strategies.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path
from typing import Any, Callable

# ---------- logging ----------

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- file loading ----------

def load_file(path: Path) -> list[dict]:
    """Load a CSV or JSON file into a list of dicts based on extension."""
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    # WHY: Support both formats so the joiner works with heterogeneous
    # data sources (one team exports CSV, another exports JSON).
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

    WHY: A typo in the --key flag would silently produce zero matches
    instead of the expected join. This validation catches the mistake
    early with a helpful error message listing available columns.
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

    WHY index first, then join? -- Indexing both sides into dicts makes
    lookups O(1) instead of scanning the entire right side for every
    left row (O(n*m) down to O(n+m)). This is the same technique
    databases use with hash joins.

    If duplicate key values exist, the last record wins.
    """
    index: dict[str, dict] = {}
    duplicates = 0

    for record in records:
        # WHY: str() + strip() normalizes the key so "101" matches "101 "
        # and integer 101 matches string "101".
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
            # WHY: {**left, **right} merges both dicts. If both sides
            # have a column with the same name, the right side wins.
            result.append({**left[key], **right[key]})
    return result


def join_left(left: dict[str, dict], right: dict[str, dict]) -> list[dict]:
    """Left join: all records from left, matched fields from right."""
    result: list[dict] = []
    for key, row in left.items():
        if key in right:
            result.append({**row, **right[key]})
        else:
            # WHY: Unmatched left rows are still included so no left-side
            # data is lost. This is useful for "show all employees even
            # if their department is unknown."
            result.append(dict(row))
    return result


def join_full(left: dict[str, dict], right: dict[str, dict]) -> list[dict]:
    """Full outer join: all records from both sides."""
    # WHY: sorted(set union) ensures deterministic output order regardless
    # of which keys come from which side.
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


# WHY: A strategy map lets the join type be specified via CLI flag
# without if/elif chains. Adding a new strategy (e.g., "right") only
# requires writing the function and adding one entry.
JOIN_STRATEGIES: dict[str, Callable[..., Any]] = {
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
    left_data = load_file(left_path)
    right_data = load_file(right_path)

    validate_key_exists(left_data, key, str(left_path))
    validate_key_exists(right_data, key, str(right_path))

    left_idx = index_by_key(left_data, key)
    right_idx = index_by_key(right_data, key)

    join_func = JOIN_STRATEGIES.get(strategy, join_inner)
    joined = join_func(left_idx, right_idx)

    # WHY: Match statistics help the user verify the join worked correctly.
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
    logging.info("%s join: %d matched rows on key '%s'",
                 strategy.capitalize(), len(joined), key)
    return report

# ---------- CLI ----------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Join records across files by a shared key")
    parser.add_argument("--left", default="data/employees.csv")
    parser.add_argument("--right", default="data/departments.csv")
    parser.add_argument("--output", default="data/joined.json")
    parser.add_argument("--key", default="dept_id")
    parser.add_argument("--join", choices=["inner", "left", "full"], default="inner")
    return parser.parse_args()

def main() -> None:
    configure_logging()
    args = parse_args()
    report = run(Path(args.left), Path(args.right), Path(args.output), args.key, args.join)
    print(f"{args.join.capitalize()} join: {report['joined_records']} matched rows on key '{args.key}'")

if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Index both sides into dictionaries before joining | Hash-based indexing makes lookups O(1). Without indexing, an inner join on two lists of 1000 rows each would require up to 1,000,000 comparisons. With indexing, it takes about 2,000. |
| Last-wins policy for duplicate keys | This matches SQL's behavior when joining on a non-unique key with `DISTINCT`. The alternative (collecting all duplicates) would require list-of-lists and complicate the merge logic. |
| Key validation before joining | A typo in `--key` produces zero matches and empty output with no error. Validating early catches this with a helpful message listing available columns. |
| Support both CSV and JSON input | Real data pipelines often combine sources in different formats. Detecting the format by file extension makes the tool more versatile. |

## Alternative Approaches

### Using pandas merge

```python
import pandas as pd

def join_with_pandas(left_path, right_path, key, how="inner"):
    left = pd.read_csv(left_path)
    right = pd.read_csv(right_path)
    merged = pd.merge(left, right, on=key, how=how)
    return merged.to_dict(orient="records")
```

Pandas handles duplicate keys, type mismatches, column name conflicts (with suffixes), and many join types out of the box. For production data pipelines, pandas is the standard tool. Building the join manually teaches the underlying algorithm.

## Common Pitfalls

1. **Join key exists in only one file** — Using `--key dept_id` when the right file uses `department_id` produces zero matches. Always verify column names in both files before joining.
2. **Duplicate keys with different data** — If the left file has two rows with `dept_id=1`, only the last one appears in the index. This silently drops data. Log the duplicate count so the user is aware.
3. **Column name collisions** — If both files have a column called `name`, the right side's value overwrites the left side's in the merged dict. In production, you would add suffixes (`name_left`, `name_right`) to preserve both.
