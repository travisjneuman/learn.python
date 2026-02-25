"""Level 3 project: CLI Arguments Workbench.

Advanced argparse patterns: subcommands, mutually exclusive groups,
custom types, and argument validation.

Skills practiced: argparse subcommands, typing basics, logging,
dataclasses, error handling patterns.
"""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ConversionResult:
    """Result of a unit conversion."""
    input_value: float
    input_unit: str
    output_value: float
    output_unit: str
    formula: str


def positive_float(value: str) -> float:
    """Custom argparse type: only accepts positive floats."""
    try:
        f = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value!r} is not a valid number")
    if f <= 0:
        raise argparse.ArgumentTypeError(f"{f} is not positive")
    return f


def celsius_to_fahrenheit(c: float) -> ConversionResult:
    """Convert Celsius to Fahrenheit."""
    f = c * 9 / 5 + 32
    return ConversionResult(c, "C", round(f, 2), "F", "F = C * 9/5 + 32")


def fahrenheit_to_celsius(f: float) -> ConversionResult:
    """Convert Fahrenheit to Celsius."""
    c = (f - 32) * 5 / 9
    return ConversionResult(f, "F", round(c, 2), "C", "C = (F - 32) * 5/9")


def km_to_miles(km: float) -> ConversionResult:
    """Convert kilometers to miles."""
    mi = km * 0.621371
    return ConversionResult(km, "km", round(mi, 4), "mi", "mi = km * 0.621371")


def miles_to_km(mi: float) -> ConversionResult:
    """Convert miles to kilometers."""
    km = mi / 0.621371
    return ConversionResult(mi, "mi", round(km, 4), "km", "km = mi / 0.621371")


def kg_to_lbs(kg: float) -> ConversionResult:
    """Convert kilograms to pounds."""
    lbs = kg * 2.20462
    return ConversionResult(kg, "kg", round(lbs, 4), "lbs", "lbs = kg * 2.20462")


def lbs_to_kg(lbs: float) -> ConversionResult:
    """Convert pounds to kilograms."""
    kg = lbs / 2.20462
    return ConversionResult(lbs, "lbs", round(kg, 4), "kg", "kg = lbs / 2.20462")


CONVERTERS = {
    "temp": {"c-to-f": celsius_to_fahrenheit, "f-to-c": fahrenheit_to_celsius},
    "dist": {"km-to-mi": km_to_miles, "mi-to-km": miles_to_km},
    "weight": {"kg-to-lbs": kg_to_lbs, "lbs-to-kg": lbs_to_kg},
}


def batch_convert(operations: list[dict]) -> list[dict]:
    """Run a batch of conversions from a JSON list."""
    results = []
    for op in operations:
        category = op.get("category", "")
        conversion = op.get("conversion", "")
        value = op.get("value", 0)
        converter = CONVERTERS.get(category, {}).get(conversion)
        if converter:
            result = converter(float(value))
            results.append(asdict(result))
        else:
            results.append({"error": f"Unknown: {category}/{conversion}"})
    return results


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        description="Unit conversion workbench",
        epilog="Examples: project.py temp --c-to-f 100",
    )
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--json", action="store_true", help="JSON output")

    sub = parser.add_subparsers(dest="command")

    # Temperature with mutually exclusive group.
    temp = sub.add_parser("temp", help="Temperature conversions")
    temp_group = temp.add_mutually_exclusive_group(required=True)
    temp_group.add_argument("--c-to-f", type=float, metavar="CELSIUS")
    temp_group.add_argument("--f-to-c", type=float, metavar="FAHRENHEIT")

    # Distance.
    dist = sub.add_parser("dist", help="Distance conversions")
    dist_group = dist.add_mutually_exclusive_group(required=True)
    dist_group.add_argument("--km-to-mi", type=positive_float, metavar="KM")
    dist_group.add_argument("--mi-to-km", type=positive_float, metavar="MILES")

    # Weight.
    weight = sub.add_parser("weight", help="Weight conversions")
    weight_group = weight.add_mutually_exclusive_group(required=True)
    weight_group.add_argument("--kg-to-lbs", type=positive_float, metavar="KG")
    weight_group.add_argument("--lbs-to-kg", type=positive_float, metavar="LBS")

    # Batch from file.
    batch = sub.add_parser("batch", help="Batch conversions from JSON")
    batch.add_argument("file", help="JSON file with operations")

    return parser


def main() -> None:
    """Entry point: parse args and run conversion."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    result: Optional[ConversionResult] = None

    if args.command == "temp":
        result = celsius_to_fahrenheit(args.c_to_f) if args.c_to_f is not None else fahrenheit_to_celsius(args.f_to_c)
    elif args.command == "dist":
        result = km_to_miles(args.km_to_mi) if args.km_to_mi is not None else miles_to_km(args.mi_to_km)
    elif args.command == "weight":
        result = kg_to_lbs(args.kg_to_lbs) if args.kg_to_lbs is not None else lbs_to_kg(args.lbs_to_kg)
    elif args.command == "batch":
        data = json.loads(Path(args.file).read_text(encoding="utf-8"))
        print(json.dumps(batch_convert(data), indent=2))
        return

    if result:
        if args.json:
            print(json.dumps(asdict(result), indent=2))
        else:
            print(f"{result.input_value} {result.input_unit} = {result.output_value} {result.output_unit}")
            if args.verbose:
                print(f"Formula: {result.formula}")


if __name__ == "__main__":
    main()
