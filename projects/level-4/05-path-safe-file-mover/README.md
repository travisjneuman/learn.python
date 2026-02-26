# Level 4 / Project 05 - Path Safe File Mover
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | [Browser](../../../browser/level-4.html) |

<!-- modality-hub-end -->

**Estimated time:** 55 minutes

## Focus
- safe move plans and collision prevention

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-4/05-path-safe-file-mover
# Create sample source files first:
mkdir -p data/source && echo "hello" > data/source/report.csv && echo "world" > data/source/data.txt
python project.py --source data/source --dest data/dest --output data/move_log.json
pytest -q
```

## Expected terminal output
```text
{
  "total_files": 2,
  "moved": 2,
  "failed": 0,
  "operations": [ ... ]
}
6 passed
```

## Expected artifacts
- `data/dest/` — moved files
- `data/move_log.json` — detailed move log with timestamps
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--pattern` flag to only move files matching a glob (e.g., `*.csv`).
2. Add a `--backup` flag that copies instead of moves, preserving the originals.
3. Re-run script and tests — add a test for the glob filter.

## Break it (required) — Core
1. Try to move files from a non-existent source directory — observe the error.
2. Create a situation where a move fails mid-batch (e.g., read-only destination) and verify rollback.
3. Run the same move twice and confirm collision handling works.

## Fix it (required) — Core
1. Add a pre-check that validates source and destination directories before planning.
2. Ensure the move log records both successes and rollbacks clearly.
3. Re-run until all tests pass.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does the mover use a two-phase approach (plan then execute) instead of moving immediately?
2. How does `resolve_collision` avoid infinite loops — what guarantees it terminates?
3. Why does `_rollback` iterate in reverse order?
4. What are the risks of `shutil.move` across different filesystems?

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
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Path Safe File Mover. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to prevent file name collisions when moving files. Can you explain strategies for handling duplicate file names?"
- "Can you explain the difference between `shutil.move()` and `Path.rename()` and when to use each?"

---

| [← Prev](../04-data-contract-enforcer/README.md) | [Home](../../../README.md) | [Next →](../06-backup-rotation-tool/README.md) |
|:---|:---:|---:|
