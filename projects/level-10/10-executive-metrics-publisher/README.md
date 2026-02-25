# Level 10 / Project 10 - Executive Metrics Publisher
Home: [README](../../../README.md)

## Focus
- Adapter pattern for normalizing metrics from different sources
- KPI transformation with trend and health analysis
- Pluggable report formatters via Protocol
- Business-meaningful narratives from technical data

## Why this project exists
Engineering teams track hundreds of metrics, but executives need concise answers: "Are we on track?" This pipeline bridges the gap by transforming raw technical data into business-meaningful KPIs with traffic-light health ratings, trend indicators, and natural-language narratives.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-10/10-executive-metrics-publisher
python project.py
pytest -v
```

## Expected terminal output
```text
{
  "report_type": "executive_summary",
  "overall_health": "yellow",
  "kpi_count": 9,
  "categories": { "reliability": [...], "velocity": [...], "quality": [...] },
  "attention_needed": [...]
}
```

## Alter it (required)
1. Add a `CostSource` that tracks cloud spend, cost per request, and budget utilization.
2. Add a `TrendReportFormatter` that groups KPIs by trend direction (improving/stable/declining).
3. Add sparkline-style text indicators (up arrow, down arrow, dash) to the narrative.

## Break it (required)
1. Pass a target of 0 to a "higher is better" metric and observe division-by-zero handling.
2. Create a KPI with no previous value and verify the trend is STABLE.
3. Register no sources and call `publish` — verify the report is empty but valid.

## Fix it (required)
1. Add a minimum KPI count validation — report should warn if fewer than 3 KPIs are collected.
2. Handle the case where all KPIs are RED — add an "executive alert" section.
3. Test both fixes.

## Explain it (teach-back)
1. How does the Adapter pattern normalize metrics from different source systems?
2. Why is "lower is better" handled separately from "higher is better" for health ratings?
3. What makes a narrative more useful than a raw number for executives?
4. How would you extend this to send reports via email or Slack?

## Mastery check
You can move on when you can:
- add a new MetricSource and see it flow through the pipeline,
- explain the trend computation logic and its 5% threshold,
- interpret the traffic-light health system (green/yellow/red),
- describe how DORA metrics (deploy frequency, lead time, MTTR, change failure rate) map to this system.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../09-strategic-architecture-review/README.md) | [Home](../../../README.md) | [Next →](../11-production-readiness-director/README.md) |
|:---|:---:|---:|
