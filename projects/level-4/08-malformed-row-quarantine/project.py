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

# WHY individual rule functions? -- Each rule is a function that takes
# (fields, header_count) and returns an error string or None. This pattern
# makes rules composable, testable in isolation, and easy to extend:
# adding a new check is just writing one small function.


def rule_column_count(fields: list[str], expected: int) -> str | None:
    """Every row must have exactly the expected number of columns."""
    if len(fields) != expected:
        return f"expected {expected} columns, got {len(fields)}"
    return None


def rule_no_empty_required(fields: list[str], required_indexes: list[int]) -> str | None:
    """Specified column indexes must not be blank."""
    missing = [i for i in required_indexes if i < len(fields) and not fields[i].strip()]
    if missing:
        return f"empty required column(s) at index(es): {missing}"
    return None


def rule_no_control_chars(fields: list[str]) -> str | None:
    """Reject rows containing control characters (except tab/newline).

    WHY allow tab and newline? -- Tabs appear in TSV data and newlines
    can appear inside quoted CSV fields. Other control characters (like
    null bytes or bell) usually indicate file corruption.
    """
    for i, field in enumerate(fields):
        for ch in field:
            if ord(ch) < 32 and ch not in ("\t", "\n", "\r"):
                return f"control character in column {i}: ord={ord(ch)}"
    return None


def rule_max_field_length(fields: list[str], max_len: int = 500) -> str | None:
    """Reject rows where any single field exceeds max_len characters."""
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
    """Process lines and separate valid from malformed.

    Returns:
        {
            "valid": [{"row": int, "fields": list[str]}],
            "quarantined": [{"row": int, "raw": str, "reasons": list[str]}],
        }
    """
    if not lines:
        return {"valid": [], "quarantined": []}

    # First line is the header — determines expected column count
    header_fields = lines[0].split(delimiter)
    expected_cols = len(header_fields)
    required = required_indexes or []

    valid: list[dict] = []
    quarantined: list[dict] = []

    for idx, line in enumerate(lines[1:], start=2):
        fields = line.split(delimiter)
        reasons: list[str] = []

        # Apply each rule
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

    # Write valid rows
    valid_path = output_dir / "valid_rows.txt"
    valid_path.write_text(
        "\n".join(lines[0:1] + [",".join(r["fields"]) for r in result["valid"]]),
        encoding="utf-8",
    )

    # Write quarantined rows with reasons
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
