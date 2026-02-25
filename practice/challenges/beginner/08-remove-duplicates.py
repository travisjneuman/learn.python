"""
Challenge: Remove Duplicates
Difficulty: Beginner
Concepts: lists, sets, order preservation, membership testing
Time: 15 minutes

Remove duplicate values from a list while preserving the original order.
The first occurrence of each value should be kept.

Examples:
    >>> remove_duplicates([1, 2, 2, 3, 1, 4])
    [1, 2, 3, 4]
    >>> remove_duplicates(["a", "b", "a", "c"])
    ['a', 'b', 'c']
"""


def remove_duplicates(items: list) -> list:
    """Remove duplicates from a list, preserving order. Implement this function."""
    # Hint: Use a set to track what you have already seen as you iterate.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Integers with duplicates
    assert remove_duplicates([1, 2, 2, 3, 1, 4]) == [1, 2, 3, 4], "Integer duplicates failed"
    # Test 2: Strings
    assert remove_duplicates(["a", "b", "a", "c"]) == ["a", "b", "c"], "String duplicates failed"
    # Test 3: No duplicates
    assert remove_duplicates([1, 2, 3]) == [1, 2, 3], "No duplicates failed"
    # Test 4: All duplicates
    assert remove_duplicates([5, 5, 5, 5]) == [5], "All duplicates failed"
    # Test 5: Empty list
    assert remove_duplicates([]) == [], "Empty list failed"
    print("All tests passed!")
