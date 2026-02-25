"""
Challenge: Palindrome Check
Difficulty: Beginner
Concepts: strings, two-pointer technique, case normalization
Time: 15 minutes

Check if a string is a palindrome. Ignore case and non-alphanumeric characters.
A palindrome reads the same forward and backward.

Examples:
    >>> is_palindrome("racecar")
    True
    >>> is_palindrome("A man, a plan, a canal: Panama")
    True
    >>> is_palindrome("hello")
    False
"""


def is_palindrome(s: str) -> bool:
    """Check if a string is a palindrome (ignoring case and non-alphanumeric chars). Implement this function."""
    # Hint: First strip out non-alphanumeric characters and lowercase everything, then compare.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Simple palindrome
    assert is_palindrome("racecar") is True, "Simple palindrome failed"
    # Test 2: Sentence palindrome
    assert is_palindrome("A man, a plan, a canal: Panama") is True, "Sentence palindrome failed"
    # Test 3: Not a palindrome
    assert is_palindrome("hello") is False, "Not a palindrome failed"
    # Test 4: Empty string
    assert is_palindrome("") is True, "Empty string failed"
    # Test 5: Single character
    assert is_palindrome("a") is True, "Single character failed"
    # Test 6: Numbers and letters
    assert is_palindrome("Was it a car or a cat I saw?") is True, "Complex palindrome failed"
    print("All tests passed!")
