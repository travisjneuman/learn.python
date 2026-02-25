"""
Challenge: Anagram Check
Difficulty: Beginner
Concepts: strings, dictionaries, sorting, character counting
Time: 15 minutes

Check if two strings are anagrams of each other. Two strings are anagrams
if they contain exactly the same characters with the same frequencies.
Ignore case and spaces.

Examples:
    >>> is_anagram("listen", "silent")
    True
    >>> is_anagram("hello", "world")
    False
"""


def is_anagram(s1: str, s2: str) -> bool:
    """Check if two strings are anagrams (ignore case and spaces). Implement this function."""
    # Hint: Count the characters in each string (after normalizing) and compare the counts.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Classic anagram
    assert is_anagram("listen", "silent") is True, "Classic anagram failed"
    # Test 2: Not an anagram
    assert is_anagram("hello", "world") is False, "Not an anagram failed"
    # Test 3: Different cases
    assert is_anagram("Astronomer", "Moon starer") is True, "Case and space failed"
    # Test 4: Empty strings
    assert is_anagram("", "") is True, "Empty strings failed"
    # Test 5: Same word
    assert is_anagram("test", "test") is True, "Same word failed"
    # Test 6: Same letters different counts
    assert is_anagram("aab", "abb") is False, "Different counts failed"
    print("All tests passed!")
