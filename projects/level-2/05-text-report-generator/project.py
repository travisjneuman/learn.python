"""Level 2 project: Text Report Generator.

Heavily commented beginner-friendly script:
- read structured data (CSV-like) from a file,
- compute summary statistics per category,
- generate a formatted plain-text report.

Skills practiced: nested data structures, dict/list comprehensions,
sorting with key functions, enumerate, zip, string formatting.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_records(path: Path) -> list[dict[str, str]]:
    """Parse a CSV-like file into a list of dicts.

    First line is treated as the header row.  Each subsequent line
    becomes a dict mapping header -> value.

    Uses zip() to pair headers with values — a core Python pattern.
    """
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    lines = [line.strip() for line in lines if line.strip()]

    if len(lines) < 2:
        return []

    # First line is the header — split on commas and strip whitespace.
    headers = [h.strip() for h in lines[0].split(",")]

    records: list[dict[str, str]] = []
    for line in lines[1:]:
        values = [v.strip() for v in line.split(",")]
        # zip pairs each header with its corresponding value.
        record = dict(zip(headers, values))
        records.append(record)

    return records


def group_by(records: list[dict], key: str) -> dict[str, list[dict]]:
    """Group records by a specific field value.

    Returns a dict where each key is a unique field value and
    each value is a list of records with that field value.

    Example:
        group_by(records, "department") -> {"Engineering": [...], "Sales": [...]}
    """
    groups: dict[str, list[dict]] = {}
    for record in records:
        group_key = record.get(key, "UNKNOWN")
        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(record)
    return groups


def compute_stats(values: list[float]) -> dict[str, float]:
    """Compute basic statistics for a list of numbers.

    Returns min, max, mean, and count.
    """
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
    """Extract numeric values from a specific field, skipping non-numeric entries.

    Uses try/except to safely convert — bad values are silently skipped.
    """
    values: list[float] = []
    for record in records:
        try:
            values.append(float(record.get(field, "")))
        except (ValueError, TypeError):
            # Skip records where this field is not a number.
            pass
    return values


def generate_report(
    records: list[dict],
    group_field: str,
    value_field: str,
    title: str = "Data Report",
) -> str:
    """Generate a formatted plain-text report.

    Groups records by group_field, computes stats on value_field,
    and formats everything into a readable table-style report.
    """
    lines: list[str] = []

    # Report header with box-drawing characters.
    border = "=" * 60
    lines.append(border)
    lines.append(f"  {title}")
    lines.append(border)
    lines.append("")

    # Overall statistics.
    all_values = extract_numeric(records, value_field)
    overall = compute_stats(all_values)
    lines.append(f"Total records: {len(records)}")
    lines.append(f"Overall {value_field}: mean={overall['mean']}, "
                 f"min={overall['min']}, max={overall['max']}, "
                 f"total={overall['total']}")
    lines.append("")

    # Per-group breakdown, sorted by group name.
    groups = group_by(records, group_field)
    lines.append(f"Breakdown by {group_field}:")
    lines.append("-" * 40)

    # Sort groups alphabetically using sorted() with key.
    for group_name in sorted(groups.keys()):
        group_records = groups[group_name]
        values = extract_numeric(group_records, value_field)
        stats = compute_stats(values)

        lines.append(f"  {group_name} ({stats['count']} records)")
        lines.append(f"    mean={stats['mean']}, min={stats['min']}, "
                     f"max={stats['max']}, total={stats['total']}")

    lines.append("")
    lines.append(border)

    # Top 5 records by value_field (sorted descending).
    top_records = sorted(
        [(r, float(r.get(value_field, 0))) for r in records
         if r.get(value_field, "").replace(".", "").replace("-", "").isdigit()],
        key=lambda pair: pair[1],
        reverse=True,
    )[:5]

    if top_records:
        lines.append(f"\nTop 5 by {value_field}:")
        for rank, (record, val) in enumerate(top_records, 1):
            # Show group field and value for each top record.
            label = record.get(group_field, "?")
            name = record.get("name", record.get("item", "?"))
            lines.append(f"  {rank}. {name} ({label}) — {val}")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Text report generator")
    parser.add_argument("input", help="Path to CSV-like input file")
    parser.add_argument(
        "--group", default="department", help="Field to group by"
    )
    parser.add_argument(
        "--value", default="salary", help="Numeric field to summarise"
    )
    parser.add_argument(
        "--title", default="Data Report", help="Report title"
    )
    parser.add_argument(
        "--json", action="store_true", help="Output as JSON instead of text"
    )
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
