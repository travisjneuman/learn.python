# Level 4 / Project 01 - Schema Validator Engine
Home: [README](../../../README.md)

## Focus
- required fields and datatype checks

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-4/01-schema-validator-engine
python project.py --schema data/schema.json --input data/records.json --output data/validation_report.json
pytest -q
```

## Expected terminal output
```text
{
  "total": 6,
  "valid": 2,
  "invalid": 4,
  "errors": [ ... ]
}
6 passed
```

## Expected artifacts
- `data/validation_report.json` — structured report with per-record errors
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `"pattern"` rule to the schema (e.g., email must contain `@`) and enforce it in `validate_record`.
2. Add a `--strict` CLI flag that treats unexpected extra fields as errors instead of warnings.
3. Re-run script and tests — add a test for your new pattern rule.

## Break it (required)
1. Feed the validator a record where `"age"` is a float like `30.5` — it should fail the `"integer"` type check.
2. Create a schema with an unknown type string (e.g., `"type": "uuid"`) and observe what happens.
3. Pass an empty JSON array `[]` and confirm the report still generates correctly.

## Fix it (required)
1. Handle unknown type strings gracefully — log a warning instead of silently skipping.
2. Add a test for float-vs-integer edge cases.
3. Re-run until all tests pass deterministically.

## Explain it (teach-back)
1. Why does `validate_record` collect all errors instead of stopping at the first one?
2. What happens if a field is optional AND absent — trace through the code path.
3. Why is `TYPE_MAP` defined as a module-level constant instead of inside the function?
4. How would you extend this to validate nested objects (dicts inside dicts)?

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
- [Functions Explained](../../../concepts/functions-explained.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../README.md) | [Home](../../../README.md) | [Next →](../02-excel-input-health-check/README.md) |
|:---|:---:|---:|
