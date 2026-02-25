"""
Challenge: Binary Search
Difficulty: Beginner
Concepts: algorithms, while loops, indexing, divide and conquer
Time: 25 minutes

Implement binary search on a sorted list. Return the index of the target
value if found, or -1 if the target is not in the list.

Examples:
    >>> binary_search([1, 3, 5, 7, 9], 5)
    2
    >>> binary_search([1, 3, 5, 7, 9], 4)
    -1
"""


def binary_search(sorted_list: list[int], target: int) -> int:
    """Find the index of target in a sorted list, or -1 if not found. Implement this function."""
    # Hint: Maintain low and high pointers. Check the middle element and narrow the range.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Target exists in middle
    assert binary_search([1, 3, 5, 7, 9], 5) == 2, "Middle element failed"
    # Test 2: Target not found
    assert binary_search([1, 3, 5, 7, 9], 4) == -1, "Not found failed"
    # Test 3: Target at start
    assert binary_search([1, 3, 5, 7, 9], 1) == 0, "First element failed"
    # Test 4: Target at end
    assert binary_search([1, 3, 5, 7, 9], 9) == 4, "Last element failed"
    # Test 5: Empty list
    assert binary_search([], 5) == -1, "Empty list failed"
    # Test 6: Single element found
    assert binary_search([42], 42) == 0, "Single element found failed"
    # Test 7: Single element not found
    assert binary_search([42], 10) == -1, "Single element not found failed"
    print("All tests passed!")
