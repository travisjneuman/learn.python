"""Tests for Malformed Row Quarantine."""

from pathlib import Path
import pytest

from project import (
    rule_column_count,
    rule_no_empty_required,
    rule_no_control_chars,
    rule_max_field_length,
    quarantine_rows,
    run,
)


@pytest.mark.parametrize(
    "fields, expected, has_error",
    [
        (["a", "b", "c"], 3, False),
        (["a", "b"], 3, True),
        (["a", "b", "c", "d"], 3, True),
    ],
)
def test_rule_column_count(fields: list[str], expected: int, has_error: bool) -> None:
    result = rule_column_count(fields, expected)
    assert (result is not None) == has_error


def test_rule_no_empty_required() -> None:
    assert rule_no_empty_required(["Alice", "30"], [0, 1]) is None
    assert rule_no_empty_required(["Alice", ""], [0, 1]) is not None


def test_rule_no_control_chars() -> None:
    assert rule_no_control_chars(["normal", "text"]) is None
    assert rule_no_control_chars(["has\x00null", "ok"]) is not None


def test_rule_max_field_length() -> None:
    assert rule_max_field_length(["short"]) is None
    assert rule_max_field_length(["x" * 600], max_len=500) is not None


def test_quarantine_rows_separates_correctly() -> None:
    lines = [
        "name,age,city",       # header
        "Alice,30,NYC",        # valid
        "Bob,25",              # too few columns
        "Charlie,28,Chicago",  # valid
        ",40,Denver",          # valid (no required check by default)
    ]
    result = quarantine_rows(lines)
    assert len(result["valid"]) == 3
    assert len(result["quarantined"]) == 1


def test_quarantine_with_required_indexes() -> None:
    lines = [
        "name,age",
        "Alice,30",
        ",25",       # empty required column 0
    ]
    result = quarantine_rows(lines, required_indexes=[0])
    assert len(result["quarantined"]) == 1
    assert "empty required" in result["quarantined"][0]["reasons"][0]


def test_run_integration(tmp_path: Path) -> None:
    input_file = tmp_path / "data.csv"
    input_file.write_text("a,b,c\n1,2,3\n4,5\n6,7,8\n", encoding="utf-8")
    output_dir = tmp_path / "output"

    summary = run(input_file, output_dir)
    assert summary["valid"] == 2
    assert summary["quarantined"] == 1
    assert (output_dir / "valid_rows.txt").exists()
    assert (output_dir / "quarantined_rows.json").exists()
