# Level 6 / Project 03 - Idempotency Key Builder
Home: [README](../../../README.md)

## Focus
- stable key generation and dedupe setup

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-6/03-idempotency-key-builder
python project.py --input data/sample_input.txt --output data/output_summary.json
pytest -q
```

## Expected terminal output
```text
{
  "total_input": 6,
  "processed": 4,
  "skipped": 2,
  "stored_keys": 4
}
```

## Expected artifacts
- `data/output_summary.json` — dedup results with key counts
- Passing tests (`pytest -q` → 7+ passed)
- Updated `notes.md`

## Alter it (required)
1. Add a `--key-fields` CLI argument that lets the user choose which fields form the key (instead of hardcoded source + action).
2. Add a TTL (time-to-live): keys older than N seconds should be considered expired and allow re-processing.
3. Add a `list_keys` CLI subcommand that prints all stored keys with their timestamps.
4. Re-run script and tests after each change.

## Break it (required)
1. Submit operations with identical `source` + `action` but different other fields — observe that they are treated as duplicates.
2. Change the separator in `build_key` from `|` to empty string and create a collision with `build_key("ab", "cd")` vs `build_key("abc", "d")`.
3. Pass an input file with missing `source` or `action` fields.

## Fix it (required)
1. Add validation that required key fields exist before calling `build_key`.
2. Write a test proving the separator prevents accidental collisions.
3. Handle the "same key, different payload" case by logging a warning.

## Explain it (teach-back)
1. Why is SHA-256 a good choice for idempotency keys vs. a simple string concat?
2. What does `INSERT OR IGNORE` do, and how does it differ from `INSERT OR REPLACE`?
3. Why is the pipe separator important for avoiding hash collisions?
4. In what real-world systems would you need idempotency keys?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Classes and Objects](../../../concepts/classes-and-objects.md)
- [Collections Explained](../../../concepts/collections-explained.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [Quiz: Classes and Objects](../../../concepts/quizzes/classes-and-objects-quiz.py)

---

| [← Prev](../02-staging-table-loader/README.md) | [Home](../../../README.md) | [Next →](../04-upsert-strategy-lab/README.md) |
|:---|:---:|---:|
