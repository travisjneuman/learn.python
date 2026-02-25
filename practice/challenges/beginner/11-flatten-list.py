"""
Challenge: Flatten List
Difficulty: Beginner
Concepts: recursion, lists, isinstance, nested structures
Time: 25 minutes

Flatten an arbitrarily nested list into a single flat list.
For example, [1, [2, [3, 4], 5], 6] becomes [1, 2, 3, 4, 5, 6].

Examples:
    >>> flatten([1, [2, [3, 4], 5], 6])
    [1, 2, 3, 4, 5, 6]
    >>> flatten([[1, 2], [3, [4, [5]]]])
    [1, 2, 3, 4, 5]
"""


def flatten(nested: list) -> list:
    """Flatten an arbitrarily nested list into a single flat list. Implement this function."""
    # Hint: For each item, check if it is a list (isinstance). If so, recurse. If not, append it.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Mixed nesting
    assert flatten([1, [2, [3, 4], 5], 6]) == [1, 2, 3, 4, 5, 6], "Mixed nesting failed"
    # Test 2: Deep nesting
    assert flatten([[1, 2], [3, [4, [5]]]]) == [1, 2, 3, 4, 5], "Deep nesting failed"
    # Test 3: Already flat
    assert flatten([1, 2, 3]) == [1, 2, 3], "Already flat failed"
    # Test 4: Empty list
    assert flatten([]) == [], "Empty list failed"
    # Test 5: Nested empty lists
    assert flatten([[], [[], []]]) == [], "Nested empty lists failed"
    # Test 6: Single deeply nested element
    assert flatten([[[[1]]]]) == [1], "Single deep element failed"
    print("All tests passed!")
