# Level 9 / Project 11 - Recovery Time Estimator
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- Monte Carlo simulation for probabilistic time estimation
- Recovery phases: detection, diagnosis, fix, verification, deployment
- Triangular distribution modeling with 3-point estimates (min, expected, max)
- Confidence intervals at p50, p90, and p99
- Impact of team size, runbooks, and incident novelty on recovery time

## Why this project exists
When systems fail, stakeholders need realistic recovery time estimates — not guesses.
"How long until the site is back?" requires modeling the full recovery process: detecting
the issue, diagnosing root cause, implementing a fix, verifying it works, and deploying.
Each phase has uncertainty. This project uses Monte Carlo simulation to model recovery
times as probability distributions, producing confidence intervals that account for
team capacity, runbook availability, and incident complexity — the same approach used
by incident management teams at Google, Netflix, and PagerDuty.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-9/11-recovery-time-estimator
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "incident": "database-outage",
  "estimates": {
    "p50_minutes": 95,
    "p90_minutes": 142,
    "p99_minutes": 198
  },
  "phases": [...],
  "scenario_comparison": {...}
}
7 passed
```

## Expected artifacts
- Console JSON output with recovery time estimates and scenario comparison
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `communication_overhead` phase that models coordination time for multi-team incidents.
2. Change the estimator to support custom estimation strategies via dependency injection.
3. Add a `--runs` flag that controls the number of Monte Carlo simulation iterations.

## Break it (required)
1. Set `team_size=0` — does the diagnosis multiplier handle division by zero?
2. Create a `PhaseEstimate` where `min > max` — what happens to the triangular distribution?
3. Run the simulation with `simulation_runs=0` — does the percentile calculation handle empty data?

## Fix it (required)
1. Validate that `team_size >= 1` in `IncidentProfile`.
2. Validate that `min <= expected <= max` in `PhaseEstimate.__post_init__`.
3. Return a default estimate when `simulation_runs` is 0.

## Explain it (teach-back)
1. What is Monte Carlo simulation and why is it used for time estimation?
2. How does the triangular distribution model 3-point estimates (min, expected, max)?
3. What do p50, p90, and p99 mean in the context of recovery time estimation?
4. Why do runbooks significantly reduce recovery time — what does the multiplier model?

## Mastery check
You can move on when you can:
- explain Monte Carlo simulation and triangular distributions in plain language,
- run a scenario comparison and interpret the improvement percentage,
- describe how team size, runbooks, and incident novelty affect recovery time,
- add a new recovery phase and see its effect on the overall estimate.

---

## Related Concepts

- [Async Explained](../../../concepts/async-explained.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Quiz: Async Explained](../../../concepts/quizzes/async-explained-quiz.py)

---

| [← Prev](../10-data-governance-enforcer/README.md) | [Home](../../../README.md) | [Next →](../12-incident-postmortem-generator/README.md) |
|:---|:---:|---:|
