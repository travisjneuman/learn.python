# Level 7 / Project 10 - Multi Source Reconciler
Home: [README](../../../README.md)

## Focus
- compare source snapshots for divergence

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-7/10-multi-source-reconciler
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
... output_summary.json written ...
2 passed
```

## Expected artifacts
- `data/output_summary.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `tolerance` parameter for numeric comparisons (e.g. prices within 0.01 count as matching).
2. Add a `reconcile_three()` function that compares three sources simultaneously.
3. Re-run script and tests — verify tolerance and three-way reconciliation work.

## Break it (required)
1. Use a key field that does not exist in any records (e.g. `"nonexistent_id"`).
2. Compare records where one side has duplicate keys.
3. Observe empty results or last-write-wins behavior with duplicates.

## Fix it (required)
1. Validate that `key_field` exists in at least one record before proceeding.
2. Log a warning when duplicate keys are found in a single source.
3. Add tests for missing key fields and duplicate-key scenarios.

## Explain it (teach-back)
1. Why is set-based reconciliation the right approach for comparing data sources?
2. What happened when the key field did not exist in the records?
3. How did the validation prevent silent empty results?
4. Where is data reconciliation used in real financial or inventory systems?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../09-contract-version-checker/README.md) | [Home](../../../README.md) | [Next →](../11-pipeline-feature-flags/README.md) |
|:---|:---:|---:|
