"""
Challenge: Count Vowels
Difficulty: Beginner
Concepts: strings, loops, membership testing, case handling
Time: 10 minutes

Count the number of vowels (a, e, i, o, u) in a string.
The count should be case-insensitive.

Examples:
    >>> count_vowels("hello")
    2
    >>> count_vowels("AEIOU")
    5
"""


def count_vowels(s: str) -> int:
    """Count vowels in a string (case-insensitive). Implement this function."""
    # Hint: Convert to lowercase first, then check each character against "aeiou".
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Basic word
    assert count_vowels("hello") == 2, "Basic word failed"
    # Test 2: All vowels
    assert count_vowels("AEIOU") == 5, "All vowels uppercase failed"
    # Test 3: No vowels
    assert count_vowels("rhythm") == 0, "No vowels failed"
    # Test 4: Empty string
    assert count_vowels("") == 0, "Empty string failed"
    # Test 5: Mixed case
    assert count_vowels("Beautiful Day") == 6, "Mixed case failed"
    print("All tests passed!")
