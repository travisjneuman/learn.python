"""Tests for Level 2 Mini Capstone: Data Pipeline.

Covers all pipeline stages:
- CSV loading
- Record cleaning
- Validation with rules
- Anomaly detection
- Full pipeline execution
"""

from pathlib import Path

import pytest

from project import (
    clean_record,
    clean_records,
    detect_anomalies,
    load_csv,
    run_pipeline,
    validate_batch,
    validate_record,
    DEFAULT_RULES,
)


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    """Create a sample CSV with valid, invalid, and anomalous data."""
    content = (
        "name,email,age,salary\n"
        "Alice,alice@example.com,30,85000\n"
        "Bob,bob@example.com,25,72000\n"
        ",bad-email,-5,50000\n"
        "Diana,diana@test.org,28,78000\n"
        "Eve,eve@company.io,32,500000\n"
    )
    p = tmp_path / "data.csv"
    p.write_text(content, encoding="utf-8")
    return p


def test_load_csv(sample_csv: Path) -> None:
    """CSV should be loaded with correct headers and records."""
    headers, records = load_csv(sample_csv)
    assert "name" in headers
    assert len(records) == 5


def test_load_csv_missing(tmp_path: Path) -> None:
    """Missing file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_csv(tmp_path / "nope.csv")


def test_clean_record() -> None:
    """Cleaning should strip whitespace and lowercase emails."""
    record = {"name": "  Alice  ", "email": "  ALICE@TEST.COM  "}
    cleaned = clean_record(record)
    assert cleaned["name"] == "Alice"
    assert cleaned["email"] == "alice@test.com"


def test_validate_record_valid() -> None:
    """A complete valid record should pass all rules."""
    record = {"name": "Alice", "email": "alice@test.com", "age": "30", "salary": "80000"}
    result = validate_record(record, DEFAULT_RULES)
    assert result["valid"] is True


def test_validate_record_invalid() -> None:
    """A record with missing name and bad email should fail."""
    record = {"name": "", "email": "bad", "age": "-5", "salary": "80000"}
    result = validate_record(record, DEFAULT_RULES)
    assert result["valid"] is False
    assert len(result["errors"]) >= 2


@pytest.mark.parametrize(
    "age,expected_valid",
    [("25", True), ("0", True), ("150", True), ("-1", False), ("200", False)],
)
def test_validate_age_range(age: str, expected_valid: bool) -> None:
    """Age validation should enforce 0-150 range."""
    record = {"name": "Test", "email": "t@t.com", "age": age, "salary": "50000"}
    result = validate_record(record, DEFAULT_RULES)
    # Check if age-specific errors exist.
    age_errors = [e for e in result["errors"] if "age" in e.lower()]
    assert (len(age_errors) == 0) == expected_valid


def test_validate_batch(sample_csv: Path) -> None:
    """Batch validation should split into valid and invalid."""
    _, records = load_csv(sample_csv)
    cleaned = clean_records(records)
    valid, invalid = validate_batch(cleaned, DEFAULT_RULES)
    assert len(valid) + len(invalid) == len(records)
    assert len(invalid) >= 1  # The row with empty name


def test_detect_anomalies() -> None:
    """Extreme salary should be flagged as anomaly."""
    records = [
        {"salary": "80000"},
        {"salary": "75000"},
        {"salary": "82000"},
        {"salary": "500000"},  # anomaly
        {"salary": "78000"},
    ]
    anomalies = detect_anomalies(records, "salary", threshold=2.0)
    assert len(anomalies) >= 1
    assert anomalies[0]["value"] == 500000.0


def test_run_pipeline(sample_csv: Path) -> None:
    """Full pipeline should execute without errors."""
    result = run_pipeline(sample_csv, DEFAULT_RULES, "salary")
    assert result["total"] == 5
    assert "report" in result
    assert result["valid_count"] + result["invalid_count"] == result["total"]
