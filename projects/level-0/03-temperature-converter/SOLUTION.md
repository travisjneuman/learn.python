# Solution: Level 0 / Project 03 - Temperature Converter

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 0 project: Temperature Converter.

Convert temperatures between Celsius, Fahrenheit, and Kelvin
using interactive input.

Concepts: functions, return values, float arithmetic, rounding, if/elif/else.
"""


# WHY a dedicated function for each direction: Each conversion is one
# formula.  Isolating it in a function means tests can verify the math
# without worrying about units or routing logic.
def celsius_to_fahrenheit(c: float) -> float:
    """Convert Celsius to Fahrenheit.

    WHY this formula? -- The Fahrenheit scale has a different zero point
    and different-sized degrees than Celsius.  Multiply by 9/5 to scale,
    then add 32 to shift the zero point.
    """
    return c * 9 / 5 + 32


def fahrenheit_to_celsius(f: float) -> float:
    """Convert Fahrenheit to Celsius (reverse of the above)."""
    # WHY (f - 32) first: We undo the +32 shift before scaling back.
    # Order of operations matters — subtracting first is mathematically correct.
    return (f - 32) * 5 / 9


def celsius_to_kelvin(c: float) -> float:
    """Convert Celsius to Kelvin.

    WHY 273.15? -- The Kelvin scale starts at absolute zero, which is
    -273.15 degrees Celsius.  Adding 273.15 shifts the scale.
    """
    return c + 273.15


def kelvin_to_celsius(k: float) -> float:
    """Convert Kelvin to Celsius."""
    # WHY check for negative Kelvin: Kelvin cannot be negative by definition.
    # Temperatures below absolute zero do not exist in nature.  Raising an
    # error early prevents nonsensical results downstream.
    if k < 0:
        raise ValueError("Kelvin cannot be negative")
    return k - 273.15


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a temperature value between any two supported units.

    Strategy: convert everything to Celsius first, then to the target unit.
    WHY go through Celsius? -- It avoids writing a separate function for
    every possible pair (F->K, K->F, etc.).  With 3 units, direct pairs
    would need 6 functions.  Hub-and-spoke needs only 4 (2 to Celsius,
    2 from Celsius).
    """
    # WHY .upper(): Normalising the unit string means "c", "C", and "celsius"
    # (if we expand) all match the same branch.
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
    # WHY round to 2 decimal places: Floating-point arithmetic can produce
    # long decimals like 99.99999999997.  Rounding keeps the output clean.
    if to_unit == "C":
        return round(celsius, 2)
    elif to_unit == "F":
        return round(celsius_to_fahrenheit(celsius), 2)
    elif to_unit == "K":
        return round(celsius_to_kelvin(celsius), 2)
    else:
        raise ValueError(f"Unknown unit: {to_unit}")


if __name__ == "__main__":
    print("=== Temperature Converter ===")
    print("Supported units: C (Celsius), F (Fahrenheit), K (Kelvin)")
    print("Type 'quit' to exit.\n")

    while True:
        value_text = input("Enter temperature value (or 'quit'): ")

        if value_text.strip().lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        try:
            value = float(value_text)
        except ValueError:
            print(f"  '{value_text}' is not a valid number. Try again.\n")
            continue

        from_unit = input("Convert from (C/F/K): ").strip().upper()
        to_unit = input("Convert to (C/F/K): ").strip().upper()

        try:
            result = convert_temperature(value, from_unit, to_unit)
            print(f"  {value} {from_unit} = {result} {to_unit}")
        except ValueError as err:
            print(f"  ERROR: {err}")

        print()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Hub-and-spoke through Celsius | With 3 units, direct conversion needs 6 functions. Hub-and-spoke needs only 4. Adding a 4th unit (Rankine) adds 2 functions, not 6 | Direct conversion functions for every pair — works but duplicates math and gets unwieldy as units grow |
| `kelvin_to_celsius()` rejects negative Kelvin | Negative Kelvin is physically impossible. Catching it early prevents silently producing nonsensical results | Allow any value and let the caller validate — pushes responsibility to code that may forget to check |
| `round(result, 2)` on all outputs | Floating-point math produces tiny errors (e.g., `99.99999997`). Rounding keeps displayed values clean | Return raw floats — more precise but confusing when `100.0 C` shows as `99.99999999997 C` |
| `convert_temperature()` raises `ValueError` for unknown units | The function signals clearly that something is wrong. The caller decides how to handle it (print error, log, etc.) | Return an error dict like the calculator project — valid but inconsistent since temperature functions already raise `ValueError` |

## Alternative approaches

### Approach B: Direct conversion functions for every pair

```python
def fahrenheit_to_kelvin(f: float) -> float:
    return (f - 32) * 5 / 9 + 273.15

def kelvin_to_fahrenheit(k: float) -> float:
    return (k - 273.15) * 9 / 5 + 32

def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    converters = {
        ("C", "F"): celsius_to_fahrenheit,
        ("F", "C"): fahrenheit_to_celsius,
        ("C", "K"): celsius_to_kelvin,
        ("K", "C"): kelvin_to_celsius,
        ("F", "K"): fahrenheit_to_kelvin,
        ("K", "F"): kelvin_to_fahrenheit,
    }
    key = (from_unit.upper(), to_unit.upper())
    if key[0] == key[1]:
        return round(value, 2)
    if key not in converters:
        raise ValueError(f"Unsupported conversion: {from_unit} -> {to_unit}")
    return round(converters[key](value), 2)
```

**Trade-off:** Direct conversion is slightly faster (one function call instead of two) and each formula is explicit. But adding a 4th unit like Rankine requires 6 new functions instead of 2. The hub-and-spoke pattern scales better and is the standard approach in real unit-conversion libraries.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| User enters `-300` as a Kelvin value | `kelvin_to_celsius(-300)` raises `ValueError("Kelvin cannot be negative")` | Already handled; the try/except in __main__ catches it |
| User enters `X` as a unit code | `convert_temperature()` raises `ValueError("Unknown unit: X")` | Already handled by the else branches in the if/elif chain |
| User enters `hot` instead of a number | `float("hot")` raises `ValueError`, caught by the try/except around `float()` | Already handled in the input loop |
| Round-trip precision loss (C to F to C) | `100.0 -> 212.0 -> 100.0` works, but some values may drift by 0.01 due to floating-point math | `round(..., 2)` keeps drift below visible thresholds. The test allows `abs(back - original) < 0.01` |
| User enters `-460` Fahrenheit (below absolute zero) | Converts to Celsius successfully (about `-273.33`), then to Kelvin gives `-0.18` — not caught | Add a check in `convert_temperature()` that the Celsius intermediate value is >= -273.15 |

## Key takeaways

1. **The hub-and-spoke pattern reduces code duplication.** Routing all conversions through one common unit (Celsius) means you only write 2 functions per new unit instead of functions for every possible pair. This pattern appears in currency converters, distance converters, and time zone libraries.
2. **Validate impossible inputs early.** Negative Kelvin is physically meaningless. Catching it inside `kelvin_to_celsius()` means every path that touches Kelvin is protected, not just the interactive input loop.
3. **`round()` tames floating-point arithmetic.** Computers store decimals in binary, which causes tiny rounding errors. Rounding the output to a reasonable number of decimal places keeps results clean for human display.
4. **Functions with clear inputs and outputs are easy to test.** `assert celsius_to_fahrenheit(100) == 212.0` is a one-line test. No files, no user input, no setup needed. This is why separating logic from I/O matters.
