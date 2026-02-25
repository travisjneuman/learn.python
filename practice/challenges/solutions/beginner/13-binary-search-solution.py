"""
Solution: Binary Search

Approach: Maintain two pointers (low and high) representing the search range.
Calculate the midpoint, compare the target to the middle element, and narrow
the range by half each iteration. This gives O(log n) time complexity.
"""


def binary_search(sorted_list: list[int], target: int) -> int:
    low = 0
    high = len(sorted_list) - 1

    while low <= high:
        mid = (low + high) // 2
        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            # Target is in the right half
            low = mid + 1
        else:
            # Target is in the left half
            high = mid - 1

    return -1  # Target not found


if __name__ == "__main__":
    assert binary_search([1, 3, 5, 7, 9], 5) == 2
    assert binary_search([1, 3, 5, 7, 9], 4) == -1
    assert binary_search([1, 3, 5, 7, 9], 1) == 0
    assert binary_search([1, 3, 5, 7, 9], 9) == 4
    assert binary_search([], 5) == -1
    assert binary_search([42], 42) == 0
    assert binary_search([42], 10) == -1
    print("All tests passed!")
