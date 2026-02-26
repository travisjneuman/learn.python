# Level 8 / Project 15 - Level 8 Mini Capstone
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- Integration of multiple observability subsystems into one platform
- Service registration with health tracking and metric collection
- Threshold-based alerting with severity levels
- Facade pattern for unified access to metrics, alerts, and health
- Comprehensive reporting with drill-down per service

## Why this project exists
This capstone integrates concepts from the entire level: KPI dashboards, response
profiling, SLA monitoring, fault injection, and graceful degradation. Real observability
platforms (Datadog, Grafana, New Relic) unify metrics, health checks, and alerting into
a single pane of glass. This project builds a mini observability platform that monitors
simulated services, detects degradation, generates alerts, and produces a unified health
report — proving you can design systems that compose multiple subsystems into a coherent
whole.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-8/15-level8-mini-capstone
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "platform_health": "warning",
  "services": [...],
  "alerts": [...],
  "metrics_summary": {...}
}
7 passed
```

## Expected artifacts
- Console JSON output with full observability platform report
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a dashboard endpoint that returns all services' health, alerts, and metrics in one JSON response.
2. Add alert severity levels (warning, critical) with different threshold multipliers.
3. Add a `--simulate` flag that generates random metrics and demonstrates real-time alerting.

## Break it (required)
1. Record metrics for a service that was never registered — does `record_metric` handle it?
2. Set `alert_threshold` to 0 — does every metric trigger an alert?
3. Call `generate_report()` with no services registered — does it produce a valid report?

## Fix it (required)
1. Add validation that services must be registered before recording metrics.
2. Guard against `alert_threshold <= 0` with a minimum value.
3. Add a test for the empty-platform edge case.

## Explain it (teach-back)
1. How does this capstone integrate metrics, alerting, and health into a unified platform?
2. What is the facade pattern and how does `ObservabilityPlatform` use it?
3. Why are mean and p95 both tracked — when does each matter?
4. How would you extend this to support distributed tracing across services?

## Mastery check
You can move on when you can:
- explain how the capstone combines patterns from projects 01-14,
- add a new subsystem (e.g. log aggregation) to the platform without modifying existing code,
- describe the three pillars of observability: metrics, logs, and traces,
- design an alerting strategy that avoids alert fatigue while catching real incidents.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Http Explained](../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../14-user-journey-tracer/README.md) | [Home](../../../README.md) | [Next →](../README.md) |
|:---|:---:|---:|
