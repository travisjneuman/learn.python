# Level 8 / Project 13 - SLA Breach Detector
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- SLA definitions with target values and measurement windows
- Time-window aggregation for SLA compliance calculation
- Breach detection with hysteresis to prevent flapping
- Alert severity escalation: warning, breach, critical
- Burn-rate analysis for error budget consumption tracking

## Why this project exists
Service Level Agreements define contractual performance guarantees — "99.9% uptime" or
"p95 latency under 200ms." Detecting breaches early prevents penalty payments and customer
churn. A service running at 99.85% might look fine to a dashboard, but it is silently
burning through its error budget. This project builds an SLA monitoring engine that tracks
metrics against SLA targets, detects breaches in sliding time windows, calculates burn
rates, and generates alerts — the pattern behind every uptime monitoring tool.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-8/13-sla-breach-detector
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "sla_count": 3,
  "breached": 1,
  "at_risk": 1,
  "healthy": 1,
  "details": [...]
}
7 passed
```

## Expected artifacts
- Console JSON output with SLA status and breach details
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `warning_threshold` to `SLADefinition` that fires before the actual breach.
2. Add burn-rate calculation — how fast is the error budget being consumed?
3. Add a `--watch` mode that simulates continuous metric ingestion and alerts in real time.

## Break it (required)
1. Set `target_value=0` for an availability SLA — does the tracker compute valid percentages?
2. Record no events and call `check_all()` — what happens with zero denominators?
3. Set `window_hours=0` on the sliding window — does breach detection still work?

## Fix it (required)
1. Validate that `target_value > 0` for percentage-based SLAs.
2. Add a guard that returns "no data" status when no events are recorded.
3. Add a test for the warning threshold alert.

## Explain it (teach-back)
1. What is an SLA vs SLO vs SLI — how do they relate to each other?
2. How does the sliding window ensure that old data does not affect current breach detection?
3. What is an error budget and why is burn rate important?
4. How do real services like AWS/GCP calculate SLA compliance?

## Mastery check
You can move on when you can:
- define SLA, SLO, and SLI with concrete examples,
- explain error budgets and how teams use them to balance reliability vs velocity,
- add a new metric type (e.g. latency p99) to the breach detector,
- describe how sliding windows and burn rates work together for alerting.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Http Explained](../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../12-release-readiness-evaluator/README.md) | [Home](../../../README.md) | [Next →](../14-user-journey-tracer/README.md) |
|:---|:---:|---:|
