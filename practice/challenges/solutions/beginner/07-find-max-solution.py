"""
Solution: Find Maximum

Approach: Handle the empty list edge case with a ValueError. Start with the
first element as the current maximum, then compare against every remaining
element, updating the maximum when a larger value is found.
"""


def find_max(numbers: list[int | float]) -> int | float:
    if not numbers:
        raise ValueError("Cannot find max of an empty list")

    current_max = numbers[0]
    for num in numbers[1:]:
        if num > current_max:
            current_max = num
    return current_max


if __name__ == "__main__":
    assert find_max([3, 1, 4, 1, 5, 9]) == 9
    assert find_max([-5, -1, -8]) == -1
    assert find_max([42]) == 42
    assert find_max([-10, 0, 10]) == 10
    try:
        find_max([])
        assert False, "Empty list should raise ValueError"
    except ValueError:
        pass
    print("All tests passed!")
