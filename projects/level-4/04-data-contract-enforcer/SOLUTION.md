# Data Contract Enforcer — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
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
    # WHY: CSV values are always strings. To enforce "age must be an integer
    # between 0 and 150," we must convert to int first so we can do numeric
    # comparisons. Without coercion, "42" < 150 is a string comparison.
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
        # WHY: Accept common boolean representations because real-world
        # data uses "yes"/"no", "1"/"0", "true"/"false" interchangeably.
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
    """Check every row against the contract and collect violations."""
    col_specs = contract.get("columns", {})
    violations: list[dict] = []

    # WHY: Check columns at the schema level first. If the CSV is missing
    # an entire column, per-row checks would generate misleading errors
    # for every single row. Catching it once here is cleaner and faster.
    expected_cols = set(col_specs.keys())
    actual_cols = set(headers)
    missing_columns = sorted(expected_cols - actual_cols)
    extra_columns = sorted(actual_cols - expected_cols)

    clean_count = 0

    for row_idx, row in enumerate(rows, start=1):
        row_ok = True

        for col_name, rules in col_specs.items():
            raw = row.get(col_name, "")

            # WHY: Check both None and empty string because DictReader
            # returns None for missing columns and "" for empty fields.
            if rules.get("required", False) and (raw is None or raw.strip() == ""):
                violations.append({
                    "row": row_idx, "column": col_name,
                    "issue": "required field is empty",
                })
                row_ok = False
                continue

            if raw is None or raw.strip() == "":
                continue  # optional and empty — skip further checks

            # WHY: Coerce before range/allowed checks so we compare actual
            # typed values, not raw strings.
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

            # WHY: Convert both sides to strings for allowed-values comparison
            # because the contract might list integers while the coerced value
            # is an int — "active" == "active" but 1 != "1" without str().
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
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Coerce CSV strings to typed values before checking constraints | CSV fields are always strings. You cannot compare `"42" < 150` meaningfully — you need the actual integer `42`. Coercion makes range and type checks correct. |
| Report missing/extra columns separately from row violations | A missing column is a structural problem (schema drift), not a per-row problem. Reporting it once at the top level is cleaner than generating N identical violations. |
| Collect violations per-row with column name and issue text | Granular violation reporting lets humans or tools pinpoint exactly which cell in which row failed which rule, making fixes targeted. |
| Accept multiple boolean representations ("true", "1", "yes") | Real-world data comes from many sources. Being flexible on boolean input reduces friction without sacrificing correctness. |

## Alternative Approaches

### Using a contract as a Python dataclass

```python
from dataclasses import dataclass

@dataclass
class ColumnRule:
    name: str
    col_type: str = "str"
    required: bool = False
    min_val: float | None = None
    max_val: float | None = None
    allowed: list[str] | None = None

def enforce_typed(row: dict, rules: list[ColumnRule]) -> list[str]:
    errors = []
    for rule in rules:
        val = row.get(rule.name, "")
        if rule.required and not val.strip():
            errors.append(f"{rule.name}: required")
    return errors
```

**Trade-off:** Dataclasses give you type safety and IDE autocompletion for the contract definition, but the contract must be defined in Python code rather than a JSON file. The JSON approach is better when non-programmers need to define or update contracts.

## Common Pitfalls

1. **Comparing coerced values with string-typed allowed lists** — If the contract says `"allowed": ["active", "inactive"]` and the coerced value is a string, the comparison works. But if allowed lists contain integers (like `[1, 2, 3]`) and the coerced value is `int`, you need to normalize both sides with `str()` or the check will miss matches.
2. **Forgetting that `DictReader` returns `None` for missing columns** — If a column exists in the contract but not in the CSV headers, `row.get("missing_col")` returns `None`, not `""`. You must handle both.
3. **Not validating the contract itself** — A contract with `"min": 100, "max": 50` is contradictory and will flag every value as a violation. Adding contract self-validation catches this before enforcement begins.
