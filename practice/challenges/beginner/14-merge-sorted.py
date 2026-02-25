"""
Challenge: Merge Sorted Lists
Difficulty: Beginner
Concepts: two-pointer technique, lists, comparison, while loops
Time: 20 minutes

Merge two sorted lists into a single sorted list. Do not use the built-in
sorted() function or .sort() method. Use the two-pointer technique.

Examples:
    >>> merge_sorted([1, 3, 5], [2, 4, 6])
    [1, 2, 3, 4, 5, 6]
    >>> merge_sorted([1, 1, 1], [2, 2, 2])
    [1, 1, 1, 2, 2, 2]
"""


def merge_sorted(list_a: list[int], list_b: list[int]) -> list[int]:
    """Merge two sorted lists into one sorted list. Implement this function."""
    # Hint: Use two index variables (one per list), always append the smaller current element.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Interleaved
    assert merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6], "Interleaved failed"
    # Test 2: Non-overlapping
    assert merge_sorted([1, 2, 3], [4, 5, 6]) == [1, 2, 3, 4, 5, 6], "Non-overlapping failed"
    # Test 3: Duplicates
    assert merge_sorted([1, 1, 1], [2, 2, 2]) == [1, 1, 1, 2, 2, 2], "Duplicates failed"
    # Test 4: One empty list
    assert merge_sorted([], [1, 2, 3]) == [1, 2, 3], "One empty failed"
    # Test 5: Both empty
    assert merge_sorted([], []) == [], "Both empty failed"
    # Test 6: Different lengths
    assert merge_sorted([1], [2, 3, 4, 5]) == [1, 2, 3, 4, 5], "Different lengths failed"
    print("All tests passed!")
