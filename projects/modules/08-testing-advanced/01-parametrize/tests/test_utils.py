"""
Tests for Project 01 — Parametrize

This file demonstrates @pytest.mark.parametrize, which lets you run one
test function with many different inputs. Instead of writing ten separate
test functions that all look the same, you write one and give it a table
of inputs and expected outputs.

Run with: pytest tests/test_utils.py -v
The -v flag shows each parametrize case as a separate line in the output.
"""

import pytest

# Import the functions we are testing. The ".." means "go up one directory"
# but pytest handles this automatically when you run from the project root.
from project import validate_email, celsius_to_fahrenheit, is_palindrome, clamp


# ── validate_email ──────────────────────────────────────────────────────
# WHY: Email validation has many edge cases. A parametrized test lets us
# list them all in one place and add new cases without writing new functions.

@pytest.mark.parametrize(
    "email, expected",
    [
        # --- Valid emails ---
        ("user@example.com", True),           # Standard email
        ("name.tag@domain.org", True),        # Dots in local part
        ("user+filter@gmail.com", True),      # Plus addressing (common in Gmail)
        ("x@y.io", True),                     # Minimal valid email
        ("UPPER@CASE.COM", True),             # Case should not matter for format

        # --- Invalid emails ---
        ("missing-at-sign", False),           # No @ symbol at all
        ("", False),                          # Empty string
        ("@no-local-part.com", False),        # Nothing before @
        ("spaces in@email.com", False),       # Spaces are not allowed
        ("double@@at.com", False),            # Two @ symbols
    ],
    # ids makes the test output readable. Without it, pytest shows the raw
    # parameter tuple. With it, you get a human-friendly label.
    ids=[
        "valid-user@example.com",
        "valid-name.tag@domain.org",
        "valid-plus-addressing",
        "valid-minimal",
        "valid-uppercase",
        "invalid-missing-at",
        "invalid-empty-string",
        "invalid-no-local-part",
        "invalid-spaces",
        "invalid-double-at",
    ],
)
def test_validate_email(email, expected):
    """Each row in the parametrize table becomes a separate test case."""
    assert validate_email(email) == expected


# WHY: We also want to make sure non-string inputs are handled gracefully.
# This is a separate parametrize because the input type is different.

@pytest.mark.parametrize(
    "bad_input",
    [None, 42, [], {}],
    ids=["none", "integer", "list", "dict"],
)
def test_validate_email_rejects_non_strings(bad_input):
    """Non-string inputs should always return False, never crash."""
    assert validate_email(bad_input) is False


# ── celsius_to_fahrenheit ───────────────────────────────────────────────
# WHY: Temperature conversion has well-known reference points. We test
# the famous ones (freezing, boiling, body temp, the crossover point)
# to make sure the formula is implemented correctly.

@pytest.mark.parametrize(
    "celsius, expected_fahrenheit",
    [
        (0, 32.0),        # Freezing point of water
        (100, 212.0),     # Boiling point of water
        (-40, -40.0),     # The crossover point (same in both scales!)
        (37, 98.6),       # Human body temperature
        (-273.15, -459.67),  # Absolute zero
    ],
    ids=["freezing", "boiling", "crossover", "body-temp", "absolute-zero"],
)
def test_celsius_to_fahrenheit(celsius, expected_fahrenheit):
    """Verify known temperature conversion pairs."""
    # We use pytest.approx because floating-point math can introduce tiny
    # rounding errors. pytest.approx checks that the values are "close enough"
    # (within a very small tolerance, by default 1e-6).
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected_fahrenheit)


# ── is_palindrome ───────────────────────────────────────────────────────
# WHY: Palindrome checking involves string cleaning (removing punctuation,
# ignoring case). We need to test both the core logic and the cleaning.

@pytest.mark.parametrize(
    "text, expected",
    [
        ("racecar", True),                          # Classic palindrome
        ("hello", False),                           # Clearly not a palindrome
        ("A man a plan a canal Panama", True),      # Sentence palindrome with spaces
        ("Was it a car or a cat I saw?", True),     # Punctuation and mixed case
        ("", True),                                 # Empty string is a palindrome
        ("a", True),                                # Single character
        ("ab", False),                              # Two different characters
        ("Madam", True),                            # Mixed case palindrome
    ],
    ids=[
        "racecar",
        "hello",
        "sentence-palindrome",
        "punctuation-mixed-case",
        "empty-string",
        "single-char",
        "two-different-chars",
        "mixed-case-madam",
    ],
)
def test_is_palindrome(text, expected):
    """Test palindrome detection with various inputs including edge cases."""
    assert is_palindrome(text) == expected


# ── clamp ───────────────────────────────────────────────────────────────
# WHY: Clamp has three distinct behaviors (below min, above max, in range)
# plus edge cases at the boundaries. Parametrize lets us cover them all
# in a compact table.

@pytest.mark.parametrize(
    "value, min_val, max_val, expected",
    [
        (5, 0, 10, 5),       # Value already in range — returned unchanged
        (-3, 0, 10, 0),      # Below minimum — clamped up to min
        (15, 0, 10, 10),     # Above maximum — clamped down to max
        (0, 0, 10, 0),       # Exactly at minimum — boundary case
        (10, 0, 10, 10),     # Exactly at maximum — boundary case
        (5, 5, 5, 5),        # Min equals max — only one valid value
        (-100, -50, 50, -50),  # Negative range
        (3.5, 0, 10, 3.5),  # Float value in range
    ],
    ids=[
        "in-range",
        "below-minimum",
        "above-maximum",
        "at-minimum",
        "at-maximum",
        "single-point-range",
        "negative-range",
        "float-value",
    ],
)
def test_clamp(value, min_val, max_val, expected):
    """Test clamp with values inside, outside, and at the boundaries."""
    assert clamp(value, min_val, max_val) == expected


# WHY: Clamp should raise an error when min > max. This is a separate test
# because we are testing for an exception, not a return value.

def test_clamp_raises_on_invalid_range():
    """Passing min > max is a programming error and should raise ValueError."""
    with pytest.raises(ValueError, match="must not be greater than"):
        clamp(5, 10, 0)
