# Schema Validator Engine — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 30 minutes attempting it independently.

## Thinking Process

Schema validation is the gatekeeper of data pipelines. Before you process, transform, or analyze data, you need to verify it conforms to an expected structure. This project asks you to build that gatekeeper: given a schema (what fields should exist, what types they should be, what ranges are valid) and a set of records, produce a report listing every violation.

The critical design decision is: **collect all errors, do not stop at the first one.** If a record has three problems, the user wants to see all three at once so they can fix them in one pass. This is different from how Python exceptions normally work (one exception, execution stops). Here, you accumulate errors into a list and return that list.

Think about the architecture in three layers. First, the **schema** defines the contract (what is expected). Second, the **validator** checks records against that contract. Third, the **reporter** presents the results. By separating these concerns, you can change the schema format, add new validation rules, or change the output format independently.

## Step 1: Define the Type Map

**What to do:** Create a module-level constant that maps JSON schema type names to Python types.

**Why:** The schema says `"type": "string"` but Python needs `isinstance(value, str)`. The type map bridges this gap. Making it a constant (rather than inline logic) means adding a new type is a one-line change.

```python
TYPE_MAP: dict[str, type] = {
    "string": str,
    "integer": int,
    "float": float,
    "boolean": bool,
    "number": (int, float),  # accepts either int or float
}
```

**Predict:** Why is `"number"` mapped to a tuple `(int, float)` instead of a single type? What kind of JSON values would match `"number"` but not `"integer"`?

## Step 2: Load the Schema and Records

**What to do:** Write two loader functions -- one for the schema JSON, one for the records JSON.

**Why:** Keeping loaders separate means you can reuse them independently. The records loader also validates that the file contains a JSON array (not a single object), which is a common data format mistake.

```python
def load_schema(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Schema not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def load_records(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Records file not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Records file must contain a JSON array")
    return data
```

**Predict:** What happens if the JSON file is malformed (invalid JSON syntax)? Which line would raise the error, and what kind of error would it be?

## Step 3: Validate a Single Record

**What to do:** Write `validate_record()` that checks one record against the schema and returns a list of error strings.

**Why:** This is the core of the entire project. It performs three checks in sequence: required fields, type correctness, and numeric range bounds. Each check adds to an `errors` list rather than raising exceptions.

```python
def validate_record(record: dict, schema: dict) -> list[str]:
    errors: list[str] = []
    fields_spec = schema.get("fields", {})

    for field_name, rules in fields_spec.items():
        value = record.get(field_name)

        # --- required check ---
        if rules.get("required", False) and (value is None or field_name not in record):
            errors.append(f"missing required field '{field_name}'")
            continue  # no point checking type/range on a missing field

        if field_name not in record:
            continue  # optional and absent — that is fine

        # --- type check ---
        expected = TYPE_MAP.get(rules.get("type", ""), None)
        if expected and not isinstance(value, expected):
            errors.append(
                f"field '{field_name}' expected {rules['type']}, "
                f"got {type(value).__name__}"
            )
            continue  # skip range check if type is wrong

        # --- range check ---
        if isinstance(value, (int, float)):
            if "min" in rules and value < rules["min"]:
                errors.append(f"field '{field_name}' value {value} < min {rules['min']}")
            if "max" in rules and value > rules["max"]:
                errors.append(f"field '{field_name}' value {value} > max {rules['max']}")

    # Flag unexpected fields
    for key in record:
        if key not in fields_spec:
            errors.append(f"unexpected field '{key}'")

    return errors
```

Three design choices to notice:

- The `continue` after each check type means a missing field does not also trigger a type error, and a wrong type does not also trigger a range error. Each record gets the most relevant error for each field.
- **Unexpected field detection** at the end catches schema drift -- when upstream systems add columns your pipeline does not expect.
- The function returns a plain list of strings, letting the caller decide how to handle errors (log them, quarantine the record, abort the run).

**Predict:** If a record has `"age": "twenty-five"`, which check catches it -- required, type, or range? What error message is produced?

## Step 4: Validate All Records

**What to do:** Write `validate_all()` that iterates records, validates each one, and builds a structured report.

**Why:** The batch wrapper adds the record index to each error, so when you see "record 5 invalid: missing required field 'email'," you know exactly which row to fix.

```python
def validate_all(records: list[dict], schema: dict) -> dict:
    report = {"total": len(records), "valid": 0, "invalid": 0, "errors": []}

    for idx, record in enumerate(records):
        issues = validate_record(record, schema)
        if issues:
            report["invalid"] += 1
            report["errors"].append({"record_index": idx, "issues": issues})
            logging.warning("record %d invalid: %s", idx, issues)
        else:
            report["valid"] += 1

    return report
```

**Predict:** If you have 6 records and 4 are invalid, what does the report look like? How many entries are in the `"errors"` list?

## Step 5: Run the Full Pipeline and Write Output

**What to do:** Write a `run()` function that loads schema and records, validates, and writes the report to a JSON file.

**Why:** This orchestrator ties everything together and handles file I/O. Notice `output_path.parent.mkdir(parents=True, exist_ok=True)` -- this creates the output directory if it does not exist, which prevents a crash when running for the first time.

```python
def run(schema_path: Path, records_path: Path, output_path: Path) -> dict:
    schema = load_schema(schema_path)
    records = load_records(records_path)
    report = validate_all(records, schema)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info("Validation complete — %d valid, %d invalid",
                 report["valid"], report["invalid"])
    return report
```

**Predict:** Why does the function both write the report to a file AND return it as a dict? What are the use cases for each?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Stopping at the first error per record | Using `return` instead of `continue` | Accumulate all errors in a list, then return the list |
| Not handling `None` values for required fields | A field can exist with `None` as its value | Check both `value is None` and `field_name not in record` |
| Forgetting to check for unexpected fields | Only checking declared fields | Loop over `record.keys()` and flag any not in the schema |
| `isinstance(True, int)` returns `True` | In Python, `bool` is a subclass of `int` | Check `bool` before `int` in TYPE_MAP, or handle explicitly |

## Testing Your Solution

```bash
pytest -q
```

Expected output:
```text
6 passed
```

Test from the command line:

```bash
python project.py --schema data/schema.json --input data/records.json --output data/validation_report.json
```

Then inspect `data/validation_report.json` to see the structured error report.

## What You Learned

- **Schema-driven validation** separates the "what is valid" definition (the schema) from the "how to validate" logic (the code). This means changing requirements is a config change, not a code change.
- **Accumulating errors instead of failing fast** gives users a complete picture of what is wrong. This pattern is standard in form validation, data pipelines, and API request validation.
- **The TYPE_MAP pattern** (a dictionary mapping names to types) replaces scattered `if/elif` chains. Adding support for a new type is a one-line addition to the map.
