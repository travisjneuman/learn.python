"""Level 7 / Project 10 — Multi-Source Reconciler.

Compares records from two or more data sources by a shared key
and reports matches, mismatches, and records missing from one side.

Key concepts:
- Key-based record matching across sources
- Set operations (intersection, difference)
- Field-level mismatch detection
- Reconciliation report generation
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

def index_by_key(records: list[dict], key_field: str) -> dict[str, dict]:
    """Build a lookup dict keyed by the given field."""
    index: dict[str, dict] = {}
    for rec in records:
        k = str(rec.get(key_field, ""))
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

    left_keys = set(left_idx.keys())
    right_keys = set(right_idx.keys())
    common = left_keys & right_keys

    report = ReconciliationReport(left_name=left_name, right_name=right_name)
    report.left_only = sorted(left_keys - right_keys)
    report.right_only = sorted(right_keys - left_keys)

    for k in sorted(common):
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
