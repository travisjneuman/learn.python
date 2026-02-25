# Level 5 / Project 02 - Alert Threshold Monitor
Home: [README](../../../README.md)

## Focus
- threshold logic and breach summaries

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-5/02-alert-threshold-monitor
python project.py --metrics data/metrics.json --thresholds data/thresholds.json --output data/alert_report.json
pytest -q
```

## Expected terminal output
```text
Alert evaluation: 3 breaches found
5 passed
```

## Expected artifacts
- `data/alert_report.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--cooldown` flag that suppresses repeated alerts for the same metric within N seconds.
2. Add an "info" severity level for metrics that are within 10% of the warn threshold.
3. Log each breach with the metric name, current value, and which threshold it crossed.
4. Re-run script and tests.

## Break it (required)
1. Set a `warn` threshold higher than the `crit` threshold in `thresholds.json` and observe what happens.
2. Remove a metric from `metrics.json` that the thresholds file expects.
3. Capture the first failing test or visible bad output.

## Fix it (required)
1. Add validation that `warn < crit` and raise a clear error if not.
2. Handle missing metrics gracefully (skip or report as "no data").
3. Add tests for the broken cases.
4. Re-run until output and tests are deterministic.

## Explain it (teach-back)
1. Why is cooldown important in production alerting systems?
2. What happens if thresholds are misconfigured in a real monitoring stack?
3. How does `check_threshold` decide between warn, crit, and ok?
4. How would this pattern apply to monitoring dashboards or PagerDuty-style alerting?

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

| [← Prev](../01-schedule-ready-script/README.md) | [Home](../../../README.md) | [Next →](../03-multi-file-etl-runner/README.md) |
|:---|:---:|---:|
