"""
Fill-In Challenge #1 — List Filtering

Implement the functions below. Each one filters or transforms a list
in a specific way. Read the docstrings for exact requirements.
"""


def filter_positive(numbers):
    """Return a new list containing only the positive numbers.

    Args:
        numbers: A list of integers (may include negative, zero, positive).

    Returns:
        A list of integers greater than zero, in original order.

    Example:
        filter_positive([3, -1, 0, 7, -5, 2]) -> [3, 7, 2]
    """
    # YOUR CODE HERE
    pass


def filter_long_words(words, min_length):
    """Return words that have at least min_length characters.

    Args:
        words: A list of strings.
        min_length: Minimum number of characters (inclusive).

    Returns:
        A list of strings with length >= min_length.

    Example:
        filter_long_words(["hi", "hello", "hey", "howdy"], 4) -> ["hello", "howdy"]
    """
    # YOUR CODE HERE
    pass


def filter_by_key(records, key, value):
    """Return records where record[key] equals value.

    Args:
        records: A list of dictionaries.
        key: The dictionary key to check.
        value: The value to match.

    Returns:
        A list of dictionaries where record[key] == value.

    Example:
        data = [{"name": "Alice", "role": "admin"}, {"name": "Bob", "role": "user"}]
        filter_by_key(data, "role", "admin") -> [{"name": "Alice", "role": "admin"}]
    """
    # YOUR CODE HERE
    pass


def unique_sorted(items):
    """Return a sorted list with duplicates removed.

    Args:
        items: A list of comparable items (all same type).

    Returns:
        A new sorted list with no duplicates.

    Example:
        unique_sorted([3, 1, 2, 3, 1]) -> [1, 2, 3]
    """
    # YOUR CODE HERE
    pass
