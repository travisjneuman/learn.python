# Level 9 / Project 15 - Level 9 Mini Capstone
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- Facade pattern unifying multiple subsystems (SLOs, costs, reliability, governance)
- Composition over inheritance for subsystem integration
- Multi-dimensional health scoring from heterogeneous data sources
- Structured reporting with per-service and aggregate views
- Platform engineering toolkit design

## Why this project exists
This capstone integrates the core Level 9 concepts: architecture decisions, SLO
management, cost estimation, reliability scoring, and governance checks into a unified
platform engineering toolkit. Real platform teams do not run each of these in isolation —
they compose them into a single operational view that answers "how healthy is this
service?" across every dimension. This project proves you can design systems that compose
multiple domain engines into a coherent whole, the architectural skill that separates
senior engineers from juniors.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-9/15-level9-mini-capstone
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "platform_health": "WARNING",
  "services": [...],
  "aggregate": {"slo_compliance": 92, "reliability_grade": "B", "monthly_cost": 14200},
  "top_risks": [...]
}
7 passed
```

## Expected artifacts
- Console JSON output with full platform engineering report
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `top_risks()` method that returns the 3 services with the worst health status.
2. Add cost trend analysis — flag services with SPIKING cost trends in the report.
3. Add a `--team` filter that generates a report scoped to a specific team's services.

## Break it (required)
1. Register a service with no SLOs, no cost data, and no governance checks — what health status results?
2. Set `budget_monthly=0` in `CostProfile` — does `over_budget` report correctly?
3. Generate a report with zero registered services — does `generate_report()` handle division by zero?

## Fix it (required)
1. Return `UNKNOWN` health status when a service has no subsystem data.
2. Guard against `budget_monthly=0` in the `over_budget` property.
3. Add a test for the empty toolkit report.

## Explain it (teach-back)
1. How does the facade pattern unify SLOs, costs, reliability, and governance into one view?
2. What is the relationship between health status and the individual subsystem scores?
3. Why does this capstone compose subsystems rather than inheriting from them?
4. How would a real platform engineering team use this toolkit day-to-day?

## Mastery check
You can move on when you can:
- explain the facade pattern and how it simplifies complex subsystem interactions,
- register a new service and predict its health status from its subsystem data,
- describe how SLOs, costs, reliability, and governance interact in platform engineering,
- extend the toolkit with a new subsystem (e.g. incident tracking) without modifying existing code.

---

## Related Concepts

- [Async Explained](../../../concepts/async-explained.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Async Explained](../../../concepts/quizzes/async-explained-quiz.py)

---

| [← Prev](../14-cross-team-handoff-kit/README.md) | [Home](../../../README.md) | [Next →](../README.md) |
|:---|:---:|---:|
