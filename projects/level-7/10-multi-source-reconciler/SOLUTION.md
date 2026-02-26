# Solution: Level 7 / Project 10 - Multi Source Reconciler

> **STOP — Try it yourself first!**
>
> You learn by building, not by reading answers. Spend at least 30 minutes
> attempting this project before looking here.
>
> - Re-read the [README](./README.md) for requirements
> - Try the [WALKTHROUGH](./WALKTHROUGH.md) for guided hints without spoilers

---

## Complete solution

```python
"""Level 7 / Project 10 — Multi-Source Reconciler.

Compares records from two or more data sources by a shared key
and reports matches, mismatches, and records missing from one side.
"""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path


# -- Data model ----------------------------------------------------------

@dataclass
class MismatchDetail:
    """One field that differs between two sources."""
    key: str
    field_name: str
    left_value: object
    right_value: object


@dataclass
class ReconciliationReport:
    """Full reconciliation outcome."""
    left_name: str
    right_name: str
    matched: int = 0
    mismatched: int = 0
    left_only: list[str] = field(default_factory=list)
    right_only: list[str] = field(default_factory=list)
    mismatches: list[MismatchDetail] = field(default_factory=list)


# -- Core logic ----------------------------------------------------------

# WHY index-then-compare? -- Building a dict keyed by the join field turns
# O(n*m) nested-loop comparison into O(n+m) hash lookups.  This is the same
# hash-join strategy databases use internally for equi-joins.
def index_by_key(records: list[dict], key_field: str) -> dict[str, dict]:
    """Build a lookup dict keyed by the given field."""
    index: dict[str, dict] = {}
    for rec in records:
        k = str(rec.get(key_field, ""))
        # WHY skip empty keys? -- Records without a key cannot be matched
        # to anything.  Including them would create a phantom "" key that
        # collects all keyless records from both sides.
        if k:
            index[k] = rec
    return index


def compare_records(
    left: dict, right: dict, compare_fields: list[str],
) -> list[MismatchDetail]:
    """Compare two records on specified fields, return differences."""
    diffs: list[MismatchDetail] = []
    key = left.get("_key", "?")
    for f in compare_fields:
        lv = left.get(f)
        rv = right.get(f)
        if lv != rv:
            diffs.append(MismatchDetail(key=key, field_name=f,
                                        left_value=lv, right_value=rv))
    return diffs


def reconcile(
    left_records: list[dict],
    right_records: list[dict],
    key_field: str,
    compare_fields: list[str],
    left_name: str = "source_a",
    right_name: str = "source_b",
) -> ReconciliationReport:
    """Run full reconciliation between two sources."""
    left_idx = index_by_key(left_records, key_field)
    right_idx = index_by_key(right_records, key_field)

    # WHY set operations? -- Intersection gives matched keys, differences
    # give left-only and right-only.  This is the most readable way to
    # express the three-way split: common, left-exclusive, right-exclusive.
    left_keys = set(left_idx.keys())
    right_keys = set(right_idx.keys())
    common = left_keys & right_keys

    report = ReconciliationReport(left_name=left_name, right_name=right_name)
    report.left_only = sorted(left_keys - right_keys)
    report.right_only = sorted(right_keys - left_keys)

    for k in sorted(common):
        # WHY inject "_key" into the copies? -- compare_records needs the
        # key for error reporting.  We copy with {**dict} to avoid mutating
        # the original records.
        l_rec = {**left_idx[k], "_key": k}
        r_rec = {**right_idx[k], "_key": k}
        diffs = compare_records(l_rec, r_rec, compare_fields)
        if diffs:
            report.mismatched += 1
            report.mismatches.extend(diffs)
        else:
            report.matched += 1

    logging.info(
        "reconciled %s vs %s: matched=%d mismatched=%d left_only=%d right_only=%d",
        left_name, right_name, report.matched, report.mismatched,
        len(report.left_only), len(report.right_only),
    )
    return report


def report_to_dict(r: ReconciliationReport) -> dict:
    return {
        "left": r.left_name,
        "right": r.right_name,
        "matched": r.matched,
        "mismatched": r.mismatched,
        "left_only": r.left_only,
        "right_only": r.right_only,
        "mismatch_details": [
            {"key": m.key, "field": m.field_name,
             "left": m.left_value, "right": m.right_value}
            for m in r.mismatches
        ],
    }


# -- Entry points --------------------------------------------------------

def run(input_path: Path, output_path: Path) -> dict:
    config = json.loads(input_path.read_text(encoding="utf-8")) if input_path.exists() else {}

    key_field = config.get("key_field", "id")
    compare_fields = config.get("compare_fields", ["value"])
    left = config.get("left", [])
    right = config.get("right", [])

    report = reconcile(left, right, key_field, compare_fields)
    summary = report_to_dict(report)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Multi-Source Reconciler")
    parser.add_argument("--input", default="data/sample_input.json")
    parser.add_argument("--output", default="data/output_summary.json")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    args = parse_args()
    summary = run(Path(args.input), Path(args.output))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Hash-join via `index_by_key` | O(n+m) instead of O(n*m) nested loops; same strategy databases use for equi-joins | Nested loop comparison -- simpler code but quadratic performance on large datasets |
| Set operations for key matching | `&` (intersection) and `-` (difference) express the logic clearly and concisely | Manual loop with `if key in other_dict` -- equivalent but more verbose |
| Separate `compare_fields` list | Only compares fields the operator cares about; ignores metadata like timestamps | Compare all fields -- catches unexpected changes but produces noisy reports |
| `report_to_dict` serializer | Keeps the dataclass clean (no JSON concerns) and the serialization explicit | `dataclasses.asdict()` -- recursive but includes internal fields like `_key` |
| Sorted output for deterministic results | Sorted keys and sorted left_only/right_only make test assertions stable | Unsorted -- faster but test order depends on dict insertion order |

## Alternative approaches

### Approach B: pandas merge for reconciliation

```python
import pandas as pd

def reconcile_with_pandas(left, right, key_field, compare_fields):
    df_l = pd.DataFrame(left)
    df_r = pd.DataFrame(right)
    merged = df_l.merge(df_r, on=key_field, how="outer", suffixes=("_left", "_right"), indicator=True)
    matched = merged[merged["_merge"] == "both"]
    # Compare fields...
```

**Trade-off:** Pandas is more efficient for large datasets and handles edge cases like duplicate keys natively. But it adds a heavy dependency and obscures the algorithm, making it harder to learn what reconciliation actually does under the hood.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| `key_field` does not exist in any records | `index_by_key` produces empty dicts; reconciliation reports everything as "left_only" and "right_only" | Validate that `key_field` exists in at least one record before proceeding |
| Duplicate keys in one source | `index_by_key` silently keeps last-write-wins; earlier records are lost | Log a warning when duplicates are detected; optionally collect all records per key |
| Comparing float fields | `0.1 + 0.2 != 0.3` due to floating-point precision; false mismatches | Add a `tolerance` parameter for numeric comparisons |
