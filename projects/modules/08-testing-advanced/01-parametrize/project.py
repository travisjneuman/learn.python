"""
Project 01 — Parametrize

A collection of small utility functions designed to be tested with
@pytest.mark.parametrize. Each function is simple enough to understand
quickly, but has enough edge cases to make parametrized testing valuable.

These are the kind of utility functions you find in real codebases —
small, pure, and used everywhere. Getting their edge cases right matters.
"""

import re


def validate_email(address):
    """
    Check whether a string looks like a valid email address.

    This is a simplified check — real email validation is surprisingly
    complex (RFC 5321 allows things you would never expect). We check for:
    - At least one @ symbol
    - Something before the @
    - Something after the @ that contains a dot

    Returns True if the address looks valid, False otherwise.
    """
    # An empty string or non-string input is never a valid email.
    if not isinstance(address, str) or not address:
        return False

    # Use a simple regex pattern. This is not perfect, but it catches
    # the most common mistakes: missing @, missing domain, missing dot.
    # The pattern says: one or more characters, then @, then one or more
    # characters, then a dot, then one or more characters.
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, address))


def celsius_to_fahrenheit(celsius):
    """
    Convert a temperature from Celsius to Fahrenheit.

    The formula is: F = C * 9/5 + 32

    This is a textbook pure function — same input always gives same output,
    no side effects. Perfect for parametrized testing because you can list
    known conversion pairs and verify them all at once.
    """
    # The formula comes from the relationship between the two scales.
    # Water freezes at 0°C / 32°F and boils at 100°C / 212°F.
    return celsius * 9 / 5 + 32


def is_palindrome(text):
    """
    Check whether a string reads the same forwards and backwards.

    Ignores case and non-alphanumeric characters, so "A man, a plan,
    a canal: Panama" is considered a palindrome.

    Returns True if the text is a palindrome, False otherwise.
    """
    # Strip out everything that is not a letter or digit, then lowercase.
    # This lets us handle punctuation and mixed case gracefully.
    cleaned = re.sub(r"[^a-zA-Z0-9]", "", text).lower()

    # An empty string after cleaning is technically a palindrome
    # (it reads the same in both directions: nothing).
    if not cleaned:
        return True

    # Compare the string to its reverse. Python's slice [::-1] reverses
    # a string by stepping backwards through every character.
    return cleaned == cleaned[::-1]


def clamp(value, min_val, max_val):
    """
    Restrict a number to a given range.

    If value is below min_val, return min_val.
    If value is above max_val, return max_val.
    Otherwise, return value unchanged.

    This is a common utility in game development, UI code, and data
    processing — anywhere you need to keep a number within bounds.
    """
    # Validate that the range makes sense. If someone passes min > max,
    # that is a programming error and we should not silently return garbage.
    if min_val > max_val:
        raise ValueError(
            f"min_val ({min_val}) must not be greater than max_val ({max_val})"
        )

    # Python's built-in min() and max() make this a one-liner.
    # max(value, min_val) ensures we are at least min_val.
    # min(..., max_val) ensures we do not exceed max_val.
    return min(max(value, min_val), max_val)


# ── Demo ────────────────────────────────────────────────────────────────
# Run this file directly to see the functions in action.
# The real tests are in tests/test_utils.py — run them with pytest.

if __name__ == "__main__":
    # Email validation examples
    print("=== Email Validation ===")
    test_emails = ["user@example.com", "bad-email", "", "a@b.c", "@missing.com"]
    for email in test_emails:
        print(f"  {email!r:30s} -> {validate_email(email)}")

    # Temperature conversion examples
    print("\n=== Celsius to Fahrenheit ===")
    test_temps = [0, 100, -40, 37]
    for c in test_temps:
        print(f"  {c}°C -> {celsius_to_fahrenheit(c)}°F")

    # Palindrome examples
    print("\n=== Palindrome Check ===")
    test_words = ["racecar", "hello", "A man a plan a canal Panama", ""]
    for word in test_words:
        print(f"  {word!r:40s} -> {is_palindrome(word)}")

    # Clamp examples
    print("\n=== Clamp ===")
    test_clamps = [(5, 0, 10), (-3, 0, 10), (15, 0, 10), (5, 5, 5)]
    for value, lo, hi in test_clamps:
        print(f"  clamp({value}, {lo}, {hi}) -> {clamp(value, lo, hi)}")
