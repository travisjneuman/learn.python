# Level 6 / Project 02 - Staging Table Loader
Home: [README](../../../README.md)

## Focus
- staging ingestion contract simulation

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-6/02-staging-table-loader
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
{
  "input_rows": 8,
  "accepted": 5,
  "rejected": 3,
  "errors": ["row=6 missing_field=timestamp", ...],
  "total_in_staging": 5
}
```

## Expected artifacts
- `data/output_summary.json` — load results with accept/reject counts
- Passing tests (`pytest -q` → 7+ passed)
- Updated `notes.md`

## Alter it (required)
1. Add a new validation rule: reject rows where the `message` field exceeds 200 characters.
2. Add a `--strict` CLI flag that aborts the entire load if any row fails validation (instead of skipping).
3. Add a `loaded_at` timestamp column to `staging_events` populated by the loader.
4. Re-run script and tests after each change.

## Break it (required)
1. Feed a CSV with mismatched column headers (e.g. rename "level" to "severity") and observe the error.
2. Insert a row with a `level` value of "DEBUG" (not in `VALID_LEVELS`) and confirm rejection.
3. Try loading the same file twice and observe whether duplicates accumulate.

## Fix it (required)
1. Add header validation that checks required columns exist before processing any rows.
2. Add an idempotency check using a hash of each row to prevent duplicate inserts.
3. Add tests for each broken scenario.

## Explain it (teach-back)
1. Why do we insert row-by-row instead of using `executemany` for this use case?
2. What is the advantage of a staging table vs inserting directly into the final table?
3. How does the `CHECK` constraint in the DDL differ from Python-side validation?
4. In production ETL, what happens to rejected rows — are they just logged?

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
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../01-sql-connection-simulator/README.md) | [Home](../../../README.md) | [Next →](../03-idempotency-key-builder/README.md) |
|:---|:---:|---:|
