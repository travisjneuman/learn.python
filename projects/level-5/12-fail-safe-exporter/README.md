# Level 5 / Project 12 - Fail Safe Exporter
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | [Browser](../../../browser/level-5.html) |

<!-- modality-hub-end -->

**Estimated time:** 85 minutes

## Focus
- atomic writes and export integrity

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-5/12-fail-safe-exporter
python project.py --input data/sample_input.json --output data/exported.json --format json
python project.py --input data/sample_input.json --output data/exported.csv --format csv
pytest -q
```

## Expected terminal output
```text
Exported 4 records to data/exported.json (atomic write)
Exported 4 records to data/exported.csv (atomic write)
6 passed
```

## Expected artifacts
- `data/exported.json` or `data/exported.csv`
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--validate` flag that checks each record has required fields before exporting.
2. Add a backup: before overwriting, copy the existing file to `.bak`.
3. Add a `--dry-run` flag that validates and reports but does not write.
4. Re-run script and tests.

## Break it (required) — Core
1. Pass an output path to a read-only directory (or a path with invalid characters).
2. Pass input data where records have inconsistent keys (some missing columns).
3. Capture the first failing test or visible bad output.

## Fix it (required) — Core
1. Catch `OSError` / `PermissionError` during atomic write and report clearly.
2. Pad missing keys with empty strings during CSV export.
3. Add tests for write failures and inconsistent records.
4. Re-run until output and tests are deterministic.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does `atomic_write_json` write to a `.tmp` file and then rename?
2. What happens if the process crashes between writing `.tmp` and renaming?
3. How does `atomic_write_csv` determine CSV headers from the records?
4. Where do you see atomic writes in production (databases, log rotation, config updates)?

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
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Classes and Objects](../../../concepts/quizzes/classes-and-objects-quiz.py)

---

| [← Prev](../11-retry-backoff-runner/README.md) | [Home](../../../README.md) | [Next →](../13-operational-run-logger/README.md) |
|:---|:---:|---:|
