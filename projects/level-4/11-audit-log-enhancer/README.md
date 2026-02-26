# Level 4 / Project 11 - Audit Log Enhancer
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | [Browser](../../../browser/level-4.html) |

<!-- modality-hub-end -->

**Estimated time:** 65 minutes

## Focus
- rich event logging for traceability

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-4/11-audit-log-enhancer
python project.py --input data/sample_input.jsonl --output data/enriched_logs.jsonl
pytest -q
```

## Expected terminal output
```text
{
  "total_entries": 6,
  "enriched": 6,
  "severity_counts": {"LOW": 3, "HIGH": 1, "MEDIUM": 1, ...}
}
7 passed
```

## Expected artifacts
- `data/enriched_logs.jsonl` — enriched log entries (JSON lines)
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--severity-filter` flag to only output entries at or above a given severity.
2. Add a `duration_category` field: "fast" (<100ms), "normal" (<1000ms), "slow" (>=1000ms).
3. Re-run script and tests — add a parametrized test for duration categories.

## Break it (required) — Core
1. Add a log entry with malformed JSON and confirm it is skipped gracefully.
2. Add entries with no `session_id` and observe how correlation IDs are assigned.
3. Use timestamps in different timezone formats and see if duration calculation handles them.

## Fix it (required) — Core
1. Handle timezone-naive timestamps by assuming UTC.
2. Add a count of skipped malformed lines to the summary.
3. Re-run until all tests pass.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. What is a correlation ID and why is it useful for debugging?
2. Why does `enrich_entry` make a shallow copy instead of modifying the original dict?
3. What is the JSON Lines format and why is it preferred over a JSON array for logs?
4. How would you handle enrichment of millions of log entries efficiently?

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

| [← Prev](../10-run-manifest-generator/README.md) | [Home](../../../README.md) | [Next →](../12-checkpoint-recovery-tool/README.md) |
|:---|:---:|---:|
