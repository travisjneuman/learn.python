# Level 3 / Project 09 - Reusable Utils Library
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | [Browser](../../../browser/level-3.html) |

<!-- modality-hub-end -->

**Estimated time:** 45 minutes

## Focus
- common helper functions and reuse

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-3/09-reusable-utils-library
python project.py slugify "Hello World!"
python project.py convert my_variable_name --to camel
python project.py validate user@example.com --type email
pytest -q
```

## Expected terminal output
```text
hello-world
myVariableName
{"valid": true, ...}
18 passed
```

## Expected artifacts
- Utility outputs on stdout
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `deep_flatten` function that flattens arbitrarily nested lists.
2. Add a `validate_phone` function similar to `validate_email`.
3. Add a `pluralize` string utility (simple English rules: "cat" -> "cats").

## Break it (required) — Core
1. Call `chunk` with size 0 — what happens?
2. Call `slugify` with only special characters — what is returned?
3. Call `camel_to_snake` on an already-snake string — is the result correct?

## Fix it (required) — Core
1. Ensure `chunk` raises a clear error for non-positive sizes.
2. Handle edge case where `slugify` produces an empty string.
3. Add idempotency: `camel_to_snake(snake_to_camel(x))` should round-trip.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. What makes a function "reusable" vs. tightly coupled to one project?
2. Why write docstrings with input/output examples?
3. How does `re.sub` work for text transformation?
4. Why use `set()` in `unique_ordered` for O(1) membership checking?

## Mastery check
You can move on when you can:
- design small, composable utility functions,
- write clear docstrings with examples,
- test edge cases and boundary conditions,
- use regex for text transformation.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../08-template-driven-reporter/README.md) | [Home](../../../README.md) | [Next →](../10-dependency-boundary-lab/README.md) |
|:---|:---:|---:|
