"""Level 0 project: Temperature Converter.

Convert temperatures between Celsius, Fahrenheit, and Kelvin
using interactive input.

Concepts: functions, return values, float arithmetic, rounding, if/elif/else.
"""


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


# This guard means the code below only runs when you execute the file
# directly (python project.py), NOT when another file imports it.
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
