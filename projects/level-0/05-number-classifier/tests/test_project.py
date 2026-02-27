"""Tests for Number Classifier."""

import pytest

from project import classify_number, is_even, is_prime


def test_is_even() -> None:
    """Even numbers should return True, odd numbers False."""
    assert is_even(4) is True
    assert is_even(7) is False
    assert is_even(0) is True


def test_is_prime_small_values() -> None:
    """Check primality for well-known small numbers."""
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(4) is False
    assert is_prime(17) is True
    assert is_prime(1) is False
    assert is_prime(0) is False
    assert is_prime(-5) is False


def test_classify_positive_odd_prime() -> None:
    """7 is positive, odd, and prime."""
    result = classify_number(7)
    assert result["sign"] == "positive"
    assert result["parity"] == "odd"
    assert result["prime"] is True


def test_classify_zero() -> None:
    """Zero is zero, even, and not prime."""
    result = classify_number(0)
    assert result["sign"] == "zero"
    assert result["parity"] == "even"
    assert result["prime"] is False


def test_classify_negative() -> None:
    """Negative numbers should be classified as negative and not prime."""
    result = classify_number(-10)
    assert result["sign"] == "negative"
    assert result["prime"] is False


def test_empty_input_does_not_crash() -> None:
    """Empty string input should be handled gracefully without crashing.

    The interactive loop tries int(text) on user input.  An empty string
    raises ValueError, which the program catches and prints a friendly
    message.  This test verifies that conversion path: int('') raises
    ValueError (so the except branch runs), and the program continues.
    """
    import subprocess
    import sys
    from pathlib import Path

    project_dir = Path(__file__).resolve().parent.parent
    result = subprocess.run(
        [sys.executable, "project.py"],
        input="\nquit\n",
        capture_output=True,
        text=True,
        cwd=str(project_dir),
        timeout=10,
    )

    # The program should exit cleanly (return code 0), not crash.
    assert result.returncode == 0
    # The error message for invalid input should appear in the output.
    assert "not a valid integer" in result.stdout
