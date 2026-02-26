# Level 5 / Project 08 - Cross File Joiner
Home: [README](../../../README.md)

> **Quick Recall:** This project uses dictionary lookups to match records across files. Before starting, make sure you can: build a dictionary from CSV rows using one column as the key, then look up values by that key (Level 1, Project 05 - CSV First Reader).

**Estimated time:** 75 minutes

## Focus
- join records across source files

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-5/08-cross-file-joiner
python project.py --left data/employees.csv --right data/departments.csv --key dept_id --join inner --output data/joined.json
pytest -q
```

## Expected terminal output
```text
Inner join: 4 matched rows on key 'dept_id'
5 passed
```

## Expected artifacts
- `data/joined.json`
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--join full` mode that includes unmatched rows from both sides with null fills.
2. Add column selection: `--select name,dept_name` to keep only specific fields in output.
3. Print a summary of matched, left-only, and right-only counts.
4. Re-run script and tests.

## Break it (required) — Core
1. Use a `--key` that exists in only one of the two files.
2. Use files with duplicate keys and observe which row wins.
3. Capture the first failing test or visible bad output.

## Fix it (required) — Core
1. Validate that the join key exists in both files before joining.
2. Document or handle the duplicate-key behavior explicitly (first-wins or last-wins).
3. Add tests for missing keys and duplicates.
4. Re-run until output and tests are deterministic.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. What is the difference between inner, left, and full outer joins?
2. How does `index_by_key` build a lookup dictionary for fast matching?
3. Why does the full join need to track "already matched" right-side keys?
4. Where do you see cross-file joining in data pipelines (SQL JOINs, pandas merge)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Quiz: Classes and Objects](../../../concepts/quizzes/classes-and-objects-quiz.py)

---

| [← Prev](../07-resilient-json-loader/README.md) | [Home](../../../README.md) | [Next →](../09-template-report-renderer/README.md) |
|:---|:---:|---:|
