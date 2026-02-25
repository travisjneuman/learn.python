"""Tests for Error Safe Divider.

Covers:
- Normal division
- Division by zero handling
- Invalid type handling
- Batch operations
- Summary statistics
- File parsing
"""

from pathlib import Path

import pytest

from project import (
    batch_divide,
    parse_operations_file,
    safe_divide,
    summarise_results,
)


def test_safe_divide_normal() -> None:
    """Normal division should succeed."""
    result = safe_divide(10, 3)
    assert result["success"] is True
    assert abs(result["result"] - 3.3333) < 0.01


def test_safe_divide_zero() -> None:
    """Dividing by zero should return an error, not crash."""
    result = safe_divide(10, 0)
    assert result["success"] is False
    assert result["error_type"] == "ZeroDivisionError"


@pytest.mark.parametrize(
    "num,den,expected_error",
    [
        ("abc", 5, "ValueError"),
        (10, "xyz", "ValueError"),
        (None, 5, "TypeError"),
    ],
)
def test_safe_divide_invalid_types(
    num: object, den: object, expected_error: str
) -> None:
    """Non-numeric inputs should produce descriptive errors."""
    result = safe_divide(num, den)
    assert result["success"] is False
    assert result["error_type"] == expected_error


def test_safe_divide_string_numbers() -> None:
    """Numeric strings like '10' should work (float conversion)."""
    result = safe_divide("10", "2.5")
    assert result["success"] is True
    assert result["result"] == 4.0


def test_batch_divide_preserves_order() -> None:
    """Batch results should keep original indices."""
    ops = [(10, 2), (0, 0), (6, 3)]
    results = batch_divide(ops)
    assert len(results) == 3
    assert [r["index"] for r in results] == [0, 1, 2]
    assert results[0]["success"] is True
    assert results[1]["success"] is False


def test_summarise_results() -> None:
    """Summary should correctly count successes and failures."""
    results = batch_divide([(10, 2), (5, 0), (8, 4)])
    summary = summarise_results(results)
    assert summary["total"] == 3
    assert summary["successes"] == 2
    assert summary["failures"] == 1
    assert summary["error_counts"] == {"ZeroDivisionError": 1}


def test_parse_operations_file(tmp_path: Path) -> None:
    """File parsing should handle comments, blanks, and valid lines."""
    p = tmp_path / "ops.txt"
    p.write_text("# comment\n10,5\n\n20,4\nbadline\n", encoding="utf-8")
    ops = parse_operations_file(p)
    assert len(ops) == 3  # 2 valid + 1 bad
    assert ops[0] == ("10", "5")
    assert ops[1] == ("20", "4")


def test_parse_operations_file_missing(tmp_path: Path) -> None:
    """Missing file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        parse_operations_file(tmp_path / "missing.txt")
