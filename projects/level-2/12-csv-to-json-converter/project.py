"""Level 2 project: CSV to JSON Converter.

Heavily commented beginner-friendly script:
- convert CSV files to JSON with automatic type inference,
- detect whether values are integers, floats, booleans, or strings,
- support both array-of-objects and object-of-arrays output formats.

Skills practiced: dict/list comprehensions, try/except for type detection,
enumerate, zip, re module for pattern matching, sorting with key.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def detect_delimiter(line: str) -> str:
    """Auto-detect the CSV delimiter by counting candidates.

    Checks comma, tab, semicolon, and pipe. Returns whichever
    appears most frequently in the header line.
    """
    candidates = {",": 0, "\t": 0, ";": 0, "|": 0}

    for char in candidates:
        candidates[char] = line.count(char)

    # Return the delimiter with the highest count.
    # sorted with key function — ties broken by dict order.
    best = sorted(candidates.items(), key=lambda pair: pair[1], reverse=True)
    return best[0][0] if best[0][1] > 0 else ","


def infer_type(value: str) -> object:
    """Infer the Python type of a string value.

    Tries conversions in order: bool, int, float, then falls back to str.
    This is how real CSV parsers decide column types.
    """
    stripped = value.strip()

    # Check for empty/null values.
    if stripped == "" or stripped.lower() in ("null", "none", "na", "n/a"):
        return None

    # Check for booleans (must come before int to avoid True -> 1).
    if stripped.lower() in ("true", "yes"):
        return True
    if stripped.lower() in ("false", "no"):
        return False

    # Try integer conversion.
    try:
        return int(stripped)
    except ValueError:
        pass

    # Try float conversion.
    try:
        return float(stripped)
    except ValueError:
        pass

    # Default: keep as string.
    return stripped


def parse_csv(
    text: str,
    delimiter: str | None = None,
    infer_types: bool = True,
) -> tuple[list[str], list[dict]]:
    """Parse CSV text into headers and a list of record dicts.

    Args:
        text: Raw CSV text content.
        delimiter: Field separator (auto-detected if None).
        infer_types: If True, convert values to int/float/bool.

    Returns:
        Tuple of (headers, records) where each record is a dict.
    """
    lines = text.splitlines()
    # Remove blank lines and comment lines.
    lines = [l for l in lines if l.strip() and not l.strip().startswith("#")]

    if not lines:
        return [], []

    # Auto-detect delimiter from header line.
    if delimiter is None:
        delimiter = detect_delimiter(lines[0])

    headers = [h.strip() for h in lines[0].split(delimiter)]
    records: list[dict] = []

    for line_num, line in enumerate(lines[1:], start=2):
        values = [v.strip() for v in line.split(delimiter)]

        # Pad short rows with empty strings.
        while len(values) < len(headers):
            values.append("")

        # Build record dict using zip to pair headers with values.
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

    This is the most common JSON format for tabular data:
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

    # Dict comprehension building column lists.
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
    parser.add_argument(
        "--output", default=None, help="Path to write JSON output"
    )
    parser.add_argument(
        "--delimiter", default=None, help="Field delimiter (auto-detect if omitted)"
    )
    parser.add_argument(
        "--format",
        choices=["objects", "columns"],
        default="objects",
        help="Output JSON format",
    )
    parser.add_argument(
        "--no-types",
        action="store_true",
        help="Keep all values as strings (no type inference)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output",
    )
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
