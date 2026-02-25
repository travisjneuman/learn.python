# Level 10 / Project 12 - Onboarding Accelerator System
Home: [README](../../../README.md)

## Focus
- Builder pattern for composing personalized onboarding plans
- Role-based templates with priority-ordered tasks
- Task dependency tracking and completion progress
- Customizable plans with buddy assignments

## Why this project exists
New-hire onboarding is expensive and inconsistent when done ad-hoc. This project codifies role-specific checklists so every engineer gets the same high-quality start. The builder pattern allows customization without a combinatorial explosion of plan variants.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-10/12-onboarding-accelerator-system
python project.py
pytest -v
```

## Expected terminal output
```text
{
  "employee": "Alice Chen",
  "role": "backend",
  "buddy": "Bob Smith",
  "total_tasks": 11,
  "completion": "18%",
  ...
}
```

## Alter it (required)
1. Add a `data_engineer_template` with tasks specific to data engineering (SQL, ETL, Spark).
2. Add task dependency enforcement — a task cannot be completed if its `depends_on` tasks are not done.
3. Add an estimated duration field to each task and compute total onboarding time.

## Break it (required)
1. Try building a plan with an unknown role — observe the `ValueError`.
2. Complete a non-existent task ID and verify it returns `False`.
3. Create circular task dependencies and see how the system handles it.

## Fix it (required)
1. Add validation that `depends_on` references only valid task IDs within the same plan.
2. Add a `block_task` method that marks a task as BLOCKED and explains why.
3. Test both fixes.

## Explain it (teach-back)
1. How does the Builder pattern differ from just using a constructor with many parameters?
2. Why are tasks organized by priority (DAY_ONE, FIRST_WEEK, etc.) instead of a flat list?
3. How does the buddy assignment integrate with the onboarding workflow?
4. How would you extend this to generate actual scripts (e.g., shell scripts for tool setup)?

## Mastery check
You can move on when you can:
- create a custom onboarding plan using the builder,
- add a new role template with appropriate tasks,
- track completion progress and identify blocked tasks,
- explain why the builder returns `self` to enable method chaining.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../11-production-readiness-director/README.md) | [Home](../../../README.md) | [Next →](../13-legacy-modernization-planner/README.md) |
|:---|:---:|---:|
