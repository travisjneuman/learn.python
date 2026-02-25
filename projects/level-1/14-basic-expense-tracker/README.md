# Level 1 / Project 14 - Basic Expense Tracker
Home: [README](../../../README.md)

## Focus
- simple ledger aggregation and reporting

## Why this project exists
Parse expense records from CSV, group them by category, compute totals and averages, and find the top spenders. You will learn CSV parsing, category aggregation, and sorting with lambda functions.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-1/14-basic-expense-tracker
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Expense Report ===

  Category     Total     Count  Average
  ──────────── ───────── ────── ────────
  Transport    $35.00    1      $35.00
  Food         $12.50    1      $12.50

  Grand total: $47.50
  Top expense: Monthly bus pass ($35.00)
8 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--category` filter flag that shows only expenses in a given category.
2. Add a monthly breakdown showing total spending per month.
3. Re-run script and tests.

## Break it (required)
1. Add a CSV row with a negative amount -- does `parse_expense()` reject it?
2. Add a row with a missing category field -- does validation catch it?
3. Use a file with no data rows (just headers) -- does `overall_stats()` crash on empty data?

## Fix it (required)
1. Ensure `parse_expense()` rejects negative amounts with a clear `ValueError`.
2. Handle the empty-expenses case in `overall_stats()` by returning zero stats.
3. Add a test for the missing-field case.

## Explain it (teach-back)
1. Why does `parse_expense()` normalise categories to lowercase with `.lower()`?
2. What does `csv.DictReader` do differently from reading lines and splitting on commas?
3. Why does `top_expenses()` use `sorted()` with `key=lambda` instead of `.sort()`?
4. Where would expense tracking appear in real software (personal finance apps, accounting systems, budget reports)?

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
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Functions Explained](../../../concepts/quizzes/functions-explained-quiz.py)

---

| [← Prev](../13-batch-rename-simulator/README.md) | [Home](../../../README.md) | [Next →](../15-level1-mini-automation/README.md) |
|:---|:---:|---:|
