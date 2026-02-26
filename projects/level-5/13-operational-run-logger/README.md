# Level 5 / Project 13 - Operational Run Logger
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | [Browser](../../../browser/level-5.html) |

<!-- modality-hub-end -->

**Estimated time:** 85 minutes

## Focus
- run lifecycle observability

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-5/13-operational-run-logger
python project.py --input data/sample_input.txt --output data/processed.json --log data/run_log.json --run-id demo-001
pytest -q
```

## Expected terminal output
```text
{"run_id": "demo-001", "status": "completed", "events": 9}
6 passed
```

## Expected artifacts
- `data/processed.json`
- `data/run_log.json`
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--verbose` flag that prints each event to stdout as it is logged.
2. Add error counting: track how many errors occurred and include in the summary.
3. Add a `log_warning` method to `RunLogger` for non-fatal issues.
4. Re-run script and tests.

## Break it (required) — Core
1. Point `--input` at a file that does not exist and observe the error handling.
2. Pass an empty input file (0 lines) and check the event count.
3. Capture the first failing test or visible bad output.

## Fix it (required) — Core
1. Ensure `RunLogger.finish` is always called even when exceptions occur.
2. Handle empty input gracefully (0 items processed, status still "completed").
3. Add tests for missing input and empty input.
4. Re-run until output and tests are deterministic.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does `RunLogger` generate a unique `run_id` for each execution?
2. How does `finish()` calculate `duration_ms` from start and end times?
3. What is the purpose of separating `log_event` and `log_error`?
4. Where do you see structured run logging in production (CI/CD pipelines, ETL jobs, cron tasks)?

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
- [Quiz: Classes and Objects](../../../concepts/quizzes/classes-and-objects-quiz.py)

---

| [← Prev](../12-fail-safe-exporter/README.md) | [Home](../../../README.md) | [Next →](../14-change-detection-tool/README.md) |
|:---|:---:|---:|
