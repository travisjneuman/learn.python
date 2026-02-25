"""Tests for Structured Error Handler."""

import pytest

from project import (
    AppError,
    ConfigError,
    ErrorRecord,
    NotFoundError,
    OperationResult,
    ValidationError,
    capture_error,
    safe_process,
    summarise_results,
    validate_field,
    validate_record,
)


# --- Custom exceptions ---

def test_app_error_has_code() -> None:
    """AppError should carry a code and context."""
    err = AppError("something broke", code="BROKEN", context={"key": "val"})
    assert err.code == "BROKEN"
    assert err.context["key"] == "val"
    assert str(err) == "something broke"


def test_validation_error_has_field() -> None:
    """ValidationError should carry a field name."""
    err = ValidationError("bad email", field="email")
    assert err.field == "email"
    assert err.code == "VALIDATION_ERROR"


def test_not_found_error() -> None:
    """NotFoundError should format resource and identifier."""
    err = NotFoundError("User", "42")
    assert "User" in str(err)
    assert "42" in str(err)
    assert err.code == "NOT_FOUND"


# --- capture_error ---

def test_capture_app_error() -> None:
    """capture_error should extract structured info from AppError."""
    try:
        raise ValidationError("bad", field="name")
    except Exception as exc:
        record = capture_error(exc)
    assert record.code == "VALIDATION_ERROR"
    assert record.field == "name"


def test_capture_unexpected_error() -> None:
    """capture_error should handle non-AppError exceptions."""
    try:
        raise ValueError("oops")
    except Exception as exc:
        record = capture_error(exc)
    assert record.code == "UNEXPECTED"
    assert "oops" in record.message


# --- validate_field ---

def test_validate_required_missing() -> None:
    """Missing required field should produce REQUIRED error."""
    errors = validate_field("name", "", {"required": True})
    assert len(errors) == 1
    assert errors[0].code == "REQUIRED"


def test_validate_min_length() -> None:
    """Too-short value should produce TOO_SHORT error."""
    errors = validate_field("pw", "ab", {"min_length": 8})
    assert any(e.code == "TOO_SHORT" for e in errors)


def test_validate_pattern() -> None:
    """Pattern mismatch should produce INVALID_FORMAT error."""
    errors = validate_field("email", "notanemail", {"pattern": r"^.+@.+\..+$"})
    assert any(e.code == "INVALID_FORMAT" for e in errors)


def test_validate_passes() -> None:
    """Valid field should produce no errors."""
    errors = validate_field("name", "Alice", {"required": True, "min_length": 2})
    assert len(errors) == 0


# --- validate_record ---

def test_validate_record_success() -> None:
    """Valid record should return success."""
    record = {"name": "Alice", "email": "a@b.com"}
    schema = {"name": {"required": True}, "email": {"required": True}}
    result = validate_record(record, schema)
    assert result.success is True


def test_validate_record_failure() -> None:
    """Invalid record should collect errors."""
    record = {"name": "", "email": ""}
    schema = {"name": {"required": True}, "email": {"required": True}}
    result = validate_record(record, schema)
    assert result.success is False
    assert len(result.errors) == 2


# --- safe_process and summarise ---

def test_safe_process() -> None:
    """Batch processing should collect results without crashing."""
    records = [{"name": "Alice"}, {"name": ""}]
    schema = {"name": {"required": True}}
    results = safe_process(records, schema)
    assert len(results) == 2
    assert results[0].success is True
    assert results[1].success is False


def test_summarise_results() -> None:
    """Summary should count passed/failed and group error codes."""
    results = [
        OperationResult(success=True),
        OperationResult(success=False, errors=[
            ErrorRecord(code="REQUIRED", message="missing"),
            ErrorRecord(code="REQUIRED", message="also missing"),
        ]),
    ]
    summary = summarise_results(results)
    assert summary["total"] == 2
    assert summary["passed"] == 1
    assert summary["failed"] == 1
    assert summary["error_counts"]["REQUIRED"] == 2
