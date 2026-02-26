# Level 7 / Project 14 - Cache Backfill Runner
Home: [README](../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus
- historical backfill workflow

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-7/14-cache-backfill-runner
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
... output_summary.json written ...
2 passed
```

## Expected artifacts
- `data/output_summary.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `max_backfills` limit so the cache only auto-backfills N times before requiring manual intervention.
2. Add an `evict_oldest()` method that removes the least-recently-added cache entry when at capacity.
3. Re-run script and tests — verify backfill limiting and eviction work.

## Break it (required)
1. Set `miss_threshold` to 0.0 so every single miss triggers a backfill.
2. Provide an empty source dict and request keys that do not exist.
3. Observe excessive backfills (thrashing) or `None` results with misleading stats.

## Fix it (required)
1. Validate that `miss_threshold` is between 0.01 and 1.0 to prevent thrashing.
2. Skip backfill when the source is empty (nothing to load).
3. Add tests for zero threshold, empty source, and backfill count limits.

## Explain it (teach-back)
1. Why does threshold-based backfill prevent unnecessary source reads?
2. What happened when miss_threshold was set to zero?
3. How did the minimum threshold validation prevent cache thrashing?
4. Where would you use cache backfill in a real high-traffic web application?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Decorators Explained](../../../concepts/decorators-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [Quiz: Decorators Explained](../../../concepts/quizzes/decorators-explained-quiz.py)

---

| [← Prev](../13-service-account-policy-check/README.md) | [Home](../../../README.md) | [Next →](../15-level7-mini-capstone/README.md) |
|:---|:---:|---:|
