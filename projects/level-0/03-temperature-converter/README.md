# Level 0 / Project 03 - Temperature Converter
Home: [README](../../../README.md)

> **Try in Browser:** [Run this exercise online](../../browser/level-0.html?ex=3) — no installation needed!

## Before You Start

Recall these prerequisites before diving in:
- Can you write a function that takes one argument and returns a calculated result?
- Can you use a dictionary to look up a value by key?

## Focus
- functions and unit conversion practice

## Why this project exists
Convert temperatures between Celsius, Fahrenheit, and Kelvin by routing all conversions through Celsius as a hub. You will learn the hub-and-spoke pattern, which reduces code duplication when supporting multiple unit types.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/03-temperature-converter
python project.py
pytest -q
```

The program asks for a temperature, source unit, and target unit interactively. Type `quit` to exit.

## Expected terminal output
```text
=== Temperature Converter ===
Supported units: C (Celsius), F (Fahrenheit), K (Kelvin)
Type 'quit' to exit.

Enter temperature value (or 'quit'): 100
Convert from (C/F/K): C
Convert to (C/F/K): F
  100.0 C = 212.0 F

Enter temperature value (or 'quit'): quit
Goodbye!
5 passed
```

## Expected artifacts
- Passing tests
- Updated `notes.md`

## Worked Example

Here is a similar (but different) problem, solved step by step.

**Problem:** Write functions to convert between miles and kilometers, using kilometers as the hub.

**Step 1: Write the direct conversion functions.**

```python
def miles_to_km(miles):
    return miles * 1.60934

def km_to_miles(km):
    return km / 1.60934
```

**Step 2: Add a hub function that routes conversions.** Instead of writing functions for every pair (miles-to-meters, meters-to-miles, etc.), everything goes through km.

```python
def meters_to_km(meters):
    return meters / 1000

def km_to_meters(km):
    return km * 1000

def convert_distance(value, from_unit, to_unit):
    # Step 1: Convert to km (the hub)
    to_km = {"km": lambda v: v, "mi": miles_to_km, "m": meters_to_km}
    # Step 2: Convert from km to target
    from_km = {"km": lambda v: v, "mi": km_to_miles, "m": km_to_meters}

    km_value = to_km[from_unit](value)
    return from_km[to_unit](km_value)
```

**Step 3: Test it.** `convert_distance(1, "mi", "km")` should give `1.60934`. `convert_distance(1000, "m", "mi")` should give about `0.621`.

**The thought process:** The hub-and-spoke pattern means adding a new unit (like feet) only requires two new functions (feet-to-km and km-to-feet), not six new pair functions. This is exactly how the temperature converter works with Celsius as the hub.

## Alter it (required)
1. Add Rankine as a fourth temperature scale (Rankine = Fahrenheit + 459.67).
2. Ask the user how many decimal places they want in results and round accordingly.
3. Re-run script and tests.

## Break it (required)
1. Enter `-300` as a Kelvin value -- this is below absolute zero. Does `convert_temperature()` catch it?
2. Enter `X` as a unit -- what happens?
3. Enter `hot` instead of a number -- does `float()` fail gracefully?

## Fix it (required)
1. Ensure `celsius_to_kelvin()` and `kelvin_to_celsius()` reject temperatures below absolute zero.
2. Add validation for unknown unit codes in `convert_temperature()`.
3. Add a test that verifies the below-absolute-zero ValueError.

## Explain it (teach-back)
1. Why does the converter route all conversions through Celsius instead of having 6 direct functions?
2. What is the "hub and spoke" pattern and how does it reduce code duplication?
3. Why does `round()` matter for temperature display?
4. Where would unit conversion code appear in real applications (weather APIs, scientific instruments)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Files and Paths](../../../concepts/files-and-paths.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Files and Paths](../../../concepts/quizzes/files-and-paths-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Temperature Converter. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to route all conversions through Celsius as a hub. Can you explain the hub-and-spoke pattern using a different example, like currency conversion?"
- "Can you explain how to validate that a number is above a minimum value and raise an error if it is not?"

---

| [← Prev](../02-calculator-basics/README.md) | [Home](../../../README.md) | [Next →](../04-yes-no-questionnaire/README.md) |
|:---|:---:|---:|
