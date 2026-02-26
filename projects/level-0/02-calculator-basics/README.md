# Level 0 / Project 02 - Calculator Basics
Home: [README](../../../README.md)

> **Try in Browser:** [Run this exercise online](../../browser/level-0.html?ex=2) — no installation needed!

## Before You Start

Recall these prerequisites before diving in:
- Can you write a function that takes two arguments and returns their sum?
- Can you convert a string to a number using `int()` or `float()`?

**Estimated time:** 15 minutes

## Focus
- numeric input, arithmetic, and safe casting

## Why this project exists
Build a four-operation calculator that reads expressions from a file. You will practise arithmetic operators, float/int conversion, and dispatching operations with a dictionary.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/02-calculator-basics
python project.py
pytest -q
```

The program asks you to type expressions interactively. Type `quit` to exit.

## Expected terminal output
```text
=== Calculator ===
Type an expression like '10 + 5' or 'quit' to exit.

Supported operators: +  -  *  /

Enter expression: 10 + 5
  10 + 5 = 15.0

Enter expression: 6 * 7
  6 * 7 = 42.0

Enter expression: quit
Goodbye!
5 passed
```

## Expected artifacts
- Passing tests
- Updated `notes.md`

## Worked Example

Here is a similar (but different) problem, solved step by step.

**Problem:** Write a function that takes a string like `"5 squared"` and returns the result.

**Step 1: Parse the input.** Split the string into parts and figure out what operation to do.

```python
def parse_power(text):
    parts = text.strip().split()
    base = float(parts[0])
    keyword = parts[1].lower()
    powers = {"squared": 2, "cubed": 3}
    if keyword not in powers:
        raise ValueError(f"Unknown power: {keyword}")
    return base ** powers[keyword]
```

**Step 2: Test it mentally.** `"5 squared"` splits into `["5", "squared"]`. `float("5")` gives `5.0`. `powers["squared"]` gives `2`. `5.0 ** 2` gives `25.0`. Looks right.

**Step 3: Think about what could go wrong.** What if the user types `"hello squared"`? `float("hello")` will raise `ValueError`. What if they type just `"5"`? `parts[1]` will raise `IndexError`. We should catch these.

```python
def parse_power(text):
    parts = text.strip().split()
    if len(parts) != 2:
        raise ValueError(f"Expected 'number power', got: {text}")
    base = float(parts[0])  # raises ValueError if not a number
    keyword = parts[1].lower()
    powers = {"squared": 2, "cubed": 3}
    if keyword not in powers:
        raise ValueError(f"Unknown power: {keyword}")
    return base ** powers[keyword]
```

**The thought process:** Parse first, validate, then compute. This is the same pattern the calculator project uses with its `operations` dict.

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add support for modulo (`%`) and exponentiation (`**`) operations.
2. After each calculation, ask the user "Round to how many decimal places? (Enter to skip): " and round accordingly.
3. Re-run script and tests.

## Break it (required) — Core
1. Type `10 / 0` -- does it raise `ValueError` or crash with `ZeroDivisionError`?
2. Type just one number like `5` -- what happens when there is no operator or second operand?
3. Type text instead of numbers like `hello + world` -- does `float()` fail gracefully?

## Fix it (required) — Core
1. Ensure `divide()` raises `ValueError` with a clear message for zero divisors.
2. Add validation in `calculate()` that checks for exactly two numeric operands.
3. Add a test for the malformed-expression case.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does the `operations` dict map strings to functions, instead of using if/elif chains?
2. What does `float()` do and when does it raise `ValueError`?
3. Why is division by zero handled in `divide()` rather than in `calculate()`?
4. Where would expression parsers be used in real software (spreadsheets, query engines)?

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

- "I am working on Calculator Basics. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to map operator strings to functions using a dictionary. Can you show me a simple example of using a dict to dispatch functions, using a different topic than calculators?"
- "Can you explain what `float()` does and when it raises an error, with examples?"

---

| [← Prev](../01-terminal-hello-lab/README.md) | [Home](../../../README.md) | [Next →](../03-temperature-converter/README.md) |
|:---|:---:|---:|
