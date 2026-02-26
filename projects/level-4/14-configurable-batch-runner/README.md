# Level 4 / Project 14 - Configurable Batch Runner
Home: [README](../../../README.md)

**Estimated time:** 75 minutes

## Focus
- batch jobs driven by config files

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-4/14-configurable-batch-runner
python project.py --config data/batch_config.json --output data/batch_report.json
pytest -q
```

## Expected terminal output
```text
{
  "total_jobs": 4,
  "succeeded": 4,
  "failed": 0
}
6 passed
```

## Expected artifacts
- `data/batch_report.json` — per-job results with status
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a new action: `search_pattern` that counts regex matches in a file.
2. Add a `--dry-run` flag that validates the config without executing jobs.
3. Re-run script and tests — add a test for the new action.

## Break it (required) — Core
1. Reference a non-existent file in the config and verify the error is logged per-job.
2. Add a job with an unknown action name and confirm it is skipped.
3. Create a config with zero jobs and verify the runner handles it.

## Fix it (required) — Core
1. Add config schema validation (each job must have name, action, input).
2. Add timing to each job result (duration_ms).
3. Re-run until all tests pass.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does the batch runner use an `ACTIONS` registry instead of `if/elif` chains?
2. What is the advantage of running jobs sequentially with individual error handling vs. stopping at first failure?
3. Why does `run_batch` resolve input paths relative to the config file's directory?
4. How would you extend this to support job dependencies (job B runs only if job A succeeds)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../13-reconciliation-reporter/README.md) | [Home](../../../README.md) | [Next →](../15-level4-mini-capstone/README.md) |
|:---|:---:|---:|
