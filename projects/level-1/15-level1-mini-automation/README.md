# Level 1 / Project 15 - Level 1 Mini Automation
Home: [README](../../../README.md)

**Estimated time:** 40 minutes

## Focus
- multi-step beginner automation flow

## Why this project exists
Build a multi-step data pipeline that parses, validates, transforms, filters, and summarises records. This Level 1 capstone combines everything you have learned into a realistic ETL (Extract-Transform-Load) workflow.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-1/15-level1-mini-automation
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Automation Pipeline ===

  Step 1: Parsed 3 records
  Step 2: Validated 3 records (0 errors)
  Step 3: Transformed values
  Step 4: Filtered to 2 active records
  Step 5: Summary -- total value: $350.00

Output written to data/output.json
8 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a Step 6: `step_export_csv()` that writes active records to a CSV file.
2. Add a `--verbose` flag that prints the result of each pipeline step as it executes.
3. Re-run script and tests.

## Break it (required) — Core
1. Add a line with only 2 pipe-separated values -- does `step_parse_records()` skip it or crash?
2. Add a record with a non-numeric value field -- does `step_transform()` use the default 0.0?
3. Use a file where all records have status "failed" -- does `step_summarise()` handle an empty active list?

## Fix it (required) — Core
1. Ensure `step_parse_records()` skips lines with fewer than 3 pipe-separated fields.
2. Handle the all-filtered-out case in `step_summarise()` by returning zero counts.
3. Add a test for the non-numeric-value fallback.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why is the pipeline split into 5 separate `step_*` functions instead of one big function?
2. What is the "pipeline pattern" and why does each step take input and return output?
3. Why does `run_pipeline()` track counts at each step (total_lines, parsed, active)?
4. Where would multi-step pipelines appear in real software (ETL systems, CI/CD, data processing)?

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
- [How Imports Work](../../../concepts/how-imports-work.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Files and Paths](../../../concepts/quizzes/files-and-paths-quiz.py)

---

| [← Prev](../14-basic-expense-tracker/README.md) | [Home](../../../README.md) | [Next →](../README.md) |
|:---|:---:|---:|
