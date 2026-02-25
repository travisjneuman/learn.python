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
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- schema helpers ----------

# Supported JSON-schema-like type strings mapped to Python builtins.
TYPE_MAP: dict[str, type] = {
    "string": str,
    "integer": int,
    "float": float,
    "boolean": bool,
    "number": (int, float),  # type: ignore[assignment]
}


def load_schema(path: Path) -> dict:
    """Load a JSON schema file that describes expected fields.

    Schema format example:
    {
      "fields": {
        "name":  {"type": "string",  "required": true},
        "age":   {"type": "integer", "required": true, "min": 0, "max": 150},
        "email": {"type": "string",  "required": false}
      }
    }
    """
    if not path.exists():
        raise FileNotFoundError(f"Schema not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_records(path: Path) -> list[dict]:
    """Load a JSON array of data records to validate."""
    if not path.exists():
        raise FileNotFoundError(f"Records file not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
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
    errors: list[str] = []
    fields_spec = schema.get("fields", {})

    # Check every field declared in the schema.
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

        # --- range check (numeric fields) ---
        if isinstance(value, (int, float)):
            if "min" in rules and value < rules["min"]:
                errors.append(
                    f"field '{field_name}' value {value} < min {rules['min']}"
                )
            if "max" in rules and value > rules["max"]:
                errors.append(
                    f"field '{field_name}' value {value} > max {rules['max']}"
                )

    # Warn about unexpected extra fields (not an error, just informational).
    for key in record:
        if key not in fields_spec:
            errors.append(f"unexpected field '{key}'")

    return errors


def validate_all(records: list[dict], schema: dict) -> dict:
    """Validate every record and return a structured report.

    Returns:
        {
            "total": int,
            "valid": int,
            "invalid": int,
            "errors": [{"record_index": int, "issues": [str]}]
        }
    """
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
