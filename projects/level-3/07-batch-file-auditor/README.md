# Level 3 / Project 07 - Batch File Auditor
Home: [README](../../../README.md)

## Focus
- scan many files with diagnostics

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-3/07-batch-file-auditor
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
1. Add CSV export of the audit results with columns: filename, size, last_modified, status.
2. Add a `--pattern` flag that filters which files to audit (e.g., `*.csv` or `*.json`).
3. Add a summary line at the end: total files scanned, passed, failed.
4. Re-run script and tests.

## Break it (required)
1. Use malformed or edge-case input.
2. Confirm behavior fails or degrades predictably.
3. Capture the first failing test or visible bad output.

## Fix it (required)
1. Add or update defensive checks.
2. Add or update tests for the broken case.
3. Re-run until output and tests are deterministic.

## Explain it (teach-back)
1. What assumptions did this project make?
2. What broke first and why?
3. What exact change fixed it?
4. How would this pattern apply in enterprise automation work?

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
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../06-structured-error-handler/README.md) | [Home](../../../README.md) | [Next →](../08-template-driven-reporter/README.md) |
|:---|:---:|---:|
