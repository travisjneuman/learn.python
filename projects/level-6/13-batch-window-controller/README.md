# Level 6 / Project 13 - Batch Window Controller
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- load window scheduling controls

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-6/13-batch-window-controller
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
{
  "windows_created": 4,
  "overlaps_found": 1,
  "gaps": [{"start": "...", "end": "..."}, ...],
  "windows": [...]
}
```

## Expected artifacts
- `data/output_summary.json` — window analysis with overlaps and gaps
- Passing tests (`pytest -q` → 6+ passed)
- Updated `notes.md`

## Alter it (required)
1. Add a `merge_overlaps` function that combines overlapping windows into a single window.
2. Add a `--auto-fill-gaps` flag that creates new pending windows for any detected gaps.
3. Add a duration column showing each window's length in hours.
4. Re-run script and tests after each change.

## Break it (required)
1. Create a window where `end < start` and observe the validation error.
2. Create three windows that all overlap each other and check all pairs are detected.
3. Try to transition a window to an invalid status (e.g. "cancelled").

## Fix it (required)
1. Add validation rejecting `end <= start` windows.
2. Ensure overlap detection handles more than 2 windows overlapping.
3. Add status validation with a clear error message.

## Explain it (teach-back)
1. Why are overlapping processing windows dangerous in data pipelines?
2. What is a "gap" in batch processing, and what data does it leave unprocessed?
3. How do real ETL systems prevent double-processing?
4. What is the interval scheduling problem and how does it relate to this project?

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
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../12-etl-health-dashboard-feed/README.md) | [Home](../../../README.md) | [Next →](../14-sql-runbook-generator/README.md) |
|:---|:---:|---:|
