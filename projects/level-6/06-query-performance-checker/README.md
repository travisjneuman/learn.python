# Level 6 / Project 06 - Query Performance Checker
Home: [README](../../../README.md)

## Focus
- timing and query diagnostics

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-6/06-query-performance-checker
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
{
  "queries_analyzed": 4,
  "indexes_created": ["CREATE INDEX IF NOT EXISTS idx_orders_customer ...", ...],
  "before": [...],
  "after": [...]
}
```

## Expected artifacts
- `data/output_summary.json` — before/after query plan analysis
- Passing tests (`pytest -q` → 6+ passed)
- Updated `notes.md`

## Alter it (required)
1. Add a composite index on `(customer, product)` and observe how multi-column queries benefit.
2. Add timing comparison: print the speedup ratio (before_ms / after_ms) for each query.
3. Add a `--seed-count` flag to control how many rows are inserted for benchmarking.
4. Re-run script and tests after each change.

## Break it (required)
1. Pass a syntactically invalid SQL query and observe the error.
2. Create an index on a column that is never used in WHERE clauses — confirm it has no effect on query plans.
3. Run a query with `SELECT *` on a table with 10,000+ rows and observe the timing.

## Fix it (required)
1. Wrap `analyze_query` in a try/except to handle invalid SQL gracefully.
2. Add a check that warns if an index exists but is never used by any analyzed query.
3. Add tests for error handling.

## Explain it (teach-back)
1. What does `EXPLAIN QUERY PLAN` output tell you about how SQLite executes a query?
2. What is the difference between "SCAN TABLE" and "SEARCH TABLE USING INDEX"?
3. Why does adding an index not always make queries faster?
4. When would you choose NOT to add an index?

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
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../05-transaction-rollback-drill/README.md) | [Home](../../../README.md) | [Next →](../07-sql-summary-publisher/README.md) |
|:---|:---:|---:|
