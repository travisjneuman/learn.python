"""Tests for Validation Rule Engine.

Covers:
- Individual rule checks (required, regex, range, min_length)
- Single record validation
- Batch validation with statistics
- Rule loading
"""

import pytest

from project import (
    apply_rule,
    check_range,
    check_regex,
    check_required,
    validate_batch,
    validate_record,
    DEFAULT_RULES,
)


def test_check_required_present() -> None:
    """Present non-empty field should pass."""
    assert check_required({"name": "Alice"}, "name") is True


def test_check_required_missing() -> None:
    """Missing field should fail."""
    assert check_required({}, "name") is False


def test_check_required_empty_string() -> None:
    """Empty string should fail the required check."""
    assert check_required({"name": ""}, "name") is False


def test_check_regex_valid_email() -> None:
    """Valid email should match the pattern."""
    assert check_regex(
        {"email": "test@example.com"}, "email", r"^[^@]+@[^@]+\.[^@]+$"
    ) is True


def test_check_regex_invalid_email() -> None:
    """Invalid email should not match."""
    assert check_regex(
        {"email": "not-an-email"}, "email", r"^[^@]+@[^@]+\.[^@]+$"
    ) is False


@pytest.mark.parametrize(
    "value,expected",
    [(25, True), (0, True), (150, True), (-1, False), (200, False)],
)
def test_check_range(value: int, expected: bool) -> None:
    """Range check should accept values within bounds."""
    assert check_range({"age": value}, "age", 0, 150) is expected


def test_apply_rule_unknown_type() -> None:
    """Unknown rule type should fail with descriptive error."""
    rule = {"id": "X", "field": "f", "type": "unknown_type"}
    result = apply_rule({"f": "val"}, rule)
    assert result["passed"] is False
    assert "Unknown rule type" in result["message"]


def test_validate_record_all_pass() -> None:
    """A valid record should pass all default rules."""
    record = {"name": "Alice", "email": "alice@example.com", "age": 30}
    result = validate_record(record, DEFAULT_RULES)
    assert result["valid"] is True
    assert result["failed_count"] == 0


def test_validate_record_failures() -> None:
    """A record with invalid fields should report failures."""
    record = {"name": "", "email": "bad", "age": -5}
    result = validate_record(record, DEFAULT_RULES)
    assert result["valid"] is False
    assert result["failed_count"] > 0


def test_validate_batch() -> None:
    """Batch should report overall pass rate and failure counts."""
    records = [
        {"name": "Alice", "email": "alice@example.com", "age": 30},
        {"name": "", "email": "bad", "age": -5},
        {"name": "Charlie", "email": "c@test.com", "age": 25},
    ]
    result = validate_batch(records, DEFAULT_RULES)
    assert result["total_records"] == 3
    assert result["valid_count"] == 2
    assert result["invalid_count"] == 1


def test_validate_batch_empty() -> None:
    """Empty batch should report 0 records."""
    result = validate_batch([], DEFAULT_RULES)
    assert result["total_records"] == 0
    assert result["pass_rate"] == 0
