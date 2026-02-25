"""
Tests for Project 01 — Parametrize (test_project.py)

Additional parametrized tests that complement test_utils.py. These focus
on edge cases and boundary conditions for each utility function.

Why more tests?
    The original test_utils.py demonstrates the @pytest.mark.parametrize
    pattern. This file adds edge-case coverage that a learner might add
    after understanding the basics. It shows that you can always add more
    test cases to a parametrized test without writing new test functions.

Run with: pytest tests/test_project.py -v
"""

import pytest

from project import validate_email, celsius_to_fahrenheit, is_palindrome, clamp


# ── validate_email: edge cases ─────────────────────────────────────────

@pytest.mark.parametrize(
    "email, expected",
    [
        # WHY: These test boundary cases that are easy to get wrong with regex.
        ("a@b.c", True),                    # Minimal valid email
        ("user@example.com", True),          # Standard email
        ("user+tag@domain.org", True),       # Plus addressing
        ("", False),                          # Empty string
        ("no-at-sign", False),                # Missing @ symbol
        ("@missing-local.com", False),        # Nothing before @
        ("missing-domain@", False),           # Nothing after @
        ("double@@at.com", False),            # Two @ symbols
        ("spaces in@email.com", False),       # Spaces are invalid
        (123, False),                         # Non-string input
        (None, False),                        # None input
    ],
    ids=[
        "minimal-valid", "standard", "plus-addressing",
        "empty-string", "no-at", "no-local-part", "no-domain",
        "double-at", "spaces", "integer-input", "none-input",
    ],
)
def test_validate_email_edge_cases(email, expected):
    """Verify email validation handles various edge cases.

    WHY: Email validation is notoriously tricky. Each test case targets
    a specific failure mode that a naive implementation might miss.
    The 'ids' parameter makes pytest output readable: instead of showing
    the raw inputs, it shows descriptive names like 'no-at' or 'spaces'.
    """
    assert validate_email(email) == expected


# ── celsius_to_fahrenheit: known conversion pairs ──────────────────────

@pytest.mark.parametrize(
    "celsius, expected_fahrenheit",
    [
        # WHY: These are well-known reference points for temperature conversion.
        # Using known physical constants makes the test self-documenting.
        (0, 32),        # Freezing point of water
        (100, 212),     # Boiling point of water
        (-40, -40),     # The point where Celsius and Fahrenheit are equal
        (37, 98.6),     # Human body temperature
        (-273.15, -459.67),  # Absolute zero
    ],
    ids=["freezing", "boiling", "equal-point", "body-temp", "absolute-zero"],
)
def test_celsius_to_fahrenheit_known_values(celsius, expected_fahrenheit):
    """Verify temperature conversion against known physical reference points.

    WHY: The formula F = C * 9/5 + 32 is simple but easy to type wrong
    (e.g., 5/9 instead of 9/5). Known reference points catch formula errors.
    """
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected_fahrenheit)


# ── is_palindrome: variety of inputs ───────────────────────────────────

@pytest.mark.parametrize(
    "text, expected",
    [
        # WHY: Palindrome detection must handle punctuation, case, and spaces.
        ("racecar", True),                          # Simple palindrome
        ("hello", False),                            # Not a palindrome
        ("A man a plan a canal Panama", True),       # Classic with spaces
        ("Was it a car or a cat I saw?", True),     # With punctuation
        ("", True),                                   # Empty string (trivially true)
        ("a", True),                                  # Single character
        ("ab", False),                                # Two different characters
        ("Aba", True),                                # Mixed case
    ],
    ids=[
        "simple", "not-palindrome", "classic-phrase", "punctuation",
        "empty", "single-char", "two-chars", "mixed-case",
    ],
)
def test_is_palindrome_various_inputs(text, expected):
    """Verify palindrome detection with diverse inputs.

    WHY: The function strips non-alphanumeric characters and lowercases
    before comparing. Testing with punctuation and mixed case verifies
    that the cleaning step works correctly.
    """
    assert is_palindrome(text) == expected


# ── clamp: boundary conditions ─────────────────────────────────────────

@pytest.mark.parametrize(
    "value, min_val, max_val, expected",
    [
        # WHY: Boundary conditions are where off-by-one errors hide.
        (5, 0, 10, 5),      # Within range — should return unchanged
        (-5, 0, 10, 0),     # Below range — should clamp to min
        (15, 0, 10, 10),    # Above range — should clamp to max
        (0, 0, 10, 0),      # Exactly at min — boundary case
        (10, 0, 10, 10),    # Exactly at max — boundary case
        (5, 5, 5, 5),       # Min equals max — only one valid value
        (-10, -20, -5, -10),  # Negative range
    ],
    ids=[
        "in-range", "below-min", "above-max", "at-min",
        "at-max", "min-equals-max", "negative-range",
    ],
)
def test_clamp_boundary_conditions(value, min_val, max_val, expected):
    """Verify clamp handles boundary conditions correctly.

    WHY: Clamp is commonly used in game development and UI code where
    off-by-one errors cause visible bugs (e.g., a slider going past its
    maximum). Testing exact boundaries catches these errors.
    """
    assert clamp(value, min_val, max_val) == expected


def test_clamp_raises_on_invalid_range():
    """clamp should raise ValueError when min_val > max_val.

    WHY: Passing min > max is a programming error. Silently returning
    garbage would hide the bug. Raising an exception makes it visible.
    """
    with pytest.raises(ValueError, match="must not be greater"):
        clamp(5, 10, 0)
