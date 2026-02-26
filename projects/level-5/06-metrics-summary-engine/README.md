# Level 5 / Project 06 - Metrics Summary Engine
Home: [README](../../../README.md)

> **Quick Recall:** This project uses numeric aggregation and statistics from structured data. Before starting, make sure you can: load a CSV into a list of dictionaries and compute a column's min, max, and average using a simple loop (Level 1, Project 05 - CSV First Reader).

**Estimated time:** 70 minutes

## Focus
- aggregate operational metrics

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-5/06-metrics-summary-engine
python project.py --input data/metrics.json --output data/metrics_summary.json
pytest -q
```

## Expected terminal output
```text
Aggregated 3 metrics: response_time, cpu_usage, error_rate
6 passed
```

## Expected artifacts
- `data/metrics_summary.json`
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--window` flag that computes moving averages over a configurable window size.
2. Add standard deviation to the summary statistics for each metric.
3. Add a `--format` flag that outputs either JSON or a human-readable table.
4. Re-run script and tests.

## Break it (required) — Core
1. Add a metric with only one data point and check if percentile calculation breaks.
2. Add a metric with an empty values list.
3. Capture the first failing test or visible bad output.

## Fix it (required) — Core
1. Handle single-value metrics gracefully (p50 = p99 = the single value).
2. Return zeros or nulls for empty metrics with a clear warning.
3. Add tests for single-value and empty-metric edge cases.
4. Re-run until output and tests are deterministic.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. How does `percentile` compute p50 vs p99 from a sorted list?
2. Why is moving average useful for smoothing noisy time-series data?
3. What happens if you pass `window=0` to `moving_average`?
4. Where do you see metrics aggregation in production (Prometheus, Datadog, Grafana)?

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
- [Quiz: Classes and Objects](../../../concepts/quizzes/classes-and-objects-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Metrics Summary Engine. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to aggregate metrics (min, max, mean, percentiles) from a list of numeric values. Can you explain how to calculate the 95th percentile?"
- "Can you explain the difference between mean, median, and mode with examples of when each is most useful?"

---

| [← Prev](../05-plugin-style-transformer/README.md) | [Home](../../../README.md) | [Next →](../07-resilient-json-loader/README.md) |
|:---|:---:|---:|
