# Level 3 / Project 06 - Structured Error Handler
Home: [README](../../../README.md)

## Focus
- typed errors and safe propagation

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-3/06-structured-error-handler
python project.py records.json --schema schema.json
python project.py records.json --schema schema.json --json
pytest -q
```

## Expected terminal output
```text
Processed 4 records: 2 passed, 2 failed
Error breakdown:
  REQUIRED: 2
  INVALID_FORMAT: 1
16 passed
```

## Expected artifacts
- Validation results on stdout
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `range` rule that validates numeric values (e.g., age 0-150).
2. Add an `--exit-code` flag that returns non-zero if any record fails.
3. Add error severity levels to the schema (warning vs error).

## Break it (required)
1. Pass a schema file that doesn't exist — what error appears?
2. Pass records with a field not in the schema — is it validated or ignored?
3. Trigger an unexpected exception inside a validator — does `safe_process` catch it?

## Fix it (required)
1. Add a friendly error message when schema or records file is missing.
2. Validate the schema itself before processing (are rule names valid?).
3. Ensure `capture_error` works for all built-in exception types.

## Explain it (teach-back)
1. Why create a custom exception hierarchy (AppError, ValidationError, etc.)?
2. What is the "Result pattern" and how does `OperationResult` implement it?
3. How does `safe_process` differ from scattering try/except everywhere?
4. What does `traceback.format_exception` return and when would you use it?

## Mastery check
You can move on when you can:
- design a custom exception hierarchy,
- use the Result pattern instead of exceptions for flow control,
- accumulate errors across a batch without crashing,
- write structured error reports with codes and context.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../05-refactor-monolith-drill/README.md) | [Home](../../../README.md) | [Next →](../07-batch-file-auditor/README.md) |
|:---|:---:|---:|
