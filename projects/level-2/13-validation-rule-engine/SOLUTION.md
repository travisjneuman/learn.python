# Validation Rule Engine — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Validation Rule Engine — complete annotated solution."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


# WHY: Rules are defined as data (list of dicts), not as hard-coded if/else
# chains. This means new validation rules can be added by editing data —
# no code changes needed. This is the "data-driven design" pattern.
DEFAULT_RULES: list[dict] = [
    {
        "id": "R001",
        "field": "email",
        "type": "regex",
        "pattern": r"^[^@]+@[^@]+\.[^@]+$",
        "message": "Invalid email format",
    },
    {
        "id": "R002",
        "field": "age",
        "type": "range",
        "min": 0,
        "max": 150,
        "message": "Age must be between 0 and 150",
    },
    {
        "id": "R003",
        "field": "name",
        "type": "required",
        "message": "Name is required",
    },
    {
        "id": "R004",
        "field": "name",
        "type": "min_length",
        "value": 2,
        "message": "Name must be at least 2 characters",
    },
]


def check_required(record: dict, field: str) -> bool:
    """Check that a field exists and is not empty."""
    value = record.get(field)
    if value is None:
        return False
    # WHY: An empty or whitespace-only string should also fail the
    # "required" check. Just checking `is not None` would let "" pass.
    if isinstance(value, str) and value.strip() == "":
        return False
    return True


def check_regex(record: dict, field: str, pattern: str) -> bool:
    """Check that a field value matches a regex pattern."""
    value = record.get(field, "")
    # WHY: Convert non-strings to strings before regex matching.
    # A numeric field value like 42 would cause re.match to crash
    # with "expected string or bytes-like object".
    if not isinstance(value, str):
        value = str(value)
    try:
        return bool(re.match(pattern, value))
    except re.error:
        # WHY: An invalid regex pattern (like "[unclosed") should not
        # crash the entire validation engine. Returning False (fail)
        # is the safe default — better to flag a record as invalid
        # than to silently skip validation.
        return False


def check_range(record: dict, field: str, min_val: float, max_val: float) -> bool:
    """Check that a numeric field is within a range."""
    value = record.get(field)
    try:
        # WHY: Convert to float to handle both int and string numeric values.
        # "25" from a CSV and 25 from JSON should both validate the same way.
        num = float(value)
        return min_val <= num <= max_val
    except (ValueError, TypeError):
        # WHY: Non-numeric values (None, "abc") cannot be range-checked.
        # Returning False means they fail validation, which is the correct
        # behavior — a non-numeric age is invalid.
        return False


def check_min_length(record: dict, field: str, min_len: int) -> bool:
    """Check that a string field has at least min_len characters."""
    value = record.get(field, "")
    # WHY: Strip before measuring length so " A " (3 chars with spaces)
    # is correctly measured as 1 meaningful character.
    return len(str(value).strip()) >= min_len


def apply_rule(record: dict, rule: dict) -> dict:
    """Apply a single validation rule to a record."""
    field = rule["field"]
    rule_type = rule["type"]

    # WHY: This dispatch pattern maps rule types to checker functions.
    # Each rule type has its own validation logic, selected at runtime
    # by the "type" field in the rule dict.
    if rule_type == "required":
        passed = check_required(record, field)
    elif rule_type == "regex":
        passed = check_regex(record, field, rule["pattern"])
    elif rule_type == "range":
        passed = check_range(record, field, rule["min"], rule["max"])
    elif rule_type == "min_length":
        passed = check_min_length(record, field, rule["value"])
    else:
        return {
            "rule_id": rule["id"],
            "field": field,
            "passed": False,
            "message": f"Unknown rule type: {rule_type}",
        }

    return {
        "rule_id": rule["id"],
        "field": field,
        "passed": passed,
        # WHY: Only include the failure message when validation fails.
        # None when passed keeps the output clean.
        "message": None if passed else rule.get("message", "Validation failed"),
    }


def validate_record(record: dict, rules: list[dict]) -> dict:
    """Apply all rules to a single record."""
    # WHY: List comprehension applies every rule and collects all results.
    # This means a record can fail multiple rules at once — the user sees
    # all problems, not just the first one.
    results = [apply_rule(record, rule) for rule in rules]
    failures = [r for r in results if not r["passed"]]

    return {
        "valid": len(failures) == 0,
        "passed_count": len(results) - len(failures),
        "failed_count": len(failures),
        "results": results,
        "failure_codes": [r["rule_id"] for r in failures],
    }


