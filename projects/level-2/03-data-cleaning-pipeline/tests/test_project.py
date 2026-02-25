"""Tests for Data Cleaning Pipeline.

Covers:
- Individual cleaning steps
- Full pipeline execution
- Deduplication with sets
- Regex-based filtering
- File loading and error handling
"""

from pathlib import Path

import pytest

from project import (
    deduplicate,
    filter_by_pattern,
    load_and_clean,
    normalise_case,
    normalise_separators,
    remove_blanks,
    run_pipeline,
    strip_whitespace,
)


def test_strip_whitespace() -> None:
    """Leading and trailing spaces should be removed."""
    assert strip_whitespace(["  hello  ", "world ", " test"]) == [
        "hello",
        "world",
        "test",
    ]


def test_remove_blanks() -> None:
    """Empty strings should be filtered out."""
    assert remove_blanks(["a", "", "b", "", "c"]) == ["a", "b", "c"]


def test_normalise_case() -> None:
    """All records should become lowercase."""
    assert normalise_case(["Hello", "WORLD", "PyThOn"]) == [
        "hello",
        "world",
        "python",
    ]


def test_deduplicate_preserves_order() -> None:
    """Duplicates removed, first occurrence kept."""
    assert deduplicate(["a", "b", "a", "c", "b"]) == ["a", "b", "c"]


def test_deduplicate_empty_list() -> None:
    """An empty list should return an empty list."""
    assert deduplicate([]) == []


def test_normalise_separators() -> None:
    """Tabs, semicolons, and pipes should become commas."""
    records = ["a;b;c", "x\ty\tz", "1|2|3"]
    result = normalise_separators(records, target=",")
    assert result == ["a,b,c", "x,y,z", "1,2,3"]


def test_filter_by_pattern() -> None:
    """Records not matching the pattern go into rejected."""
    records = ["user@example.com", "not-an-email", "admin@test.org"]
    valid, rejected = filter_by_pattern(records, r"@.*\.")
    assert valid == ["user@example.com", "admin@test.org"]
    assert rejected == ["not-an-email"]


@pytest.mark.parametrize(
    "input_records,expected_count",
    [
        (["a", "b", "c"], 3),
        (["a", "a", "a"], 1),
        (["  a  ", "a", "A"], 1),  # whitespace + case duplicates
    ],
)
def test_pipeline_dedup_counts(
    input_records: list[str], expected_count: int
) -> None:
    """Pipeline should report correct cleaned counts."""
    result = run_pipeline(input_records)
    assert result["cleaned_count"] == expected_count


def test_load_and_clean_from_file(tmp_path: Path) -> None:
    """Full pipeline should work from a file."""
    p = tmp_path / "data.txt"
    p.write_text("  Hello \nworld\n\nhello\nWORLD\n", encoding="utf-8")
    result = load_and_clean(p)
    assert result["cleaned"] == ["hello", "world"]


def test_load_and_clean_missing_file(tmp_path: Path) -> None:
    """Missing file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_and_clean(tmp_path / "nope.txt")
