"""Tests for Calculator Basics.

Each test targets a specific behaviour of the calculator functions.
"""

import pytest

from project import add, calculate, divide


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


def test_calculate_multiplication() -> None:
    """Multiplication should return the correct product."""
    result = calculate("6 * 7")
    assert result["result"] == 42.0


def test_calculate_non_numeric_input() -> None:
    """Non-numeric input like 'abc' should return an error dict, not crash.

    When the user types words instead of numbers, float() raises ValueError.
    The calculate function catches this and returns a dict with an 'error' key
    describing the problem.
    """
    result = calculate("abc + 5")
    assert "error" in result
    assert "Invalid numbers" in result["error"]

    # Both operands non-numeric.
    result = calculate("foo * bar")
    assert "error" in result
    assert "Invalid numbers" in result["error"]

    # Second operand non-numeric.
    result = calculate("10 / xyz")
    assert "error" in result
    assert "Invalid numbers" in result["error"]
