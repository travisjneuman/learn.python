"""Tests for Mock API Response Parser.

Covers:
- JSON parsing (valid and invalid)
- Response validation
- Item extraction from nested structures
- Status code categorisation
- Item summarisation
"""

import pytest

from project import (
    check_status,
    extract_items,
    parse_response,
    summarise_items,
    validate_response,
)


def test_parse_response_valid() -> None:
    """Valid JSON should be parsed successfully."""
    result = parse_response('{"status": 200, "data": []}')
    assert result["success"] is True
    assert result["data"]["status"] == 200


def test_parse_response_invalid() -> None:
    """Invalid JSON should return an error dict."""
    result = parse_response("not json at all")
    assert result["success"] is False
    assert "Invalid JSON" in result["error"]


def test_validate_response_all_present() -> None:
    """Response with all required fields should be valid."""
    resp = {"status": 200, "data": [], "message": "ok"}
    result = validate_response(resp, ["status", "data"])
    assert result["valid"] is True
    assert result["missing_fields"] == []


def test_validate_response_missing_fields() -> None:
    """Missing required fields should be reported."""
    resp = {"status": 200}
    result = validate_response(resp, ["status", "data", "message"])
    assert result["valid"] is False
    assert "data" in result["missing_fields"]


def test_extract_items_list() -> None:
    """Should extract a list from the specified key."""
    resp = {"data": [{"id": 1}, {"id": 2}]}
    items = extract_items(resp, "data")
    assert len(items) == 2


def test_extract_items_missing_key() -> None:
    """Missing key should return empty list."""
    items = extract_items({"other": "stuff"}, "data")
    assert items == []


def test_extract_items_single_object() -> None:
    """A single object at the key should be wrapped in a list."""
    resp = {"data": {"id": 1, "name": "test"}}
    items = extract_items(resp, "data")
    assert len(items) == 1


@pytest.mark.parametrize(
    "status_code,expected_category",
    [
        (200, "success"),
        (201, "success"),
        (301, "redirect"),
        (404, "client_error"),
        (500, "server_error"),
    ],
)
def test_check_status(status_code: int, expected_category: str) -> None:
    """Status codes should be categorised correctly."""
    result = check_status({"status": status_code})
    assert result["category"] == expected_category


def test_check_status_missing() -> None:
    """Missing status should return 'unknown'."""
    result = check_status({"data": []})
    assert result["category"] == "unknown"


def test_summarise_items_with_grouping() -> None:
    """Grouping should count items per group value."""
    items = [
        {"type": "user", "name": "Alice"},
        {"type": "admin", "name": "Bob"},
        {"type": "user", "name": "Charlie"},
    ]
    summary = summarise_items(items, group_field="type")
    assert summary["groups"]["user"] == 2
    assert summary["groups"]["admin"] == 1


def test_summarise_items_empty() -> None:
    """Empty items list should produce zero counts."""
    summary = summarise_items([])
    assert summary["count"] == 0
