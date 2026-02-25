# Level 10 / Project 06 - Resilience Chaos Workbench
Home: [README](../../../README.md)

## Focus
- Strategy pattern for injectable fault types
- Service state modeling with health simulation
- Resilience scoring and grading system
- Experiment rollback and recovery measurement

## Why this project exists
Netflix's Chaos Monkey proved that systems must be tested against failure. This framework lets you define chaos experiments, inject faults into a service model, measure impact, and quantify resilience with letter grades — turning "we think it's reliable" into a measurable score.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-10/06-resilience-chaos-workbench
python project.py
pytest -v
```

## Expected terminal output
```text
{
  "service": "order-service",
  "experiments": 4,
  "recovery_rate": "100%",
  "grade": "A",
  ...
}
```

## Alter it (required)
1. Add a `NetworkPartition` chaos action that removes all dependencies at once — implement `apply` and `rollback`.
2. Add a `CombinedFault` that applies multiple actions simultaneously (e.g., latency + errors).
3. Add a "blast radius" metric to the scorecard based on impact severity.

## Break it (required)
1. Set `MemoryPressure` to 100% and observe the service becoming unhealthy.
2. Inject 100% error rate and verify the service fails all requests.
3. Kill all dependencies and check how the health check responds.

## Fix it (required)
1. Add circuit-breaker logic to `ServiceState.handle_request` that stops accepting requests when error rate exceeds a threshold.
2. Add a `graceful_degradation` mode where the service returns cached responses when dependencies are down.
3. Test that degraded mode still counts as "recovered" in the scorecard.

## Explain it (teach-back)
1. How does the Strategy pattern make it easy to add new fault types without modifying the experiment runner?
2. Why is rollback essential in chaos engineering — what happens if you don't roll back?
3. How does the grading system translate recovery rates into actionable categories?
4. How would you adapt this to test real distributed systems instead of a simulation?

## Mastery check
You can move on when you can:
- create a custom ChaosAction and run it in an experiment,
- explain the relationship between fault injection, impact measurement, and rollback,
- interpret a resilience scorecard and identify the weakest fault type,
- describe how Netflix's Chaos Monkey works at a high level.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../05-compliance-evidence-builder/README.md) | [Home](../../../README.md) | [Next →](../07-high-risk-change-gate/README.md) |
|:---|:---:|---:|
