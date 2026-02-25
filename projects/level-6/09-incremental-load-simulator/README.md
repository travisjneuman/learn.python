# Level 6 / Project 09 - Incremental Load Simulator
Home: [README](../../../README.md)

## Focus
- windowed load logic

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-6/09-incremental-load-simulator
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
{
  "source_records": 5,
  "loaded": 5,
  "skipped": 0,
  "previous_watermark": null,
  "new_watermark": "2025-01-15T11:15:00",
  "total_in_target": 5
}
```

## Expected artifacts
- `data/output_summary.json` — load stats with watermark values
- Passing tests (`pytest -q` → 6+ passed)
- Updated `notes.md`

## Alter it (required)
1. Use a persistent database (`--db data/events.db`) and run the script twice to see the watermark in action.
2. Add a `--full-load` flag that ignores the watermark and reloads everything.
3. Add a `modified_at` check: if a record's ID exists but its timestamp is newer, update it (change detection).
4. Re-run script and tests after each change.

## Break it (required)
1. Feed records with timestamps older than the current watermark — confirm they are all skipped.
2. Feed records with identical timestamps and observe whether the `<=` comparison causes off-by-one issues.
3. Feed records out of chronological order and check whether the watermark is set correctly.

## Fix it (required)
1. Use `<` instead of `<=` if you want to include records at exactly the watermark timestamp.
2. Add a test proving that out-of-order input still produces the correct final watermark.
3. Log a warning when all source records are skipped (may indicate a stale source).

## Explain it (teach-back)
1. What is a high-water mark, and why is it useful for incremental loading?
2. What happens if the source data is late (arrives after the watermark has advanced)?
3. How does incremental loading compare to full-table reload in terms of performance?
4. What are the risks of losing or corrupting the watermark value?

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

| [← Prev](../08-data-lineage-capture/README.md) | [Home](../../../README.md) | [Next →](../10-table-drift-detector/README.md) |
|:---|:---:|---:|
