# Level 6 / Project 10 - Table Drift Detector
Home: [README](../../../README.md)

## Focus
- schema drift detection and alerts

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-6/10-table-drift-detector
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
{
  "tables_checked": 2,
  "drift_detected": false,
  "reports": [{"table": "users", "columns": ["id", "name", "email"], ...}, ...]
}
```

## Expected artifacts
- `data/output_summary.json` — drift reports per table
- Passing tests (`pytest -q` → 6+ passed)
- Updated `notes.md`

## Alter it (required)
1. Add a severity level: "warning" for added columns, "critical" for removed columns or type changes.
2. Store multiple snapshots and add a `--compare` flag to diff any two specific snapshots by ID.
3. Add a NOT NULL constraint change detector (a column changing from nullable to NOT NULL).
4. Re-run script and tests after each change.

## Break it (required)
1. Run twice with the same schema — confirm drift is not falsely detected.
2. Add a column via `ALTER TABLE` between runs and confirm drift IS detected.
3. Pass a table name that does not exist and observe the error.

## Fix it (required)
1. Handle non-existent tables gracefully with a clear error message.
2. Add a "no change" status to the report when schemas match.
3. Add a test for the ALTER TABLE drift scenario.

## Explain it (teach-back)
1. What is schema drift, and why is it dangerous in data pipelines?
2. How does `PRAGMA table_info()` work in SQLite?
3. Why do we store snapshots as JSON instead of comparing live schemas?
4. In production, what tools detect schema drift automatically?

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

| [← Prev](../09-incremental-load-simulator/README.md) | [Home](../../../README.md) | [Next →](../11-dead-letter-row-handler/README.md) |
|:---|:---:|---:|
