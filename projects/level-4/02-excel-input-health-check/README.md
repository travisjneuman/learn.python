# Level 4 / Project 02 - Excel Input Health Check
Home: [README](../../../README.md)

## Focus
- tabular input quality scoring

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-4/02-excel-input-health-check
python project.py --input data/sample_input.csv --output data/health_report.json
pytest -q
```

## Expected terminal output
```text
{
  "file": "data/sample_input.csv",
  "status": "WARN",
  "headers": { ... },
  "completeness": { "short_rows": [6], ... }
}
6 passed
```

## Expected artifacts
- `data/health_report.json` — structured quality report
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a check for rows that contain only numeric data (possible header/data swap).
2. Add a `--format` flag that supports both CSV and TSV input auto-detection.
3. Re-run script and tests — add a test for TSV delimiter detection.

## Break it (required)
1. Create a CSV where every row has a different number of columns — observe how completeness reports it.
2. Feed it a file with mixed encodings (e.g., Latin-1 characters) and watch the encoding check fail.
3. Create a CSV with 100+ duplicate header names and check the report.

## Fix it (required)
1. Add a max-issues limit so the report does not grow unbounded on very messy files.
2. Handle the mixed-encoding case by falling back to `latin-1` when UTF-8 fails.
3. Re-run until all tests pass.

## Explain it (teach-back)
1. Why does `detect_delimiter` use the *minimum* count across rows instead of the *average*?
2. What is the difference between `check_headers` and `check_row_completeness` — could they be merged?
3. Why does the health check return early when encoding fails instead of continuing?
4. How would you extend this to support Excel `.xlsx` files?

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
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../01-schema-validator-engine/README.md) | [Home](../../../README.md) | [Next →](../03-robust-csv-ingestor/README.md) |
|:---|:---:|---:|
