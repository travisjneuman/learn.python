# Level 7 / Project 04 - Source Field Mapper
Home: [README](../../../README.md)

## Focus
- explicit source-to-target mapping contracts

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-7/04-source-field-mapper
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
1. Add a `"datetime"` cast type that parses ISO-format strings into Unix timestamps.
2. Add a `drop_unmapped` option that removes source fields not in the mapping rules.
3. Re-run script and tests — verify new cast and drop behavior work correctly.

## Break it (required)
1. Map a field with `cast: "int"` but provide a non-numeric string (e.g. `"abc"`).
2. Reference a source field that does not exist in the record and has no default.
3. Observe the ValueError or KeyError in the output.

## Fix it (required)
1. Wrap cast operations in try/except and log a warning instead of crashing.
2. Skip missing source fields when no default is configured, adding them to a `skipped_fields` report.
3. Add a test for bad cast values and missing source fields.

## Explain it (teach-back)
1. Why are explicit mapping rules better than renaming fields in-place?
2. What happened when a string could not be cast to int?
3. How did the try/except prevent a pipeline crash on bad data?
4. Where would you use field mapping in a real ETL pipeline?

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
- [Http Explained](../../../concepts/http-explained.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../03-unified-cache-writer/README.md) | [Home](../../../README.md) | [Next →](../05-polling-cadence-manager/README.md) |
|:---|:---:|---:|
