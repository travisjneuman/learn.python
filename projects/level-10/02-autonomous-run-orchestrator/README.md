# Level 10 / Project 02 - Autonomous Run Orchestrator
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| [Concept](../../../concepts/how-imports-work.md) | **This project** | — | [Quiz](../../../concepts/quizzes/how-imports-work-quiz.py) | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- DAG-based dependency resolution via topological sort
- Command pattern for self-contained workflow steps
- Retry logic with configurable attempt limits
- Fail-fast vs continue-on-error execution modes

## Why this project exists
Production pipelines (ETL, CI/CD, ML training) involve steps that depend on each other. A topological scheduler prevents running a step before its inputs are ready, while retry logic handles transient failures without restarting the entire pipeline. This project builds a workflow orchestrator from scratch using Kahn's algorithm.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-10/02-autonomous-run-orchestrator
python project.py
pytest -v
```

## Expected terminal output
```text
Pipeline PASSED
  [SUCCESS] extract (1 attempt(s), 0ms)
  [SUCCESS] validate (1 attempt(s), 0ms)
  [SUCCESS] transform (1 attempt(s), 0ms)
  [SUCCESS] load (1 attempt(s), 0ms)
  [SUCCESS] notify (1 attempt(s), 0ms)
Total: 1ms
```

## Expected artifacts
- Pipeline execution report printed to stdout
- Passing tests (`pytest -v` shows ~11 passed)

## Alter it (required)
1. Add a `timeout_ms` enforcement to `_execute_with_retry` — if a step exceeds its timeout, treat it as failed.
2. Add a `parallel_groups` feature: steps with no dependency between them could run in the same "tier". Compute the tiers from the topological sort.
3. Re-run tests to confirm no regressions.

## Break it (required)
1. Create a cycle in the pipeline (A depends on B, B depends on A) and observe the `CyclicDependencyError`.
2. Make a step reference a non-existent dependency and see the `ValueError`.
3. Set `max_retries=0` and confirm the step is treated as failed immediately.

## Fix it (required)
1. Add validation that `max_retries >= 1` at `WorkflowStep` construction time.
2. Handle the edge case where `_execute_with_retry` is called with an empty action (returns empty string).
3. Add a test for the new validation.

## Explain it (teach-back)
1. Why is Kahn's algorithm used instead of DFS-based topological sort? What are the tradeoffs?
2. How does the fail-fast flag change downstream behavior when a step fails?
3. Why does the orchestrator track `failed_names` as a set rather than stopping at the first failure?
4. How would you extend this to support parallel step execution within dependency tiers?

## Mastery check
You can move on when you can:
- trace the topological sort by hand for a diamond-shaped dependency graph,
- explain why cycles make topological sorting impossible,
- add a new step to the demo pipeline with correct dependency wiring,
- describe the retry vs skip decision tree for each step.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../01-enterprise-python-blueprint/README.md) | [Home](../../../README.md) | [Next →](../03-policy-as-code-validator/README.md) |
|:---|:---:|---:|
