# Level 1 / Project 07 - Date Difference Helper
Home: [README](../../../README.md)

## Focus
- basic datetime parsing and deltas

## Why this project exists
Compute differences between dates, add days to a date, and find the day of the week. You will learn the `datetime` module, `strptime`/`strftime` for parsing and formatting, and `timedelta` for date arithmetic.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-1/07-date-difference-helper
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Date Helper ===

  diff 2024-01-01 2024-12-31 => 365 days
  diff 2024-06-15 2024-07-04 => 19 days
  add  2024-01-01 90         => 2024-03-31

Output written to data/output.json
6 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `weeks` command that returns the number of weeks and remaining days between two dates.
2. Add support for alternate date formats like `DD/MM/YYYY` using a `--format` flag.
3. Re-run script and tests.

## Break it (required)
1. Add a line with an invalid date like `diff 2024-02-30 2024-03-01` (Feb 30 does not exist) -- does `parse_date()` crash?
2. Add a `diff` command with dates in reversed order -- does `days_between()` return a negative number?
3. Add a command with a misspelled action like `dif 2024-01-01 2024-01-10` -- what happens?

## Fix it (required)
1. Wrap `parse_date()` in a try/except to handle invalid dates with a clear error message.
2. Ensure `days_between()` always returns a non-negative value using `abs()`.
3. Add a test for the reversed-dates case.

## Explain it (teach-back)
1. What does `datetime.strptime("2024-01-15", "%Y-%m-%d")` do and what does each `%` code mean?
2. Why does `timedelta(days=N)` exist and how is it different from just adding an integer to a date?
3. What does `.strftime("%A")` return and why is day-of-week useful?
4. Where would date calculations appear in real software (billing cycles, SLA tracking, scheduling)?

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

| [← Prev](../06-simple-gradebook-engine/README.md) | [Home](../../../README.md) | [Next →](../08-path-exists-checker/README.md) |
|:---|:---:|---:|
