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
python project.py audit .
python project.py audit . --pattern "*.py" --json
python project.py scan .
pytest -q
```

## Expected terminal output
```text
Audit: .
Files: 5, Total size: 12,345 bytes
Issues (2):
  [WARNING] empty.txt: File is empty (0 bytes)
  [INFO   ] notes: File has no extension
10 passed
```

## Expected artifacts
- Audit report on stdout
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add CSV export of audit results with columns: filename, size, last_modified, status.
2. Add a `--recursive` flag to scan subdirectories.
3. Add a `check_encoding` function that flags non-UTF-8 files.

## Break it (required)
1. Point the auditor at a file instead of a directory — what error appears?
2. Audit a directory with no files — does the summary handle zero files?
3. Use a glob pattern that matches nothing — what does the report show?

## Fix it (required)
1. Add a clear error message for non-directory input.
2. Handle permission errors when scanning protected directories.
3. Show "No files match pattern" instead of an empty report.

## Explain it (teach-back)
1. How does `Path.glob()` differ from `Path.rglob()`?
2. Why separate each check into its own function (check_empty, check_large, etc.)?
3. What is `Path.stat()` and what metadata does it provide?
4. How does the `@dataclass` `field(default_factory=list)` pattern work?

## Mastery check
You can move on when you can:
- scan directories with pathlib and glob patterns,
- build composable check functions that return structured results,
- aggregate check results into a summary report,
- use dataclasses for structured audit data.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../06-structured-error-handler/README.md) | [Home](../../../README.md) | [Next →](../08-template-driven-reporter/README.md) |
|:---|:---:|---:|
