# Text Report Generator — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Text Report Generator — complete annotated solution."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_records(path: Path) -> list[dict[str, str]]:
    """Parse a CSV-like file into a list of dicts."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    lines = [line.strip() for line in lines if line.strip()]

    if len(lines) < 2:
        return []

    headers = [h.strip() for h in lines[0].split(",")]

    records: list[dict[str, str]] = []
    for line in lines[1:]:
        values = [v.strip() for v in line.split(",")]
        # WHY: zip pairs each header with its corresponding value positionally.
        # zip("name,age", "Alice,30") -> [("name","Alice"), ("age","30")]
        # dict() converts those pairs into {"name": "Alice", "age": "30"}.
        record = dict(zip(headers, values))
        records.append(record)

    return records


def group_by(records: list[dict], key: str) -> dict[str, list[dict]]:
    """Group records by a specific field value.

    Example: group_by(records, "department") -> {"Engineering": [...], "Sales": [...]}
    """
    groups: dict[str, list[dict]] = {}
    for record in records:
        # WHY: dict.get(key, "UNKNOWN") provides a safe default when a record
        # is missing the group field, instead of crashing with KeyError.
        group_key = record.get(key, "UNKNOWN")
        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(record)
    return groups


def compute_stats(values: list[float]) -> dict[str, float]:
    """Compute basic statistics for a list of numbers."""
    # WHY: Guard against empty lists — min(), max(), and division would all
    # crash on an empty list. Returning zeros is a safe, predictable fallback.
    if not values:
        return {"count": 0, "min": 0.0, "max": 0.0, "mean": 0.0, "total": 0.0}

    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "mean": round(sum(values) / len(values), 2),
        "total": round(sum(values), 2),
    }


def extract_numeric(records: list[dict], field: str) -> list[float]:
    """Extract numeric values from a field, skipping non-numeric entries."""
    values: list[float] = []
    for record in records:
        try:
            # WHY: try/except is the Pythonic way to handle mixed data.
            # Some records may have "N/A" or "" in a numeric field. Instead of
            # checking with regex first, we just try the conversion and skip failures.
            values.append(float(record.get(field, "")))
        except (ValueError, TypeError):
            pass
    return values


def generate_report(
    records: list[dict],
    group_field: str,
    value_field: str,
    title: str = "Data Report",
) -> str:
    """Generate a formatted plain-text report."""
    lines: list[str] = []

    border = "=" * 60
    lines.append(border)
    lines.append(f"  {title}")
    lines.append(border)
    lines.append("")

    # WHY: Overall statistics give context — is this a large or small dataset?
    # What is the global average before we break down by group?
    all_values = extract_numeric(records, value_field)
    overall = compute_stats(all_values)
    lines.append(f"Total records: {len(records)}")
    lines.append(f"Overall {value_field}: mean={overall['mean']}, "
                 f"min={overall['min']}, max={overall['max']}, "
                 f"total={overall['total']}")
    lines.append("")

    groups = group_by(records, group_field)
    lines.append(f"Breakdown by {group_field}:")
    lines.append("-" * 40)

    # WHY: sorted(groups.keys()) ensures deterministic output. Without sorting,
    # dict iteration order depends on insertion order, which varies with input.
    # Sorted output is easier to compare across runs.
    for group_name in sorted(groups.keys()):
        group_records = groups[group_name]
        values = extract_numeric(group_records, value_field)
        stats = compute_stats(values)

        lines.append(f"  {group_name} ({stats['count']} records)")
        lines.append(f"    mean={stats['mean']}, min={stats['min']}, "
                     f"max={stats['max']}, total={stats['total']}")

    lines.append("")
    lines.append(border)

    # WHY: Top 5 records by value give a quick "leaderboard" view.
    # The isdigit() check (with replace for decimals/negatives) filters out
    # non-numeric entries before sorting.
    top_records = sorted(
        [(r, float(r.get(value_field, 0))) for r in records
         if r.get(value_field, "").replace(".", "").replace("-", "").isdigit()],
        key=lambda pair: pair[1],
        reverse=True,
    )[:5]

    if top_records:
        lines.append(f"\nTop 5 by {value_field}:")
        for rank, (record, val) in enumerate(top_records, 1):
            label = record.get(group_field, "?")
            name = record.get("name", record.get("item", "?"))
            lines.append(f"  {rank}. {name} ({label}) — {val}")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Text report generator")
    parser.add_argument("input", help="Path to CSV-like input file")
    parser.add_argument("--group", default="department", help="Field to group by")
    parser.add_argument("--value", default="salary", help="Numeric field to summarise")
    parser.add_argument("--title", default="Data Report", help="Report title")
    parser.add_argument("--json", action="store_true", help="Output as JSON instead of text")
    return parser.parse_args()


def main() -> None:
    """Entry point: parse data, generate and print report."""
    args = parse_args()
    records = parse_records(Path(args.input))

    if args.json:
        groups = group_by(records, args.group)
        result = {}
        for name, group in groups.items():
            values = extract_numeric(group, args.value)
            result[name] = compute_stats(values)
        print(json.dumps(result, indent=2))
    else:
        report = generate_report(
            records,
            group_field=args.group,
            value_field=args.value,
            title=args.title,
        )
        print(report)


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| `zip(headers, values)` for record building | `zip` is the idiomatic Python way to pair two parallel lists. It is concise, readable, and handles unequal lengths gracefully (stops at the shorter list). |
| `group_by` as a standalone function | Grouping is a reusable pattern. Making it a function means you can group by any field without rewriting the logic. This is the manual version of `itertools.groupby` or SQL `GROUP BY`. |
| Sorted group names in report | Deterministic output makes testing and diffing possible. If groups appeared in random order, every test would need to sort before comparing. |
| `extract_numeric` with try/except | Real CSV data is messy — salary columns might contain "N/A", blank strings, or currency symbols. Silently skipping non-numeric values is more robust than crashing on bad data. |
| Text report format with `=` borders | Plain text reports work everywhere (email, terminal, log files) without requiring a rendering engine. The visual structure makes them scannable. |

## Alternative Approaches

### Using `collections.defaultdict` for grouping

```python
from collections import defaultdict

def group_by_defaultdict(records, key):
    groups = defaultdict(list)
    for record in records:
        groups[record.get(key, "UNKNOWN")].append(record)
    return dict(groups)
```

`defaultdict(list)` automatically creates an empty list for new keys, eliminating the `if key not in groups` check. It is slightly more concise but introduces a new import and concept. The manual approach teaches the underlying pattern.

### Using f-string alignment for table formatting

```python
# Right-align numbers in 10-char columns for clean tables
print(f"{'mean':>10} {'min':>10} {'max':>10}")
print(f"{stats['mean']:>10.2f} {stats['min']:>10.2f} {stats['max']:>10.2f}")
```

F-string format specifiers like `>10.2f` (right-align, 10 chars wide, 2 decimal places) produce professional-looking tables. The solution uses a simpler format for readability at this level.

## Common Pitfalls

1. **`zip` with unequal-length lists** — If a CSV row has fewer values than headers, `zip` silently drops the extra headers. The record will be missing fields. Defensive code should pad short rows with empty strings before zipping.

2. **Grouping by a missing field** — If `--group department` is used but "department" does not exist in the CSV headers, every record gets grouped under "UNKNOWN". The `.get(key, "UNKNOWN")` default handles this gracefully, but the user may not realise their field name was wrong.

3. **Integer vs float in statistics** — If all values happen to be integers, `sum(values) / len(values)` produces a float in Python 3, which is correct. But `min([])` and `max([])` raise `ValueError` on empty lists — always guard against empty data before calling these builtins.
