# Level 5 / Project 03 - Multi File ETL Runner
Home: [README](../../../README.md)

## Focus
- multi-file ingestion orchestration

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-5/03-multi-file-etl-runner
python project.py --source-dir data/sources --output data/etl_output.json --strategy deduplicate --key id
pytest -q
```

## Expected terminal output
```text
ETL complete: 5 records from 2 files
6 passed
```

## Expected artifacts
- `data/etl_output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--verbose` flag that prints each file name and row count as it is processed.
2. If one file fails, continue processing the remaining files and report failures at the end.
3. Add a summary report: total files processed, total rows ingested, files skipped, elapsed time.
4. Re-run script and tests.

## Break it (required)
1. Put a CSV with different headers (e.g. `user,value`) in the sources directory alongside the existing files.
2. Point `--source-dir` at an empty directory with no CSV files.
3. Capture the first failing test or visible bad output.

## Fix it (required)
1. Validate that all source files share the same header columns before merging.
2. Return an empty result with a clear message when no files are found.
3. Add tests for mixed-header and empty-directory cases.
4. Re-run until output and tests are deterministic.

## Explain it (teach-back)
1. What is the difference between append, deduplicate, and update merge strategies?
2. Why does `merge_deduplicate` use a set to track seen keys?
3. What happens if two files have overlapping keys with `merge_update`?
4. How does this ETL pattern apply to data warehouse loading in production?

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

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Multi File ETL Runner. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to process multiple files in a specific order. Can you explain the Extract-Transform-Load (ETL) pattern with a simple example?"
- "Can you explain how to use `pathlib.Path.glob()` to find files matching a pattern?"

---

| [← Prev](../02-alert-threshold-monitor/README.md) | [Home](../../../README.md) | [Next →](../04-config-layer-priority/README.md) |
|:---|:---:|---:|
