# Level 2 Mini Capstone — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 2 Mini Capstone: Data Pipeline — complete annotated solution.

This capstone combines skills from all Level 2 projects:
- Stage 1 (Load):     CSV parsing (project 12)
- Stage 2 (Clean):    Data cleaning (project 03)
- Stage 3 (Validate): Rule-based validation (project 13)
- Stage 4 (Analyse):  Anomaly detection (project 14)
- Stage 5 (Report):   Text report generation (project 05)
"""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path


# --- Stage 1: Load and Parse ---

def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    """Load a CSV file into headers and record dicts."""
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    # WHY: Strip and filter in one pass. Comment lines (#) are skipped
    # to allow annotated data files.
    lines = [l.strip() for l in lines if l.strip() and not l.startswith("#")]

    if not lines:
        return [], []

    headers = [h.strip() for h in lines[0].split(",")]
    records = []

    for line in lines[1:]:
        values = [v.strip() for v in line.split(",")]
        # WHY: Pad short rows so zip does not silently drop columns.
        while len(values) < len(headers):
            values.append("")
        records.append(dict(zip(headers, values)))

    return headers, records


# --- Stage 2: Clean ---

def clean_record(record: dict[str, str]) -> dict[str, str]:
    """Clean a single record: strip whitespace, normalise emails."""
    cleaned = {}
    for key, value in record.items():
        value = value.strip()
        # WHY: Email normalisation to lowercase ensures "Alice@Test.com"
        # and "alice@test.com" are treated as the same address.
        if "email" in key.lower():
            value = value.lower()
        cleaned[key] = value
    return cleaned


def clean_records(records: list[dict[str, str]]) -> list[dict[str, str]]:
    """Clean all records."""
    # WHY: List comprehension applies clean_record to every record.
    # This is more concise and Pythonic than a for loop with append.
    return [clean_record(r) for r in records]


# --- Stage 3: Validate ---

def validate_record(record: dict[str, str], rules: dict) -> dict:
    """Validate a single record against rules."""
    errors: list[str] = []

    # WHY: Each rule type is checked independently. A record can fail
    # multiple rules at once — the user sees all problems.
    for field in rules.get("required", []):
        if not record.get(field, "").strip():
            errors.append(f"Missing required field: {field}")

    email_field = rules.get("email_field")
    if email_field and record.get(email_field):
        # WHY: This regex checks for basic email structure: something@something.something.
        # It is not RFC-compliant but catches most obvious formatting errors.
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", record[email_field]):
            errors.append(f"Invalid email: {record[email_field]}")

    for field, bounds in rules.get("ranges", {}).items():
        value = record.get(field, "")
        try:
            num = float(value)
            if num < bounds["min"] or num > bounds["max"]:
                errors.append(f"{field} out of range: {num}")
        except (ValueError, TypeError):
            # WHY: Only flag non-empty values as errors. An empty string
            # might be handled by the "required" rule instead.
            if value:
                errors.append(f"{field} is not numeric: {value}")

    return {"valid": len(errors) == 0, "errors": errors}


def validate_batch(records: list[dict], rules: dict) -> tuple[list[dict], list[dict]]:
    """Split records into valid and invalid batches."""
    valid = []
    invalid = []

    for idx, record in enumerate(records):
        result = validate_record(record, rules)
        if result["valid"]:
            valid.append(record)
        else:
            # WHY: Attach errors and original index to invalid records
            # so the report can show exactly which row failed and why.
            invalid.append({**record, "_errors": result["errors"], "_index": idx})

    return valid, invalid


# --- Stage 4: Analyse (anomaly detection) ---

def detect_anomalies(
    records: list[dict], field: str, threshold: float = 2.0
) -> list[dict]:
    """Detect anomalies in a numeric field using z-score."""
    # WHY: Extract numeric values with try/except to handle mixed data.
    # Non-numeric values in the field are silently skipped.
    values: list[float] = []
    for r in records:
        try:
            values.append(float(r.get(field, "")))
        except (ValueError, TypeError):
            pass

    # WHY: Z-score requires at least 2 values (for std_dev). With fewer,
    # the concept of "deviation from normal" is meaningless.
    if len(values) < 2:
        return []

    avg = sum(values) / len(values)
    variance = sum((x - avg) ** 2 for x in values) / len(values)
    sd = math.sqrt(variance) if variance > 0 else 0

    # WHY: If std_dev is 0, all values are identical. Nothing can be anomalous.
    if sd == 0:
        return []

    anomalies = []
    for idx, record in enumerate(records):
        try:
            val = float(record.get(field, ""))
            z = (val - avg) / sd
            if abs(z) > threshold:
                anomalies.append({
                    "index": idx,
                    "value": val,
                    "z_score": round(z, 3),
                    "record": record,
                })
        except (ValueError, TypeError):
            pass

    return anomalies


# --- Stage 5: Report ---

def generate_report(
    total: int,
    valid: list[dict],
    invalid: list[dict],
    anomalies: list[dict],
    numeric_field: str,
) -> str:
    """Generate a formatted pipeline report."""
    lines = [
        "=" * 60,
        "  DATA PIPELINE REPORT",
        "=" * 60,
        "",
        f"Records loaded:    {total}",
        f"Records valid:     {len(valid)}",
        f"Records invalid:   {len(invalid)}",
        f"Anomalies found:   {len(anomalies)}",
        # WHY: Guard against total=0 to prevent ZeroDivisionError.
        f"Pass rate:         {round(len(valid) / total * 100, 1) if total else 0}%",
        "",
    ]

    if invalid:
        lines.append("--- Validation Failures ---")
        # WHY: Show only the first 5 failures to keep the report readable.
        # A "... and N more" message indicates when there are additional failures.
        for rec in invalid[:5]:
            lines.append(f"  Row {rec['_index']}: {rec['_errors']}")
        if len(invalid) > 5:
            lines.append(f"  ... and {len(invalid) - 5} more")
        lines.append("")

    if anomalies:
        lines.append(f"--- Anomalies in '{numeric_field}' ---")
        for a in anomalies:
            lines.append(f"  Row {a['index']}: value={a['value']}, z={a['z_score']}")
        lines.append("")

    # WHY: Summary statistics on valid records give context for the data quality.
    values = []
    for r in valid:
        try:
            values.append(float(r.get(numeric_field, "")))
        except (ValueError, TypeError):
            pass

    if values:
        lines.append(f"--- Statistics for '{numeric_field}' (valid records) ---")
        lines.append(f"  Count:  {len(values)}")
        lines.append(f"  Mean:   {round(sum(values) / len(values), 2)}")
        lines.append(f"  Min:    {min(values)}")
        lines.append(f"  Max:    {max(values)}")

    lines.append("")
    lines.append("=" * 60)
    return "\n".join(lines)


# --- Pipeline Runner ---

def run_pipeline(
    input_path: Path,
    rules: dict,
    numeric_field: str,
    anomaly_threshold: float = 2.0,
) -> dict:
    """Execute the full pipeline: load -> clean -> validate -> analyse -> report.

    Each stage feeds its output into the next, forming a data pipeline.
    """
    # WHY: Each stage is a separate function call. This makes it easy to
    # insert new stages (like deduplication) between existing ones without
    # modifying the stage functions themselves.
    headers, raw_records = load_csv(input_path)
    cleaned = clean_records(raw_records)
    valid, invalid = validate_batch(cleaned, rules)
    anomalies = detect_anomalies(valid, numeric_field, threshold=anomaly_threshold)

    report = generate_report(
        total=len(raw_records),
        valid=valid,
        invalid=invalid,
        anomalies=anomalies,
        numeric_field=numeric_field,
    )

    return {
        "headers": headers,
        "total": len(raw_records),
        "valid_count": len(valid),
        "invalid_count": len(invalid),
        "anomaly_count": len(anomalies),
        "report": report,
        "valid_records": valid,
        "invalid_records": invalid,
        "anomalies": anomalies,
    }


# WHY: Default rules are defined as a module-level constant so they can be
# used without loading an external file. Each rule type maps to a concept
# from earlier projects.
DEFAULT_RULES: dict = {
    "required": ["name", "email"],
    "email_field": "email",
    "ranges": {
        "age": {"min": 0, "max": 150},
        "salary": {"min": 0, "max": 1000000},
    },
}


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Level 2 capstone data pipeline")
    parser.add_argument("input", help="Path to CSV data file")
    parser.add_argument(
        "--numeric-field", default="salary", help="Numeric field for anomaly detection"
    )
    parser.add_argument(
        "--threshold", type=float, default=2.0, help="Z-score anomaly threshold"
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    return parser.parse_args()


def main() -> None:
    """Entry point: run the full data pipeline."""
    args = parse_args()
    result = run_pipeline(
        input_path=Path(args.input),
        rules=DEFAULT_RULES,
        numeric_field=args.numeric_field,
        anomaly_threshold=args.threshold,
    )

    if args.json:
        # WHY: Remove the text report from JSON output because it is a
        # formatted string, not structured data. JSON consumers want the
        # raw numbers, not a human-readable report.
        output = {k: v for k, v in result.items() if k != "report"}
        print(json.dumps(output, indent=2))
    else:
        print(result["report"])


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Five separate stages as functions | Each stage (load, clean, validate, analyse, report) is a standalone function with clear inputs and outputs. This follows the Unix philosophy: do one thing well, then compose. Adding a deduplication stage means inserting one function call between existing stages. |
| Anomaly detection runs on valid records only | Invalid records (missing fields, bad formats) would corrupt statistical calculations. Filtering them out before analysis ensures the statistics are meaningful. |
| Default rules as a module-level constant | Rules defined as data (not code) can be loaded from a JSON file, modified at runtime, or replaced for different use cases. This is the same data-driven pattern from project 13. |
| Pipeline returns a comprehensive result dict | Returning all artifacts (valid records, invalid records, anomalies, report text) lets callers choose what to use. A CLI prints the report; an API returns the JSON; a test checks the counts. |
| Text report with truncated failure list | Showing only the first 5 failures keeps the report scannable. The full list is available in the JSON output for programmatic analysis. |

## Alternative Approaches

### Using generator functions for pipeline stages

```python
def clean_stage(records):
    for record in records:
        yield clean_record(record)

def validate_stage(records, rules):
    for record in records:
        result = validate_record(record, rules)
        if result["valid"]:
            yield record
```

Generators process one record at a time without holding the entire dataset in memory. For million-row CSV files, this is essential to avoid running out of RAM. The list-based approach in this project is simpler and fine for datasets that fit in memory.

### Using `pandas` for the entire pipeline

```python
import pandas as pd

df = pd.read_csv("data.csv")
df["email"] = df["email"].str.lower()           # Clean
valid = df[df["name"].notna() & df["email"].str.contains("@")]  # Validate
z_scores = (valid["salary"] - valid["salary"].mean()) / valid["salary"].std()
anomalies = valid[z_scores.abs() > 2]           # Analyse
```

Pandas performs all five stages in a few lines with optimized C code. The manual approach here teaches the underlying concepts. In production data engineering, pandas (or Polars/Spark for larger datasets) is the standard choice.

## Common Pitfalls

1. **Zero records after validation** — If every record is invalid, the anomaly detection and statistics stages receive empty lists. Without guards, `sum(values) / len(values)` and `min(values)` would crash. Every stage must handle empty inputs gracefully.

2. **Numeric field does not exist** — If `--numeric-field` specifies a column that is not in the CSV, `detect_anomalies` gets no values and returns an empty list. This is correct behavior, but the user may not realize their field name was wrong. A warning message would improve the experience.

3. **Pipeline stage ordering matters** — Running anomaly detection before validation would include invalid records in the statistical calculations, potentially flagging valid records as anomalous or missing real anomalies. The pipeline order (load, clean, validate, analyse, report) is deliberate and should not be reordered without understanding the consequences.
