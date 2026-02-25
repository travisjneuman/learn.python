# Level 7 / Project 15 - Level 7 Mini Capstone
Home: [README](../../../README.md)

## Focus
- multi-source telemetry ingest package

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-7/15-level7-mini-capstone
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
1. Add a `"gamma"` source adapter that maps `{"ref": ..., "content": ...}` to the unified schema.
2. Add a `dry_run` flag that runs the full pipeline but skips writing the output file.
3. Re-run script and tests — verify the new adapter and dry-run mode work end-to-end.

## Break it (required)
1. Disable the `adapt` flag while keeping other stages enabled — observe what happens with no records.
2. Provide a payload where `id` is None and watch contract validation behave unexpectedly.
3. Add a source with records that conflict with another source on the same key.

## Fix it (required)
1. Have downstream stages check for empty input and short-circuit gracefully.
2. Treat `None` id values as missing in contract validation.
3. Add a test confirming each stage handles empty input without crashing.

## Explain it (teach-back)
1. How does this capstone combine all Level 7 concepts into one pipeline?
2. What happened when the adapt stage was disabled but downstream stages ran?
3. How did the empty-input guard prevent cascading failures?
4. How would you decompose this monolithic pipeline into microservices in production?

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

| [← Prev](../14-cache-backfill-runner/README.md) | [Home](../../../README.md) | [Next →](../README.md) |
|:---|:---:|---:|
