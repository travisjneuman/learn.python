# Level 0 / Project 13 - Alarm Message Generator
Home: [README](../../../README.md)

## Focus
- template strings and alert text building

## Why this project exists
Parse pipe-delimited alarm records, sort them by severity, and generate formatted notification messages. You will learn delimiter parsing, priority ordering with a lookup dict, and template-based text generation.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/13-alarm-message-generator
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Alarm Notifications ===

  [CRITICAL] web-server-01: CPU usage above 95%
  [WARNING]  db-primary: Replication lag 30 seconds
  [INFO]     load-balancer: Health check passed

Summary: 1 critical, 1 warning, 1 info
Output written to data/output.json
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `--severity` filter flag that shows only alarms at or above a given severity level.
2. Add timestamps to each alarm notification (use a hardcoded time for reproducibility).
3. Re-run script and tests.

## Break it (required)
1. Add a line with an unknown severity like `unknown|server01|disk full` -- does `parse_alarm()` reject it?
2. Add a line with missing fields like `critical|` -- does it crash or handle gracefully?
3. Add a line with extra pipe characters -- does the parser split correctly?

## Fix it (required)
1. Ensure `parse_alarm()` validates severity against the allowed list (critical, warning, info).
2. Handle lines with fewer than 3 pipe-delimited fields by raising `ValueError`.
3. Add a test for the unknown-severity edge case.

## Explain it (teach-back)
1. Why does `sort_by_severity()` use a priority dict `{"critical": 0, "warning": 1, "info": 2}` instead of alphabetical sorting?
2. What does the pipe `|` delimiter offer over commas when data might contain commas?
3. Why does `alarm_summary()` count by severity level instead of just total count?
4. Where would alarm formatting appear in real software (monitoring dashboards, PagerDuty, incident management)?

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

| [← Prev](../12-contact-card-builder/README.md) | [Home](../../../README.md) | [Next →](../14-line-length-summarizer/README.md) |
|:---|:---:|---:|
