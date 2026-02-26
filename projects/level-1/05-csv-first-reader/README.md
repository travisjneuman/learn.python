# Level 1 / Project 05 - CSV First Reader
Home: [README](../../../README.md)

> **Try in Browser:** [Run this exercise online](../../browser/level-1.html?ex=5) — no installation needed!

## Before You Start

Recall these prerequisites before diving in:
- Can you open a file and read its contents line by line?
- Can you use a dictionary to store key-value pairs?

## Focus
- read csv rows into dictionaries

## Why this project exists
Load a CSV file using Python's `csv` module, display the data as a formatted table, and compute basic column statistics. This is your first encounter with structured tabular data and auto-detecting numeric columns.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-1/05-csv-first-reader
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== CSV Table ===

  name             department    salary  years
  ──────────────── ──────────── ─────── ──────
  Alice Johnson    Engineering   85000      5
  Bob Smith        Marketing     62000      3

  Numeric columns: salary (avg: 73500.0), years (avg: 4.0)
4 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--columns` flag that selects which columns to display (comma-separated names).
2. Add row numbering to the formatted table output.
3. Re-run script and tests.

## Break it (required)
1. Use a CSV file with no data rows (just headers) -- does `column_stats()` crash on empty data?
2. Use a CSV with inconsistent column counts (some rows have extra commas) -- what happens?
3. Use a column with mixed numeric/text values like `"10, N/A, 30"` -- does `detect_numeric_columns()` handle it?

## Fix it (required)
1. Handle empty-data CSVs by returning zero stats without crashing.
2. Ensure `detect_numeric_columns()` treats columns with any non-numeric values as text.
3. Add a test for the headers-only CSV case.

## Explain it (teach-back)
1. Why does `load_csv()` use `csv.DictReader` instead of splitting lines on commas?
2. What does `detect_numeric_columns()` do and why is auto-detection useful?
3. Why does `format_table()` truncate long values instead of letting them overflow?
4. Where would CSV table display appear in real software (data explorers, admin dashboards, report generators)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on CSV First Reader. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to format a table with aligned columns. Can you explain how Python string formatting with `:>10` or `:<20` works?"
- "Can you explain the difference between `csv.reader` and `csv.DictReader` with a simple example?"

---

| [← Prev](../04-log-line-parser/README.md) | [Home](../../../README.md) | [Next →](../06-simple-gradebook-engine/README.md) |
|:---|:---:|---:|
