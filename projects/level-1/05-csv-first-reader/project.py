"""Level 1 project: CSV First Reader.

Read a CSV file, display it as a formatted table, and compute
basic column statistics for numeric columns.

Concepts: csv.DictReader, string formatting, type detection, aggregation.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def load_csv(path: Path) -> list[dict]:
    """Read a CSV file and return rows as a list of dicts.

    WHY DictReader? -- It uses the header row as keys, so each
    row becomes a dictionary like {'name': 'Ada', 'age': '35'}.
    """
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    rows = []
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def detect_numeric_columns(rows: list[dict]) -> list[str]:
    """Find columns where all non-empty values are numeric.

    WHY detect? -- We need to know which columns can be averaged
    and summed.  Trying to average a 'name' column would fail.
    """
    if not rows:
        return []

    columns = list(rows[0].keys())
    numeric = []

    for col in columns:
        is_numeric = True
        for row in rows:
            value = row[col].strip()
            if not value:
                continue
            try:
                float(value)
            except ValueError:
                is_numeric = False
                break
        if is_numeric:
            numeric.append(col)

    return numeric


def column_stats(rows: list[dict], column: str) -> dict:
    """Compute min, max, sum, and average for a numeric column."""
    values = []
    for row in rows:
        val = row[column].strip()
        if val:
            values.append(float(val))

    if not values:
        return {"column": column, "count": 0}

    return {
        "column": column,
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "sum": round(sum(values), 2),
        "average": round(sum(values) / len(values), 2),
    }


def format_table(rows: list[dict], max_width: int = 15) -> str:
    """Format rows as a simple text table.

    WHY truncate? -- Long values would break the table alignment.
    We cap each cell to max_width characters.
    """
    if not rows:
        return "(empty table)"

    headers = list(rows[0].keys())

    def truncate(val: str) -> str:
        if len(val) > max_width:
            return val[: max_width - 3] + "..."
        return val

    # Build header row.
    header_line = "  ".join(truncate(h).ljust(max_width) for h in headers)
    separator = "  ".join("-" * max_width for _ in headers)

    lines = [header_line, separator]
    for row in rows:
        cells = [truncate(row.get(h, "")).ljust(max_width) for h in headers]
        lines.append("  ".join(cells))

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CSV First Reader")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_csv(Path(args.input))

    print("=== CSV Table ===\n")
    print(format_table(rows))

    numeric_cols = detect_numeric_columns(rows)
    if numeric_cols:
        print(f"\n=== Column Statistics ===\n")
        stats_list = []
        for col in numeric_cols:
            stats = column_stats(rows, col)
            stats_list.append(stats)
            print(f"  {col}: min={stats['min']}, max={stats['max']}, avg={stats['average']}")
    else:
        stats_list = []

    print(f"\n  {len(rows)} rows, {len(rows[0]) if rows else 0} columns")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps({"rows": rows, "stats": stats_list}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
