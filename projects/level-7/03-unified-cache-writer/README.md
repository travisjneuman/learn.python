# Level 7 / Project 03 - Unified Cache Writer
Home: [README](../../../README.md)

## Focus
- write normalized records to cache model

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-7/03-unified-cache-writer
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
1. Add a TTL (time-to-live) parameter so cached entries expire after N seconds.
2. Add a `clear()` method to each backend that removes all entries and resets stats.
3. Re-run script and tests — verify TTL expiry and clear work on all three backends.

## Break it (required)
1. Request an unknown backend name (e.g. `"redis"`) from `get_cache()` and observe the KeyError.
2. Write a very large value to the file backend and check if JSON serialization handles it.
3. Close the SQLite connection mid-operation and observe the error.

## Fix it (required)
1. Have `get_cache()` raise a clear `ValueError` for unknown backends with the valid options listed.
2. Add a max-size check before writing to the file backend.
3. Add a test confirming unknown backends produce a helpful error message.

## Explain it (teach-back)
1. Why is the strategy pattern useful for swappable cache backends?
2. What happened when an unknown backend was requested?
3. How did the explicit `ValueError` message help debugging?
4. When would you choose SQLite cache over memory or file cache in production?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Decorators Explained](../../../concepts/decorators-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Decorators Explained](../../../concepts/quizzes/decorators-explained-quiz.py)

---

| [← Prev](../02-monitoring-api-adapter/README.md) | [Home](../../../README.md) | [Next →](../04-source-field-mapper/README.md) |
|:---|:---:|---:|
