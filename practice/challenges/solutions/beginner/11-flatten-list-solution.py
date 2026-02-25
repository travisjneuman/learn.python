"""
Solution: Flatten List

Approach: Use recursion. For each element, check if it is a list using
isinstance. If it is, recursively flatten it and extend the result.
If it is not a list, append it directly. This handles arbitrary nesting depth.
"""


def flatten(nested: list) -> list:
    result = []
    for item in nested:
        if isinstance(item, list):
            # Recurse into the sublist and add all its flattened elements
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


if __name__ == "__main__":
    assert flatten([1, [2, [3, 4], 5], 6]) == [1, 2, 3, 4, 5, 6]
    assert flatten([[1, 2], [3, [4, [5]]]]) == [1, 2, 3, 4, 5]
    assert flatten([1, 2, 3]) == [1, 2, 3]
    assert flatten([]) == []
    assert flatten([[], [[], []]]) == []
    assert flatten([[[[1]]]]) == [1]
    print("All tests passed!")
