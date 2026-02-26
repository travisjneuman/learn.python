# CLI Arguments Workbench — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Level 3 project: CLI Arguments Workbench."""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


# WHY: a dataclass makes the conversion result self-documenting.
# Instead of returning a bare float, the caller gets the input,
# output, units, AND the formula — all in one structured object.
@dataclass
class ConversionResult:
    """Result of a unit conversion."""
    input_value: float
    input_unit: str
    output_value: float
    output_unit: str
    formula: str


def positive_float(value: str) -> float:
    """Custom argparse type: only accepts positive floats.

    WHY: argparse calls this function to validate and convert input.
    By raising ArgumentTypeError, argparse shows a user-friendly
    error instead of a raw traceback.
    """
    try:
        f = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value!r} is not a valid number")
    if f <= 0:
        raise argparse.ArgumentTypeError(f"{f} is not positive")
    return f


# WHY: each converter is a small, testable function with a single
# responsibility. They all return ConversionResult, so the caller
# does not need to know which specific conversion ran.

def celsius_to_fahrenheit(c: float) -> ConversionResult:
    f = c * 9 / 5 + 32
    return ConversionResult(c, "C", round(f, 2), "F", "F = C * 9/5 + 32")


def fahrenheit_to_celsius(f: float) -> ConversionResult:
    c = (f - 32) * 5 / 9
    return ConversionResult(f, "F", round(c, 2), "C", "C = (F - 32) * 5/9")


def km_to_miles(km: float) -> ConversionResult:
    mi = km * 0.621371
    return ConversionResult(km, "km", round(mi, 4), "mi", "mi = km * 0.621371")


def miles_to_km(mi: float) -> ConversionResult:
    km = mi / 0.621371
    return ConversionResult(mi, "mi", round(km, 4), "km", "km = mi / 0.621371")


def kg_to_lbs(kg: float) -> ConversionResult:
    lbs = kg * 2.20462
    return ConversionResult(kg, "kg", round(lbs, 4), "lbs", "lbs = kg * 2.20462")


def lbs_to_kg(lbs: float) -> ConversionResult:
    kg = lbs / 2.20462
    return ConversionResult(lbs, "lbs", round(kg, 4), "kg", "kg = lbs / 2.20462")


# WHY: the CONVERTERS registry maps (category, conversion_name) to
# a function. This avoids a massive if/elif chain and makes it trivial
# to add new conversions — just add an entry to the dict.
CONVERTERS = {
    "temp": {"c-to-f": celsius_to_fahrenheit, "f-to-c": fahrenheit_to_celsius},
    "dist": {"km-to-mi": km_to_miles, "mi-to-km": miles_to_km},
    "weight": {"kg-to-lbs": kg_to_lbs, "lbs-to-kg": lbs_to_kg},
}


def batch_convert(operations: list[dict]) -> list[dict]:
    """Run a batch of conversions from a JSON list.

    WHY: batch mode lets users script many conversions in a single
    invocation. Each operation is looked up in the CONVERTERS registry.
    """
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

    # WHY: mutually exclusive groups ensure the user picks exactly
    # ONE conversion direction per category. argparse enforces this
    # automatically — you cannot pass both --c-to-f and --f-to-c.
    temp = sub.add_parser("temp", help="Temperature conversions")
    temp_group = temp.add_mutually_exclusive_group(required=True)
    temp_group.add_argument("--c-to-f", type=float, metavar="CELSIUS")
    temp_group.add_argument("--f-to-c", type=float, metavar="FAHRENHEIT")

    # WHY: distance and weight use positive_float to reject negative
    # values (negative distances/weights are physically meaningless).
    # Temperature uses plain float because negatives are valid.
    dist = sub.add_parser("dist", help="Distance conversions")
    dist_group = dist.add_mutually_exclusive_group(required=True)
    dist_group.add_argument("--km-to-mi", type=positive_float, metavar="KM")
    dist_group.add_argument("--mi-to-km", type=positive_float, metavar="MILES")

    weight = sub.add_parser("weight", help="Weight conversions")
    weight_group = weight.add_mutually_exclusive_group(required=True)
    weight_group.add_argument("--kg-to-lbs", type=positive_float, metavar="KG")
    weight_group.add_argument("--lbs-to-kg", type=positive_float, metavar="LBS")

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

    # WHY: check `is not None` rather than truthiness because 0.0 is
    # a valid temperature input but is falsy in Python.
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
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Custom `positive_float` type function | Argparse calls it during parsing, giving immediate user-friendly errors instead of crashing later in business logic. |
| `add_mutually_exclusive_group` per category | Prevents nonsensical input like `--c-to-f 100 --f-to-c 212` in the same command. Argparse enforces this constraint for free. |
| `ConversionResult` dataclass | Bundles input, output, units, and formula together. Functions return structured data, not bare numbers, so the caller has full context. |
| CONVERTERS registry dict | Adding a new conversion is a one-line dict entry instead of another if/elif branch. The registry pattern is used extensively in real frameworks. |
| Temperature allows negative, distance/weight does not | -40 degrees is valid; -10 km is not. Domain-appropriate validation at the parser level. |

## Alternative Approaches

### Using a single generic conversion function

```python
CONVERSION_TABLE = {
    ("C", "F"): lambda v: v * 9 / 5 + 32,
    ("F", "C"): lambda v: (v - 32) * 5 / 9,
    ("km", "mi"): lambda v: v * 0.621371,
}

def convert(value: float, from_unit: str, to_unit: str) -> float:
    key = (from_unit, to_unit)
    if key not in CONVERSION_TABLE:
        raise ValueError(f"No conversion from {from_unit} to {to_unit}")
    return CONVERSION_TABLE[key](value)
```

**Trade-off:** This is more compact and extensible (one table for all conversions), but you lose the per-conversion formula metadata and the clear function names that make tests self-documenting. Good for production code; less pedagogical.

## Common Pitfalls

1. **Checking `if args.c_to_f` instead of `if args.c_to_f is not None`** — The value 0.0 is falsy in Python, so `if args.c_to_f` would skip a valid input of 0 degrees. Always use `is not None` when a valid value could be zero.

2. **Forgetting `required=True` on mutually exclusive groups** — Without it, the user can run `project.py temp` with no conversion flag, and argparse will silently accept it, leading to a confusing `None` value downstream.

3. **Hardcoding conversion factors inline** — Scattering `* 2.20462` throughout the code makes it impossible to find and update. Keeping each conversion in its own named function (or a constants dict) makes the factor discoverable and testable.
