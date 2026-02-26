# Level 10 / Project 13 - Legacy Modernization Planner
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| [Concept](../../../concepts/how-imports-work.md) | **This project** | — | [Quiz](../../../concepts/quizzes/how-imports-work-quiz.py) | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- Multi-dimensional scoring (urgency, effort, risk) for prioritization
- Strangler Fig pattern for incremental migration
- Phased roadmap generation with time estimates
- Strategy selection (rewrite, refactor, wrap, replace, retire)

## Why this project exists
Legacy systems are the backbone of most enterprises. Rewriting everything at once is risky and expensive. The Strangler Fig pattern wraps legacy functionality in new interfaces and redirects traffic incrementally. This project builds a planner that scores components and generates phased roadmaps.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-10/13-legacy-modernization-planner
python project.py
pytest -v
```

## Expected terminal output
```text
{
  "components_analyzed": 4,
  "total_estimated_weeks": 60,
  "priorities": [
    {"component": "billing-monolith", "priority": 45.2, "strategy": "WRAP"},
    ...
  ]
}
```

## Alter it (required)
1. Add a `team_capacity` parameter that limits how many weeks of work can happen in parallel.
2. Add a `cost_estimate` based on effort score multiplied by an hourly rate.
3. Add a RETIRE strategy for components with zero monthly traffic.

## Break it (required)
1. Set `business_criticality` to 0 — observe the validation error.
2. Create a component with zero effort and watch how priority calculation handles division.
3. Score a tiny well-documented component and verify it recommends REFACTOR.

## Fix it (required)
1. Add a minimum effort floor of 1 to prevent division-by-zero in priority calculation.
2. Handle the edge case where all components have the same priority — add a tiebreaker.
3. Test both fixes.

## Explain it (teach-back)
1. What is the Strangler Fig pattern and why is it safer than a big-bang rewrite?
2. How do the three scoring dimensions (urgency, effort, risk) interact in the priority formula?
3. Why does `has_documentation` reduce effort score?
4. When would you choose REPLACE over WRAP as a modernization strategy?

## Mastery check
You can move on when you can:
- score a legacy component and interpret its priority ranking,
- generate a phased roadmap and explain the five phases (assess/wrap/migrate/validate/decommission),
- compare Strangler Fig to branch-by-abstraction,
- describe real-world modernization examples (e.g., Amazon's monolith decomposition).

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../12-onboarding-accelerator-system/README.md) | [Home](../../../README.md) | [Next →](../14-sme-mentorship-toolkit/README.md) |
|:---|:---:|---:|
