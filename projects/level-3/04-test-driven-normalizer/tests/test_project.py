"""Tests for Test Driven Normalizer.

Written FIRST (TDD style) — each test defines expected behaviour
before the implementation exists.
"""

import pytest

from project import (
    NormalisationResult,
    normalise_batch,
    normalise_date,
    normalise_email,
    normalise_name,
    normalise_phone,
    normalise_record,
    normalise_whitespace,
)


# --- Whitespace normalisation ---

@pytest.mark.parametrize("input_text,expected", [
    ("hello   world", "hello world"),
    ("  leading", "leading"),
    ("trailing  ", "trailing"),
    ("\ttabs\tand\nlines", "tabs and lines"),
    ("already clean", "already clean"),
])
def test_normalise_whitespace(input_text: str, expected: str) -> None:
    """Whitespace normaliser should collapse and strip."""
    result = normalise_whitespace(input_text)
    assert isinstance(result, NormalisationResult)
    assert result.normalised == expected


# --- Email normalisation ---

def test_normalise_email_lowercase() -> None:
    """Emails should be lowercased."""
    result = normalise_email("User@Example.COM")
    assert result.normalised == "user@example.com"
    assert result.changed is True


def test_normalise_email_strips_whitespace() -> None:
    """Leading/trailing whitespace should be removed."""
    result = normalise_email("  test@test.com  ")
    assert result.normalised == "test@test.com"


# --- Phone normalisation ---

@pytest.mark.parametrize("raw,expected", [
    ("555-867-5309", "(555) 867-5309"),
    ("1-555-867-5309", "(555) 867-5309"),
    ("(555) 867-5309", "(555) 867-5309"),
    ("5558675309", "(555) 867-5309"),
])
def test_normalise_phone(raw: str, expected: str) -> None:
    """Phone numbers should normalise to (XXX) XXX-XXXX."""
    result = normalise_phone(raw)
    assert result.normalised == expected


def test_normalise_phone_invalid() -> None:
    """Non-10-digit numbers should be returned as-is (stripped)."""
    result = normalise_phone("123")
    assert result.normalised == "123"


# --- Name normalisation ---

def test_normalise_name_uppercase() -> None:
    """All-caps names should become title case."""
    result = normalise_name("JANE DOE")
    assert result.normalised == "Jane Doe"


def test_normalise_name_lowercase() -> None:
    """All-lower names should become title case."""
    result = normalise_name("john smith")
    assert result.normalised == "John Smith"


# --- Date normalisation ---

@pytest.mark.parametrize("raw,expected", [
    ("01/15/2024", "2024-01-15"),
    ("25-12-2023", "2023-12-25"),
    ("2024.03.07", "2024-03-07"),
    ("2024-01-15", "2024-01-15"),  # Already normalised.
])
def test_normalise_date(raw: str, expected: str) -> None:
    """Various date formats should normalise to YYYY-MM-DD."""
    result = normalise_date(raw)
    assert result.normalised == expected


# --- Record and batch normalisation ---

def test_normalise_record() -> None:
    """A record should have specified fields normalised."""
    record = {"email": "TEST@Example.COM", "age": 30, "name": "ALICE"}
    field_types = {"email": "email", "name": "name"}
    result = normalise_record(record, field_types)
    assert result["email"] == "test@example.com"
    assert result["name"] == "Alice"
    assert result["age"] == 30  # Untouched.


def test_normalise_batch() -> None:
    """Batch should normalise all records."""
    records = [
        {"email": "A@B.COM"},
        {"email": "C@D.COM"},
    ]
    result = normalise_batch(records, {"email": "email"})
    assert len(result) == 2
    assert result[0]["email"] == "a@b.com"
    assert result[1]["email"] == "c@d.com"
