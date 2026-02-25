# Level 5 / Project 01 - Schedule Ready Script
Home: [README](../../../README.md)

## Focus
- non-interactive execution patterns

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-5/01-schedule-ready-script
python project.py --input data/sample_input.txt --output data/output.json --start-hour 0 --end-hour 24
pytest -q
```

## Expected terminal output
```text
{
  "processed": 5,
  "status": "completed"
}
6 passed
```

## Expected artifacts
- `data/output.json` — processed results
- `data/run.log` — execution log
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--max-retries` flag that retries the work function on failure.
2. Add email notification simulation (log a "would send email" message) on success/failure.
3. Re-run script and tests — add a test for the retry behavior.

## Break it (required)
1. Set `--start-hour 23 --end-hour 1` (overnight window) and run at noon — confirm it skips.
2. Manually create a lock file and run — verify the "another instance running" message.
3. Point `--input` at a missing file and observe the error status.

## Fix it (required)
1. Add lock-file staleness detection with a configurable timeout.
2. Add a `--force` flag that ignores the time window check.
3. Re-run until all tests pass.

## Explain it (teach-back)
1. Why does the script use a lock file instead of checking if another process is running?
2. What is the purpose of time-window checks in scheduled scripts?
3. Why does `is_within_time_window` handle overnight windows (start > end)?
4. How would you set this up as a real cron job on Linux or Task Scheduler on Windows?

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

| [← Prev](../README.md) | [Home](../../../README.md) | [Next →](../02-alert-threshold-monitor/README.md) |
|:---|:---:|---:|
