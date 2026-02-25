# Level 3 / Project 11 - Project Config Bootstrap
Home: [README](../../../README.md)

## Focus
- bootstrap config with environment overrides

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-3/11-project-config-bootstrap
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
... output_summary.json written ...
2 passed
```

## Expected artifacts
- `data/output_summary.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add one reliability or readability improvement.
2. Add one validation or guard clause.
3. Re-run script and tests.

## Break it (required)
1. Use malformed or edge-case input.
2. Confirm behavior fails or degrades predictably.
3. Capture the first failing test or visible bad output.

## Fix it (required)
1. Add or update defensive checks.
2. Add or update tests for the broken case.
3. Re-run until output and tests are deterministic.

## Explain it (teach-back)
1. What assumptions did this project make?
2. What broke first and why?
3. What exact change fixed it?
4. How would this pattern apply in enterprise automation work?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../10-dependency-boundary-lab/README.md) | [Home](../../../README.md) | [Next →](../12-parser-with-fixtures/README.md) |
|:---|:---:|---:|
