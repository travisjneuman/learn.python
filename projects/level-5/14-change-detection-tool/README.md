# Level 5 / Project 14 - Change Detection Tool
Home: [README](../../../README.md)

## Focus
- baseline vs current delta detection

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-5/14-change-detection-tool
python project.py --old data/old_version.txt --new data/new_version.txt --output data/change_report.json
pytest -q
```

## Expected terminal output
```text
Change detection: modified
7 passed
```

## Expected artifacts
- `data/change_report.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--summary-only` flag that prints just the status and counts, not the full diff.
2. Add percentage change calculation: what fraction of lines were added/removed.
3. Support comparing entire directories (detect new, deleted, and modified files).
4. Re-run script and tests.

## Break it (required)
1. Compare two binary files (e.g. images) and observe what happens to `line_diff`.
2. Compare a file against itself (both `--old` and `--new` pointing to the same path).
3. Capture the first failing test or visible bad output.

## Fix it (required)
1. Detect binary files (by checking for null bytes) and skip line-level diffing.
2. Short-circuit when old and new paths are identical (status = "unchanged").
3. Add tests for binary detection and same-path comparison.
4. Re-run until output and tests are deterministic.

## Explain it (teach-back)
1. How does `file_hash` use SHA-256 to detect whether content changed?
2. Why does `line_diff` use sets instead of comparing line-by-line in order?
3. What information does the "modified" status include beyond just "changed"?
4. Where do you see change detection in production (git, config drift, file integrity monitoring)?

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
- [Quiz: Classes and Objects](../../../concepts/quizzes/classes-and-objects-quiz.py)

---

| [← Prev](../13-operational-run-logger/README.md) | [Home](../../../README.md) | [Next →](../15-level5-mini-capstone/README.md) |
|:---|:---:|---:|
