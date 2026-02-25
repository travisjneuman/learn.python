# Level 1 / Project 12 - File Extension Counter
Home: [README](../../../README.md)

## Focus
- directory scanning and grouped counts

## Why this project exists
Count file extensions from a list of paths (or by scanning a directory), then display the distribution with percentages and a bar chart. You will learn `Path.suffix`, `rglob()` for recursive scanning, and grouped counting.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-1/12-file-extension-counter
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== File Extension Counter ===

  .py   5 files (50%)  ##########
  .txt  3 files (30%)  ######
  .md   2 files (20%)  ####

  10 files, 3 unique extensions
4 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--filter` flag that shows only specific extensions (e.g. `--filter .py,.txt`).
2. Add a "hidden files" category for files starting with `.` (like `.gitignore`).
3. Re-run script and tests.

## Break it (required)
1. Point `--dir` at an empty directory -- does `count_extensions()` return an empty dict or crash?
2. Use a file list with files that have double extensions like `archive.tar.gz` -- which extension is counted?
3. Point `--dir` at a path that does not exist -- does it raise `NotADirectoryError`?

## Fix it (required)
1. Handle the empty-directory case by returning an empty dict with a "(no files found)" message.
2. Ensure `NotADirectoryError` is raised with the path in the message for non-existent directories.
3. Add a test for the empty-directory case.

## Explain it (teach-back)
1. Why does `count_extensions()` use `rglob("*")` instead of `iterdir()`?
2. What does `Path.suffix` return for a file like `archive.tar.gz`? (Just `.gz` -- not `.tar.gz`.)
3. Why normalise extensions to lowercase with `.lower()`?
4. Where would extension counting appear in real software (disk usage analysis, build systems, file managers)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../11-command-dispatcher/README.md) | [Home](../../../README.md) | [Next →](../13-batch-rename-simulator/README.md) |
|:---|:---:|---:|
