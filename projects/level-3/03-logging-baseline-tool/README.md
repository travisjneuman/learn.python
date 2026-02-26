# Level 3 / Project 03 - Logging Baseline Tool
Home: [README](../../../README.md)

> **Try in Browser:** [Practice similar concepts online](../../browser/level-2.html?ex=3) — browser exercises cover Level 2 topics

## Before You Start

Recall these prerequisites before diving in:
- Can you use `logging.basicConfig()` to set up Python's logging module?
- Can you explain the difference between `print()` and `logging.info()`?

**Estimated time:** 35 minutes

## Focus
- structured logs and run summaries

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-3/03-logging-baseline-tool
python project.py parse data/sample_input.txt
python project.py summary data/sample_input.txt
python project.py parse data/sample_input.txt --min-level WARNING
pytest -q
```

## Expected terminal output
```text
[INFO    ] auth         | User admin logged in successfully
[WARNING ] db           | Query took 2.3s (threshold: 1.0s)
...
12 passed
```

## Expected artifacts
- Parsed log output on stdout
- Passing tests
- Updated `notes.md`

## Design First
Before writing code, sketch your approach in `notes.md`:
- What functions or classes do you need?
- What data structures will you use?
- What's the flow from input to output?
- What could go wrong?

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. What filtering or output options would make this tool more useful for a sysadmin?
2. Try improving the output format — what information is missing?
3. Can you redirect output to a file instead of the terminal?

## Break it (required) — Core
1. What happens when the input data does not match the expected format?
2. Try passing invalid arguments — how does the tool respond?
3. What edge case produces surprising output?

## Fix it (required) — Core
1. Add validation for the issue you found most confusing.
2. Make the tool handle empty or minimal input gracefully.
3. Improve parsing to handle messy real-world log data.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. What is `logging.getLogger(__name__)` and why use `__name__`?
2. What is the difference between `logging.basicConfig()` and adding handlers manually?
3. How does the level ordering (DEBUG < INFO < WARNING < ERROR < CRITICAL) work?
4. Why use `@dataclass` for `LogEntry` instead of a plain dict?

## Mastery check
You can move on when you can:
- configure Python's logging module with handlers and formatters,
- filter log entries by level and source programmatically,
- explain the logging level hierarchy,
- use dataclasses for structured data in a real tool.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Logging Baseline Tool. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to configure Python logging with different levels (DEBUG, INFO, WARNING). Can you explain the logging level hierarchy with examples?"
- "Can you explain the difference between `logging.getLogger(__name__)` and `logging.getLogger('myapp')`?"

---

| [← Prev](../02-cli-arguments-workbench/README.md) | [Home](../../../README.md) | [Next →](../04-test-driven-normalizer/README.md) |
|:---|:---:|---:|
