# Schema Validator Engine — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 4 / Project 01 — Schema Validator Engine.

Validates data records against a JSON schema definition.
Demonstrates: schema loading, type checking, required-field enforcement,
and structured error collection.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

# ---------- logging setup ----------

def configure_logging() -> None:
    """Set up structured logging so every validation event is traceable."""
    # WHY: The pipe-delimited layout (timestamp | level | message) makes logs
    # easy to parse with CLI tools like awk and grep, which matters when
    # debugging validation failures across thousands of records.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- schema helpers ----------

# WHY: We translate JSON schema type names ("string", "integer") into Python
# builtins so isinstance() can check values directly. This avoids scattered
# if/elif chains and makes adding new types a one-line change.
TYPE_MAP: dict[str, type] = {
    "string": str,
    "integer": int,
    "float": float,
    "boolean": bool,
    "number": (int, float),  # type: ignore[assignment]
}


def load_schema(path: Path) -> dict:
    """Load a JSON schema file that describes expected fields."""
    # WHY: Fail early with a clear message if the schema file is missing,
    # rather than letting json.loads raise a confusing error later.
    if not path.exists():
        raise FileNotFoundError(f"Schema not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_records(path: Path) -> list[dict]:
    """Load a JSON array of data records to validate."""
    if not path.exists():
        raise FileNotFoundError(f"Records file not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    # WHY: Validate the top-level structure up front. A JSON object instead
    # of an array would cause cryptic errors during iteration.
    if not isinstance(data, list):
        raise ValueError("Records file must contain a JSON array")
    return data

# ---------- validation logic ----------


def validate_record(record: dict, schema: dict) -> list[str]:
    """Validate one record against the schema, returning a list of errors.

    Checks performed:
    1. Required fields must be present and non-null.
    2. Field values must match the declared type.
    3. Numeric fields must fall within min/max bounds (if specified).
    """
    # WHY: Returning a list instead of raising exceptions lets the caller
    # decide how to handle invalid records (log, quarantine, fail, etc.).
    errors: list[str] = []
    fields_spec = schema.get("fields", {})

    for field_name, rules in fields_spec.items():
        value = record.get(field_name)

        # WHY: Check both "value is None" and "field_name not in record"
        # because a field could exist with a None value or be entirely
        # absent — both count as missing.
        if rules.get("required", False) and (value is None or field_name not in record):
            errors.append(f"missing required field '{field_name}'")
            continue  # no point checking type/range on a missing field

        if field_name not in record:
            continue  # optional and absent — that is fine

        # WHY: Look up the Python type from TYPE_MAP so we can use isinstance()
        # for a clean, extensible type check.
        expected = TYPE_MAP.get(rules.get("type", ""), None)
        if expected and not isinstance(value, expected):
            errors.append(
                f"field '{field_name}' expected {rules['type']}, "
                f"got {type(value).__name__}"
            )
            continue  # skip range check if type is wrong

        # WHY: Range checks only make sense for numeric values, so guard
        # with isinstance before comparing.
        if isinstance(value, (int, float)):
            if "min" in rules and value < rules["min"]:
                errors.append(
                    f"field '{field_name}' value {value} < min {rules['min']}"
                )
            if "max" in rules and value > rules["max"]:
                errors.append(
                    f"field '{field_name}' value {value} > max {rules['max']}"
                )

    # WHY: Flag extra fields because in data pipelines, unexpected columns
    # often signal upstream schema drift. Surfacing them early prevents
    # silent data loss or misinterpretation downstream.
    for key in record:
        if key not in fields_spec:
            errors.append(f"unexpected field '{key}'")

    return errors


def validate_all(records: list[dict], schema: dict) -> dict:
    """Validate every record and return a structured report."""
    report: dict = {"total": len(records), "valid": 0, "invalid": 0, "errors": []}

    for idx, record in enumerate(records):
        issues = validate_record(record, schema)
        if issues:
            report["invalid"] += 1
            report["errors"].append({"record_index": idx, "issues": issues})
            logging.warning("record %d invalid: %s", idx, issues)
        else:
            report["valid"] += 1

    return report

# ---------- CLI ----------


def run(schema_path: Path, records_path: Path, output_path: Path) -> dict:
    """Full validation run: load schema + records, validate, write report."""
    schema = load_schema(schema_path)
    records = load_records(records_path)
    report = validate_all(records, schema)

    # WHY: Create parent directories automatically so the user does not need
    # to manually mkdir before running the tool.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info("Validation complete — %d valid, %d invalid", report["valid"], report["invalid"])
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate records against a JSON schema")
    parser.add_argument("--schema", default="data/schema.json", help="Path to schema file")
    parser.add_argument("--input", default="data/records.json", help="Path to records file")
    parser.add_argument("--output", default="data/validation_report.json", help="Output report path")
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    report = run(Path(args.schema), Path(args.input), Path(args.output))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| `TYPE_MAP` as a module-level constant | Keeps the mapping in one place. Adding a new type (e.g., `"date"`) is a single-line change instead of editing validation logic. |
| Collect all errors per record instead of stopping at the first | Batch reporting is more useful for data pipelines — fixing one error at a time and re-running is slow when you have thousands of records. |
| Flag unexpected fields in the record | Catches upstream schema drift early. In production, a new column appearing silently can cause downstream bugs that are hard to trace. |
| Separate `load_schema` / `load_records` / `validate_record` functions | Each function has one job. You can test validation without touching the filesystem, or swap the loader for a database reader. |

## Alternative Approaches

### Using a validation library (e.g., `jsonschema` or `pydantic`)

```python
from pydantic import BaseModel, validator

class PersonRecord(BaseModel):
    name: str
    age: int
    email: str | None = None

    @validator("age")
    def age_in_range(cls, v):
        if not 0 <= v <= 150:
            raise ValueError("age out of range")
        return v
```

**Trade-off:** Libraries like `pydantic` handle nested objects, custom validators, and type coercion out of the box, but they add a dependency and hide the validation mechanics. Writing your own validator teaches you exactly how schema checking works, which matters when you need to customize behavior or debug failures.

### Using `try/except` per record instead of error lists

```python
def validate_or_raise(record, schema):
    for field, rules in schema["fields"].items():
        if rules["required"] and field not in record:
            raise ValueError(f"Missing {field}")
```

**Trade-off:** Raising exceptions is simpler to write but only reports the first error per record. The list-based approach in the main solution is better for batch data work where you want to see all problems at once.

## Common Pitfalls

1. **Forgetting that `bool` is a subclass of `int` in Python** — `isinstance(True, int)` returns `True`. If your schema has both `"boolean"` and `"integer"` types, check for `bool` first or a boolean value will pass an integer check.
2. **Checking `value is None` but not `field_name not in record`** — A field can be present with value `None` (explicit null in JSON), or entirely absent from the dict. Both are "missing" but require different checks.
3. **Mutating the input records during validation** — If you add or modify fields on the original dicts, subsequent validation passes or downstream code will see corrupted data. Always work on copies if you need to transform.
