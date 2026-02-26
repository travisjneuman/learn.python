"""Level 5 / Project 03 — Multi-File ETL Runner.

Extract-Transform-Load across multiple source CSV files with merge
strategies (append, deduplicate, or update-by-key). Produces a single
consolidated output with a run log.
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

def extract_csv(path: Path) -> tuple[list[str], list[dict]]:
    """Read a CSV and return (headers, rows)."""
    text = path.read_text(encoding="utf-8")
    reader = csv.DictReader(text.splitlines())
    return list(reader.fieldnames or []), list(reader)

def transform_row(row: dict) -> dict:
    """Normalize a row: strip whitespace, lowercase keys."""
    return {k.strip().lower(): v.strip() if isinstance(v, str) else v for k, v in row.items()}

def merge_append(existing: list[dict], new_rows: list[dict]) -> list[dict]:
    """Simple append — just concatenate."""
    return existing + new_rows

def merge_deduplicate(existing: list[dict], new_rows: list[dict], key_field: str) -> list[dict]:
    """Append only rows whose key is not already present."""
    seen = {row.get(key_field) for row in existing}
    result = list(existing)
    for row in new_rows:
        if row.get(key_field) not in seen:
            result.append(row)
            seen.add(row.get(key_field))
    return result

def merge_update(existing: list[dict], new_rows: list[dict], key_field: str) -> list[dict]:
    """Update existing rows by key; append new keys."""
    index = {row.get(key_field): i for i, row in enumerate(existing)}
    result = list(existing)
    for row in new_rows:
        key = row.get(key_field)
        if key in index:
            result[index[key]] = row  # update
        else:
            result.append(row)
            index[key] = len(result) - 1
    return result

# WHY multiple merge strategies? -- Different business needs require
# different behavior: "append" for growing a log, "deduplicate" for
# combining sources without repeats, "update" for syncing latest values.
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
        if strategy == "append":
            merged = merge_append(merged, transformed)
        elif strategy in ("deduplicate", "update"):
            func = MERGE_STRATEGIES[strategy]
            merged = func(merged, transformed, key_field)
        after = len(merged)
        run_log.append({"file": str(path), "rows_read": len(transformed), "merged_total": after, "new_rows": after - before})
        logging.info("Processed %s: %d rows", path.name, len(transformed))

    return merged, run_log

def run(source_dir: Path, output_path: Path, strategy: str = "append", key_field: str = "id") -> dict:
    sources = sorted(source_dir.glob("*.csv"))
    if not sources:
        raise FileNotFoundError(f"No CSV files in {source_dir}")
    data, log = run_etl(sources, strategy, key_field)
    report = {"strategy": strategy, "source_files": len(sources), "total_records": len(data), "run_log": log, "data": data}
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
    print(json.dumps({"total_records": report["total_records"], "source_files": report["source_files"]}, indent=2))

if __name__ == "__main__":
    main()
