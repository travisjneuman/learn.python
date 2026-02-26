# Level 5 / Project 15 - Level 5 Mini Capstone
Home: [README](../../../README.md)

**Estimated time:** 90 minutes

## Focus
- intermediate-grade automation package

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-5/15-level5-mini-capstone
python project.py --config data/pipeline_config.json
pytest -q
```

## Expected terminal output
```text
Pipeline complete: 5 rows, 2 alerts, 12ms
8 passed
```

## Expected artifacts
- `data/output/summary.json`
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--dry-run` flag that runs extract and transform but skips the export step.
2. Add env var overrides: `PIPELINE_THRESHOLD_WARN=80` should override the config file value.
3. Add a retry wrapper around `extract_csv_files` so one bad file does not abort the pipeline.
4. Re-run script and tests.

## Break it (required) — Core
1. Point `input_dir` in the config at a directory that does not exist.
2. Add a CSV with no numeric columns and observe what `_numeric` defaults to.
3. Set `threshold_warn` higher than `threshold_crit` in the config.
4. Capture the first failing test or visible bad output.

## Fix it (required) — Core
1. Validate that `input_dir` exists before starting extraction.
2. Log a clear warning when no numeric column is found in a row.
3. Validate that `warn < crit` at config load time.
4. Add tests for each broken scenario.
5. Re-run until output and tests are deterministic.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. How does `load_config` implement the three-layer priority (defaults, file, env)?
2. Why does `atomic_write` use a `.tmp` file and rename instead of writing directly?
3. How does `check_thresholds` separate warnings from criticals?
4. How does this capstone tie together config, ETL, monitoring, and atomic export from earlier projects?
5. Where would you see a pipeline like this in production (data warehousing, CI/CD, monitoring)?

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
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Classes and Objects](../../../concepts/quizzes/classes-and-objects-quiz.py)

---

| [← Prev](../14-change-detection-tool/README.md) | [Home](../../../README.md) | [Next →](../README.md) |
|:---|:---:|---:|