def validate_batch(
    records: list[dict], rules: list[dict]
) -> dict:
    """Validate a batch of records and return aggregate results."""
    all_results: list[dict] = []
    valid_records: list[dict] = []
    invalid_records: list[dict] = []

    for idx, record in enumerate(records):
        result = validate_record(record, rules)
        result["record_index"] = idx
        all_results.append(result)

        if result["valid"]:
            valid_records.append(record)
        else:
            invalid_records.append({**record, "_failures": result["failure_codes"]})

    # WHY: Count failures by rule ID to identify the most common problems.
    # This is the same accumulator pattern used in error counting — dict.get
    # with default 0 avoids the "key not in dict" check.
    failure_counts: dict[str, int] = {}
    for result in all_results:
        for code in result["failure_codes"]:
            failure_counts[code] = failure_counts.get(code, 0) + 1

    sorted_failures = dict(
        sorted(failure_counts.items(), key=lambda pair: pair[1], reverse=True)
    )

    return {
        "total_records": len(records),
        "valid_count": len(valid_records),
        "invalid_count": len(invalid_records),
        # WHY: Guard against empty records to prevent ZeroDivisionError.
        "pass_rate": round(len(valid_records) / len(records) * 100, 1) if records else 0,
        "failure_counts": sorted_failures,
        "valid_records": valid_records,
        "invalid_records": invalid_records,
    }


def load_rules(path: Path) -> list[dict]:
    """Load validation rules from a JSON file."""
    if not path.exists():
        return DEFAULT_RULES
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("rules", DEFAULT_RULES)
    except (json.JSONDecodeError, OSError):
        return DEFAULT_RULES


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Validation rule engine")
    parser.add_argument("input", help="Path to JSON records file")
    parser.add_argument("--rules", default=None, help="Path to rules JSON file")
    parser.add_argument("--verbose", action="store_true", help="Show per-record details")
    return parser.parse_args()


def main() -> None:
    """Entry point: load records, apply rules, report results."""
    args = parse_args()
    path = Path(args.input)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    records = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        records = [records]

    rules = load_rules(Path(args.rules)) if args.rules else DEFAULT_RULES

    result = validate_batch(records, rules)

    print(f"Validated {result['total_records']} records: "
          f"{result['valid_count']} valid, {result['invalid_count']} invalid "
          f"({result['pass_rate']}% pass rate)")

    if result["failure_counts"]:
        print("\nMost common failures:")
        for code, count in result["failure_counts"].items():
            print(f"  {code}: {count} occurrences")

    if args.verbose and result["invalid_records"]:
        print("\nInvalid records:")
        for rec in result["invalid_records"]:
            print(f"  {rec}")


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Rules as data (list of dicts) | Data-driven validation is extensible. Adding a new rule means adding a dict to the list, not writing new if/else logic. This is how production systems like JSON Schema and database constraints work. |
| Dispatch pattern in `apply_rule` | The `if rule_type == ...` block maps rule types to checker functions. This is a simple Strategy pattern — the behavior changes based on the rule's "type" field without the caller needing to know which checker runs. |
| All rules checked per record | Reporting all failures at once (not stopping at the first) gives users a complete picture. Fixing one problem at a time and re-validating is frustrating when there are multiple issues. |
| Failure counts sorted by frequency | The most common failures appear first, telling the data provider where to focus their fixes. If 80% of failures are bad emails, fixing the email column has the biggest impact. |
| Separate checker functions | Each `check_*` function handles one rule type. This makes them independently testable and composable. Adding a new rule type means writing one new function and one new `elif` branch. |

## Alternative Approaches

### Using a dict of checker functions

```python
CHECKERS = {
    "required": lambda rec, rule: check_required(rec, rule["field"]),
    "regex": lambda rec, rule: check_regex(rec, rule["field"], rule["pattern"]),
    "range": lambda rec, rule: check_range(rec, rule["field"], rule["min"], rule["max"]),
}

def apply_rule_dispatch(record, rule):
    checker = CHECKERS.get(rule["type"])
    if checker is None:
        return {"passed": False, "message": f"Unknown rule type: {rule['type']}"}
    passed = checker(record, rule)
    return {"passed": passed, "message": None if passed else rule.get("message")}
```

A dispatch dict eliminates the if/elif chain entirely. Adding a new rule type means adding one entry to the dict. This is cleaner for many rule types but less explicit for beginners learning the dispatch concept.

### Using Pydantic for validation

```python
from pydantic import BaseModel, EmailStr, validator

class PersonRecord(BaseModel):
    name: str
    email: EmailStr
    age: int

    @validator("age")
    def age_must_be_valid(cls, v):
        if not 0 <= v <= 150:
            raise ValueError("Age must be between 0 and 150")
        return v
```

Pydantic provides type validation, custom validators, and automatic error messages. It is the standard for API input validation in modern Python. The manual approach here teaches the underlying concepts of rule evaluation and dispatch.

## Common Pitfalls

1. **Invalid regex patterns crashing the engine** — A rule with `"pattern": "[unclosed"` would cause `re.match` to raise `re.error`. The `try/except re.error` in `check_regex` prevents one bad rule from crashing validation for all records.

2. **Division by zero in pass rate** — If the records list is empty, `len(valid) / len(records)` divides by zero. The `if records else 0` guard handles this, but it is easy to forget when computing percentages.

3. **Type mismatch in range checks** — A JSON record might have `"age": "twenty-five"` as a string. Calling `float("twenty-five")` raises ValueError. The `try/except` in `check_range` catches this, but without it the entire batch validation would crash on one bad record.
