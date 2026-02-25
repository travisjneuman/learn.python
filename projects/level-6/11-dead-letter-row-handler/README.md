# Level 6 / Project 11 - Dead Letter Row Handler
Home: [README](../../../README.md)

## Focus
- bad row pipeline and quarantine

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-6/11-dead-letter-row-handler
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
{
  "input_records": 6,
  "processed": 3,
  "dead_lettered": 3,
  "dead_letter_stats": {"total": 3, "unresolved": 3, "resolved": 0}
}
```

## Expected artifacts
- `data/output_summary.json` — processing results with dead-letter details
- Passing tests (`pytest -q` → 6+ passed)
- Updated `notes.md`

## Alter it (required)
1. Add a `--max-retries` flag: dead-letter rows with retry_count >= max should be marked as permanently failed.
2. Add a `retry_all` CLI command that re-runs validation on every unresolved dead-letter row.
3. Add a `reason_summary` that counts how many dead-letters failed for each error type.
4. Re-run script and tests after each change.

## Break it (required)
1. Process a record with `value: null` and observe the error path.
2. Retry a dead-letter row that still has the same validation issue — confirm retry_count increments.
3. Delete the dead_letters table mid-run and observe the crash.

## Fix it (required)
1. Handle `null` values explicitly in `validate_record`.
2. Add a `--create-tables` flag that ensures tables exist before processing (idempotent).
3. Add a test for the retry-increment behavior.

## Explain it (teach-back)
1. What is a dead-letter queue, and where does the name come from?
2. Why store the original payload alongside the error, instead of just logging?
3. When should dead-letter rows be retried vs. permanently discarded?
4. How does this pattern apply to message queues like RabbitMQ or SQS?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Virtual Environments](../../../concepts/virtual-environments.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../10-table-drift-detector/README.md) | [Home](../../../README.md) | [Next →](../12-etl-health-dashboard-feed/README.md) |
|:---|:---:|---:|
