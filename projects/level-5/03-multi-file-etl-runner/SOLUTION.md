# Multi-File ETL Runner — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Level 5 / Project 03 — Multi-File ETL Runner.

Extract-Transform-Load across multiple source CSV files with merge
strategies (append, deduplicate, or update-by-key).
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path

def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

# ---------- ETL functions ----------

# WHY: Separate extract, transform, and merge into independent functions.
# This follows the ETL pattern used in data warehousing: each stage can
# be tested, swapped, or retried independently.

def extract_csv(path: Path) -> tuple[list[str], list[dict]]:
    """Read a CSV and return (headers, rows)."""
    text = path.read_text(encoding="utf-8")
    reader = csv.DictReader(text.splitlines())
    # WHY: Return headers separately so callers can validate that
    # all source files share the same structure.
    return list(reader.fieldnames or []), list(reader)

def transform_row(row: dict) -> dict:
    """Normalize a row: strip whitespace, lowercase keys."""
    # WHY: Real-world CSVs have inconsistent casing ("Name" vs "name")
    # and trailing spaces. Normalizing early prevents merge key mismatches.
    return {k.strip().lower(): v.strip() if isinstance(v, str) else v for k, v in row.items()}

def merge_append(existing: list[dict], new_rows: list[dict]) -> list[dict]:
    """Simple append — just concatenate."""
    return existing + new_rows

def merge_deduplicate(existing: list[dict], new_rows: list[dict], key_field: str) -> list[dict]:
    """Append only rows whose key is not already present."""
    # WHY: A set tracks seen keys for O(1) lookups. Without this,
    # checking "is this key already in the list?" would be O(n) per row.
    seen = {row.get(key_field) for row in existing}
    result = list(existing)
    for row in new_rows:
        if row.get(key_field) not in seen:
            result.append(row)
            seen.add(row.get(key_field))
    return result

def merge_update(existing: list[dict], new_rows: list[dict], key_field: str) -> list[dict]:
    """Update existing rows by key; append new keys."""
    # WHY: Build an index mapping key -> position so updates are O(1)
    # instead of scanning the entire list for each new row.
    index = {row.get(key_field): i for i, row in enumerate(existing)}
    result = list(existing)
    for row in new_rows:
        key = row.get(key_field)
        if key in index:
            result[index[key]] = row  # overwrite with newer data
        else:
            result.append(row)
            index[key] = len(result) - 1
    return result

# WHY: A strategy map lets the merge method be selected by string name
# (from CLI or config) without if/elif chains. Adding a new strategy
# only requires writing the function and adding one entry here.
MERGE_STRATEGIES = {"append": merge_append, "deduplicate": merge_deduplicate, "update": merge_update}

def run_etl(source_paths: list[Path], strategy: str, key_field: str = "id") -> tuple[list[dict], list[dict]]:
    """Run ETL across multiple files. Returns (merged_data, run_log)."""
    merged: list[dict] = []
    run_log: list[dict] = []

    for path in source_paths:
        if not path.exists():
            run_log.append({"file": str(path), "status": "missing"})
            logging.warning("Skipping missing file: %s", path)
            continue
        headers, rows = extract_csv(path)
        transformed = [transform_row(r) for r in rows]
        before = len(merged)
        # WHY: Dispatch to the right merge function based on strategy name.
        if strategy == "append":
            merged = merge_append(merged, transformed)
        elif strategy in ("deduplicate", "update"):
            func = MERGE_STRATEGIES[strategy]
            merged = func(merged, transformed, key_field)
        after = len(merged)
        run_log.append({"file": str(path), "rows_read": len(transformed),
                        "merged_total": after, "new_rows": after - before})
        logging.info("Processed %s: %d rows", path.name, len(transformed))

    return merged, run_log

def run(source_dir: Path, output_path: Path, strategy: str = "append", key_field: str = "id") -> dict:
    sources = sorted(source_dir.glob("*.csv"))
    if not sources:
        raise FileNotFoundError(f"No CSV files in {source_dir}")
    data, log = run_etl(sources, strategy, key_field)
    report = {"strategy": strategy, "source_files": len(sources),
              "total_records": len(data), "run_log": log, "data": data}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info("ETL complete: %d records from %d files", len(data), len(sources))
    return report

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Multi-file ETL with merge strategies")
    parser.add_argument("--source-dir", default="data/sources")
    parser.add_argument("--output", default="data/etl_output.json")
    parser.add_argument("--strategy", choices=["append", "deduplicate", "update"], default="append")
    parser.add_argument("--key", default="id")
    return parser.parse_args()

def main() -> None:
    configure_logging()
    args = parse_args()
    report = run(Path(args.source_dir), Path(args.output), args.strategy, args.key)
    print(json.dumps({"total_records": report["total_records"],
                       "source_files": report["source_files"]}, indent=2))

if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Separate extract / transform / merge functions | Following the ETL pattern makes each stage independently testable. You can swap CSV extraction for JSON extraction without touching the transform or merge logic. |
| Set-based deduplication in `merge_deduplicate` | Using a set for seen keys gives O(1) lookups per row. A naive list scan would be O(n) per row, making the overall merge O(n*m). |
| Strategy dispatch via dictionary | Adding a new merge strategy requires only one new function and one dictionary entry. No existing code needs modification (Open/Closed Principle). |
| Skip missing files instead of crashing | In batch processing, one missing file should not abort the entire pipeline. Logging the skip and continuing lets the operator review the run log afterward. |

## Alternative Approaches

### Using pandas for the ETL

```python
import pandas as pd

def run_etl_pandas(source_paths, strategy, key_field="id"):
    frames = [pd.read_csv(p) for p in source_paths if p.exists()]
    combined = pd.concat(frames, ignore_index=True)
    if strategy == "deduplicate":
        combined = combined.drop_duplicates(subset=[key_field], keep="first")
    return combined.to_dict(orient="records")
```

Pandas is far more powerful for complex transforms (groupby, pivots, type coercion) and handles large datasets efficiently. However, it adds a heavy dependency and is overkill when the transform is simple string normalization. Learning the manual approach first helps you understand what pandas does under the hood.

## Common Pitfalls

1. **Inconsistent column names across files** — If one CSV has "Name" and another has "name", deduplication on "name" silently misses records from the first file. The `transform_row` function solves this by lowercasing all keys before merging.
2. **Forgetting to sort source files** — `glob("*.csv")` returns files in filesystem order, which varies by OS. Using `sorted()` ensures deterministic processing order, which matters for "update" strategy (last file's values win).
3. **Using "deduplicate" without specifying a key field** — If the key field does not exist in the data, `row.get(key_field)` returns `None` for every row, and all rows after the first are treated as duplicates and dropped.
