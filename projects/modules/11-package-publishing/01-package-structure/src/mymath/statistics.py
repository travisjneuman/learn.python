"""
statistics.py — Basic statistical functions.

This module provides mean, median, and mode calculations.
It demonstrates a second module within the same package.
"""

from collections import Counter


def mean(numbers):
    """
    Calculate the arithmetic mean (average) of a list of numbers.

    Example: mean([1, 2, 3, 4, 5]) → 3.0
    """
    if not numbers:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(numbers) / len(numbers)


def median(numbers):
    """
    Calculate the median (middle value) of a list of numbers.

    For an odd-length list, this is the middle element.
    For an even-length list, this is the average of the two middle elements.

    Example: median([1, 3, 5]) → 3
    Example: median([1, 3, 5, 7]) → 4.0
    """
    if not numbers:
        raise ValueError("Cannot calculate median of empty list")

    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2

    if n % 2 == 0:
        # Even length: average the two middle values.
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
    else:
        # Odd length: return the middle value.
        return sorted_nums[mid]


def mode(numbers):
    """
    Find the most common value in a list of numbers.

    If there is a tie, returns the one that appears first.

    Example: mode([1, 2, 2, 3, 3, 3]) → 3
    """
    if not numbers:
        raise ValueError("Cannot calculate mode of empty list")

    # Counter counts how many times each value appears.
    counts = Counter(numbers)

    # most_common(1) returns a list of (value, count) tuples.
    return counts.most_common(1)[0][0]


if __name__ == "__main__":
    sample = [4, 8, 15, 16, 23, 42, 23]
    print(f"Sample data: {sample}")
    print(f"Mean: {mean(sample)}")
    print(f"Median: {median(sample)}")
    print(f"Mode: {mode(sample)}")
