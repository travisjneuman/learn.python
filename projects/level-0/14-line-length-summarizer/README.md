# Level 0 / Project 14 - Line Length Summarizer
Home: [README](../../../README.md)

**Estimated time:** 30 minutes

## Focus
- loop metrics and summary output

## Why this project exists
Measure the length of every line in a file and compute min, max, and average statistics. You will also build a text-based histogram and categorise lines as short, medium, or long -- practising loops, aggregation, and visual output.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/14-line-length-summarizer
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Line Length Summary ===
  Total lines: 4
  Shortest:    5 chars
  Longest:     64 chars
  Average:     28 chars

  Histogram:
    11 | ######
    64 | ##################################
     5 | ###
4 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a "median line length" metric to `compute_stats()`.
2. Add a `--threshold` flag that customises the short/medium/long category boundaries.
3. Re-run script and tests.

## Break it (required) — Core
1. Use an empty file -- does `compute_stats()` crash on `min([])` or `sum([]) / 0`?
2. Use a file where every line is the same length -- does the histogram still display correctly?
3. Use a file with one very long line (10,000+ characters) -- does the histogram bar overflow?

## Fix it (required) — Core
1. Add a guard for empty files that returns zero stats without crashing.
2. Cap histogram bar length to a maximum width (e.g. 50 characters).
3. Add a test for the empty-file edge case.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does `compute_stats()` compute min, max, and average but not median?
2. What does `build_histogram()` use to scale the bar lengths proportionally?
3. Why categorise lines as short/medium/long instead of just showing raw lengths?
4. Where would line length analysis appear in real software (linting, code style checks, log analysis)?

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

| [← Prev](../13-alarm-message-generator/README.md) | [Home](../../../README.md) | [Next →](../15-level0-mini-toolkit/README.md) |
|:---|:---:|---:|
