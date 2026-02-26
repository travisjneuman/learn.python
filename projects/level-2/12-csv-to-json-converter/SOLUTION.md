# CSV to JSON Converter — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""CSV to JSON Converter — complete annotated solution."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def detect_delimiter(line: str) -> str:
    """Auto-detect the CSV delimiter by counting candidates."""
    candidates = {",": 0, "\t": 0, ";": 0, "|": 0}

    for char in candidates:
        candidates[char] = line.count(char)

    # WHY: The delimiter that appears most often in the header line is
    # almost certainly the field separator. sorted() with key gives us
    # the highest count first.
    best = sorted(candidates.items(), key=lambda pair: pair[1], reverse=True)
    # WHY: Fall back to comma if no delimiter candidates were found at all
    # (e.g., a single-column CSV).
    return best[0][0] if best[0][1] > 0 else ","


def infer_type(value: str) -> object:
    """Infer the Python type of a string value.

    Tries conversions in order: null check, bool, int, float, then string.
    """
    stripped = value.strip()

    # WHY: Check for null/empty values first. These should become None,
    # not the string "null" or "N/A".
    if stripped == "" or stripped.lower() in ("null", "none", "na", "n/a"):
        return None

    # WHY: Boolean check must come before int check because Python's
    # int("true") would fail, but more importantly, True/False have
    # semantic meaning that should not be lost to integer conversion.
    if stripped.lower() in ("true", "yes"):
        return True
    if stripped.lower() in ("false", "no"):
        return False

    # WHY: Try int before float because int is more specific. "42" should
    # become int 42, not float 42.0. If int fails, float might still work
    # for values like "3.14".
    try:
        return int(stripped)
    except ValueError:
        pass

    try:
        return float(stripped)
    except ValueError:
        pass

    # WHY: If nothing else matches, keep the original string.
    return stripped


def parse_csv(
    text: str,
    delimiter: str | None = None,
    infer_types: bool = True,
) -> tuple[list[str], list[dict]]:
    """Parse CSV text into headers and a list of record dicts."""
    lines = text.splitlines()
    # WHY: Filter out blank lines and comment lines (starting with #)
    # to handle messy real-world CSV files gracefully.
    lines = [l for l in lines if l.strip() and not l.strip().startswith("#")]

    if not lines:
        return [], []

    if delimiter is None:
        delimiter = detect_delimiter(lines[0])

    headers = [h.strip() for h in lines[0].split(delimiter)]
    records: list[dict] = []

    for line_num, line in enumerate(lines[1:], start=2):
        values = [v.strip() for v in line.split(delimiter)]

        # WHY: Pad short rows so every record has the same fields.
        # Without padding, a row with 3 values and 5 headers would
        # produce a record missing 2 fields.
        while len(values) < len(headers):
            values.append("")

        # WHY: zip pairs each header with its corresponding value.
        # With type inference, each value is converted to its natural type.
        if infer_types:
            record = {h: infer_type(v) for h, v in zip(headers, values)}
        else:
            record = dict(zip(headers, values))

        records.append(record)

    return headers, records


def csv_to_json_objects(
    text: str, delimiter: str | None = None, infer_types: bool = True
) -> list[dict]:
    """Convert CSV to array-of-objects format.

    The most common JSON format for tabular data:
        [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
    """
    _, records = parse_csv(text, delimiter=delimiter, infer_types=infer_types)
    return records


def csv_to_json_columns(
    text: str, delimiter: str | None = None, infer_types: bool = True
) -> dict[str, list]:
    """Convert CSV to object-of-arrays (columnar) format.

    Useful for data analysis and charting:
        {"name": ["Alice", "Bob"], "age": [30, 25]}
    """
    headers, records = parse_csv(text, delimiter=delimiter, infer_types=infer_types)

    # WHY: Dict comprehension builds each column by extracting one field
    # from every record. This is a transpose operation — rows become columns.
    columns = {h: [r.get(h) for r in records] for h in headers}
    return columns


