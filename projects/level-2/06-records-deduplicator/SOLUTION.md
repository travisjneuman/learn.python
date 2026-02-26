# Records Deduplicator — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Records Deduplicator — complete annotated solution."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_csv_records(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    """Parse a CSV file into headers and a list of record dicts."""
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
        # WHY: Pad short rows so zip does not silently drop columns.
        # A row with fewer values than headers would otherwise lose fields.
        while len(values) < len(headers):
            values.append("")
        record = dict(zip(headers, values))
        records.append(record)

    return headers, records


def make_dedup_key(record: dict[str, str], key_fields: list[str]) -> str:
    """Create a deduplication key from specified fields.

    The key is a pipe-separated string of normalised field values.
    """
    parts = []
    for field in key_fields:
        # WHY: Strip and lowercase so "Alice " and "alice" produce the same
        # dedup key. Without normalisation, trivial whitespace or case
        # differences would make records appear unique when they are not.
        value = record.get(field, "").strip().lower()
        parts.append(value)
    # WHY: Join with "|" so multi-field keys are unambiguous.
    # Without a separator, keys from ("a","bc") and ("ab","c") would
    # both produce "abc" and collide. With "|" they become "a|bc" and "ab|c".
    return "|".join(parts)


def deduplicate(
    records: list[dict[str, str]],
    key_fields: list[str],
    keep: str = "first",
) -> dict:
    """Remove duplicate records based on key fields."""
    if keep not in ("first", "last"):
        raise ValueError(f"keep must be 'first' or 'last', got '{keep}'")

    # WHY: The set gives O(1) lookup for "have we seen this key before?"
    # The dict maps each key to its record for the "last" mode replacement.
    seen: set[str] = set()
    key_to_record: dict[str, dict] = {}

    unique: list[dict] = []
    duplicates: list[dict] = []

    for idx, record in enumerate(records):
        dedup_key = make_dedup_key(record, key_fields)
        record_with_meta = {**record, "_original_index": idx, "_dedup_key": dedup_key}

        if dedup_key in seen:
            if keep == "last":
                # WHY: In "last" mode, the previously stored record becomes
                # a duplicate, and the current record takes its place.
                old = key_to_record[dedup_key]
                duplicates.append(old)
                key_to_record[dedup_key] = record_with_meta
            else:
                # WHY: In "first" mode, the current record is the duplicate
                # because we already have an earlier occurrence.
                duplicates.append(record_with_meta)
        else:
            seen.add(dedup_key)
            key_to_record[dedup_key] = record_with_meta
            if keep == "first":
                unique.append(record_with_meta)

    if keep == "last":
        # WHY: Sort by original index to maintain stable insertion order.
        # Without sorting, records would appear in arbitrary dict-iteration order.
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
    """Group records sharing the same dedup key. Only returns actual duplicates."""
    groups: dict[str, list[dict]] = {}
    for record in records:
        key = make_dedup_key(record, key_fields)
        # WHY: setdefault is a one-liner replacement for the common
        # "if key not in dict: dict[key] = []; dict[key].append(item)" pattern.
        groups.setdefault(key, []).append(record)

    # WHY: Dict comprehension filters to only groups with >1 record.
    # Unique records are not interesting when investigating duplicates.
    return {k: v for k, v in groups.items() if len(v) > 1}


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Records deduplicator")
    parser.add_argument("input", help="Path to CSV input file")
    parser.add_argument(
        "--keys", nargs="+", required=True,
        help="Fields to use for duplicate detection",
    )
    parser.add_argument(
        "--keep", choices=["first", "last"], default="first",
        help="Which duplicate to keep (default: first)",
    )
    parser.add_argument(
        "--show-groups", action="store_true",
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
        # WHY: Filter out internal metadata (keys starting with "_") before
        # displaying. Users should not see implementation details.
        display = {k: v for k, v in r.items() if not k.startswith("_")}
        print(f"  {display}")

    if result["duplicates"]:
        print(f"\nRemoved duplicates ({result['stats']['duplicate_count']}):")
        for r in result["duplicates"]:
            display = {k: v for k, v in r.items() if not k.startswith("_")}
            print(f"  {display}")


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Pipe-separated composite key | Joining field values with `\|` creates an unambiguous key. Without a separator, `("ab", "c")` and `("a", "bc")` would both produce `"abc"` and be treated as duplicates when they are not. |
| Configurable `keep` mode | Real deduplication needs vary. Sometimes the first record is authoritative (original entry), sometimes the last record is (most recent update). Making this a parameter avoids hard-coding a business decision. |
| Set + dict dual tracking | The set provides O(1) "seen before?" checks. The dict stores the actual record for each key, which is needed for the "last" mode where we replace the stored record. Using both is slightly redundant for "first" mode but keeps the logic uniform. |
| Lowercase normalisation in key building | Without normalisation, "alice@test.com" and "Alice@test.com" would appear as different records. Dedup keys should represent semantic identity, not exact character sequences. |
| Metadata with `_` prefix convention | Internal fields like `_original_index` and `_dedup_key` are prefixed with `_` to distinguish them from data fields. This is a common convention in Python (and MongoDB) for metadata. |

## Alternative Approaches

### Using `pandas.DataFrame.drop_duplicates()`

```python
import pandas as pd

df = pd.read_csv("data/sample_input.txt")
unique = df.drop_duplicates(subset=["email"], keep="first")
duplicates = df[df.duplicated(subset=["email"], keep="first")]
```

Pandas handles deduplication in one line with optimized C code. The manual approach here teaches the underlying set-based algorithm. For datasets over 100K rows, pandas is significantly faster.

### Using `tuple` keys instead of string joining

```python
def make_dedup_key_tuple(record, key_fields):
    return tuple(record.get(f, "").strip().lower() for f in key_fields)
```

Tuples are hashable and can be used as dict keys directly. This avoids the separator ambiguity problem entirely. The string approach is used here because it produces readable keys for debugging output.

## Common Pitfalls

1. **Using a non-existent key field** — If `--keys department` is passed but "department" is not in the CSV headers, every record gets an empty string for that field, and all records appear to be duplicates of each other. Validate that key fields exist in headers before processing.

2. **Forgetting order stability** — In "last" mode, building the unique list from `key_to_record.values()` produces records in dict-insertion order, which may not match the original file order. Sorting by `_original_index` restores the expected order.

3. **Hash collisions with dedup keys** — If you use a hash function instead of the full key string, different records could produce the same hash and be incorrectly treated as duplicates. Always use the full composite key for correctness.
