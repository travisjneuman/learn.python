# Level 4 / Project 04 - Data Contract Enforcer
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | [Browser](../../../browser/level-4.html) |

<!-- modality-hub-end -->

**Estimated time:** 50 minutes

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

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `"pattern"` rule (regex) to the contract for email-like fields.
2. Add a `--strict` flag that also treats extra columns as violations.
3. Re-run script and tests — add a test for pattern enforcement.

## Break it (required) — Core
1. Remove a required column entirely from the CSV and see what `missing_columns` reports.
2. Feed a value that is technically the right type but fails range AND allowed-values checks simultaneously.
3. Create a contract with contradictory rules (e.g., `min: 100, max: 50`) and observe the behavior.

## Fix it (required) — Core
1. Add contract self-validation that catches contradictory rules before enforcement begins.
2. Handle the case where a column exists in the contract but not in the CSV data headers.
3. Re-run until all tests pass.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

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

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Data Contract Enforcer. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to detect when a data file's structure changes unexpectedly. Can you explain what 'schema drift' means with a practical example?"
- "Can you explain how to compare two schemas and identify the differences?"

---

| [← Prev](../03-robust-csv-ingestor/README.md) | [Home](../../../README.md) | [Next →](../05-path-safe-file-mover/README.md) |
|:---|:---:|---:|
