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

## Design First
Before writing code, sketch your approach in `notes.md`:
- What functions or classes do you need?
- What data structures will you use?
- What's the flow from input to output?
- What could go wrong?

## Alter it (required)
1. How could you make the tool more observable — what progress information would help?
2. What should happen when one file in the batch fails?
3. Add a summary report with the statistics you think matter most.

## Break it (required)
1. What happens when source files do not share the same structure?
2. Try running with no input files at all.
3. Find the first failure and capture it.

## Fix it (required)
1. Add validation for the structural consistency issue you found.
2. Handle the empty-input case with a clear message.
3. Write tests for both edge cases and re-run until deterministic.

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
