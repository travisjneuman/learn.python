# Level 6 / Project 05 - Transaction Rollback Drill
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- rollback-first failure handling

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-6/05-transaction-rollback-drill
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
{
  "committed": 3,
  "rolled_back": 1,
  "final_accounts": [
    {"id": 1, "name": "Alice", "balance": 425.0},
    ...
  ]
}
```

## Expected artifacts
- `data/output_summary.json` — transfer results with account balances
- Passing tests (`pytest -q` → 6+ passed)
- Updated `notes.md`

## Alter it (required)
1. Add a transfer fee: deduct an extra 1% from the source account on each successful transfer.
2. Add a `--max-amount` flag that rejects any single transfer above a threshold.
3. Add a `rollback_all` mode: if any transfer in the batch fails, roll back the entire batch.
4. Re-run script and tests after each change.

## Break it (required)
1. Transfer the exact full balance (e.g. 500.00 from an account with 500.00) — does the CHECK constraint allow balance = 0?
2. Transfer between the same account (from=1, to=1) — what happens?
3. Remove the SAVEPOINT logic and observe what happens when a mid-batch transfer fails.

## Fix it (required)
1. Add a guard that rejects self-transfers (from_id == to_id).
2. Ensure the CHECK constraint allows zero balance but not negative.
3. Add a test that proves savepoints isolate failures from successful transfers.

## Explain it (teach-back)
1. What is a SAVEPOINT, and how does it differ from a regular transaction?
2. Why can we roll back a single transfer without losing the others?
3. What would happen without explicit transaction control (autocommit mode)?
4. How do real banks handle the "insufficient funds" scenario at scale?

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

| [← Prev](../04-upsert-strategy-lab/README.md) | [Home](../../../README.md) | [Next →](../06-query-performance-checker/README.md) |
|:---|:---:|---:|
