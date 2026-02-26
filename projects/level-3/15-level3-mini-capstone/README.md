# Level 3 / Project 15 - Level 3 Mini Capstone
Home: [README](../../../README.md)

**Estimated time:** 60 minutes

## Focus
- junior-level production-style utility

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-3/15-level3-mini-capstone
python project.py report .
python project.py report . --json
python project.py scan . --pattern "*.py"
pytest -q
```

## Expected terminal output
```text
Project Health: 15-level3-mini-capstone
Score: 90/100 (Grade: A)
==================================================
Files: 3
Total lines: 250
Code lines: 180
...
12 passed
```

## Expected artifacts
- Health report on stdout
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `check_type_hints` function that flags functions missing type annotations.
2. Add a `--compare` flag that compares two directories side by side.
3. Add a trend tracker that saves scores to a JSON file and shows improvement over time.

## Break it (required) — Core
1. Point it at a file instead of a directory — what error appears?
2. Scan a directory with binary files (.pyc, .jpg) — do they cause errors?
3. Run on an empty directory — does the score calculation handle division by zero?

## Fix it (required) — Core
1. Add clear error handling for non-directory input.
2. Skip binary files gracefully with a warning.
3. Handle empty directories without crashing.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. How does this capstone combine skills from projects 01-14?
2. What is a "health score" and how do you weigh different issue severities?
3. Why use `Path.rglob()` for recursive scanning?
4. How would you extend this tool to check additional languages beyond Python?

## Mastery check
You can move on when you can:
- combine dataclasses, logging, argparse, and pathlib in one tool,
- build composable health checks,
- generate a scored report from metrics,
- scan and analyse project structures recursively.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../14-service-simulator/README.md) | [Home](../../../README.md) | [Next →](../README.md) |
|:---|:---:|---:|
