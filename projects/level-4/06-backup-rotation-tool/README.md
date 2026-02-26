# Level 4 / Project 06 - Backup Rotation Tool
Home: [README](../../../README.md)

**Estimated time:** 55 minutes

## Focus
- retention windows and cleanup policies

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-4/06-backup-rotation-tool
# Create sample backup files first:
mkdir -p data/backups
for d in $(seq 1 20); do touch "data/backups/backup_2025-01-$(printf '%02d' $d).tar.gz"; done
python project.py --backup-dir data/backups --output data/rotation_report.json --daily 7 --weekly 4 --monthly 6
pytest -q
```

## Expected terminal output
```text
{
  "keep": [ ... ],
  "delete": [ ... ],
  "summary": { "total": 20, "keeping": 11, "deleting": 9, ... }
}
5 passed
```

## Expected artifacts
- `data/rotation_report.json` — keep/delete lists with retention reasons
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--execute` flag that actually deletes the files marked for deletion (default: plan only).
2. Add a `--min-keep` safety net that refuses to delete if fewer than N backups would remain.
3. Re-run script and tests — add a test for the min-keep guard.

## Break it (required) — Core
1. Create backup files with unparseable names (no date) and confirm they land in `unparseable`.
2. Set `--daily 0 --weekly 0 --monthly 0` and observe whether ALL backups are scheduled for deletion.
3. Create two backups on the same day and verify only one is counted for the daily slot.

## Fix it (required) — Core
1. Add a confirmation prompt before actual deletion (when `--execute` is used).
2. Handle the edge case of monthly retention when months vary in length (28-31 days).
3. Re-run until all tests pass.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why does `classify_backups` take `now` as a parameter instead of calling `datetime.now()` internally?
2. What is the purpose of `kept_set` — why not just check the `keep` list directly?
3. Why does weekly retention use ISO week numbers instead of just counting 7-day intervals?
4. How would this pattern scale to thousands of backup files?

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

- "I am working on Backup Rotation Tool. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to implement a retention policy that keeps daily backups for 7 days and weekly for 4 weeks. Can you explain the logic for deciding which files to keep vs delete?"
- "Can you explain how to sort files by modification time using `pathlib` and `os.stat`?"

---

| [← Prev](../05-path-safe-file-mover/README.md) | [Home](../../../README.md) | [Next →](../07-duplicate-record-investigator/README.md) |
|:---|:---:|---:|
