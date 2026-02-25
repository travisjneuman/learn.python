# Level 5 / Project 07 - Resilient JSON Loader
Home: [README](../../../README.md)

## Focus
- safe parsing with fallback behavior

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-5/07-resilient-json-loader
python project.py --input data/primary.json --fallback data/backup.json --output data/loaded_data.json
pytest -q
```

## Expected terminal output
```text
Loaded 3 records via primary
8 passed
```

## Expected artifacts
- `data/loaded_data.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--strict` flag that fails immediately instead of trying fallbacks.
2. Add repair support for JSON with single quotes instead of double quotes.
3. Log a detailed report of which sources were tried, in order, and which succeeded.
4. Re-run script and tests.

## Break it (required)
1. Corrupt `primary.json` by adding a trailing comma and delete `backup.json`.
2. Create a `primary.json` that is valid JSON but not a list (e.g. a plain string).
3. Capture the first failing test or visible bad output.

## Fix it (required)
1. Make `try_repair_json` handle the trailing-comma case and restore the data.
2. Validate that loaded data is a list; wrap non-list data in a list with a warning.
3. Add tests for repair and type-mismatch cases.
4. Re-run until output and tests are deterministic.

## Explain it (teach-back)
1. Why does `try_load_json` return a tuple of `(data, error)` instead of raising?
2. How does `try_repair_json` attempt to fix trailing commas?
3. What is the fallback chain order and why does repair come last?
4. Where do you see resilient loading in production (config servers, cached fallbacks)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../06-metrics-summary-engine/README.md) | [Home](../../../README.md) | [Next →](../08-cross-file-joiner/README.md) |
|:---|:---:|---:|
