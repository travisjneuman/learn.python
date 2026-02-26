# Level 6 / Project 14 - SQL Runbook Generator
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- operational runbook artifact creation

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-6/14-sql-runbook-generator
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
{
  "runbooks_generated": 2,
  "runbooks": [{"name": "table_maintenance", "steps": 3, ...}, ...],
  "history": [...]
}
```

## Expected artifacts
- `data/output_summary.json` — generated runbook details with history
- Passing tests (`pytest -q` → 6+ passed)
- Updated `notes.md`

## Alter it (required)
1. Add a custom template: `"backup_restore"` with steps for backing up and restoring a table.
2. Add a `--execute` flag that actually runs each SQL step against the database (with confirmation prompts in a real CLI).
3. Add step numbering and estimated execution time to the formatted output.
4. Re-run script and tests after each change.

## Break it (required)
1. Request a non-existent template name and observe the error.
2. Use a template parameter that contains SQL injection (`'; DROP TABLE users; --`) and observe what happens.
3. Leave a required template parameter unset and observe the KeyError.

## Fix it (required)
1. Validate template names against available templates before generation.
2. Add SQL injection detection in `validate_sql` for common patterns.
3. Catch missing parameter errors and report which parameters are required.

## Explain it (teach-back)
1. Why is template-based SQL generation safer than string concatenation?
2. What is the difference between `string.Template` substitution and parameterized queries?
3. Why store runbook history in a database instead of just generating text files?
4. What is an operational runbook and why do teams maintain them?

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
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../13-batch-window-controller/README.md) | [Home](../../../README.md) | [Next →](../15-level6-mini-capstone/README.md) |
|:---|:---:|---:|
