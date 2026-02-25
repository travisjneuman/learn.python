"""
Solution: Remove Duplicates

Approach: Use a set to track values already seen. Iterate through the list
and only append items that are not yet in the seen set. This preserves
insertion order while achieving O(1) membership checks.
"""


def remove_duplicates(items: list) -> list:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


if __name__ == "__main__":
    assert remove_duplicates([1, 2, 2, 3, 1, 4]) == [1, 2, 3, 4]
    assert remove_duplicates(["a", "b", "a", "c"]) == ["a", "b", "c"]
    assert remove_duplicates([1, 2, 3]) == [1, 2, 3]
    assert remove_duplicates([5, 5, 5, 5]) == [5]
    assert remove_duplicates([]) == []
    print("All tests passed!")
