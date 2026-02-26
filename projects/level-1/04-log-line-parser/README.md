# Level 1 / Project 04 - Log Line Parser
Home: [README](../../../README.md)

> **Try in Browser:** [Run this exercise online](../../browser/level-1.html?ex=4) — no installation needed!

## Before You Start

Recall these prerequisites before diving in:
- Can you split a string on a specific delimiter? (`"a:b:c".split(":")`)
- Can you use `datetime.strptime()` to parse a date string?

**Estimated time:** 25 minutes

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| [Concept](../../../concepts/how-imports-work.md) | **This project** | — | [Quiz](../../../concepts/quizzes/how-imports-work-quiz.py) | [Flashcards](../../../practice/flashcards/README.md) | — | [Browser](../../../browser/level-1.html) |

<!-- modality-hub-end -->

## Focus
- split and parse structured text

## Why this project exists
Parse structured log lines into timestamp, level, and message fields, then count entries by level and optionally filter. You will learn string splitting on delimiters, datetime parsing, and building analysis summaries.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-1/04-log-line-parser
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Log Analysis ===

  2024-01-15 09:30:00 [INFO]    Server started on port 8080
  2024-01-15 09:30:05 [INFO]    Database connection established
  2024-01-15 09:31:12 [WARNING] Slow query detected (2.3s)

  Level counts: INFO=2, WARNING=1
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--after` flag that only shows log entries after a given timestamp.
2. Add a "most active hour" metric that shows which hour had the most log entries.
3. Re-run script and tests.

## Break it (required) — Core
1. Add a malformed line like `not a log entry at all` -- does `parse_log_line()` return `None` or crash?
2. Add a line with an invalid timestamp like `9999-99-99 00:00:00` -- does `datetime.strptime()` fail?
3. Use `--level CRITICAL` when no CRITICAL entries exist -- does `filter_by_level()` return an empty list?

## Fix it (required) — Core
1. Ensure `parse_log_line()` returns `None` for unparseable lines instead of crashing.
2. Wrap `datetime.strptime()` in a try/except to handle invalid timestamps.
3. Add a test for the malformed-line case.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does `parse_log_line()` use string splitting instead of regex for this log format?
2. What does `datetime.strptime()` do and what happens when the format does not match?
3. Why does `count_by_level()` use a dict instead of separate counters for each level?
4. Where would log parsing appear in real software (monitoring dashboards, incident response, audit trails)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Files and Paths](../../../concepts/files-and-paths.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Files and Paths](../../../concepts/quizzes/files-and-paths-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Log Line Parser. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to split a log line into timestamp, level, and message. The format is `[2024-01-15 10:30:00] INFO: message`. Can you give me a hint about how to extract the parts?"
- "Can you explain `datetime.strptime()` format codes with examples that are not about log files?"

---

| [← Prev](../03-unit-price-calculator/README.md) | [Home](../../../README.md) | [Next →](../05-csv-first-reader/README.md) |
|:---|:---:|---:|
