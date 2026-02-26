# Level 4 / Project 12 - Checkpoint Recovery Tool
Home: [README](../../../README.md)

**Estimated time:** 70 minutes

## Focus
- resume from checkpoints safely

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-4/12-checkpoint-recovery-tool
python project.py --input data/sample_input.txt --output data/processed_output.json --checkpoint data/.checkpoint.json --batch-size 3
pytest -q
```

## Expected terminal output
```text
{
  "total_items": 10,
  "processed": 10,
  "checkpoint_cleared": true
}
6 passed
```

## Expected artifacts
- `data/processed_output.json` — processed results
- `data/.checkpoint.json` — checkpoint file (cleared on success)
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--simulate-crash` flag that stops after N items to test recovery.
2. Add a progress bar (percentage) logged at each checkpoint.
3. Re-run script and tests — verify crash simulation creates a valid checkpoint.

## Break it (required) — Core
1. Corrupt the checkpoint file (write invalid JSON) and run — observe the "starting fresh" behavior.
2. Modify `process_item` to raise an exception on a specific item — verify the checkpoint has progress up to the failure point.
3. Set `--batch-size 0` and observe what happens.

## Fix it (required) — Core
1. Validate `batch_size` is positive in `parse_args`.
2. Add error handling in `process_item` so one bad item does not crash the whole batch.
3. Re-run until all tests pass.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does `save_checkpoint` write to a `.tmp` file first then rename?
2. What would happen if the process crashed DURING a checkpoint write?
3. Why is the checkpoint cleared after successful completion?
4. How would you extend this to support parallel processing with checkpoints?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../11-audit-log-enhancer/README.md) | [Home](../../../README.md) | [Next →](../13-reconciliation-reporter/README.md) |
|:---|:---:|---:|
