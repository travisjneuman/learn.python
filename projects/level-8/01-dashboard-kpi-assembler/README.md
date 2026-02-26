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
Extend this project in a meaningful way — add a feature that addresses a real use case.

## Break it (required)
Introduce a subtle bug and see if your tests catch it. If they don't, write a test that would.

## Fix it (required)
Review your code critically — is there a design pattern that would improve it?

## Explain it (teach-back)
Could you explain the architectural trade-offs to a colleague?

## Mastery check
You can move on when you can:
- explain the difference between mean and p95 and why dashboards show both,
- add a new KPI end-to-end (definition + samples + threshold) without looking at docs,
- describe how this pattern scales to thousands of metrics per minute,
- explain why trend detection needs a minimum sample count.

## Mastery Check
- [ ] Can you explain the architectural trade-offs in your solution?
- [ ] Could you refactor this for a completely different use case?
- [ ] Can you identify at least two alternative approaches and explain why you chose yours?
- [ ] Could you debug this without print statements, using only breakpoint()?

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
