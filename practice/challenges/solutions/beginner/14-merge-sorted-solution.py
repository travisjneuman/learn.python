"""
Solution: Merge Sorted Lists

Approach: Use two index pointers, one for each list. Compare the current
elements and append the smaller one to the result. When one list is
exhausted, append the remainder of the other. This is the merge step
from merge sort, running in O(n + m) time.
"""


def merge_sorted(list_a: list[int], list_b: list[int]) -> list[int]:
    result = []
    i = 0  # pointer into list_a
    j = 0  # pointer into list_b

    # Compare elements from both lists, taking the smaller each time.
    while i < len(list_a) and j < len(list_b):
        if list_a[i] <= list_b[j]:
            result.append(list_a[i])
            i += 1
        else:
            result.append(list_b[j])
            j += 1

    # Append any remaining elements from whichever list is not exhausted.
    while i < len(list_a):
        result.append(list_a[i])
        i += 1
    while j < len(list_b):
        result.append(list_b[j])
        j += 1

    return result


if __name__ == "__main__":
    assert merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
    assert merge_sorted([1, 2, 3], [4, 5, 6]) == [1, 2, 3, 4, 5, 6]
    assert merge_sorted([1, 1, 1], [2, 2, 2]) == [1, 1, 1, 2, 2, 2]
    assert merge_sorted([], [1, 2, 3]) == [1, 2, 3]
    assert merge_sorted([], []) == []
    assert merge_sorted([1], [2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    print("All tests passed!")
