# Level 10 / Project 09 - Strategic Architecture Review
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| [Concept](../../../concepts/how-imports-work.md) | **This project** | — | [Quiz](../../../concepts/quizzes/how-imports-work-quiz.py) | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- Architecture fitness functions as executable constraints
- System model with service dependencies
- Health scoring with automated recommendations
- Transitive dependency depth calculation

## Why this project exists
Architecture erodes silently — each small shortcut seems harmless until the system becomes unmaintainable. Fitness functions make architectural constraints executable and measurable, so drift is detected in CI rather than discovered during a crisis. This project builds a review engine with pluggable checks.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-10/09-strategic-architecture-review
python project.py
pytest -v
```

## Expected terminal output
```text
{
  "system": "ecommerce-platform",
  "health_score": 50.0,
  "status": "warning",
  "recommendations": [...]
}
```

## Alter it (required)
1. Add an `APIStabilityCheck` that fails when services have different API versions.
2. Add a `CircularDependencyCheck` that detects cycles in the dependency graph.
3. Weight recommendations by priority and show the top 3 in the summary.

## Break it (required)
1. Create a system with a service that has 10+ dependencies and observe the coupling check fail.
2. Add a service with 15,000 LOC and watch the complexity check flag it.
3. Create a deep dependency chain (A->B->C->D->E->F) and trigger the depth check.

## Fix it (required)
1. Add configurable thresholds per service (some services legitimately need more dependencies).
2. Make `DependencyDepthCheck` detect and report cycles instead of infinite-looping.
3. Test the cycle detection.

## Explain it (teach-back)
1. What is an architecture fitness function and why is it better than a document?
2. How does the health score aggregate multiple checks into a single number?
3. Why does the dependency depth check use recursive traversal with a visited set?
4. How would you run these checks in CI to catch architectural drift automatically?

## Mastery check
You can move on when you can:
- write a new fitness function and register it in the engine,
- interpret a health score and prioritize recommendations,
- model a system with known architectural problems and verify the checks catch them,
- explain the difference between coupling, cohesion, and complexity metrics.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../08-zero-downtime-migration-lab/README.md) | [Home](../../../README.md) | [Next →](../10-executive-metrics-publisher/README.md) |
|:---|:---:|---:|
