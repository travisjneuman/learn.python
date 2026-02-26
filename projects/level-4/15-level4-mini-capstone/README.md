# Level 4 / Project 15 - Level 4 Mini Capstone
Home: [README](../../../README.md)

**Estimated time:** 75 minutes

## Focus
- data-quality-first automation workflow

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-4/15-level4-mini-capstone
python project.py --input data/sample_input.csv --output-dir data/output --required name,age --batch-size 3
pytest -q
```

## Expected terminal output
```text
{
  "total_rows": 8,
  "valid": 5,
  "quarantined": 3,
  "run_id": "capstone_20250115_100000"
}
6 passed
```

## Expected artifacts
- `data/output/valid_data.json` — validated and transformed rows
- `data/output/quarantined.json` — rejected rows with reasons
- `data/output/manifest.json` — file inventory with checksums
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `--schema` flag that loads validation rules from a JSON file (like project 01).
2. Add a `--report` flag that generates a human-readable summary alongside the JSON.
3. Re-run script and tests — verify the schema-based validation works.

## Break it (required) — Core
1. Kill the process mid-run (Ctrl+C after 2 rows) and restart — verify it resumes from checkpoint.
2. Feed it a CSV with headers but no data rows.
3. Remove the output directory and verify it is created automatically.

## Fix it (required) — Core
1. Handle keyboard interrupts gracefully (save checkpoint before exiting).
2. Add total processing time to the manifest.
3. Re-run until all tests pass.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. How does this project combine skills from projects 01-14?
2. Why is checkpoint recovery important for data pipelines?
3. What is the purpose of the manifest — when would you use it?
4. If this pipeline processed 1 million rows, what would be the bottleneck and how would you optimize?

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

| [← Prev](../14-configurable-batch-runner/README.md) | [Home](../../../README.md) | [Next →](../README.md) |
|:---|:---:|---:|
