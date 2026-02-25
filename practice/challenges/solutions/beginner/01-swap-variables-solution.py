"""
Solution: Swap Variables

Approach: Use Python's tuple unpacking to swap values in a single line.
Python evaluates the right side fully before assigning to the left side,
so no temporary variable is needed.
"""


def swap(a, b) -> tuple:
    # Python's tuple unpacking evaluates the right-hand side (b, a) first,
    # creating a tuple, then unpacks it into the left-hand variables.
    a, b = b, a
    return (a, b)


if __name__ == "__main__":
    assert swap(1, 2) == (2, 1)
    assert swap("hello", "world") == ("world", "hello")
    assert swap(5, 5) == (5, 5)
    assert swap(42, "answer") == ("answer", 42)
    print("All tests passed!")
