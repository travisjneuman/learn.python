# Level 4 / Project 04 - Data Contract Enforcer
Home: [README](../../../README.md)

## Focus
- contract validation and drift detection

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-4/04-data-contract-enforcer
python project.py --contract data/contract.json --input data/sample_input.csv --output data/enforcement_report.json
pytest -q
```

## Expected terminal output
```text
{
  "total_rows": 8,
  "clean_rows": 3,
  "violation_count": 5,
  ...
}
6 passed
```

## Expected artifacts
- `data/enforcement_report.json` — per-row violation details
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `"pattern"` rule (regex) to the contract for email-like fields.
2. Add a `--strict` flag that also treats extra columns as violations.
3. Re-run script and tests — add a test for pattern enforcement.

## Break it (required)
1. Remove a required column entirely from the CSV and see what `missing_columns` reports.
2. Feed a value that is technically the right type but fails range AND allowed-values checks simultaneously.
3. Create a contract with contradictory rules (e.g., `min: 100, max: 50`) and observe the behavior.

## Fix it (required)
1. Add contract self-validation that catches contradictory rules before enforcement begins.
2. Handle the case where a column exists in the contract but not in the CSV data headers.
3. Re-run until all tests pass.

## Explain it (teach-back)
1. Why does `coerce_value` try to convert strings instead of checking types directly?
2. What is the difference between `missing_columns` and a required field that is empty?
3. Why are violations collected per-row instead of per-column?
4. How would this pattern work with a streaming data source (no full CSV in memory)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../03-robust-csv-ingestor/README.md) | [Home](../../../README.md) | [Next →](../05-path-safe-file-mover/README.md) |
|:---|:---:|---:|
