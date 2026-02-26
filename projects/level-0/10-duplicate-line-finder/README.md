# Level 0 / Project 10 - Duplicate Line Finder
Home: [README](../../../README.md)

**Estimated time:** 25 minutes

## Focus
- set usage and duplicate detection

## Why this project exists
Find repeated lines in a text file, report how many times each appears and on which line numbers. You will learn dictionary-based counting and set-based uniqueness checks -- the fundamental pattern for deduplication.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/10-duplicate-line-finder
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Duplicate Line Report ===
  Total lines: 5
  Unique lines: 3
  Duplicated lines: 2

  Duplicates found:
    'check server status' appears 2 times (lines 1, 3)
    'restart web service' appears 2 times (lines 2, 5)

  Report written to data/output.json
4 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add case-insensitive duplicate detection (so "Hello" and "hello" count as duplicates).
2. Add a `--ignore-blank` flag that skips empty lines when checking for duplicates.
3. Re-run script and tests.

## Break it (required) — Core
1. Use a file with no duplicates at all -- does `find_duplicates()` return an empty dict?
2. Use a file where every line is identical -- does the report show the correct count?
3. Use a file with trailing spaces -- are `"hello"` and `"hello "` treated as duplicates?

## Fix it (required) — Core
1. Ensure `load_lines()` strips trailing whitespace so `"hello "` matches `"hello"`.
2. Handle the no-duplicates case by printing a clear "No duplicates found" message.
3. Add a test for the all-unique-lines case.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does `count_line_occurrences()` use a dict to count instead of nested loops?
2. What is the difference between `dict.get(key, 0)` and `dict[key]` when the key might not exist?
3. Why does `find_duplicates()` only return lines with count > 1?
4. Where would duplicate detection appear in real software (data deduplication, log analysis, CSV cleaning)?

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

| [← Prev](../09-daily-checklist-writer/README.md) | [Home](../../../README.md) | [Next →](../11-simple-menu-loop/README.md) |
|:---|:---:|---:|
