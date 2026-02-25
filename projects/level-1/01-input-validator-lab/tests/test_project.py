"""Tests for Input Validator Lab."""

from project import validate_email, validate_input, validate_phone, validate_zip_code


def test_valid_email() -> None:
    result = validate_email("user@example.com")
    assert result["valid"] is True


def test_invalid_email_no_at() -> None:
    result = validate_email("userexample.com")
    assert result["valid"] is False


def test_valid_phone() -> None:
    result = validate_phone("555-123-4567")
    assert result["valid"] is True


def test_invalid_phone_short() -> None:
    result = validate_phone("555-12")
    assert result["valid"] is False


def test_valid_zip() -> None:
    assert validate_zip_code("90210")["valid"] is True
    assert validate_zip_code("90210-1234")["valid"] is True


def test_invalid_zip() -> None:
    assert validate_zip_code("9021")["valid"] is False


def test_validate_input_dispatch() -> None:
    result = validate_input("email: test@test.com")
    assert result["type"] == "email"
    assert result["valid"] is True
