# Level 9 / Project 04 - Observability SLO Pack
Home: [README](../../../README.md)

## Focus
- SRE primitives: SLO, SLI, and error budget management
- Time-window compliance calculation with rolling windows
- Burn-rate alerting for early degradation detection
- Strategy pattern for different SLI types (availability, latency)
- Structured SLO dashboard reporting

## Why this project exists
SLOs (Service Level Objectives) are the foundation of Site Reliability Engineering.
A team with a 99.9% availability SLO has an error budget of 0.1% — roughly 43 minutes
of downtime per month. When the budget is exhausted, feature work stops and reliability
becomes the priority. This project builds an SLO management system that tracks SLIs,
computes compliance, calculates burn rates, and manages error budgets — the same system
Google SRE teams use to balance reliability with feature velocity.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-9/04-observability-slo-pack
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "slo_count": 3,
  "compliant": 2,
  "breached": 1,
  "burn_rate_alerts": [...]
}
7 passed
```

## Expected artifacts
- Console JSON output with SLO compliance and burn rate data
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `latency` SLI type that tracks p99 latency instead of success ratios.
2. Add multi-window burn-rate alerting (e.g. 1-hour and 6-hour windows with different thresholds).
3. Add a `--dashboard` flag that outputs a formatted text dashboard of all SLO statuses.

## Break it (required)
1. Set `target_pct=100.0` — what happens to the error budget (it becomes 0%)?
2. Record zero events and check compliance — does the SLI value calculation divide by zero?
3. Set a burn rate threshold of 0 — does every SLO trigger an alert?

## Fix it (required)
1. Validate that `target_pct < 100.0` (a 100% target has zero error budget).
2. Add a guard in `SLI.value` that returns 100.0 when `total_count == 0`.
3. Validate burn rate thresholds are positive in `check_burn_rates`.

## Explain it (teach-back)
1. What is an SLI, SLO, and error budget — how do they relate?
2. How does burn rate indicate whether you will exhaust your error budget early?
3. Why is a 100% availability target impractical — what is the "nines" system?
4. How do Google SRE teams use error budgets to balance reliability vs feature velocity?

## Mastery check
You can move on when you can:
- calculate error budgets from SLO targets (e.g. 99.9% = 0.1% budget),
- explain burn rate alerting and why it catches slow degradations,
- add a new SLI type and wire it through the full pack,
- describe how real teams use error budgets to decide when to freeze deployments.

---

## Related Concepts

- [Async Explained](../../../concepts/async-explained.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [Quiz: Async Explained](../../../concepts/quizzes/async-explained-quiz.py)

---

| [← Prev](../03-event-driven-pipeline-lab/README.md) | [Home](../../../README.md) | [Next →](../05-capacity-planning-model/README.md) |
|:---|:---:|---:|
