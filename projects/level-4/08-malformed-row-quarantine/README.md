# Level 4 / Project 08 - Malformed Row Quarantine
Home: [README](../../../README.md)

## Focus
- reject queue and reason tracking

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-4/08-malformed-row-quarantine
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

- [Api Basics](../../../concepts/api-basics.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../07-duplicate-record-investigator/README.md) | [Home](../../../README.md) | [Next →](../09-transformation-pipeline-v1/README.md) |
|:---|:---:|---:|
