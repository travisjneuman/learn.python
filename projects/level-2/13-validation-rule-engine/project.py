"""Level 2 project: Validation Rule Engine.

Heavily commented beginner-friendly script:
- define validation rules as data (not hard-coded logic),
- apply rules to records and collect pass/fail results,
- generate a validation report with reason codes.

Skills practiced: dict/list comprehensions, re module for patterns,
try/except, nested data structures, sorting with key, enumerate.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


# Rules are defined as data — each rule is a dict describing what to check.
# This makes the engine extensible without changing code.
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
    if isinstance(value, str) and value.strip() == "":
        return False
    return True


def check_regex(record: dict, field: str, pattern: str) -> bool:
    """Check that a field value matches a regex pattern."""
    value = record.get(field, "")
    if not isinstance(value, str):
        value = str(value)
    try:
        return bool(re.match(pattern, value))
    except re.error:
        return False


def check_range(record: dict, field: str, min_val: float, max_val: float) -> bool:
    """Check that a numeric field is within a range."""
    value = record.get(field)
    try:
        num = float(value)
        return min_val <= num <= max_val
    except (ValueError, TypeError):
        return False


def check_min_length(record: dict, field: str, min_len: int) -> bool:
    """Check that a string field has at least min_len characters."""
    value = record.get(field, "")
    return len(str(value).strip()) >= min_len


def apply_rule(record: dict, rule: dict) -> dict:
    """Apply a single validation rule to a record.

    Returns a result dict with pass/fail and the reason code.
    """
    field = rule["field"]
    rule_type = rule["type"]

    # Dispatch to the appropriate checker based on rule type.
    if rule_type == "required":
        passed = check_required(record, field)
    elif rule_type == "regex":
        passed = check_regex(record, field, rule["pattern"])
    elif rule_type == "range":
        passed = check_range(record, field, rule["min"], rule["max"])
    elif rule_type == "min_length":
        passed = check_min_length(record, field, rule["value"])
    else:
        # Unknown rule type — fail safe.
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
        "message": None if passed else rule.get("message", "Validation failed"),
    }


def validate_record(record: dict, rules: list[dict]) -> dict:
    """Apply all rules to a single record.

    Returns a dict with overall pass/fail and individual rule results.
    """
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
    """Validate a batch of records and return aggregate results.

    Uses enumerate to track record indices.
    """
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

    # Count failures by rule ID using a dict comprehension pattern.
    failure_counts: dict[str, int] = {}
    for result in all_results:
        for code in result["failure_codes"]:
            failure_counts[code] = failure_counts.get(code, 0) + 1

    # Sort by count descending — most common failures first.
    sorted_failures = dict(
        sorted(failure_counts.items(), key=lambda pair: pair[1], reverse=True)
    )

    return {
        "total_records": len(records),
        "valid_count": len(valid_records),
        "invalid_count": len(invalid_records),
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
