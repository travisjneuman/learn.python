# Level 6 / Project 04 - Upsert Strategy Lab
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- insert/update decision logic

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-6/04-upsert-strategy-lab
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
{
  "strategy": "on_conflict",
  "input_rows": 6,
  "inserted": 4,
  "updated": 2,
  "final_products": 4,
  ...
}
```

## Expected artifacts
- `data/output_summary.json` — upsert results with insert/update counts
- Passing tests (`pytest -q` → 6+ passed)
- Updated `notes.md`

## Alter it (required)
1. Add a `last_updated_by` column that records which strategy performed the upsert.
2. Run the same input with `--strategy replace` and `--strategy on_conflict` — compare the `products` output to see the difference.
3. Add a `--dry-run` flag that validates and counts without actually writing to the database.
4. Re-run script and tests after each change.

## Break it (required)
1. Feed a CSV row with a non-numeric `price` (e.g. "free") and observe the error handling.
2. Feed duplicate SKUs with conflicting data and compare how `replace` vs `on_conflict` handle it.
3. Remove the `sku` column from the CSV and observe the KeyError.

## Fix it (required)
1. Add input validation that catches non-numeric prices before the database insert.
2. Add a `--log-conflicts` flag that prints when an existing row is being overwritten.
3. Handle missing columns gracefully with a clear error message.

## Explain it (teach-back)
1. What is the difference between `INSERT OR REPLACE` and `INSERT ... ON CONFLICT DO UPDATE`?
2. Why does `REPLACE` delete and re-insert while `ON CONFLICT` updates in place?
3. When would you choose one strategy over the other in production?
4. What role does the `UNIQUE` constraint play in making upserts work?

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
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../03-idempotency-key-builder/README.md) | [Home](../../../README.md) | [Next →](../05-transaction-rollback-drill/README.md) |
|:---|:---:|---:|
