"""
Challenge: Reverse String
Difficulty: Beginner
Concepts: strings, loops, iteration, string building
Time: 15 minutes

Reverse a string without using slice notation ([::-1]).
You may use loops, recursion, or any other approach.

Examples:
    >>> reverse_string("hello")
    'olleh'
    >>> reverse_string("Python")
    'nohtyP'
"""


def reverse_string(s: str) -> str:
    """Reverse a string without using [::-1]. Implement this function."""
    # Hint: Build a new string by iterating from the end, or use a loop to prepend characters.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Basic word
    assert reverse_string("hello") == "olleh", "Basic word failed"
    # Test 2: Palindrome
    assert reverse_string("racecar") == "racecar", "Palindrome failed"
    # Test 3: Empty string
    assert reverse_string("") == "", "Empty string failed"
    # Test 4: Single character
    assert reverse_string("x") == "x", "Single character failed"
    # Test 5: Spaces and punctuation
    assert reverse_string("hi there!") == "!ereht ih", "Spaces and punctuation failed"
    print("All tests passed!")
