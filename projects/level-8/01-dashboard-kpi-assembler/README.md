# Level 8 / Project 01 - Dashboard KPI Assembler
Home: [README](../../../README.md)

## Focus
- KPI aggregation from heterogeneous metric sources
- Threshold evaluation with traffic-light statuses
- Trend detection (improving / stable / degrading)
- Percentile-based statistical summaries

## Why this project exists
Real dashboards pull metrics from many sources — API gateways, infrastructure agents, monitoring
systems. This project teaches you to aggregate those readings, evaluate them against thresholds,
and produce a structured dashboard payload — the same pattern used in Grafana, Datadog, and custom BI tools.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-8/01-dashboard-kpi-assembler
python project.py --input data/sample_input.json --output data/dashboard_output.json
pytest -q
```

## Expected terminal output
```text
{
  "title": "Operations Dashboard",
  "overall_health": "warning",
  "counts": {"red": 0, "yellow": 1, "green": 2},
  "kpis": [...]
}
7 passed
```

## Expected artifacts
- `data/dashboard_output.json` — full dashboard payload
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a new KPI definition (e.g. `memory_usage_pct`) to `sample_input.json` with samples.
2. Change `compute_trend` to use a sliding-window approach instead of simple half-split.
3. Add a `--format` flag that supports both JSON and CSV output.

## Break it (required)
1. Remove one KPI from `kpi_definitions` but leave its samples — what happens to orphan data?
2. Pass negative values in samples — does the percentile function handle them?
3. Set `green_threshold` higher than `yellow_threshold` — what status does `evaluate` return?

## Fix it (required)
1. Add validation that `green_threshold <= yellow_threshold` in `KPIDefinition`.
2. Handle the case where samples reference a KPI not in definitions (log a warning).
3. Add a test for negative metric values.

## Explain it (teach-back)
1. Why does the project use `dataclass` instead of plain dictionaries?
2. What is the nearest-rank percentile method and when might it give surprising results?
3. How does `compute_trend` decide between "improving" and "degrading"?
4. In a production system, where would the metric samples come from?

## Mastery check
You can move on when you can:
- explain the difference between mean and p95 and why dashboards show both,
- add a new KPI end-to-end (definition + samples + threshold) without looking at docs,
- describe how this pattern scales to thousands of metrics per minute,
- explain why trend detection needs a minimum sample count.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Collections Explained](../../../concepts/collections-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../README.md) | [Home](../../../README.md) | [Next →](../02-query-cache-layer/README.md) |
|:---|:---:|---:|
