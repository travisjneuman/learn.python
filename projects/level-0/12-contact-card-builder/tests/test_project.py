"""Tests for Contact Card Builder."""

from pathlib import Path

from project import contacts_summary, format_card, parse_contact_line


def test_parse_valid_contact() -> None:
    """A well-formed line should produce a contact dict."""
    result = parse_contact_line("Ada Lovelace, 555-0101, ada@example.com")
    assert result["name"] == "Ada Lovelace"
    assert result["phone"] == "555-0101"
    assert result["email"] == "ada@example.com"
    assert "error" not in result


def test_parse_missing_fields() -> None:
    """A line with too few fields should return an error."""
    result = parse_contact_line("only name")
    assert "error" in result


def test_parse_invalid_email() -> None:
    """An email without @ should be flagged as invalid."""
    result = parse_contact_line("Bob, 555-0102, not-an-email")
    assert "error" in result
    assert "Invalid email" in result["error"]


def test_format_card_valid() -> None:
    """A valid contact should produce a formatted card string."""
    contact = {"name": "Test User", "phone": "555-0000", "email": "test@x.com"}
    card = format_card(contact)
    assert "Test User" in card
    assert "555-0000" in card


def test_contacts_summary_counts() -> None:
    """Summary should correctly count valid and error contacts."""
    contacts = [
        {"name": "A", "phone": "1", "email": "a@b.com"},
        {"raw": "bad", "error": "oops"},
        {"name": "B", "phone": "2", "email": "b@c.com"},
    ]
    summary = contacts_summary(contacts)
    assert summary["valid"] == 2
    assert summary["errors"] == 1
