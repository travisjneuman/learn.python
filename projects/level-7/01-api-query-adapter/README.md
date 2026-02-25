# Level 7 / Project 01 - API Query Adapter
Home: [README](../../../README.md)

## Focus
- API query abstraction and response parsing

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-7/01-api-query-adapter
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
1. Add a third source adapter (e.g. `gamma`) that maps `{"ref": ..., "info": ...}` to the unified schema.
2. Add a `sort_by` parameter to `filter_records` that sorts results by a chosen field.
3. Re-run script and tests — verify the new adapter appears in output.

## Break it (required)
1. Pass a source name that has no registered adapter (e.g. `"unknown_api"`).
2. Feed a record where the expected field is missing (e.g. `{"uid": "1"}` with no `"data"` key).
3. Observe the KeyError or None values in the unified output.

## Fix it (required)
1. Return a clear error or skip unknown sources instead of crashing.
2. Add `.get()` with defaults in each adapter so missing fields produce `None` instead of KeyError.
3. Add a test that confirms unknown sources are handled gracefully.

## Explain it (teach-back)
1. Why does the adapter pattern make adding new sources easy?
2. What happened when a source had no adapter registered?
3. How did `.get()` with a default prevent the crash?
4. Where would you use this pattern in a real multi-vendor integration?

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
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../README.md) | [Home](../../../README.md) | [Next →](../02-monitoring-api-adapter/README.md) |
|:---|:---:|---:|
