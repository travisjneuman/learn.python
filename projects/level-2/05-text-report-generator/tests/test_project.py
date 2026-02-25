"""Tests for Text Report Generator.

Covers:
- CSV parsing with zip
- Grouping records
- Numeric extraction with error handling
- Statistics computation
- Report generation
"""

from pathlib import Path

import pytest

from project import (
    compute_stats,
    extract_numeric,
    generate_report,
    group_by,
    parse_records,
)


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    """Create a sample CSV file for testing."""
    content = (
        "name, department, salary\n"
        "Alice, Engineering, 95000\n"
        "Bob, Marketing, 72000\n"
        "Charlie, Engineering, 88000\n"
        "Diana, Sales, 68000\n"
        "Eve, Marketing, 75000\n"
    )
    p = tmp_path / "employees.csv"
    p.write_text(content, encoding="utf-8")
    return p


def test_parse_records(sample_csv: Path) -> None:
    """CSV parsing should produce dicts with correct keys."""
    records = parse_records(sample_csv)
    assert len(records) == 5
    assert records[0]["name"] == "Alice"
    assert records[0]["department"] == "Engineering"


def test_parse_records_empty_file(tmp_path: Path) -> None:
    """An empty or header-only file should return no records."""
    p = tmp_path / "empty.csv"
    p.write_text("name, value\n", encoding="utf-8")
    assert parse_records(p) == []


def test_group_by(sample_csv: Path) -> None:
    """Records should be grouped by the specified field."""
    records = parse_records(sample_csv)
    groups = group_by(records, "department")
    assert len(groups["Engineering"]) == 2
    assert len(groups["Marketing"]) == 2
    assert len(groups["Sales"]) == 1


def test_extract_numeric(sample_csv: Path) -> None:
    """Numeric fields should be extracted as floats."""
    records = parse_records(sample_csv)
    values = extract_numeric(records, "salary")
    assert len(values) == 5
    assert 95000.0 in values


def test_extract_numeric_skips_bad_values() -> None:
    """Non-numeric values in a numeric field should be skipped."""
    records = [{"val": "100"}, {"val": "bad"}, {"val": "200"}]
    values = extract_numeric(records, "val")
    assert values == [100.0, 200.0]


@pytest.mark.parametrize(
    "values,expected_mean",
    [
        ([10, 20, 30], 20.0),
        ([100], 100.0),
        ([], 0.0),
    ],
)
def test_compute_stats(values: list[float], expected_mean: float) -> None:
    """Stats should compute correct mean values."""
    stats = compute_stats(values)
    assert stats["mean"] == expected_mean


def test_generate_report_contains_title(sample_csv: Path) -> None:
    """Generated report should include the title and group breakdowns."""
    records = parse_records(sample_csv)
    report = generate_report(records, "department", "salary", "Employee Report")
    assert "Employee Report" in report
    assert "Engineering" in report
    assert "Marketing" in report


def test_parse_records_missing_file(tmp_path: Path) -> None:
    """Missing file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        parse_records(tmp_path / "nope.csv")
