"""Tests for Calculator Basics.

Each test targets a specific behaviour of the calculator functions.
"""

from pathlib import Path

import pytest

from project import add, calculate, divide, process_file


def test_add_two_numbers() -> None:
    """Basic addition should return the correct sum."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_divide_by_zero_raises() -> None:
    """Dividing by zero must raise ValueError, not crash."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)


def test_calculate_valid_expression() -> None:
    """A well-formed expression should return a numeric result."""
    result = calculate("10 + 5")
    assert result["result"] == 15.0
    assert "error" not in result


def test_calculate_bad_operator() -> None:
    """An unknown operator should produce an error dict, not a crash."""
    result = calculate("10 ^ 5")
    assert "error" in result
    assert "Unknown operator" in result["error"]


def test_process_file_reads_expressions(tmp_path: Path) -> None:
    """process_file should calculate each line in the input file."""
    sample = tmp_path / "calc.txt"
    sample.write_text("3 + 4\n10 / 2\n", encoding="utf-8")

    results = process_file(sample)
    assert len(results) == 2
    assert results[0]["result"] == 7.0
    assert results[1]["result"] == 5.0
