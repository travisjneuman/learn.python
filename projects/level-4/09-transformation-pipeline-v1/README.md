# Level 4 / Project 09 - Transformation Pipeline V1
Home: [README](../../../README.md)

**Estimated time:** 60 minutes

## Focus
- multi-step transform sequencing

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-4/09-transformation-pipeline-v1
python project.py --input data/sample_input.csv --output data/pipeline_output.json --steps strip_whitespace,lowercase_keys,filter_empty_rows,coerce_numbers,add_row_id
pytest -q
```

## Expected terminal output
```text
{
  "steps": [
    {"step": "strip_whitespace", "status": "ok", ...},
    ...
  ],
  "output_records": 5
}
8 passed
```

## Expected artifacts
- `data/pipeline_output.json` — transformed data with step log
- Passing tests
- Updated `notes.md`

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a `transform_rename_columns` step that accepts a rename mapping (e.g., `Name -> full_name`).
2. Add a `--dry-run` flag that shows the step log without writing output.
3. Re-run script and tests — add a test for the rename transform.

## Break it (required) — Core
1. Pass an unknown step name in `--steps` and verify it is logged as skipped.
2. Reorder the steps (e.g., `add_row_id` before `filter_empty_rows`) and observe the difference.
3. Feed it a CSV where all rows are empty and see what `filter_empty_rows` does.

## Fix it (required) — Core
1. Add step ordering validation — warn if `add_row_id` runs before `filter_empty_rows`.
2. Handle the case where an input CSV has no rows (only headers) gracefully.
3. Re-run until all tests pass.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. Why are transforms written as pure functions (no side effects)?
2. What is the `TRANSFORMS` registry pattern and why is it useful?
3. Why does the step log track `records_before` and `records_after`?
4. How would you add error handling so one failing step does not crash the whole pipeline?

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

| [← Prev](../08-malformed-row-quarantine/README.md) | [Home](../../../README.md) | [Next →](../10-run-manifest-generator/README.md) |
|:---|:---:|---:|
