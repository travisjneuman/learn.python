"""Level 2 project: Records Deduplicator.

Heavily commented beginner-friendly script:
- find and remove duplicate records by configurable keys,
- preserve first or last occurrence,
- report which records were duplicates.

Skills practiced: sets, dict comprehensions, sorting with key functions,
enumerate, nested data structures, try/except.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_csv_records(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    """Parse a CSV file into headers and a list of record dicts.

    Returns:
        A tuple of (headers, records) where records are dicts.
    """
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    lines = [line.strip() for line in lines if line.strip()]

    if not lines:
        return [], []

    headers = [h.strip() for h in lines[0].split(",")]
    records = []

    for line in lines[1:]:
        values = [v.strip() for v in line.split(",")]
        # Pad with empty strings if row has fewer values than headers.
        while len(values) < len(headers):
            values.append("")
        record = dict(zip(headers, values))
        records.append(record)

    return headers, records


def make_dedup_key(record: dict[str, str], key_fields: list[str]) -> str:
    """Create a deduplication key from specified fields.

    The key is a pipe-separated string of normalised field values.
    Normalisation: strip whitespace, lowercase.

    This key is used to detect duplicates — two records with the
    same key are considered duplicates.
    """
    parts = []
    for field in key_fields:
        value = record.get(field, "").strip().lower()
        parts.append(value)
    # Join with | so "a|b" is different from "ab".
    return "|".join(parts)


def deduplicate(
    records: list[dict[str, str]],
    key_fields: list[str],
    keep: str = "first",
) -> dict:
    """Remove duplicate records based on key fields.

    Args:
        records: List of record dicts.
        key_fields: Which fields to use for duplicate detection.
        keep: "first" keeps the first occurrence, "last" keeps the last.

    Returns:
        A dict with unique records, duplicates, and stats.
    """
    if keep not in ("first", "last"):
        raise ValueError(f"keep must be 'first' or 'last', got '{keep}'")

    # Track seen keys using a set for O(1) lookup.
    seen: set[str] = set()
    # For 'last' mode, we use a dict to overwrite with latest occurrence.
    key_to_record: dict[str, dict] = {}

    unique: list[dict] = []
    duplicates: list[dict] = []

    for idx, record in enumerate(records):
        dedup_key = make_dedup_key(record, key_fields)
        record_with_meta = {**record, "_original_index": idx, "_dedup_key": dedup_key}

        if dedup_key in seen:
            if keep == "last":
                # Move the previous one to duplicates, replace with current.
                old = key_to_record[dedup_key]
                duplicates.append(old)
                key_to_record[dedup_key] = record_with_meta
            else:
                # 'first' mode: current record is the duplicate.
                duplicates.append(record_with_meta)
        else:
            seen.add(dedup_key)
            key_to_record[dedup_key] = record_with_meta
            if keep == "first":
                unique.append(record_with_meta)

    if keep == "last":
        # Sort by original index to maintain stable order.
        unique = sorted(key_to_record.values(), key=lambda r: r["_original_index"])

    return {
        "unique": unique,
        "duplicates": duplicates,
        "stats": {
            "total_records": len(records),
            "unique_count": len(unique),
            "duplicate_count": len(duplicates),
            "dedup_fields": key_fields,
            "keep_mode": keep,
        },
    }


def find_duplicate_groups(
    records: list[dict[str, str]], key_fields: list[str]
) -> dict[str, list[dict]]:
    """Group records that share the same dedup key.

    Only returns groups with more than one record (actual duplicates).
    Uses a dict comprehension to filter.
    """
    groups: dict[str, list[dict]] = {}
    for record in records:
        key = make_dedup_key(record, key_fields)
        groups.setdefault(key, []).append(record)

    # Dict comprehension — keep only groups with duplicates.
    return {k: v for k, v in groups.items() if len(v) > 1}


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Records deduplicator")
    parser.add_argument("input", help="Path to CSV input file")
    parser.add_argument(
        "--keys",
        nargs="+",
        required=True,
        help="Fields to use for duplicate detection",
    )
    parser.add_argument(
        "--keep",
        choices=["first", "last"],
        default="first",
        help="Which duplicate to keep (default: first)",
    )
    parser.add_argument(
        "--show-groups",
        action="store_true",
        help="Show duplicate groups instead of deduplicating",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point: load records, deduplicate, report results."""
    args = parse_args()
    headers, records = parse_csv_records(Path(args.input))

    if args.show_groups:
        groups = find_duplicate_groups(records, args.keys)
        print(f"Found {len(groups)} duplicate groups:")
        for key, group in groups.items():
            print(f"\n  Key: {key} ({len(group)} records)")
            for r in group:
                print(f"    {r}")
        return

    result = deduplicate(records, args.keys, keep=args.keep)
    print(json.dumps(result["stats"], indent=2))

    print(f"\nUnique records ({result['stats']['unique_count']}):")
    for r in result["unique"]:
        # Remove internal metadata before display.
        display = {k: v for k, v in r.items() if not k.startswith("_")}
        print(f"  {display}")

    if result["duplicates"]:
        print(f"\nRemoved duplicates ({result['stats']['duplicate_count']}):")
        for r in result["duplicates"]:
            display = {k: v for k, v in r.items() if not k.startswith("_")}
            print(f"  {display}")


if __name__ == "__main__":
    main()
