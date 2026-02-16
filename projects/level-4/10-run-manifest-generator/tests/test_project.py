"""Intermediate test module with heavy comments.

These tests validate:
- loader cleanup behavior,
- record transformation structure,
- summary metric correctness.
"""

# Path helps build reliable temporary files in test environments.
from pathlib import Path

# Import functions under test from the local project module.
from project import build_records, build_summary, load_items


def test_load_items_strips_blank_lines(tmp_path: Path) -> None:
    """Ensure loader trims whitespace and skips empty lines."""
    # Arrange: create mixed-quality text input.
    sample = tmp_path / "sample.txt"
    sample.write_text("alpha\n\n beta \n", encoding="utf-8")

    # Act: run loader.
    items = load_items(sample)

    # Assert: expect cleaned output.
    assert items == ["alpha", "beta"]


def test_build_records_assigns_row_numbers() -> None:
    """Ensure transform assigns stable row numbering for traceability."""
    # Arrange: define minimal input list.
    raw_items = ["one", "two"]

    # Act: build structured records.
    records = build_records(raw_items)

    # Assert: check row-number assignment and record count.
    assert len(records) == 2
    assert records[0]["row_num"] == 1
    assert records[1]["row_num"] == 2


def test_build_summary_counts_records() -> None:
    """Ensure summary reports core metrics correctly."""
    # Arrange: create records from known-length strings.
    records = build_records(["abc", "xy"])

    # Act: build summary from records.
    summary = build_summary(records)

    # Assert: verify counts and min/max lengths.
    assert summary["record_count"] == 2
    assert summary["max_length"] == 3
    assert summary["min_length"] == 2
