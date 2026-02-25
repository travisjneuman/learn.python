"""Tests for Records Deduplicator.

Covers:
- CSV parsing
- Dedup key generation
- First vs last keep modes
- Duplicate group detection
- Edge cases
"""

from pathlib import Path

import pytest

from project import (
    deduplicate,
    find_duplicate_groups,
    make_dedup_key,
    parse_csv_records,
)


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    """Create a CSV file with known duplicates."""
    content = (
        "name, email, department\n"
        "Alice, alice@example.com, Engineering\n"
        "Bob, bob@example.com, Marketing\n"
        "alice, ALICE@EXAMPLE.COM, Sales\n"
        "Charlie, charlie@test.org, Engineering\n"
        "Bob, bob@example.com, Marketing\n"
    )
    p = tmp_path / "records.csv"
    p.write_text(content, encoding="utf-8")
    return p


def test_parse_csv_records(sample_csv: Path) -> None:
    """CSV should be parsed into header + record dicts."""
    headers, records = parse_csv_records(sample_csv)
    assert "name" in headers
    assert len(records) == 5


def test_make_dedup_key() -> None:
    """Dedup key should normalise and join field values."""
    record = {"name": " Alice ", "email": "ALICE@test.com"}
    key = make_dedup_key(record, ["name", "email"])
    assert key == "alice|alice@test.com"


def test_deduplicate_keep_first(sample_csv: Path) -> None:
    """Keep=first should retain the first occurrence of each duplicate."""
    _, records = parse_csv_records(sample_csv)
    result = deduplicate(records, key_fields=["email"], keep="first")
    assert result["stats"]["unique_count"] == 4
    assert result["stats"]["duplicate_count"] == 1


def test_deduplicate_keep_last(sample_csv: Path) -> None:
    """Keep=last should retain the last occurrence of each duplicate."""
    _, records = parse_csv_records(sample_csv)
    result = deduplicate(records, key_fields=["email"], keep="last")
    assert result["stats"]["unique_count"] == 4


@pytest.mark.parametrize(
    "key_fields,expected_unique",
    [
        (["name"], 3),       # alice appears twice (case-insensitive)
        (["email"], 4),      # bob@example.com appears twice
        (["name", "email"], 4),  # combined key is more specific
    ],
)
def test_deduplicate_different_keys(
    sample_csv: Path, key_fields: list[str], expected_unique: int
) -> None:
    """Different key field combinations should yield different results."""
    _, records = parse_csv_records(sample_csv)
    result = deduplicate(records, key_fields=key_fields)
    assert result["stats"]["unique_count"] == expected_unique


def test_find_duplicate_groups(sample_csv: Path) -> None:
    """Should return only groups with 2+ records."""
    _, records = parse_csv_records(sample_csv)
    groups = find_duplicate_groups(records, ["email"])
    assert len(groups) == 1  # only bob@example.com has duplicates
    assert len(list(groups.values())[0]) == 2


def test_deduplicate_invalid_keep() -> None:
    """Invalid keep mode should raise ValueError."""
    with pytest.raises(ValueError, match="keep must be"):
        deduplicate([], key_fields=["name"], keep="middle")


def test_deduplicate_empty_records() -> None:
    """Empty input should produce empty output."""
    result = deduplicate([], key_fields=["name"])
    assert result["stats"]["unique_count"] == 0
