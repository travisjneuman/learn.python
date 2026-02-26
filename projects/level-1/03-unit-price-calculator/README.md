# Level 1 / Project 03 - Unit Price Calculator
Home: [README](../../../README.md)

> **Try in Browser:** [Run this exercise online](../../browser/level-1.html?ex=3) — no installation needed!

## Before You Start

Recall these prerequisites before diving in:
- Can you open and read a CSV file using Python's `csv` module?
- Can you sort a list using `sorted()` with a `key` argument?

**Estimated time:** 25 minutes

## Focus
- math accuracy and formatting

## Why this project exists
Compare products by computing price-per-unit from CSV data, rank them from best to worst deal, and find the best value. You will learn CSV parsing with `csv.DictReader`, float arithmetic, and sorting with key functions.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-1/03-unit-price-calculator
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Unit Price Comparison ===

  Rice 10lb Bag     $15.49 / 10 lb  =>  $1.55/lb
  Rice 5lb Bag      $8.99  / 5 lb   =>  $1.80/lb

  Best deal: Rice 10lb Bag at $1.55/lb
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--category` filter flag that shows only products matching a category column.
2. Add a "savings" column showing how much you save vs the most expensive option.
3. Re-run script and tests.

## Break it (required) — Core
1. Add a CSV row with quantity `0` -- does `calculate_unit_price()` crash with division by zero?
2. Add a row with a negative price -- does the calculator accept it or reject it?
3. Add a row with missing columns -- does `parse_product_row()` handle it gracefully?

## Fix it (required) — Core
1. Ensure `calculate_unit_price()` raises `ValueError` for zero or negative quantities.
2. Validate that prices are non-negative in `parse_product_row()`.
3. Add a test for the zero-quantity edge case.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does `csv.DictReader` map columns by header name instead of by index?
2. What does `round(price / quantity, 2)` do and why round to 2 decimal places?
3. Why does `find_best_deal()` use `min()` with a `key` function instead of a manual loop?
4. Where would unit price calculations appear in real software (grocery apps, procurement systems)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Functions Explained](../../../concepts/functions-explained.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Functions Explained](../../../concepts/quizzes/functions-explained-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Unit Price Calculator. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to sort a list of dictionaries by one of the values. Can you show me how `sorted()` with a `key` function works, using a different example?"
- "Can you explain `csv.DictReader` with a simple example that is not about prices?"

---

| [← Prev](../02-password-strength-checker/README.md) | [Home](../../../README.md) | [Next →](../04-log-line-parser/README.md) |
|:---|:---:|---:|
