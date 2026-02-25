# Level 6 / Project 08 - Data Lineage Capture
Home: [README](../../../README.md)

## Focus
- capture lineage metadata fields

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-6/08-data-lineage-capture
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
{
  "records_processed": 3,
  "pipeline_steps": 3,
  "total_lineage_entries": 9,
  "lineage": {"order-101": [...], ...}
}
```

## Expected artifacts
- `data/output_summary.json` — lineage chains per record
- Passing tests (`pytest -q` → 6+ passed)
- Updated `notes.md`

## Alter it (required)
1. Add a `filter` step between `normalize` and `publish` that removes records below a threshold value.
2. Add a `format_lineage_report(key)` function that prints a record's full journey in human-readable form.
3. Store a hash of the data at each step so you can verify no corruption occurred.
4. Re-run script and tests after each change.

## Break it (required)
1. Process the same records twice and observe whether lineage entries are duplicated.
2. Remove the `normalize` step and observe the gap in the lineage chain.
3. Pass a record with a missing `key` field and trace what happens.

## Fix it (required)
1. Add deduplication: skip lineage recording if the same (record_key, step) already exists.
2. Validate that every record has a `key` field before processing.
3. Add a lineage integrity check that verifies parent_id chains are unbroken.

## Explain it (teach-back)
1. What is data lineage, and why do regulated industries require it?
2. How does the parent_id column create a chain of custody for each record?
3. What is a recursive CTE, and how could it trace a full lineage path?
4. How would you implement lineage in a real data warehouse?

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

| [← Prev](../07-sql-summary-publisher/README.md) | [Home](../../../README.md) | [Next →](../09-incremental-load-simulator/README.md) |
|:---|:---:|---:|
