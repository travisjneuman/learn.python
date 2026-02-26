# Level 1 / Project 10 - Ticket Priority Router
Home: [README](../../../README.md)

**Estimated time:** 35 minutes

## Focus
- business rules to route work

## Why this project exists
Route support tickets to priority queues (critical/high/medium/low) by scanning for keywords in the ticket text. You will learn keyword matching, priority ordering, and grouping data into categories with dictionaries.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-1/10-ticket-priority-router
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Ticket Priority Router ===

  [CRITICAL] (1 tickets)
    #1: Website is completely down, customers cannot access...

  [HIGH] (1 tickets)
    #2: Login page error for users in Europe

  [MEDIUM] (1 tickets)
    #3: Dashboard loading slow during peak hours
4 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--priority` filter flag that shows only tickets matching a given priority level.
2. Add an "escalation" rule: tickets containing "urgent" get bumped up one priority level.
3. Re-run script and tests.

## Break it (required) — Core
1. Add a ticket with no keywords at all like `"Everything is fine"` -- does it correctly default to "low"?
2. Add a ticket matching keywords from multiple priorities -- which priority wins?
3. Add an empty line in the ticket file -- does `process_tickets()` skip it or crash?

## Fix it (required) — Core
1. Ensure `classify_ticket()` checks keywords in priority order (critical first) so the highest match wins.
2. Handle blank lines by skipping them in `process_tickets()`.
3. Add a test for the multi-keyword-match priority resolution.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does `PRIORITY_KEYWORDS` use a dict mapping priority names to keyword lists?
2. What does `any(kw in text.lower() for kw in keywords)` do and why use `any()`?
3. Why does `classify_ticket()` check priorities in order from critical to low?
4. Where would ticket routing appear in real software (help desks, incident management, support queues)?

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

| [← Prev](../09-json-settings-loader/README.md) | [Home](../../../README.md) | [Next →](../11-command-dispatcher/README.md) |
|:---|:---:|---:|
