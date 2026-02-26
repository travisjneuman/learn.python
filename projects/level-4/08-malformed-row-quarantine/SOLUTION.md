# Malformed Row Quarantine — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 4 / Project 08 — Malformed Row Quarantine.

Reads a data file line-by-line, applies multiple validation rules to each
row, and separates valid rows from malformed ones. Each quarantined row
gets a reason annotation explaining exactly why it was rejected.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

# ---------- logging ----------

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- validation rules ----------

# WHY: Each rule is a standalone function. This pattern makes rules
# composable, testable in isolation, and easy to extend — adding a new
# check is just writing one small function and calling it in the engine.


def rule_column_count(fields: list[str], expected: int) -> str | None:
    """Every row must have exactly the expected number of columns."""
    if len(fields) != expected:
        return f"expected {expected} columns, got {len(fields)}"
    return None


def rule_no_empty_required(fields: list[str], required_indexes: list[int]) -> str | None:
    """Specified column indexes must not be blank."""
    # WHY: Guard with `i < len(fields)` to avoid IndexError on short rows.
    # If the row is too short, the column_count rule will catch it separately.
    missing = [i for i in required_indexes if i < len(fields) and not fields[i].strip()]
    if missing:
        return f"empty required column(s) at index(es): {missing}"
    return None


def rule_no_control_chars(fields: list[str]) -> str | None:
    """Reject rows containing control characters (except tab/newline).

    WHY: Tabs appear in TSV data and newlines can appear inside quoted CSV
    fields. Other control characters (like null bytes or bell) usually
    indicate file corruption.
    """
    for i, field in enumerate(fields):
        for ch in field:
            if ord(ch) < 32 and ch not in ("\t", "\n", "\r"):
                return f"control character in column {i}: ord={ord(ch)}"
    return None


def rule_max_field_length(fields: list[str], max_len: int = 500) -> str | None:
    """Reject rows where any single field exceeds max_len characters."""
    # WHY: Unusually long fields often indicate parse errors (e.g., a missing
    # delimiter caused two fields to merge) or data injection. A 500-char
    # default catches obvious problems without rejecting legitimate text.
    for i, field in enumerate(fields):
        if len(field) > max_len:
            return f"column {i} exceeds max length {max_len} ({len(field)} chars)"
    return None

# ---------- quarantine engine ----------


def quarantine_rows(
    lines: list[str],
    delimiter: str = ",",
    required_indexes: list[int] | None = None,
) -> dict:
    """Process lines and separate valid from malformed."""
    if not lines:
        return {"valid": [], "quarantined": []}

    # WHY: Use simple split() instead of csv.reader because this project
    # focuses on line-level validation. The csv module handles quoting but
    # masks structural problems we want to catch.
    header_fields = lines[0].split(delimiter)
    expected_cols = len(header_fields)
    required = required_indexes or []

    valid: list[dict] = []
    quarantined: list[dict] = []

    for idx, line in enumerate(lines[1:], start=2):
        fields = line.split(delimiter)
        reasons: list[str] = []

        # WHY: Apply ALL rules to every row and collect ALL reasons.
        # Stopping at the first failure would force the user to fix one
        # problem, re-run, find the next — a slow feedback loop.
        err = rule_column_count(fields, expected_cols)
        if err:
            reasons.append(err)

        err = rule_no_empty_required(fields, required)
        if err:
            reasons.append(err)

        err = rule_no_control_chars(fields)
        if err:
            reasons.append(err)

        err = rule_max_field_length(fields)
        if err:
            reasons.append(err)

        if reasons:
            quarantined.append({"row": idx, "raw": line, "reasons": reasons})
            logging.warning("Row %d quarantined: %s", idx, reasons)
        else:
            valid.append({"row": idx, "fields": fields})

    return {"valid": valid, "quarantined": quarantined}

# ---------- runner ----------


