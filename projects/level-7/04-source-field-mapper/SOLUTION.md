# Solution: Level 7 / Project 04 - Source Field Mapper

> **STOP — Try it yourself first!**
>
> You learn by building, not by reading answers. Spend at least 30 minutes
> attempting this project before looking here.
>
> - Re-read the [README](./README.md) for requirements
> 
---

## Complete solution

```python
"""Level 7 / Project 04 — Source Field Mapper.

Maps fields between different data source schemas using configurable
mapping rules.  Supports renaming, type casting, and default values.
"""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass
from pathlib import Path


# WHY a dataclass for FieldRule? -- Makes each mapping rule explicit and
# self-documenting: source field, target field, cast type, and default.
# Much clearer than a raw dict with magic keys.
@dataclass
class FieldRule:
    source_field: str
    target_field: str
    cast: str = "str"
    default: str | None = None


def parse_rules(raw: list[dict]) -> list[FieldRule]:
    return [
        FieldRule(source_field=r["source"], target_field=r["target"],
                  cast=r.get("cast", "str"), default=r.get("default"))
        for r in raw
    ]


# WHY a cast registry dict? -- Mapping type names to callables avoids a
# long if/elif chain for type coercion.  Adding a new type means adding one
# dict entry, not modifying control flow.  This is the Strategy pattern
# applied to type conversion.
CAST_FUNCTIONS = {
    "str": str,
    "int": int,
    "float": float,
    # WHY a lambda for bool? -- Python's bool("false") is True because the
    # string is non-empty.  We need custom logic to interpret common truthy values.
    "bool": lambda v: str(v).lower() in ("true", "1", "yes"),
}


def apply_mapping(record: dict, rules: list[FieldRule]) -> dict:
    """Map one record from source schema to target schema."""
    result: dict = {}
    for rule in rules:
        raw_value = record.get(rule.source_field)

        # WHY check for None then apply default? -- The source field might
        # be missing entirely.  The default acts as a fallback so downstream
        # code always gets a value for required fields.
        if raw_value is None:
            if rule.default is not None:
                raw_value = rule.default
            else:
                continue

        cast_fn = CAST_FUNCTIONS.get(rule.cast, str)
        try:
            result[rule.target_field] = cast_fn(raw_value)
        except (ValueError, TypeError) as exc:
            # WHY log and keep the raw value? -- Crashing the whole pipeline
            # because one field has a bad type is too aggressive.  Log the
            # issue so operators can fix the data, but keep processing.
            logging.warning("cast_error field=%s value=%r cast=%s err=%s",
                            rule.source_field, raw_value, rule.cast, exc)
            result[rule.target_field] = raw_value
    return result


def map_records(records: list[dict], rules: list[FieldRule]) -> tuple[list[dict], list[str]]:
    """Apply mapping rules to all records, collecting errors."""
    mapped, errors = [], []
    for idx, rec in enumerate(records, 1):
        try:
            mapped.append(apply_mapping(rec, rules))
        except Exception as exc:
            errors.append(f"record={idx} error={exc}")
    return mapped, errors


def validate_mapped(records: list[dict], required_fields: list[str]) -> list[str]:
    """Check that all required fields are present in mapped output."""
    issues = []
    for idx, rec in enumerate(records, 1):
        for f in required_fields:
            if f not in rec:
                issues.append(f"record={idx} missing={f}")
    return issues


def run(input_path: Path, output_path: Path) -> dict:
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")
    config = json.loads(input_path.read_text(encoding="utf-8"))
    rules = parse_rules(config["rules"])
    records = config["records"]
    required = config.get("required_fields", [])

    mapped, errors = map_records(records, rules)
    validation_issues = validate_mapped(mapped, required)

    summary = {
        "input_records": len(records), "mapped_records": len(mapped),
        "mapping_errors": errors, "validation_issues": validation_issues,
        "sample_output": mapped[:5],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info("mapped %d records, %d errors", len(mapped), len(errors))
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Source Field Mapper")
    parser.add_argument("--input", default="data/sample_input.json")
    parser.add_argument("--output", default="data/output_summary.json")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    args = parse_args()
    summary = run(Path(args.input), Path(args.output))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `CAST_FUNCTIONS` registry dict | Open for extension -- add new types without modifying `apply_mapping` | `if/elif` chain inside `apply_mapping` -- works but violates open/closed |
| Custom `bool` lambda | Python's `bool("false")` returns `True`; custom logic handles common truthy/falsy strings | `json.loads()` for bools -- only handles `true`/`false`, not `1`/`yes` |
| Fallback to raw value on cast failure | One bad field should not crash the whole pipeline; log the issue for operators | Raise immediately -- stricter but too fragile for batch ETL |
| Separate `validate_mapped` step | Separates mapping (transformation) from validation (correctness check) -- single responsibility | Validate inside `apply_mapping` -- couples two concerns together |

## Alternative approaches

### Approach B: Declarative mapping with pandas

```python
import pandas as pd

def map_with_pandas(records, rules):
    df = pd.DataFrame(records)
    rename = {r.source_field: r.target_field for r in rules}
    df = df.rename(columns=rename)
    for r in rules:
        if r.cast == "int":
            df[r.target_field] = pd.to_numeric(df[r.target_field], errors="coerce")
    return df.to_dict(orient="records")
```

**Trade-off:** Pandas is faster for large datasets (vectorized operations) and has built-in type coercion. But it adds a heavy dependency and hides the mapping logic inside library calls, making it harder to debug individual records.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| `cast: "int"` on a value like `"abc"` | `ValueError` during int conversion; code falls back to raw value | Validate data before casting, or use the try/except fallback as shown |
| Source field missing and no default configured | Field is silently skipped -- the target field will not appear | Add the field to `required_fields` so `validate_mapped` catches the omission |
| Rules reference the same `target_field` twice | Second rule overwrites the first; data loss | Validate rules for duplicate target fields during `parse_rules` |
