# Level 3 / Project 13 - Quality Gate Runner
Home: [README](../../../README.md)

**Estimated time:** 55 minutes

## Focus
- simulate lint/test/build gate process

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-3/13-quality-gate-runner
python project.py project.py
python project.py project.py --json
python project.py project.py --max-lines 100
pytest -q
```

## Expected terminal output
```text
Pipeline: FAIL (5.2ms)
  [PASS] file_exists:project.py: File found
  [PASS] syntax:project.py: No syntax errors
  [FAIL] no_print:project.py: 3 print statement(s) found
  [PASS] size:project.py: 165 lines (limit: 300)
3/4 gates passed
14 passed
```

## Expected artifacts
- Pipeline results on stdout
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `check_docstrings` gate that verifies all functions have docstrings.
2. Add a `--gate` flag to run only specific gates.
3. Add `--strict` mode where any warning is treated as a failure.

## Break it (required) — Core
1. Run on a non-Python file — do syntax and print checks handle it?
2. Run on a file that doesn't exist — does the pipeline still report all gates?
3. Set `--max-lines 0` — does the size check handle the edge case?

## Fix it (required) — Core
1. Add file type detection (skip syntax check for non-.py files).
2. Ensure all gates handle missing files consistently.
3. Add a `--quiet` flag that only shows failures.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. What is a "quality gate" in CI/CD and how does this project simulate one?
2. How does `compile()` check for syntax errors without running the code?
3. Why use `time.perf_counter()` instead of `time.time()` for timing?
4. How does the pipeline aggregate individual gate results?

## Mastery check
You can move on when you can:
- build composable quality gate checks,
- use `compile()` for syntax validation,
- aggregate results into a pass/fail pipeline,
- time operations with `time.perf_counter()`.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../12-parser-with-fixtures/README.md) | [Home](../../../README.md) | [Next →](../14-service-simulator/README.md) |
|:---|:---:|---:|
