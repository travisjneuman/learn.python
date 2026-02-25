"""
Challenge: Find Maximum
Difficulty: Beginner
Concepts: lists, iteration, comparison, edge cases
Time: 10 minutes

Find the maximum value in a list of numbers without using the built-in max() function.
Raise a ValueError if the list is empty.

Examples:
    >>> find_max([3, 1, 4, 1, 5, 9])
    9
    >>> find_max([-5, -1, -8])
    -1
"""


def find_max(numbers: list[int | float]) -> int | float:
    """Find the maximum value in a list without using max(). Implement this function."""
    # Hint: Start with the first element as your candidate, then compare against each remaining element.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Positive numbers
    assert find_max([3, 1, 4, 1, 5, 9]) == 9, "Positive numbers failed"
    # Test 2: Negative numbers
    assert find_max([-5, -1, -8]) == -1, "Negative numbers failed"
    # Test 3: Single element
    assert find_max([42]) == 42, "Single element failed"
    # Test 4: Mixed positive and negative
    assert find_max([-10, 0, 10]) == 10, "Mixed numbers failed"
    # Test 5: Empty list raises ValueError
    try:
        find_max([])
        assert False, "Empty list should raise ValueError"
    except ValueError:
        pass
    print("All tests passed!")
