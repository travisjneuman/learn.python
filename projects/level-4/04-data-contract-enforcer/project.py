"""Level 4 / Project 04 — Data Contract Enforcer.

Enforces column types, value ranges, required fields, and allowed values
on a dataset (CSV). A "contract" is a JSON definition describing what
each column must look like. Violations are collected and reported.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
from pathlib import Path

# ---------- logging ----------

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- contract types ----------

# A contract looks like:
# {
#   "columns": {
#     "age": {"type": "int", "required": true, "min": 0, "max": 150},
#     "status": {"type": "str", "required": true, "allowed": ["active", "inactive"]},
#     "email": {"type": "str", "required": false}
#   }
# }


def load_contract(path: Path) -> dict:
    """Load a data contract JSON file."""
    if not path.exists():
        raise FileNotFoundError(f"Contract not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv_data(path: Path) -> tuple[list[str], list[dict]]:
    """Load CSV and return (headers, list-of-row-dicts)."""
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    text = path.read_text(encoding="utf-8")
    reader = csv.DictReader(text.splitlines())
    headers = reader.fieldnames or []
    rows = list(reader)
    return headers, rows

# ---------- enforcement logic ----------


def coerce_value(raw: str, expected_type: str) -> tuple[object, str | None]:
    """Try to coerce a string value to the expected type.

    Returns (coerced_value, error_message_or_None).
    """
    if expected_type == "int":
        try:
            return int(raw), None
        except ValueError:
            return raw, f"cannot convert '{raw}' to int"

    if expected_type == "float":
        try:
            return float(raw), None
        except ValueError:
            return raw, f"cannot convert '{raw}' to float"

    if expected_type == "bool":
        if raw.lower() in ("true", "1", "yes"):
            return True, None
        if raw.lower() in ("false", "0", "no"):
            return False, None
        return raw, f"cannot convert '{raw}' to bool"

    # Default: treat as string — always succeeds.
    return raw, None


def enforce_contract(
    headers: list[str],
    rows: list[dict],
    contract: dict,
) -> dict:
    """Check every row against the contract and collect violations.

    Returns:
        {
            "total_rows": int,
            "clean_rows": int,
            "violation_count": int,
            "violations": [{"row": int, "column": str, "issue": str}],
            "missing_columns": [str],
            "extra_columns": [str]
        }
    """
    col_specs = contract.get("columns", {})
    violations: list[dict] = []

    # Check for missing/extra columns at the schema level.
    expected_cols = set(col_specs.keys())
    actual_cols = set(headers)
    missing_columns = sorted(expected_cols - actual_cols)
    extra_columns = sorted(actual_cols - expected_cols)

    clean_count = 0

    for row_idx, row in enumerate(rows, start=1):
        row_ok = True

        for col_name, rules in col_specs.items():
            raw = row.get(col_name, "")

            # Required check
            if rules.get("required", False) and (raw is None or raw.strip() == ""):
                violations.append({
                    "row": row_idx, "column": col_name,
                    "issue": "required field is empty",
                })
                row_ok = False
                continue

            if raw is None or raw.strip() == "":
                continue  # optional and empty — skip further checks

            # Type coercion check
            coerced, err = coerce_value(raw.strip(), rules.get("type", "str"))
            if err:
                violations.append({"row": row_idx, "column": col_name, "issue": err})
                row_ok = False
                continue

            # Range check (numeric)
            if isinstance(coerced, (int, float)):
                if "min" in rules and coerced < rules["min"]:
                    violations.append({
                        "row": row_idx, "column": col_name,
                        "issue": f"value {coerced} below min {rules['min']}",
                    })
                    row_ok = False
                if "max" in rules and coerced > rules["max"]:
                    violations.append({
                        "row": row_idx, "column": col_name,
                        "issue": f"value {coerced} above max {rules['max']}",
                    })
                    row_ok = False

            # Allowed-values check
            if "allowed" in rules:
                if str(coerced) not in [str(a) for a in rules["allowed"]]:
                    violations.append({
                        "row": row_idx, "column": col_name,
                        "issue": f"value '{coerced}' not in allowed set {rules['allowed']}",
                    })
                    row_ok = False

        if row_ok:
            clean_count += 1

    return {
        "total_rows": len(rows),
        "clean_rows": clean_count,
        "violation_count": len(violations),
        "violations": violations,
        "missing_columns": missing_columns,
        "extra_columns": extra_columns,
    }

# ---------- runner ----------


def run(contract_path: Path, data_path: Path, output_path: Path) -> dict:
    """Load contract + data, enforce, write report."""
    contract = load_contract(contract_path)
    headers, rows = load_csv_data(data_path)
    report = enforce_contract(headers, rows, contract)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info(
        "Enforcement complete — %d clean, %d violations",
        report["clean_rows"], report["violation_count"],
    )
    return report

# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Enforce a data contract on CSV data")
    parser.add_argument("--contract", default="data/contract.json")
    parser.add_argument("--input", default="data/sample_input.csv")
    parser.add_argument("--output", default="data/enforcement_report.json")
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    report = run(Path(args.contract), Path(args.input), Path(args.output))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
