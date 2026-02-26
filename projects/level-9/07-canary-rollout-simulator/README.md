# Level 9 / Project 07 - Canary Rollout Simulator
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- State machine for deployment stages (canary, promoted, rolled back)
- Statistical comparison: canary error rate vs baseline
- Configurable rollout strategy with progressive traffic percentages
- Automatic promotion and rollback based on metric thresholds
- Deterministic simulation with seeded random number generation

## Why this project exists
Deploying new code to 100% of traffic at once is a gamble — a bug hits everyone
simultaneously. Canary deployments route a small percentage (1%, then 5%, then 25%)
to the new version, comparing its error rate and latency against the stable baseline.
If metrics degrade, traffic is automatically rolled back. This project simulates the
full canary rollout process with configurable stages, automatic promotion/rollback
triggers, and metric comparison — the same pattern used by Kubernetes, Argo Rollouts,
and AWS CodeDeploy.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-9/07-canary-rollout-simulator
python project.py --demo
pytest -q
```

## Expected terminal output
```text
{
  "final_state": "COMPLETED",
  "stages_completed": 4,
  "rollback_triggered": false,
  "metrics": {...}
}
7 passed
```

## Expected artifacts
- Console JSON output with rollout simulation results
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `PAUSED` state that halts progression without rolling back.
2. Add configurable rollback thresholds per stage (e.g. stricter for 50% than for 5%).
3. Add a `--seed` CLI flag for deterministic simulation results.

## Break it (required)
1. Define stages with non-increasing traffic percentages (e.g. 50%, 25%, 100%) — what happens?
2. Set `error_rate_threshold=0.0` — does every stage trigger a rollback?
3. Call `advance()` after the rollout has already completed — does it handle the terminal state?

## Fix it (required)
1. Validate that stage traffic percentages are strictly increasing.
2. Add a guard that prevents advancing past the COMPLETED or ROLLED_BACK states.
3. Add a test for the PAUSED state transition.

## Explain it (teach-back)
1. What is a canary deployment and how does it reduce risk compared to big-bang releases?
2. How does the state machine (stages -> COMPLETED or ROLLED_BACK) model the rollout?
3. Why is deterministic simulation (via seed) important for testing deployment strategies?
4. How do real platforms like Kubernetes or Argo Rollouts implement canary deployments?

## Mastery check
You can move on when you can:
- draw the state machine for a canary rollout including all transitions,
- explain why traffic percentages increase progressively (1% -> 5% -> 25% -> 50% -> 100%),
- add a new rollback condition (e.g. latency spike) to the simulator,
- describe the difference between canary, blue-green, and rolling deployments.

---

## Related Concepts

- [Async Explained](../../../concepts/async-explained.md)
- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Async Explained](../../../concepts/quizzes/async-explained-quiz.py)

---

| [← Prev](../06-reliability-scorecard/README.md) | [Home](../../../README.md) | [Next →](../08-change-impact-analyzer/README.md) |
|:---|:---:|---:|
