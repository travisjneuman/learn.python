# Reconciliation Reporter — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
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

    WHY key by a field? Indexing rows by a unique key (like "id") lets
    us look up matching records in O(1) instead of scanning the entire
    list for each comparison. This is what makes reconciliation fast.
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    text = path.read_text(encoding="utf-8")
    reader = csv.DictReader(text.splitlines())
    headers = reader.fieldnames or []

    # WHY: Fail early if the key field is not in the headers. Without this
    # check, every row would silently produce a KeyError or None key.
    if key_field not in headers:
        raise ValueError(f"Key field '{key_field}' not found in headers: {headers}")

    result: dict[str, dict] = {}
    for row in reader:
        key_value = row[key_field]
        # WHY: Warn on duplicate keys because "last row wins" silently
        # drops data. The user needs to know their key field is not unique.
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
            "mismatches": [{"key": str, "differences": {...}}],
            "matched": int
        }
    """
    # WHY: Set operations (-, &) are the natural way to express "only in A,"
    # "only in B," and "in both." They run in O(n) time and make the
    # intent crystal clear.
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

        # WHY: If compare_fields is None, compare all fields that exist
        # in both rows. This default is the safest choice — it catches
        # any difference without requiring the user to enumerate fields.
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

    # WHY: Include a summary with counts so the user can quickly assess
    # the scope of differences without parsing the full details.
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
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Index records by key field in a dictionary | O(1) lookup per key turns reconciliation from O(n*m) to O(n+m). For two files with 10,000 rows each, this is the difference between 100 million comparisons and 20,000. |
| Use set operations for finding only-in-source / only-in-target | Set difference (`-`) and intersection (`&`) express the reconciliation logic naturally and concisely. The code reads almost like the English description of the problem. |
| Separate "only in source" from "mismatches" | These are different problems with different fixes. "Only in source" means a record was deleted or never migrated. "Mismatch" means a record exists in both but with conflicting values. Different root causes require different investigation workflows. |
| Warn on duplicate keys instead of crashing | Duplicate keys are a data quality issue, not a tool failure. Warning and proceeding (with "last row wins") lets the reconciliation complete while flagging the problem. |

## Alternative Approaches

### Using `pandas` for reconciliation

```python
import pandas as pd

def reconcile_pandas(source_path, target_path, key):
    src = pd.read_csv(source_path)
    tgt = pd.read_csv(target_path)
    merged = src.merge(tgt, on=key, how="outer", indicator=True, suffixes=("_src", "_tgt"))
    only_source = merged[merged["_merge"] == "left_only"][key].tolist()
    only_target = merged[merged["_merge"] == "right_only"][key].tolist()
    both = merged[merged["_merge"] == "both"]
    return only_source, only_target, both
```

**Trade-off:** `pandas` handles the merge in one line and scales well to large datasets (millions of rows) with its optimized C backend. However, it adds a large dependency (200+ MB) and its API has a steep learning curve. The dict-based approach in the main solution uses only standard library tools and is transparent about every step.

### Using `difflib` for detailed field comparison

```python
import difflib

def detailed_diff(src_val: str, tgt_val: str) -> str:
    diff = difflib.unified_diff(
        src_val.splitlines(), tgt_val.splitlines(),
        fromfile="source", tofile="target", lineterm=""
    )
    return "\n".join(diff)
```

**Trade-off:** `difflib` provides character-level diffs that show exactly what changed within a field (useful for long text fields). For short fields like names and IDs, the simple `source vs target` comparison in the main solution is clearer.

## Common Pitfalls

1. **Duplicate keys cause silent data loss** — If the key field has duplicates, `dict[key] = row` overwrites the previous row with the same key. The reconciliation then compares against the last occurrence only. Always validate key uniqueness or handle duplicates explicitly.
2. **Comparing files with different headers** — If source has columns `[id, name, email]` and target has `[id, name, phone]`, the "email" column comparison will show every record as mismatched (source has it, target does not). Check header alignment before reconciling.
3. **String comparison of numeric values** — CSV values are strings. `"100"` and `"100.0"` are different as strings but equal as numbers. If your data contains numeric fields, consider coercing to float before comparing.
