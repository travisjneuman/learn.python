# Level 3 / Project 10 - Dependency Boundary Lab
Home: [README](../../../README.md)

**Estimated time:** 50 minutes

## Focus
- separate io from business logic

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-3/10-dependency-boundary-lab
python project.py records.json output.json --config config.json
pytest -q
```

## Expected terminal output
```text
Processed: 4 in, 3 out, 1 filtered
10 passed
```

## Expected artifacts
- Processed JSON output file
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `sort_by` config option to sort output records by a field.
2. Add a `CsvFileReader` that reads CSV instead of JSON.
3. Add a `--dry-run` flag that shows what would be processed without writing.

## Break it (required) — Core
1. Pass a config with a rename map that creates duplicate keys — what happens?
2. Pass a JSON file that contains a string instead of an array — what error appears?
3. Use `InMemoryReader` with no records — does the pipeline handle empty input?

## Fix it (required) — Core
1. Validate config keys before running the pipeline.
2. Handle non-list JSON input by wrapping in a list.
3. Add clear error messages when reader/writer operations fail.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. What is "dependency inversion" and why does it make code testable?
2. How do `InMemoryReader`/`InMemoryWriter` replace real files in tests?
3. Why is the `run()` orchestrator the ONLY place that touches I/O?
4. What is a Python `Protocol` and how does it define an interface?

## Mastery check
You can move on when you can:
- separate I/O from business logic,
- test business logic without touching the filesystem,
- use the Protocol pattern for dependency boundaries,
- build a configurable data processing pipeline.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Virtual Environments](../../../concepts/virtual-environments.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../09-reusable-utils-library/README.md) | [Home](../../../README.md) | [Next →](../11-project-config-bootstrap/README.md) |
|:---|:---:|---:|
