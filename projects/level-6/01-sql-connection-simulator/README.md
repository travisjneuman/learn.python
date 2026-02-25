# Level 6 / Project 01 - SQL Connection Simulator
Home: [README](../../../README.md)

## Focus
- connection config and retry patterns

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-6/01-sql-connection-simulator
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
{
  "rows_inserted": 7,
  "rows": [ ... ],
  "health": {"status": "healthy", "sqlite_version": "..."},
  "pool_stats": {"created": 1, "reused": 1, ...}
}
```

## Expected artifacts
- `data/output_summary.json` — full run results with pool stats
- Passing tests (`pytest -q` → 8+ passed)
- Updated `notes.md`

## Alter it (required)
1. Add a `--timeout` CLI flag that sets `ConnectionConfig.timeout` (observe what happens with very small values like 0.001).
2. Track *peak* concurrent connections (the highest number of connections checked out simultaneously) and include it in `pool.stats()`.
3. Add a `ConnectionPool.shrink()` method that closes idle connections down to a target count.
4. Re-run script and tests after each change.

## Break it (required)
1. Set `pool_size=0` and observe what happens when connections cannot be pooled.
2. Pass an invalid database path (e.g. `/nonexistent/dir/db.sqlite`) and observe the retry/failure behaviour.
3. Close a connection manually, then return it to the pool — what happens on the next acquire?

## Fix it (required)
1. Add a guard in `release()` that pings the connection before returning it to the pool (discard broken ones).
2. Validate that `pool_size >= 1` in `ConnectionConfig.__post_init__`.
3. Add tests for each broken case above.

## Explain it (teach-back)
1. Why do context managers (`with` blocks) matter for database connections?
2. What is the performance difference between creating a new connection per query vs. pooling?
3. Why does the retry use *exponential* backoff instead of a fixed delay?
4. In a production web server, what problems arise if the pool is too small? Too large?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Collections Explained](../../../concepts/collections-explained.md)
- [Decorators Explained](../../../concepts/decorators-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Quiz: Collections Explained](../../../concepts/quizzes/collections-explained-quiz.py)

---

| [← Prev](../README.md) | [Home](../../../README.md) | [Next →](../02-staging-table-loader/README.md) |
|:---|:---:|---:|