def run(input_path: Path, output_dir: Path, required_indexes: list[int] | None = None) -> dict:
    """Full quarantine run: read file, separate rows, write outputs."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    lines = input_path.read_text(encoding="utf-8").splitlines()
    result = quarantine_rows(lines, required_indexes=required_indexes)

    output_dir.mkdir(parents=True, exist_ok=True)

    # WHY: Write valid rows back to a text file (preserving original format)
    # so they can be fed directly into the next pipeline stage.
    valid_path = output_dir / "valid_rows.txt"
    valid_path.write_text(
        "\n".join(lines[0:1] + [",".join(r["fields"]) for r in result["valid"]]),
        encoding="utf-8",
    )

    # WHY: Quarantined rows use JSON (not CSV) because the "reasons" field
    # is a list of strings. JSON naturally represents nested data structures
    # that would be awkward to flatten into CSV columns.
    quarantine_path = output_dir / "quarantined_rows.json"
    quarantine_path.write_text(
        json.dumps(result["quarantined"], indent=2), encoding="utf-8",
    )

    summary = {
        "total_data_rows": len(lines) - 1 if lines else 0,
        "valid": len(result["valid"]),
        "quarantined": len(result["quarantined"]),
    }

    report_path = output_dir / "quarantine_report.json"
    report_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info("Quarantine complete: %d valid, %d quarantined", summary["valid"], summary["quarantined"])
    return summary

# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Quarantine malformed rows with reason tracking")
    parser.add_argument("--input", default="data/sample_input.csv")
    parser.add_argument("--output-dir", default="data/output")
    parser.add_argument("--required", default="0,1", help="Comma-separated required column indexes")
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    required = [int(i) for i in args.required.split(",") if i.strip()]
    summary = run(Path(args.input), Path(args.output_dir), required_indexes=required)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Individual rule functions instead of one big `if/else` block | Each rule is independently testable, reusable, and extensible. Adding a new check is just writing one function — no risk of breaking existing rules. |
| Collect ALL reasons per row instead of stopping at the first | Batch error reporting gives users a complete picture. Fixing one error, re-running, finding the next — this cycle is slow. Showing all problems at once is faster. |
| Quarantine file uses JSON instead of CSV | Reasons are a list of strings per row — a nested structure. JSON handles nesting naturally, while CSV would require awkward flattening or serialization. |
| Use `str.split()` instead of `csv.reader` | Intentional choice for this project: we want to detect structural problems (wrong column count) that `csv.reader` might silently handle through quoting rules. |

## Alternative Approaches

### Using a rule registry for dynamic rule loading

```python
RULES = []

def register_rule(func):
    RULES.append(func)
    return func

@register_rule
def rule_column_count(fields, expected):
    if len(fields) != expected:
        return f"expected {expected} columns, got {len(fields)}"

def apply_all_rules(fields, expected, required):
    reasons = []
    for rule in RULES:
        err = rule(fields, expected)
        if err:
            reasons.append(err)
    return reasons
```

**Trade-off:** A decorator-based registry makes rules auto-discoverable and avoids manually listing each rule call in the engine. However, rules have different signatures (some need `expected_cols`, some need `required_indexes`), which makes a uniform registry harder. The explicit call pattern in the main solution is clearer about what data each rule needs.

## Common Pitfalls

1. **Confusing "too few columns" with "all fields empty"** — A row with 2 fields out of 5 expected fails the column count rule. A row with 5 empty fields passes the column count rule but fails the empty-required rule. These are different problems with different fixes.
2. **Forgetting to handle the header-only file** — A file with one line (just headers) has zero data rows. `lines[1:]` is empty, so the loop runs zero times, which is correct — but the summary must report `total_data_rows: 0`, not crash.
3. **Not preserving the raw line for quarantined rows** — If you only store the split fields, information about the original delimiter and quoting is lost. Preserving the raw line text lets humans see exactly what the source data looked like.
