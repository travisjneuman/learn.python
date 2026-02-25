# Level 6 / Project 12 - ETL Health Dashboard Feed
Home: [README](../../../README.md)

## Focus
- publish etl status dataset

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-6/12-etl-health-dashboard-feed
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
{
  "runs_recorded": 5,
  "success_rate": 80.0,
  "avg_duration_ms": 2410.0,
  "per_job": [...],
  "recent_runs": [...]
}
```

## Expected artifacts
- `data/output_summary.json` — health metrics for dashboard consumption
- Passing tests (`pytest -q` → 6+ passed)
- Updated `notes.md`

## Alter it (required)
1. Add a `row_loss_rate` metric: `(rows_in - rows_out) / rows_in` per job, flagging jobs losing more than 5%.
2. Add a `--window` flag to compute metrics only for runs in the last N hours.
3. Add a trend indicator: is the success rate improving or declining over the last 5 runs?
4. Re-run script and tests after each change.

## Break it (required)
1. Record a run with `rows_in=0` and observe how `row_loss_rate` handles division by zero.
2. Record a run with status "running" (never finished) and observe the metrics.
3. Feed an empty runs array and observe the health output.

## Fix it (required)
1. Guard against division by zero in rate calculations.
2. Exclude "running" status from completed metrics.
3. Return safe defaults for empty datasets.

## Explain it (teach-back)
1. What metrics would a real ETL dashboard display?
2. Why track both `rows_in` and `rows_out` instead of just one?
3. What is a "success rate SLA" and how would you alert on violations?
4. How do tools like Airflow or dbt track ETL health?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Http Explained](../../../concepts/http-explained.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../11-dead-letter-row-handler/README.md) | [Home](../../../README.md) | [Next →](../13-batch-window-controller/README.md) |
|:---|:---:|---:|
