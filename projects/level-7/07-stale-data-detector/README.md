# Level 7 / Project 07 - Stale Data Detector
Home: [README](../../../README.md)

## Focus
- freshness checks and stale alerts

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-7/07-stale-data-detector
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
1. Add a `"degraded"` severity level between warning and stale (e.g. at 75% of stale threshold).
2. Add a `most_stale()` method that returns the single stalest source.
3. Re-run script and tests — verify the new severity and method appear in output.

## Break it (required)
1. Provide a `last_updated` timestamp in the future (ahead of `now`) and observe negative age.
2. Remove the `source` key from one of the source records.
3. Capture the KeyError or nonsensical "fresh" classification for future timestamps.

## Fix it (required)
1. Clamp negative ages to zero (a future timestamp means "just refreshed").
2. Validate that each source record has the required `source` and `last_updated` keys.
3. Add tests for future timestamps and missing required keys.

## Explain it (teach-back)
1. Why do different data sources need different freshness thresholds?
2. What happened when a timestamp was in the future?
3. How did clamping to zero prevent misleading results?
4. Where would stale-data detection be used in a real data platform?

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
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../06-token-rotation-simulator/README.md) | [Home](../../../README.md) | [Next →](../08-ingestion-observability-kit/README.md) |
|:---|:---:|---:|
