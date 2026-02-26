# Level 0 / Project 11 - Simple Menu Loop
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| [Concept](../../../concepts/errors-and-debugging.md) | **This project** | — | [Quiz](../../../concepts/quizzes/errors-and-debugging-quiz.py) | [Flashcards](../../../practice/flashcards/README.md) | [Diagram](../../../concepts/diagrams/errors-and-debugging.md) | [Browser](../../../browser/level-0.html) |

<!-- modality-hub-end -->

**Estimated time:** 25 minutes

## Focus
- while loops and command menu flow

## Why this project exists
Build a text-based menu that dispatches numbered choices to action functions. You will practise while loops, if/elif dispatch, and processing batch commands from a file -- the pattern behind every CLI tool.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/11-simple-menu-loop
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Simple Menu ===
  1. Greet
  2. Reverse text
  3. Count characters
  4. Quit

  [1] => Hello, World!
  [2] => nohtyP
  [3] => "programming" has 11 characters

3 commands processed. Output: data/output.json
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a new menu action: "5. Count vowels" that counts vowels in a given string.
2. Add a `--verbose` flag that prints the menu before each action in batch mode.
3. Re-run script and tests.

## Break it (required) — Core
1. Enter choice `99` -- does `execute_choice()` handle unknown options gracefully?
2. Enter choice `quit` in the middle of the batch file -- does `run_batch()` stop processing?
3. Enter an action with no argument like just `1` with no name -- what happens?

## Fix it (required) — Core
1. Ensure `execute_choice()` returns a clear error message for unknown choices.
2. Handle missing arguments by using a default value (e.g. "World" for greet).
3. Add a test for the missing-argument edge case.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does `run_batch()` use a for loop instead of a while loop?
2. What is the advantage of mapping menu choices to functions in the `actions` dict?
3. Why does the menu loop `break` on "quit" instead of using `sys.exit()`?
4. Where would menu-driven interfaces appear in real software (CLI tools, admin consoles, kiosk systems)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Classes and Objects](../../../concepts/quizzes/classes-and-objects-quiz.py)

---

| [← Prev](../10-duplicate-line-finder/README.md) | [Home](../../../README.md) | [Next →](../12-contact-card-builder/README.md) |
|:---|:---:|---:|
