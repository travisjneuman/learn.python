# Solution: Level 1 / Project 05 - CSV First Reader

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 1 project: CSV First Reader.

Read a CSV file, display it as a formatted table, and compute
basic column statistics for numeric columns.

Concepts: csv.DictReader, string formatting, type detection, aggregation.
"""


import argparse
import csv
import json
from pathlib import Path


# WHY load_csv: This function handles the file I/O and CSV parsing in
# one place.  Everything downstream works with plain Python lists of
# dicts, making it easy to test without actual files.
def load_csv(path: Path) -> list[dict]:
    """Read a CSV file and return rows as a list of dicts.

    WHY DictReader? -- It uses the header row as keys, so each
    row becomes a dictionary like {'name': 'Ada', 'age': '35'}.
    """
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    rows = []
    # WHY newline="": The csv module handles line endings internally.
    # Passing newline="" prevents double-interpretation of carriage
    # returns, which causes phantom blank rows on Windows.
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


# WHY detect_numeric_columns: Before computing statistics, we need to
# know which columns contain numbers.  Auto-detection means the script
# works on any CSV without hardcoding column names.
def detect_numeric_columns(rows: list[dict]) -> list[str]:
    """Find columns where all non-empty values are numeric."""
    if not rows:
        return []

    # WHY use first row's keys: All rows from DictReader share the
    # same keys (the CSV header).  We iterate the columns, not the rows.
    columns = list(rows[0].keys())
    numeric = []

    for col in columns:
        is_numeric = True
        for row in rows:
            value = row[col].strip()
            # WHY skip empty: A missing value should not disqualify a
            # column as numeric.  Real CSVs often have blank cells.
            if not value:
                continue
            try:
                # WHY float not int: float() accepts both "42" and
                # "3.14", so it catches all numeric formats.
                float(value)
            except ValueError:
                is_numeric = False
                # WHY break: Once we find one non-numeric value in a
                # column, we know the whole column is not numeric.
                # No need to check remaining rows.
                break
        if is_numeric:
            numeric.append(col)

    return numeric


# WHY column_stats: Computing min/max/sum/average for numeric columns
# is the most common first analysis people do with tabular data.
def column_stats(rows: list[dict], column: str) -> dict:
    """Compute min, max, sum, and average for a numeric column."""
    values = []
    for row in rows:
        val = row[column].strip()
        if val:
            values.append(float(val))

    # WHY guard against empty: If all values in the column are blank,
    # we have nothing to compute.  Returning count=0 signals this.
    if not values:
        return {"column": column, "count": 0}

    return {
        "column": column,
        "count": len(values),
        "min": min(values),
        "max": max(values),
        # WHY round: Prevents floating-point noise like 73500.00000001
        # from cluttering the output.
        "sum": round(sum(values), 2),
        "average": round(sum(values) / len(values), 2),
    }


# WHY format_table: Displaying data as an aligned table makes it
# immediately readable.  This is the output humans expect when
# previewing tabular data — every data explorer and admin dashboard
# formats data this way.
def format_table(rows: list[dict], max_width: int = 15) -> str:
    """Format rows as a simple text table."""
    if not rows:
        return "(empty table)"

    headers = list(rows[0].keys())

    # WHY truncate: A cell containing a 200-character string would
    # destroy the table alignment.  Capping to max_width with "..."
    # keeps the table readable.
    def truncate(val: str) -> str:
        if len(val) > max_width:
            return val[: max_width - 3] + "..."
        return val

    # WHY ljust: Left-justifying each cell to the same width creates
    # even columns.  The "  " separator between columns adds breathing room.
    header_line = "  ".join(truncate(h).ljust(max_width) for h in headers)
    separator = "  ".join("-" * max_width for _ in headers)

    lines = [header_line, separator]
    for row in rows:
        cells = [truncate(row.get(h, "")).ljust(max_width) for h in headers]
        lines.append("  ".join(cells))

    return "\n".join(lines)


# WHY parse_args: argparse gives us --input and --output flags for
# flexible file paths without editing code.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CSV First Reader")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


# WHY main: Orchestrates loading, displaying, computing stats, and
# saving.  Keeps the module importable so tests can use individual
# functions without side effects.
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `csv.DictReader` instead of `csv.reader` | Accessing columns by name (`row["salary"]`) is self-documenting and resilient to column reordering | `csv.reader` with numeric indices — fragile and unreadable (`row[2]` means nothing without context) |
| Auto-detect numeric columns | The script works on any CSV without the user specifying which columns are numeric | Require column names as arguments — less convenient, more error-prone |
| Truncate long cell values | Preserves table alignment; long text would push columns out of line | Wrap text — much harder to implement in a plain-text terminal table |
| Separate `column_stats` from `detect_numeric_columns` | Detection tells us which columns to analyse; stats computes the actual values — single responsibility | One function that does both — harder to test detection logic independently |

## Alternative approaches

### Approach B: Using pandas for CSV reading and stats

```python
# NOTE: pandas is introduced in later levels.  This shows what the
# same task looks like with a data analysis library.

import pandas as pd

def load_and_stats_pandas(path: str) -> None:
    """Load CSV and compute stats using pandas."""
    df = pd.read_csv(path)
    # WHY describe: pandas.describe() automatically computes count,
    # mean, std, min, max, and quartiles for all numeric columns.
    print(df.to_string())
    print(df.describe())
```

**Trade-off:** pandas does in two lines what this project does in dozens. But this project teaches you how CSV parsing, type detection, and aggregation work at a fundamental level. When you learn pandas in Level 7 (data analysis module), you will understand what it is doing under the hood because you built it yourself here.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| CSV with headers only (no data rows) | `load_csv()` returns `[]`, `detect_numeric_columns()` returns `[]`, table shows "(empty table)" | All functions guard against empty lists; no crashes |
| Column with mixed values like `"10, N/A, 30"` | `detect_numeric_columns()` correctly marks it non-numeric because `float("N/A")` raises ValueError | The try/except + break pattern catches the first non-numeric and moves on |
| CSV with inconsistent column counts | `csv.DictReader` handles ragged rows by filling missing values with `None` or leaving keys absent | Using `.get(h, "")` in `format_table()` handles missing keys safely |
| Very wide CSV (many columns) | Table may exceed terminal width; columns get squeezed or wrap awkwardly | `max_width` parameter can be reduced; future improvement: add `--columns` filter |

## Key takeaways

1. **`csv.DictReader` turns CSV rows into dictionaries automatically.** This is far more readable than index-based access and is the standard way to read CSVs in Python. The header row becomes the dict keys.
2. **Auto-detecting data types is a real-world pattern.** Spreadsheet applications, databases, and data tools all infer column types from the values. The try/except with `float()` approach is the simplest form of type inference.
3. **This project connects directly to data analysis workflows.** The load-detect-compute-display pattern is exactly what pandas, Excel, and SQL do. When you reach the data analysis module, you will recognise these operations as `df.read_csv()`, `df.dtypes`, and `df.describe()`.
