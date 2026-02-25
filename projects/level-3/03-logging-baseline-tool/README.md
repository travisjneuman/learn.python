# Level 3 / Project 03 - Logging Baseline Tool
Home: [README](../../../README.md)

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

## Alter it (required)
1. Add a `--log-level` flag that controls the minimum level written to the log file.
2. Add ISO 8601 timestamps to the text output format.
3. Add a `--output` flag that writes results to a file instead of stdout.

## Break it (required)
1. Parse a file with malformed log lines (no pipe delimiters) — what happens?
2. Pass `--min-level TRACE` (not a valid level) — does filtering still work?
3. Pass an empty file to `summary` — does it crash or return zeroes?

## Fix it (required)
1. Add validation for the `--min-level` argument against known levels.
2. Handle empty files gracefully in `summarise_entries`.
3. Improve `parse_log_line` to handle lines with extra pipe characters.

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

| [← Prev](../02-cli-arguments-workbench/README.md) | [Home](../../../README.md) | [Next →](../04-test-driven-normalizer/README.md) |
|:---|:---:|---:|
