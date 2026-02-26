# Level 1 / Project 06 - Simple Gradebook Engine
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| [Concept](../../../concepts/how-imports-work.md) | **This project** | — | [Quiz](../../../concepts/quizzes/how-imports-work-quiz.py) | [Flashcards](../../../practice/flashcards/README.md) | — | [Browser](../../../browser/level-1.html) |

<!-- modality-hub-end -->

**Estimated time:** 25 minutes

## Focus
- aggregate scores and grade bands

## Why this project exists
Calculate student averages from multiple scores, assign letter grades using threshold bands (A/B/C/D/F), and produce a class-wide summary. You will learn CSV-based score parsing, numeric aggregation, and grade-band logic.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-1/06-simple-gradebook-engine
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Gradebook Report ===

  Alice Johnson   Avg: 91.25  Grade: A
  Bob Smith       Avg: 73.75  Grade: C

  Class average: 82.50
  Highest: Alice Johnson (91.25)
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--curve` flag that adds N points to every student's average before assigning letter grades.
2. Add a "pass/fail" summary showing how many students scored above/below 60%.
3. Re-run script and tests.

## Break it (required) — Core
1. Add a student row with non-numeric scores like `Alice,A,B,C` -- does `calculate_average()` crash?
2. Add a student with no scores (just a name) -- does the parser handle it?
3. Add a score above 100 like `Alice,105,98,92` -- does `letter_grade()` still work?

## Fix it (required) — Core
1. Validate that all scores are numeric in `parse_student_row()`.
2. Handle students with no scores by assigning an average of 0.
3. Add a test for the non-numeric-scores case.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does `letter_grade()` use if/elif chains with descending thresholds (90, 80, 70, 60)?
2. What does `calculate_average()` do with `sum(scores) / len(scores)` and when does it fail?
3. Why does `class_summary()` compute class-wide statistics separately from individual grades?
4. Where would gradebook logic appear in real software (LMS platforms, school administration, HR training)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Functions Explained](../../../concepts/functions-explained.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Functions Explained](../../../concepts/quizzes/functions-explained-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Simple Gradebook Engine. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to assign letter grades based on score ranges. Can you show me how to map numeric ranges to categories using if/elif, with a different example like age groups?"
- "Can you explain how to calculate an average from a list of numbers in Python?"

---

| [← Prev](../05-csv-first-reader/README.md) | [Home](../../../README.md) | [Next →](../07-date-difference-helper/README.md) |
|:---|:---:|---:|
