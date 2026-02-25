# Level 4 / Project 05 - Path Safe File Mover
Home: [README](../../../README.md)

## Focus
- safe move plans and collision prevention

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-4/05-path-safe-file-mover
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
1. Add a `--dry-run` flag that prints the planned moves without actually moving files.
2. Handle filename collisions by appending a counter (e.g., `report_1.csv`, `report_2.csv`) instead of overwriting.
3. Create a move log (JSON or CSV) recording source, destination, timestamp, and success/failure for each file.
4. Re-run script and tests.

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

- [Api Basics](../../../concepts/api-basics.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../04-data-contract-enforcer/README.md) | [Home](../../../README.md) | [Next →](../06-backup-rotation-tool/README.md) |
|:---|:---:|---:|
