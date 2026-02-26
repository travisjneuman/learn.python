# Level 7 / Project 08 - Ingestion Observability Kit
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- metrics and event visibility pipeline

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-7/08-ingestion-observability-kit
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
1. Add a `filter_logs(stage, level)` method to the ObservabilityKit that returns matching log entries.
2. Add a third pipeline stage (e.g. `"load"`) that writes records to a dict-based store.
3. Re-run script and tests — verify the new stage metrics appear in the summary.

## Break it (required)
1. Call `end_stage()` for a stage name that was never started with `start_stage()`.
2. Pass an empty records list and check if error_rate causes a division-by-zero.
3. Observe the KeyError or ZeroDivisionError in the output.

## Fix it (required)
1. Check if the stage exists in `self.metrics` before accessing it in `end_stage()`.
2. Guard the `error_rate` property against zero `rows_in` (already done — verify it).
3. Add a test that calls `end_stage` on an unknown stage and expects a clear error.

## Explain it (teach-back)
1. Why are correlation IDs essential for debugging pipeline failures?
2. What happened when end_stage was called for an unregistered stage?
3. How did the KeyError check prevent the crash?
4. How does structured logging differ from print-statement debugging?

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
- [Virtual Environments](../../../concepts/virtual-environments.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../07-stale-data-detector/README.md) | [Home](../../../README.md) | [Next →](../09-contract-version-checker/README.md) |
|:---|:---:|---:|
