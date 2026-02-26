# Level 0 / Project 09 - Daily Checklist Writer
Home: [README](../../../README.md)

**Estimated time:** 25 minutes

## Focus
- write text output files

## Why this project exists
Read a list of tasks from a file and generate a formatted checklist with numbered items and checkboxes. This is your first project that writes output files, not just prints to the terminal.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/09-daily-checklist-writer
python project.py --input data/sample_input.txt --title "Daily Checklist"
pytest -q
```

## Expected terminal output
```text
=== Daily Checklist ===

  1. [ ] Review yesterday's notes
  2. [ ] Complete Python exercise
  3. [ ] Read one chapter of documentation

Checklist written to data/checklist.txt
4 passed
```

## Expected artifacts
- `data/output.txt` (formatted checklist)
- `data/output.json` (JSON summary)
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--header` flag that puts a custom title at the top of the checklist (e.g. "Monday Tasks").
2. Add priority markers -- lines starting with `!` get a `[!]` prefix instead of `[ ]`.
3. Re-run script and tests.

## Break it (required) — Core
1. Use an empty task list -- does `format_checklist()` return something sensible or crash?
2. Add tasks with only whitespace -- do blank tasks get numbered or skipped?
3. Use a task file with 100+ items -- does the numbering still align correctly?

## Fix it (required) — Core
1. Handle the empty-list case by returning a "(no tasks)" message.
2. Ensure `load_tasks()` strips whitespace and skips blank lines.
3. Add a test for the empty-task-list edge case.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does `format_checklist()` use `enumerate(tasks, start=1)` instead of a manual counter?
2. What does `[ ]` checkbox format represent and where is it used (Markdown, GitHub issues)?
3. Why write the checklist to a `.txt` file instead of JSON?
4. Where would checklist generation appear in real software (project management tools, daily standup reports)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../08-string-cleaner-starter/README.md) | [Home](../../../README.md) | [Next →](../10-duplicate-line-finder/README.md) |
|:---|:---:|---:|
