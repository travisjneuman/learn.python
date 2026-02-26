# Level 3 / Project 05 - Refactor Monolith Drill
Home: [README](../../../README.md)

> **Try in Browser:** [Practice similar concepts online](../../browser/level-2.html?ex=5) — browser exercises cover Level 2 topics

## Before You Start

Recall these prerequisites before diving in:
- Can you move a function from one file to another and update the import?
- Can you explain what "separation of concerns" means?

**Estimated time:** 40 minutes

## Focus
- split large function into modules

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-3/05-refactor-monolith-drill
python project.py data/sample_input.txt
python project.py data/sample_input.txt --json
python project.py data/sample_input.txt --department Engineering
pytest -q
```

## Expected terminal output
```text
Company Report: 10 employees, $849,000.00 total payroll
===========================================================
Engineering (4 people)
  Salary range: $88,000 - $115,000
  ...
10 passed
```

## Expected artifacts
- Formatted report on stdout
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--sort-by` flag (headcount, salary, tenure) to order departments.
2. Add a median salary calculation to `DepartmentStats`.
3. Add a `--top-earners N` flag to show the top N earners across all departments.

## Break it (required) — Core
1. Use a CSV with a missing `salary` column — what error appears?
2. Pass a non-numeric value in the salary column — does it crash or skip?
3. Filter to a department that doesn't exist — what happens?

## Fix it (required) — Core
1. Add validation that all required CSV columns exist before processing.
2. Handle non-numeric salary/years values gracefully (skip with warning).
3. Show a clear message when `--department` matches nothing.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. What is the "monolith" anti-pattern and why is it hard to test?
2. How does decomposing into parse -> group -> compute -> format help?
3. Why is `parse_csv` separate from `load_employees`?
4. What is the Single Responsibility Principle?

## Mastery check
You can move on when you can:
- decompose a large function into small, testable units,
- explain the Single Responsibility Principle,
- test each function independently,
- build a data pipeline with clear step separation.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Refactor Monolith Drill. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I have a large function (100+ lines) and need to split it into smaller functions. Can you give me a strategy for deciding where to split?"
- "Can you explain relative imports in Python packages with a simple two-file example?"

---

| [← Prev](../04-test-driven-normalizer/README.md) | [Home](../../../README.md) | [Next →](../06-structured-error-handler/README.md) |
|:---|:---:|---:|
