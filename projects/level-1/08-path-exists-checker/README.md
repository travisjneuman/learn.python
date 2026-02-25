# Level 1 / Project 08 - Path Exists Checker
Home: [README](../../../README.md)

## Focus
- filesystem existence and type checks

## Why this project exists
Check whether file paths exist, determine if each is a file or directory, and report sizes in human-readable format. You will learn `pathlib.Path` methods like `exists()`, `is_file()`, `is_dir()`, and `stat()`.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-1/08-path-exists-checker
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Path Checker ===

  data/sample_input.txt     EXISTS   file    0.1 KB
  data/output.json          EXISTS   file    0.3 KB
  /nonexistent/path/file    MISSING  --      --

  2/3 paths exist
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a "last modified" field showing when each file was last changed (use `os.path.getmtime()`).
2. Add a `--exists-only` flag that only shows paths that actually exist.
3. Re-run script and tests.

## Break it (required)
1. Add a path with special characters like `data/my file (1).txt` -- does `check_path()` handle spaces in paths?
2. Add a symbolic link (if on Linux/Mac) or a path to a network drive -- does it detect the type correctly?
3. Add a very deeply nested path that does not exist -- does the checker handle long paths gracefully?

## Fix it (required)
1. Ensure `check_path()` works with paths containing spaces by using `Path` objects consistently.
2. Handle permission errors (e.g. restricted directories) by catching `PermissionError`.
3. Add a test for the missing-path case.

## Explain it (teach-back)
1. What does `Path.exists()` do and why is it better than `os.path.exists()`?
2. Why does `format_size()` convert bytes to KB/MB/GB instead of just showing raw bytes?
3. What is the difference between `is_file()`, `is_dir()`, and `exists()` on a `Path` object?
4. Where would path checking appear in real software (deployment scripts, backup tools, file managers)?

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

| [← Prev](../07-date-difference-helper/README.md) | [Home](../../../README.md) | [Next →](../09-json-settings-loader/README.md) |
|:---|:---:|---:|
