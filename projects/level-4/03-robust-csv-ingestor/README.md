# Level 4 / Project 03 - Robust CSV Ingestor
Home: [README](../../../README.md)

## Focus
- malformed row handling and recovery

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-4/03-robust-csv-ingestor
python project.py --input data/sample_input.csv --output-dir data/output
pytest -q
```

## Expected terminal output
```text
{
  "total_rows": 8,
  "good": 5,
  "quarantined": 3,
  "errors": [ ... ]
}
5 passed
```

## Expected artifacts
- `data/output/clean_data.csv` — rows that passed validation
- `data/output/quarantined_rows.csv` — bad rows with row numbers
- `data/output/ingestion_report.json` — summary with error details
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--max-errors` flag that stops processing after N quarantined rows.
2. Add type validation: check that the `age` column contains only integers.
3. Re-run script and tests — add a parametrized test for the new type check.

## Break it (required)
1. Feed it a CSV with no header row — observe what happens to the column count logic.
2. Create a CSV where quoted fields contain the delimiter character (`"Smith, Jr."`) — does it handle this?
3. Add a row with embedded newlines and see if the parser splits it incorrectly.

## Fix it (required)
1. Add a `--has-header` flag (default True) to handle header-less CSVs.
2. Ensure the quarantine file includes the original error reason per row.
3. Re-run until all tests pass.

## Explain it (teach-back)
1. Why does the quarantine file prepend the original row number?
2. What is the difference between "too few columns" and "all fields empty"?
3. Why do we write the quarantine file even if it is empty?
4. How would you adapt this pattern for streaming very large files (gigabytes)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Robust CSV Ingestor. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to handle malformed CSV rows without crashing. Can you explain strategies for recovering from bad rows in a data pipeline?"
- "Can you explain the difference between skipping bad rows, quarantining them, and fixing them automatically?"

---

| [← Prev](../02-excel-input-health-check/README.md) | [Home](../../../README.md) | [Next →](../04-data-contract-enforcer/README.md) |
|:---|:---:|---:|
