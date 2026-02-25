# Level 1 / Project 13 - Batch Rename Simulator
Home: [README](../../../README.md)

## Focus
- safe rename planning without destructive changes

## Why this project exists
Plan file renames without actually moving anything. Apply rules like lowercase, strip-numbers, or add-prefix, detect naming conflicts, and preview a before/after mapping. You will learn safe simulation before destructive operations.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-1/13-batch-rename-simulator
python project.py --input data/sample_input.txt --rule lower
pytest -q
```

## Expected terminal output
```text
=== Batch Rename Plan (rule: lower) ===

  001_Project Report.docx      => 001_project report.docx
  002_Meeting Notes.txt        => 002_meeting notes.txt
  003_Budget Spreadsheet.xlsx  => 003_budget spreadsheet.xlsx

  3 renames planned, 0 conflicts
8 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a new rule: `add_date` that prepends today's date as `YYYY-MM-DD_` to the filename.
2. Add a `--dry-run` flag that prints the plan but does not write the output file.
3. Re-run script and tests.

## Break it (required)
1. Add two files that would rename to the same target (e.g. `A.TXT` and `a.txt` with the `lower` rule) -- does `detect_conflicts()` catch it?
2. Add an empty filename (blank line) -- does `simulate_rename()` raise `ValueError`?
3. Use an unknown rule name like `--rule banana` -- does argparse reject it or does the code crash?

## Fix it (required)
1. Ensure `detect_conflicts()` identifies all files that would collide after renaming.
2. Handle blank lines in the input by skipping them in `simulate_batch()`.
3. Add a test for the conflict-detection case.

## Explain it (teach-back)
1. Why is this a "simulator" and not an actual renamer? What safety benefit does simulation provide?
2. Why does `RULES` store functions as dict values instead of using if/elif?
3. What does `re.sub(r"^\d+[\-_ ]*", "", stem)` do in `apply_rule_strip_numbers()`?
4. Where would batch rename simulation appear in real software (file managers, migration scripts, DevOps tools)?

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
- [How Loops Work](../../../concepts/how-loops-work.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Functions Explained](../../../concepts/quizzes/functions-explained-quiz.py)

---

| [← Prev](../12-file-extension-counter/README.md) | [Home](../../../README.md) | [Next →](../14-basic-expense-tracker/README.md) |
|:---|:---:|---:|
