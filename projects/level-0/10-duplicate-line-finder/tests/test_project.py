"""Tests for Duplicate Line Finder."""

from project import build_report, count_line_occurrences, find_duplicates


def test_count_line_occurrences() -> None:
    """Each line should be counted correctly."""
    lines = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    counts = count_line_occurrences(lines)
    assert counts["apple"] == 3
    assert counts["banana"] == 2
    assert counts["cherry"] == 1


def test_find_duplicates_returns_only_dupes() -> None:
    """Only lines appearing more than once should be in the result."""
    lines = ["a", "b", "a", "c"]
    dupes = find_duplicates(lines)
    assert len(dupes) == 1
    assert dupes[0]["text"] == "a"
    assert dupes[0]["count"] == 2
    assert dupes[0]["line_numbers"] == [1, 3]


def test_find_duplicates_no_dupes() -> None:
    """When all lines are unique, the result should be empty."""
    lines = ["one", "two", "three"]
    assert find_duplicates(lines) == []


def test_build_report_counts() -> None:
    """The report should have correct totals."""
    lines = ["x", "y", "x", "z", "y"]
    report = build_report(lines)
    assert report["total_lines"] == 5
    assert report["unique_lines"] == 3
    assert report["duplicate_count"] == 2
