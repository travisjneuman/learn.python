# Level 10 / Project 08 - Zero Downtime Migration Lab
Home: [README](../../../README.md)

## Focus
- Expand-migrate-contract pattern for zero-downtime schema changes
- State machine for migration phase tracking
- In-memory table simulation with column operations
- Safety validation and rollback mechanisms

## Why this project exists
Traditional "stop the world" migrations cause downtime. The expand-contract pattern adds new columns first, backfills data, then removes old columns. At every phase, both old and new code paths work — enabling zero-downtime rollout. This project simulates the entire lifecycle in Python.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-10/08-zero-downtime-migration-lab
python project.py
pytest -v
```

## Expected terminal output
```text
Migration: Add display_name
Phase: COMPLETE
Progress: 100%
History (3 entries):
  [EXPANDING] Add column 'display_name' ...
  [MIGRATING] Backfill 'display_name' ...
  [COMPLETE] Migration finished successfully
```

## Alter it (required)
1. Add a `build_split_table_migration` that creates a new table, copies data, then drops the old one.
2. Add a `dry_run` mode to `MigrationExecutor` that logs steps without executing them.
3. Add a step-level progress callback so callers can monitor migration progress.

## Break it (required)
1. Try adding a duplicate column name — observe the `ValueError`.
2. Create a contracting step without an expanding step and check the safety warning.
3. Drop a non-existent column and see the error.

## Fix it (required)
1. Make `add_column` idempotent — skip silently if the column already exists.
2. Add validation that migration steps are in the correct phase order (EXPANDING before MIGRATING before CONTRACTING).
3. Test the phase order validation.

## Explain it (teach-back)
1. Why must the EXPANDING phase come before MIGRATING? What breaks if you skip it?
2. How does the contract phase differ from just dropping a column directly?
3. Why is rollback essential in production migrations?
4. How does this pattern apply to real databases using tools like Alembic or Django migrations?

## Mastery check
You can move on when you can:
- build a migration plan for renaming a column and trace each phase,
- explain why both old and new code must work during the MIGRATING phase,
- describe what happens if a migration fails mid-way and gets rolled back,
- compare expand-contract to "big bang" migration and explain the tradeoffs.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../07-high-risk-change-gate/README.md) | [Home](../../../README.md) | [Next →](../09-strategic-architecture-review/README.md) |
|:---|:---:|---:|
