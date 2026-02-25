"""Level 0 project: Temperature Converter.

Convert temperatures between Celsius, Fahrenheit, and Kelvin.
Reads conversion requests from a file and prints a results table.

Concepts: functions, return values, float arithmetic, rounding, if/elif/else.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def celsius_to_fahrenheit(c: float) -> float:
    """Convert Celsius to Fahrenheit.

    WHY this formula? -- The Fahrenheit scale has a different zero point
    and different-sized degrees than Celsius.  Multiply by 9/5 to scale,
    then add 32 to shift the zero point.
    """
    return c * 9 / 5 + 32


def fahrenheit_to_celsius(f: float) -> float:
    """Convert Fahrenheit to Celsius (reverse of the above)."""
    return (f - 32) * 5 / 9


def celsius_to_kelvin(c: float) -> float:
    """Convert Celsius to Kelvin.

    WHY 273.15? -- The Kelvin scale starts at absolute zero, which is
    -273.15 degrees Celsius.  Adding 273.15 shifts the scale.
    """
    return c + 273.15


def kelvin_to_celsius(k: float) -> float:
    """Convert Kelvin to Celsius."""
    if k < 0:
        raise ValueError("Kelvin cannot be negative")
    return k - 273.15


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a temperature value between any two supported units.

    Strategy: convert everything to Celsius first, then to the target unit.
    WHY go through Celsius? -- It avoids writing a separate function for
    every possible pair (F->K, K->F, etc.).  Two hops is simpler.
    """
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()

    # Step 1: normalise to Celsius.
    if from_unit == "C":
        celsius = value
    elif from_unit == "F":
        celsius = fahrenheit_to_celsius(value)
    elif from_unit == "K":
        celsius = kelvin_to_celsius(value)
    else:
        raise ValueError(f"Unknown unit: {from_unit}")

    # Step 2: convert from Celsius to the target.
    if to_unit == "C":
        return round(celsius, 2)
    elif to_unit == "F":
        return round(celsius_to_fahrenheit(celsius), 2)
    elif to_unit == "K":
        return round(celsius_to_kelvin(celsius), 2)
    else:
        raise ValueError(f"Unknown unit: {to_unit}")


def process_file(path: Path) -> list[dict]:
    """Read conversion requests from a file.

    Expected format per line: VALUE FROM_UNIT TO_UNIT
    Example: 100 C F
    """
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    results = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        parts = stripped.split()
        if len(parts) != 3:
            results.append({"input": stripped, "error": "Expected: VALUE FROM_UNIT TO_UNIT"})
            continue

        raw_value, from_unit, to_unit = parts

        try:
            value = float(raw_value)
        except ValueError:
            results.append({"input": stripped, "error": f"Not a number: {raw_value}"})
            continue

        try:
            converted = convert_temperature(value, from_unit, to_unit)
        except ValueError as err:
            results.append({"input": stripped, "error": str(err)})
            continue

        results.append({
            "input": stripped,
            "value": value,
            "from": from_unit.upper(),
            "to": to_unit.upper(),
            "result": converted,
        })

    return results


def parse_args() -> argparse.Namespace:
    """Define command-line options."""
    parser = argparse.ArgumentParser(description="Temperature Converter")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    """Program entry point."""
    args = parse_args()
    results = process_file(Path(args.input))

    for item in results:
        if "error" in item:
            print(f"  {item['input']}  =>  ERROR: {item['error']}")
        else:
            print(f"  {item['value']} {item['from']} => {item['result']} {item['to']}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\n{len(results)} conversions written to {output_path}")


if __name__ == "__main__":
    main()
