"""
Challenge: Swap Variables
Difficulty: Beginner
Concepts: variables, tuple unpacking, arithmetic tricks
Time: 10 minutes

Swap two variables without using a temporary third variable.
Return them as a tuple (b, a) where the values have been exchanged.

Examples:
    >>> swap(1, 2)
    (2, 1)
    >>> swap("hello", "world")
    ('world', 'hello')
"""


def swap(a, b) -> tuple:
    """Swap two values and return them as a tuple. Implement this function."""
    # Hint: Python supports simultaneous assignment with commas.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Basic integers
    assert swap(1, 2) == (2, 1), "Basic integer swap failed"
    # Test 2: Strings
    assert swap("hello", "world") == ("world", "hello"), "String swap failed"
    # Test 3: Same values
    assert swap(5, 5) == (5, 5), "Same value swap failed"
    # Test 4: Mixed types
    assert swap(42, "answer") == ("answer", 42), "Mixed type swap failed"
    print("All tests passed!")
