# Level 0 / Project 04 - Yes No Questionnaire
Home: [README](../../../README.md)

## Before You Start

Recall these prerequisites before diving in:
- Can you use `.strip()` and `.lower()` to clean up a string?
- Can you check if a value is in a set? (`"yes" in {"yes", "y", "true"}`)

## Focus
- boolean logic and input normalization

## Why this project exists
Process yes/no survey answers, normalise messy input like "YES", "y", "True" into clean booleans, and tally the results with percentages. You will learn input normalisation and basic statistics.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/04-yes-no-questionnaire
python project.py
pytest -q
```

The program asks you 5 questions interactively and tallies your answers.

## Expected terminal output
```text
=== Yes/No Questionnaire ===
Answer 5 questions with yes or no.

  1. Do you enjoy learning new things? yes
  2. Have you used a computer before today? y
  3. Do you like solving puzzles? yeah
  4. Are you excited to learn Python? YES
  5. Do you prefer working alone? no

=== Results ===
  Total responses: 5
  Yes: 4 (80.0%)
  No:  1 (20.0%)
  Invalid: 0
5 passed
```

## Expected artifacts
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add "maybe" as a third valid answer category (accept "maybe", "perhaps", "unsure").
2. Add a percentage bar using `#` characters next to each tally count.
3. Re-run script and tests.

## Break it (required)
1. Answer every question with just spaces or blank -- does `tally_answers()` crash or return zeros?
2. Answer with "YES!!!" or "y e s" -- does `normalise_answer()` handle them?
3. What happens if you call `tally_answers([])` with an empty list?

## Fix it (required)
1. Handle the empty-answers case by returning a tally with all zeros.
2. Strip punctuation from answers so "YES!!!" normalises to "yes".
3. Add a test for the all-blank-answers edge case.

## Explain it (teach-back)
1. Why does `normalise_answer()` use `.strip().lower()` before checking membership in a set?
2. What is the difference between checking `answer in {"yes", "y", "true"}` vs using if/elif?
3. Why return "invalid" for unrecognised answers instead of raising an error?
4. Where would answer normalisation appear in real software (survey tools, form validation)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Files and Paths](../../../concepts/quizzes/files-and-paths-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Yes No Questionnaire. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to normalize messy input strings like 'YES', 'y', 'True' into a consistent format. Can you explain `.strip().lower()` with examples that are not about yes/no answers?"
- "Can you explain how to calculate a percentage from a count and a total, with a simple example?"

---

| [← Prev](../03-temperature-converter/README.md) | [Home](../../../README.md) | [Next →](../05-number-classifier/README.md) |
|:---|:---:|---:|
