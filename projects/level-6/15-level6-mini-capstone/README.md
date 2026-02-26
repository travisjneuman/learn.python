# Level 6 / Project 15 - Level 6 Mini Capstone
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- sql-centric pipeline resilience project

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-6/15-level6-mini-capstone
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
{
  "input_records": 7,
  "staged": 5,
  "loaded": 5,
  "rejected": 2,
  "dead_letters": 2,
  "lineage_entries": 12,
  "watermark": "2025-01-15T12:00:00"
}
```

## Expected artifacts
- `data/output_summary.json` — full pipeline results
- Passing tests (`pytest -q` → 6+ passed)
- Updated `notes.md`

## Alter it (required)
1. Run the pipeline twice with a persistent database to confirm the watermark prevents reprocessing.
2. Add a `--report` flag that prints a summary of lineage entries grouped by step.
3. Add a `run_log` query to the output showing all historical pipeline runs.
4. Re-run script and tests after each change.

## Break it (required)
1. Feed a record with key `evt-003` and an older timestamp than the existing record — does the upsert overwrite with stale data?
2. Feed only invalid records and observe that the pipeline handles an all-rejection batch gracefully.
3. Corrupt the watermark table manually and observe the next run's behavior.

## Fix it (required)
1. Add a timestamp comparison in the upsert: only update if the new timestamp is newer.
2. Handle the case where 100% of records are rejected without errors.
3. Add watermark validation to reject obviously invalid values.

## Explain it (teach-back)
1. How do the individual Level 6 patterns (staging, upsert, lineage, watermark, dead-letter) combine into a full pipeline?
2. What would break if you removed the staging step and loaded directly to target?
3. How does the watermark enable idempotent reruns?
4. How would you adapt this pipeline for a production environment with millions of records?

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
- [Virtual Environments](../../../concepts/virtual-environments.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../14-sql-runbook-generator/README.md) | [Home](../../../README.md) | [Next →](../README.md) |
|:---|:---:|---:|