def convert_file(
    path: Path,
    output_format: str = "objects",
    delimiter: str | None = None,
    infer_types: bool = True,
) -> dict:
    """Convert a CSV file to JSON and return result with metadata."""
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    text = path.read_text(encoding="utf-8")
    headers, records = parse_csv(text, delimiter=delimiter, infer_types=infer_types)

    if output_format == "columns":
        data = csv_to_json_columns(text, delimiter=delimiter, infer_types=infer_types)
    else:
        data = csv_to_json_objects(text, delimiter=delimiter, infer_types=infer_types)

    return {
        "headers": headers,
        "row_count": len(records),
        "format": output_format,
        "data": data,
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="CSV to JSON converter")
    parser.add_argument("input", help="Path to CSV input file")
    parser.add_argument("--output", default=None, help="Path to write JSON output")
    parser.add_argument("--delimiter", default=None, help="Field delimiter")
    parser.add_argument(
        "--format", choices=["objects", "columns"], default="objects",
        help="Output JSON format",
    )
    parser.add_argument("--no-types", action="store_true", help="Keep all values as strings")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    return parser.parse_args()


def main() -> None:
    """Entry point: convert CSV to JSON."""
    args = parse_args()
    result = convert_file(
        Path(args.input),
        output_format=args.format,
        delimiter=args.delimiter,
        infer_types=not args.no_types,
    )

    indent = 2 if args.pretty else None
    json_str = json.dumps(result["data"], indent=indent)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json_str + "\n", encoding="utf-8")
        print(f"Wrote {result['row_count']} records to {args.output}")
    else:
        print(json_str)


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Auto-detect delimiter | Real CSV files use commas, tabs, semicolons, or pipes inconsistently. Auto-detection by counting characters in the header line makes the tool work without manual configuration. |
| Type inference order: bool, int, float, string | Booleans must be checked before integers (otherwise `True` would not match any numeric pattern). Integers before floats because `42` should be `int(42)`, not `float(42.0)`. The order matters for correct type assignment. |
| Two output formats (objects vs columns) | Array-of-objects is human-readable and matches how databases return rows. Columnar format is more efficient for data analysis (e.g., computing the mean of a column). Supporting both covers the main use cases. |
| `--no-types` flag | Sometimes you want all values as strings (e.g., ZIP codes like "01234" that would lose the leading zero as int 1234). Disabling type inference preserves the exact original values. |
| Padding short rows | A row with fewer values than headers is common in messy CSVs. Padding with empty strings ensures every record has the same set of keys, preventing downstream `KeyError` crashes. |

## Alternative Approaches

### Using Python's `csv` module

```python
import csv
from io import StringIO

def parse_with_csv_module(text):
    reader = csv.DictReader(StringIO(text))
    return list(reader)  # Returns list of OrderedDicts
```

The `csv` module handles quoting (`"Smith, Jr."` as a single field), escaping, and multi-line values automatically. The manual `split()` approach in this project breaks on quoted fields containing commas. For production code, always use the `csv` module.

### Using `pandas.read_csv`

```python
import pandas as pd

df = pd.read_csv("data.csv")
json_str = df.to_json(orient="records")  # array-of-objects
# or
json_str = df.to_json(orient="columns")  # columnar
```

Pandas handles encoding detection, type inference, missing values, and quoted fields in one line. It is the standard tool for CSV processing in data science. This manual implementation teaches the underlying concepts.

## Common Pitfalls

1. **Quoted fields with commas** — The CSV value `"Smith, Jr.",30` should be one field `Smith, Jr.` followed by `30`. Naive `split(",")` produces three fields: `"Smith`, ` Jr."`, `30`. Use the `csv` module for files with quoted fields.

2. **Leading zeros lost in type inference** — ZIP code `"01234"` becomes `int(1234)`, losing the leading zero. Phone numbers, IDs, and codes should remain strings. The `--no-types` flag handles this, but a smarter approach would check if the leading character is `0` before converting to int.

3. **Encoding mismatches** — A CSV file saved as UTF-8 with BOM (byte order mark) will have `\ufeff` at the start of the first header. This makes the first column name something like `\ufeffname` instead of `name`. Use `encoding="utf-8-sig"` in `read_text()` to handle BOMs automatically.
