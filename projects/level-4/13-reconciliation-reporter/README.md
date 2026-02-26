# Level 4 / Project 13 - Reconciliation Reporter
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | [Browser](../../../browser/level-4.html) |

<!-- modality-hub-end -->

**Estimated time:** 70 minutes

## Focus
- source vs target comparison outputs

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-4/13-reconciliation-reporter
python project.py --source data/source.csv --target data/target.csv --output data/reconciliation_report.json --key id
pytest -q
```

## Expected terminal output
```text
{
  "source_records": 5,
  "target_records": 4,
  "matched": 1,
  "mismatches": 2,
  "only_in_source": 2,
  "only_in_target": 1
}
6 passed
```

## Expected artifacts
- `data/reconciliation_report.json` — full comparison report
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--tolerance` flag for numeric fields (e.g., salary difference within 5% is still "matched").
2. Add a `--format` flag to output the report as CSV instead of JSON.
3. Re-run script and tests — add a test for numeric tolerance.

## Break it (required) — Core
1. Use a key field that has duplicate values in one file — observe the "last row wins" behavior.
2. Feed two CSVs with completely different headers and see what happens.
3. Use an empty CSV (headers only) as one of the inputs.

## Fix it (required) — Core
1. Handle duplicate keys by reporting them as a warning instead of silently overwriting.
2. Report header differences as part of the reconciliation.
3. Re-run until all tests pass.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does `reconcile` use set operations (union, intersection, difference)?
2. What is the purpose of `compare_fields` — when would you NOT compare all fields?
3. Why does the report separate "only_in_source" from "mismatches"?
4. How would this scale to files with millions of rows?

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
- [Http Explained](../../../concepts/http-explained.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../12-checkpoint-recovery-tool/README.md) | [Home](../../../README.md) | [Next →](../14-configurable-batch-runner/README.md) |
|:---|:---:|---:|
