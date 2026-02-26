# Level 4 / Project 10 - Run Manifest Generator
Home: [README](../../../README.md)

**Estimated time:** 65 minutes

## Focus
- artifact manifest and run metadata

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-4/10-run-manifest-generator
python project.py --dir data --output data/manifest.json --run-id my-batch-001
pytest -q
```

## Expected terminal output
```text
{
  "run_id": "my-batch-001",
  "file_count": 2,
  "total_size_bytes": 123
}
6 passed
```

## Expected artifacts
- `data/manifest.json` — file inventory with checksums and metadata
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--algorithm` flag supporting `sha256` in addition to `md5`.
2. Add a `--exclude` glob pattern to skip certain files (e.g., `*.json`).
3. Re-run script and tests — add a test for SHA-256 checksums.

## Break it (required) — Core
1. Point `--dir` at a non-existent directory and observe the error.
2. Create a very large file (10 MB+) and verify the chunked checksum still works.
3. Create a directory with symlinks and see if they are followed or skipped.

## Fix it (required) — Core
1. Add a `--no-follow-symlinks` option to skip symbolic links.
2. Handle permission errors gracefully (log a warning, skip the file).
3. Re-run until all tests pass.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does `compute_checksum` read in 8192-byte chunks instead of the whole file at once?
2. What is the difference between `iterdir()` and `rglob("*")` in `scan_files`?
3. Why does the manifest include timestamps and how would you use them for change detection?
4. What are the security considerations of using MD5 vs. SHA-256 for checksums?

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
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../09-transformation-pipeline-v1/README.md) | [Home](../../../README.md) | [Next →](../11-audit-log-enhancer/README.md) |
|:---|:---:|---:|
