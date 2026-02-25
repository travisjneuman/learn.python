"""Level 0 project: Calculator Basics.

A four-operation calculator that reads expressions from a file,
computes results, and writes an output report.

Concepts: arithmetic operators, float/int conversion, input validation, functions.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of two numbers."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return the quotient of two numbers.

    WHY check for zero? -- Dividing by zero crashes the program.
    Checking first lets us return a clear error message instead.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def calculate(expression: str) -> dict:
    """Parse a simple expression like '10 + 5' and return the result.

    WHY split on spaces? -- We expect the format 'number operator number'.
    Splitting on whitespace gives us exactly three pieces to work with.

    Returns a dict with the original expression and computed result,
    or an error message if parsing fails.
    """
    parts = expression.strip().split()

    if len(parts) != 3:
        return {"expression": expression.strip(), "error": "Expected format: number operator number"}

    raw_a, operator, raw_b = parts

    # Try converting strings to numbers. If the user typed 'abc' this fails.
    try:
        a = float(raw_a)
        b = float(raw_b)
    except ValueError:
        return {"expression": expression.strip(), "error": f"Invalid numbers: {raw_a}, {raw_b}"}

    # Map the operator string to the right function.
    operations = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
    }

    if operator not in operations:
        return {"expression": expression.strip(), "error": f"Unknown operator: {operator}"}

    try:
        result = operations[operator](a, b)
    except ValueError as err:
        return {"expression": expression.strip(), "error": str(err)}

    return {"expression": expression.strip(), "result": result}


def process_file(path: Path) -> list[dict]:
    """Read a file of expressions (one per line) and calculate each.

    WHY return a list of dicts? -- Each dict holds one result.
    A list of dicts is easy to convert to JSON for the output file.
    """
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    results = []

    for line in lines:
        # Skip blank lines so stray newlines don't cause errors.
        if not line.strip():
            continue
        results.append(calculate(line))

    return results


def parse_args() -> argparse.Namespace:
    """Define command-line options."""
    parser = argparse.ArgumentParser(description="Calculator Basics")
    parser.add_argument("--input", default="data/sample_input.txt", help="File with expressions")
    parser.add_argument("--output", default="data/output.json", help="Results output file")
    return parser.parse_args()


def main() -> None:
    """Program entry point."""
    args = parse_args()

    results = process_file(Path(args.input))

    # Print each result to the terminal.
    for item in results:
        if "error" in item:
            print(f"  {item['expression']}  =>  ERROR: {item['error']}")
        else:
            print(f"  {item['expression']}  =>  {item['result']}")

    # Write results to JSON.
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\n{len(results)} results written to {output_path}")


if __name__ == "__main__":
    main()
