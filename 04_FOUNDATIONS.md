# 04 - Foundations (Build Real Python Muscle)
Home: [README](./README.md)

## Who this is for
- Beginners who can run Python but still feel lost reading code.
- Learners who need repeated, hands-on drills.

## What you will build
- A set of foundational scripts that solve small, real tasks.
- A debugging notebook that captures mistakes and fixes.

## Prerequisites
- Setup complete from [03_SETUP_ALL_PLATFORMS.md](./03_SETUP_ALL_PLATFORMS.md).
- Working `.venv` and pytest.

## Step-by-step lab pack

### Lab 1 - Inputs, outputs, and types
Goal:
- Understand `str`, `int`, `float`, `bool`, and `None`.

Task:
- Write a script that reads text values and converts them safely.

Minimum script behaviors:
- Convert `"42"` to integer and add 10.
- Reject invalid number text with a clear error message.

### Lab 2 - Conditionals and decisions
Goal:
- Build confidence with `if`, `elif`, `else`.

Task:
- Evaluate an alert severity string and print an action:
  - `Critical` -> `Page On-Call`
  - `Warning` -> `Create Ticket`
  - else -> `Log Only`

### Lab 3 - Loops and collections
Goal:
- Process many records with predictable logic.

Task:
- Iterate over a list of alert dictionaries.
- Print a one-line summary for each.
- Count critical alerts.

### Lab 4 - Functions and reuse
Goal:
- Break logic into testable units.

Task:
- Implement:
  - `normalize_status(text: str) -> str`
  - `is_critical(status: str) -> bool`
- Add pytest tests for both functions.

### Lab 5 - Files and paths
Goal:
- Read and write files safely with `pathlib`.

Task:
- Read a text file of events.
- Write a summary file containing counts by severity.

### Lab 6 - Debugging drills
Goal:
- Read tracebacks and isolate root cause quickly.

Task:
- Trigger and fix:
  - `KeyError`
  - `TypeError`
  - `FileNotFoundError`

Record each incident in `notes/debug_journal.md` with:
- error message,
- root cause,
- fix,
- prevention rule.

## Expected output
- 15+ micro-scripts in a dedicated foundations project.
- 20+ passing tests across key logic helpers.
- Debug journal with repeated failure patterns and fixes.

## Break/fix drills
1. Delete a required dict key and handle it safely.
2. Change a numeric input to text and validate before math.
3. Rename an input file and recover with clear error handling.

## Troubleshooting
- If loops confuse you: print intermediate values each iteration.
- If functions confuse you: write expected input/output examples first.
- If tests confuse you: test one function at a time with tiny data.

## Mastery check
You are ready for the next phase when you can:
- write and test small functions from scratch,
- explain tracebacks in plain English,
- process list-of-dict data without guesswork.

## Learning-style options (Play/Build/Dissect/Teach-back)
- Play: mutate examples aggressively and observe behavior.
- Build: complete every lab in order and commit after each lab.
- Dissect: read a peer script and refactor it into smaller functions.
- Teach-back: explain one lab weekly in writing or a recorded walkthrough.

## Primary Sources
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)

## Optional Resources
- [Automate the Boring Stuff](https://automatetheboringstuff.com/3e/)
- [Exercism Python](https://exercism.org/tracks/python)

## Next
Go to [09_QUALITY_TOOLING.md](./09_QUALITY_TOOLING.md).
