"""
Tests for Project 01 — Package Structure (test_project.py)

Additional tests that complement test_calculator.py and test_statistics.py.
These test the package's public API (imports from mymath) to verify that
__init__.py re-exports functions correctly.

Why test the public API?
    Users of your package write "from mymath import add" — they do not
    care which internal module provides the function. If __init__.py
    forgets to re-export a function, users get ImportError even though
    the function exists internally.

Run with: pytest tests/test_project.py -v
"""

import pytest

# Test the public API — import from the package, not from internal modules.
# This verifies that __init__.py re-exports everything correctly.
from mymath import add, subtract, multiply, divide, mean, median, mode
from mymath import __version__


# ── Test: package version ──────────────────────────────────────────────

def test_version_exists():
    """The package should expose a __version__ string.

    WHY: Version strings are used by pip, build tools, and users to
    identify which version is installed. Missing version causes issues
    with packaging tools.
    """
    assert isinstance(__version__, str), "__version__ should be a string"
    assert len(__version__) > 0, "__version__ should not be empty"


# ── Test: calculator functions via public API ──────────────────────────

def test_add():
    """add(a, b) should return a + b.

    WHY: Tests the re-export from mymath.calculator through __init__.py.
    If the import chain is broken, this test fails with ImportError.
    """
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract():
    """subtract(a, b) should return a - b."""
    assert subtract(10, 4) == 6
    assert subtract(0, 5) == -5


def test_multiply():
    """multiply(a, b) should return a * b."""
    assert multiply(3, 7) == 21
    assert multiply(-2, 3) == -6
    assert multiply(0, 100) == 0


def test_divide():
    """divide(a, b) should return a / b.

    WHY: Division must handle the zero case. The function raises
    ZeroDivisionError explicitly, which is better than letting Python
    raise it implicitly (same error, but with a clearer message).
    """
    assert divide(15, 3) == 5.0
    assert divide(7, 2) == 3.5


def test_divide_by_zero():
    """divide(a, 0) should raise ZeroDivisionError.

    WHY: Division by zero is a runtime error. The function should raise
    a clear exception, not return infinity or NaN.
    """
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(10, 0)


# ── Test: statistics functions via public API ──────────────────────────

def test_mean():
    """mean(numbers) should return the arithmetic average.

    WHY: Tests the re-export from mymath.statistics through __init__.py.
    """
    assert mean([1, 2, 3, 4, 5]) == 3.0
    assert mean([10]) == 10.0


def test_mean_empty_raises():
    """mean of an empty list should raise ValueError.

    WHY: The mean of nothing is undefined. Returning 0 or NaN would be
    misleading. A clear exception tells the caller something is wrong.
    """
    with pytest.raises(ValueError, match="empty"):
        mean([])


def test_median_odd():
    """median of an odd-length list should return the middle element."""
    assert median([1, 3, 5]) == 3
    assert median([7, 2, 9]) == 7  # sorted: [2, 7, 9]


def test_median_even():
    """median of an even-length list should return the average of the two middle elements."""
    assert median([1, 3, 5, 7]) == 4.0


def test_median_empty_raises():
    """median of an empty list should raise ValueError."""
    with pytest.raises(ValueError, match="empty"):
        median([])


def test_mode():
    """mode should return the most common value.

    WHY: mode uses Counter.most_common() which returns items sorted by
    count. This test verifies the function returns the value, not the
    count or a tuple.
    """
    assert mode([1, 2, 2, 3, 3, 3]) == 3
    assert mode([5, 5, 5]) == 5


def test_mode_empty_raises():
    """mode of an empty list should raise ValueError."""
    with pytest.raises(ValueError, match="empty"):
        mode([])
