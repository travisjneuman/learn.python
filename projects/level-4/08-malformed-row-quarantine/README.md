# Level 4 / Project 08 - Malformed Row Quarantine
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | [Browser](../../../browser/level-4.html) |

<!-- modality-hub-end -->

**Estimated time:** 60 minutes

## Focus
- reject queue and reason tracking

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-4/08-malformed-row-quarantine
python project.py --input data/sample_input.csv --output-dir data/output --required 0,1
pytest -q
```

## Expected terminal output
```text
{
  "total_data_rows": 7,
  "valid": 4,
  "quarantined": 3
}
7 passed
```

## Expected artifacts
- `data/output/valid_rows.txt` — clean rows that passed all rules
- `data/output/quarantined_rows.json` — rejected rows with reasons
- `data/output/quarantine_report.json` — summary counts
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a new rule: `rule_no_duplicate_values` that rejects rows where a key field repeats a value seen in a prior row.
2. Add a `--delimiter` CLI flag to handle TSV or pipe-delimited files.
3. Re-run script and tests — add a parametrized test for the new rule.

## Break it (required) — Core
1. Feed it a file with only a header and no data rows — observe the counts.
2. Create a row with a field containing 10,000+ characters and see if `rule_max_field_length` catches it.
3. Remove the header row entirely and observe what happens to column-count validation.

## Fix it (required) — Core
1. Handle the no-data-rows case gracefully (valid output, zero counts).
2. Add a `--has-header` flag for header-less files.
3. Re-run until all tests pass.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why are validation rules written as separate functions instead of one big `if/else` block?
2. What is the advantage of collecting ALL reasons per row instead of stopping at the first?
3. Why does the quarantine file use JSON instead of CSV?
4. How would you add custom rules at runtime (without editing the source code)?

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

| [← Prev](../07-duplicate-record-investigator/README.md) | [Home](../../../README.md) | [Next →](../09-transformation-pipeline-v1/README.md) |
|:---|:---:|---:|
