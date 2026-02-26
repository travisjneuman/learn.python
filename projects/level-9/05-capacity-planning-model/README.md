# Level 9 / Project 05 - Capacity Planning Model
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- Growth modeling: linear, exponential, and step-function curves
- Strategy pattern for pluggable growth curve selection
- Resource profiling with current usage and capacity limits
- Forecast generation with headroom recommendations
- What-if scenario analysis for capacity decisions

## Why this project exists
Capacity planning prevents outages by projecting resource needs before demand exceeds
supply. A service growing at 15% month-over-month will exhaust its database connections
in 8 months — but without a model, the team only discovers this during a production
incident. This project models compute, storage, and bandwidth growth using configurable
curves and generates capacity forecasts with months-until-exhaustion calculations — the
same approach infrastructure teams use at every major tech company.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-9/05-capacity-planning-model
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "resources": [...],
  "forecasts": [...],
  "months_until_exhaustion": {"compute": 14, "storage": 8, ...}
}
7 passed
```

## Expected artifacts
- Console JSON output with capacity forecasts
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `seasonal` growth function that models periodic spikes (e.g. Black Friday traffic).
2. Add a `--chart` flag that outputs a text-based ASCII chart of the capacity forecast.
3. Add cost estimation — multiply forecasted usage by per-unit cost to project spend.

## Break it (required)
1. Set `growth_rate=0` for exponential growth — does the forecast handle it?
2. Create a resource profile with `capacity < current_usage` — is it flagged as already exhausted?
3. Pass `months=0` to `forecast()` — does it return an empty forecast or error?

## Fix it (required)
1. Validate that `growth_rate > 0` for exponential models.
2. Add "already exhausted" detection for resources that are over capacity at month 0.
3. Validate `months >= 1` in the forecast method.

## Explain it (teach-back)
1. What is capacity planning and why is it critical for infrastructure teams?
2. How do linear, exponential, and step growth functions differ in real-world modeling?
3. What is the "months until exhaustion" calculation and why is it a key metric?
4. How do what-if scenarios help teams decide when to add infrastructure?

## Mastery check
You can move on when you can:
- explain the difference between linear and exponential growth forecasting,
- run a what-if scenario that compares current vs optimized resource profiles,
- describe how capacity planning prevents outages vs reactive scaling,
- add a new growth model without modifying existing forecast logic.

## Mastery Check
- [ ] Can you explain the architectural trade-offs in your solution?
- [ ] Could you refactor this for a completely different use case?
- [ ] Can you identify at least two alternative approaches and explain why you chose yours?
- [ ] Could you debug this without print statements, using only breakpoint()?

---

## Related Concepts

- [Async Explained](../../../concepts/async-explained.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Async Explained](../../../concepts/quizzes/async-explained-quiz.py)

---

| [← Prev](../04-observability-slo-pack/README.md) | [Home](../../../README.md) | [Next →](../06-reliability-scorecard/README.md) |
|:---|:---:|---:|
