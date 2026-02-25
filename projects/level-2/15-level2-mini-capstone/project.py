"""Level 2 Mini Capstone: Data Pipeline.

This capstone combines skills from all Level 2 projects:
- load CSV data (like project 12),
- clean and validate records (like projects 03, 13),
- detect anomalies (like project 14),
- generate a text report (like project 05),
- export results to JSON.

This is your chance to prove you can combine multiple techniques
into a working end-to-end pipeline.
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
    lines = [l.strip() for l in lines if l.strip() and not l.startswith("#")]

    if not lines:
        return [], []

    headers = [h.strip() for h in lines[0].split(",")]
    records = []

    for line in lines[1:]:
        values = [v.strip() for v in line.split(",")]
        while len(values) < len(headers):
            values.append("")
        records.append(dict(zip(headers, values)))

    return headers, records


# --- Stage 2: Clean ---

def clean_record(record: dict[str, str]) -> dict[str, str]:
    """Clean a single record: strip whitespace, normalise case for emails."""
    cleaned = {}
    for key, value in record.items():
        value = value.strip()
        # Normalise email fields to lowercase.
        if "email" in key.lower():
            value = value.lower()
        cleaned[key] = value
    return cleaned


def clean_records(records: list[dict[str, str]]) -> list[dict[str, str]]:
    """Clean all records using a list comprehension."""
    return [clean_record(r) for r in records]


# --- Stage 3: Validate ---

def validate_record(record: dict[str, str], rules: dict) -> dict:
    """Validate a single record against rules.

    Returns a dict with valid status and list of errors.
    """
    errors: list[str] = []

    # Check required fields.
    for field in rules.get("required", []):
        if not record.get(field, "").strip():
            errors.append(f"Missing required field: {field}")

    # Check email format.
    email_field = rules.get("email_field")
    if email_field and record.get(email_field):
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", record[email_field]):
            errors.append(f"Invalid email: {record[email_field]}")

    # Check numeric ranges.
    for field, bounds in rules.get("ranges", {}).items():
        value = record.get(field, "")
        try:
            num = float(value)
            if num < bounds["min"] or num > bounds["max"]:
                errors.append(f"{field} out of range: {num}")
        except (ValueError, TypeError):
            if value:  # Only flag if value exists but is non-numeric.
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
            invalid.append({**record, "_errors": result["errors"], "_index": idx})

    return valid, invalid


# --- Stage 4: Analyse (anomaly detection) ---

def detect_anomalies(
    records: list[dict], field: str, threshold: float = 2.0
) -> list[dict]:
    """Detect anomalies in a numeric field using z-score."""
    values: list[float] = []
    for r in records:
        try:
            values.append(float(r.get(field, "")))
        except (ValueError, TypeError):
            pass

    if len(values) < 2:
        return []

    avg = sum(values) / len(values)
    variance = sum((x - avg) ** 2 for x in values) / len(values)
    sd = math.sqrt(variance) if variance > 0 else 0

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
        f"Pass rate:         {round(len(valid) / total * 100, 1) if total else 0}%",
        "",
    ]

    if invalid:
        lines.append("--- Validation Failures ---")
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

    # Summary statistics for valid records' numeric field.
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
    """Execute the full pipeline: load -> clean -> validate -> analyse -> report."""
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


# Default validation rules.
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
    parser.add_argument(
        "--json", action="store_true", help="Output results as JSON"
    )
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
        # Remove the text report from JSON output (it is a formatted string).
        output = {k: v for k, v in result.items() if k != "report"}
        print(json.dumps(output, indent=2))
    else:
        print(result["report"])


if __name__ == "__main__":
    main()
