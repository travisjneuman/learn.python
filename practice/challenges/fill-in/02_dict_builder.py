"""
Fill-In Challenge #2 — Dictionary Builder

Implement the functions below. Each one builds or transforms dictionaries.
"""


def zip_to_dict(keys, values):
    """Build a dictionary from two parallel lists.

    Args:
        keys: A list of strings to use as dictionary keys.
        values: A list of values (same length as keys).

    Returns:
        A dictionary mapping each key to its corresponding value.

    Raises:
        ValueError: If keys and values have different lengths.

    Example:
        zip_to_dict(["a", "b", "c"], [1, 2, 3]) -> {"a": 1, "b": 2, "c": 3}
    """
    # YOUR CODE HERE
    pass


def invert_dict(d):
    """Swap keys and values in a dictionary.

    Args:
        d: A dictionary with hashable values.

    Returns:
        A new dictionary where original values become keys and vice versa.

    Example:
        invert_dict({"a": 1, "b": 2}) -> {1: "a", 2: "b"}
    """
    # YOUR CODE HERE
    pass


def merge_dicts(dict_a, dict_b):
    """Merge two dictionaries. Values from dict_b win on conflicts.

    Args:
        dict_a: First dictionary.
        dict_b: Second dictionary (takes priority).

    Returns:
        A new dictionary containing all keys from both inputs.

    Example:
        merge_dicts({"a": 1, "b": 2}, {"b": 3, "c": 4}) -> {"a": 1, "b": 3, "c": 4}
    """
    # YOUR CODE HERE
    pass


def group_by(items, key_func):
    """Group a list of items by the result of key_func.

    Args:
        items: A list of items.
        key_func: A function that takes an item and returns a grouping key.

    Returns:
        A dictionary mapping each key to a list of items with that key.

    Example:
        group_by(["ant", "bee", "ape", "bat"], lambda w: w[0])
        -> {"a": ["ant", "ape"], "b": ["bee", "bat"]}
    """
    # YOUR CODE HERE
    pass
