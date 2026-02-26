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

## Worked Example

Here is a similar (but different) problem, solved step by step.

**Problem:** Write a function that validates a config file against expected keys and types.

**Step 1: Define the schema as a dict.**

```python
SCHEMA = {
    "host": {"type": "str", "required": True},
    "port": {"type": "int", "required": True},
    "debug": {"type": "bool", "required": False, "default": False},
}
```

**Step 2: Write the validator.**

```python
def validate_config(config, schema):
    errors = []
    for key, rules in schema.items():
        if key not in config:
            if rules["required"]:
                errors.append(f"Missing required field: {key}")
            continue
        expected_type = {"str": str, "int": int, "bool": bool}[rules["type"]]
        if not isinstance(config[key], expected_type):
            errors.append(f"Field '{key}' expected {rules['type']}, got {type(config[key]).__name__}")
    return {"valid": len(errors) == 0, "errors": errors}
```

**Step 3: Test it.** Valid config passes. Missing required field fails. Wrong type fails.

**The thought process:** Separate schema definition from validation logic. Check each field against its rules. Collect all errors (do not stop at the first one). This is exactly how the schema validator engine works.

## Design First
Before writing code, sketch your approach in `notes.md`:
- What functions or classes do you need?
- What data structures will you use?
- What's the flow from input to output?
- What could go wrong?

## Alter it (required)
1. What additional validation rule would make the schema more useful? Implement it.
2. How could the CLI be more configurable for strict vs lenient validation?
3. Write a test for your new feature.

## Break it (required)
1. Try feeding the validator data with subtle type mismatches — what slips through?
2. What happens when the schema itself contains something unexpected?
3. Test with minimal or empty input — does the tool handle it?

## Fix it (required)
1. Address the most surprising failure you found — make it produce a clear message instead.
2. Add a test for an edge case the original code misses.
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

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on Schema Validator Engine. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to validate records against a JSON schema. Can you explain how to check if a value matches an expected type dynamically?"
- "Can you explain the difference between collecting all validation errors vs stopping at the first one, and when each approach is better?"

---

| [← Prev](../README.md) | [Home](../../../README.md) | [Next →](../02-excel-input-health-check/README.md) |
|:---|:---:|---:|
