"""
Fill-In Challenge #6 — Error Handler

Implement the functions below. Each one uses try/except to handle errors.
"""


def safe_divide(a, b):
    """Divide a by b, returning None if division is impossible.

    Args:
        a: Numerator (number).
        b: Denominator (number).

    Returns:
        The result of a / b, or None if b is zero.

    Example:
        safe_divide(10, 3) -> 3.3333...
        safe_divide(10, 0) -> None
    """
    # YOUR CODE HERE
    pass


def safe_int(value):
    """Convert a value to int, returning None on failure.

    Args:
        value: Any value to convert.

    Returns:
        The integer value, or None if conversion fails.

    Example:
        safe_int("42") -> 42
        safe_int("hello") -> None
        safe_int(3.7) -> 3
    """
    # YOUR CODE HERE
    pass


def safe_key_access(data, *keys):
    """Safely navigate nested dictionaries.

    Args:
        data: A (possibly nested) dictionary.
        *keys: One or more keys to traverse.

    Returns:
        The value at the nested key path, or None if any key is missing.

    Example:
        d = {"user": {"name": "Alice", "age": 25}}
        safe_key_access(d, "user", "name") -> "Alice"
        safe_key_access(d, "user", "email") -> None
        safe_key_access(d, "missing") -> None
    """
    # YOUR CODE HERE
    pass


def process_records(records):
    """Process a list of records, collecting successes and errors.

    Each record is a dict with "name" (str) and "score" (str that should
    be convertible to float). Process each record:
    - Convert score to float.
    - If successful, add {"name": name, "score": float_score} to successes.
    - If conversion fails, add {"name": name, "error": str(exception)} to errors.

    Args:
        records: A list of dicts with "name" and "score" keys.

    Returns:
        A tuple of (successes, errors) where each is a list of dicts.

    Example:
        process_records([{"name": "A", "score": "95"}, {"name": "B", "score": "N/A"}])
        -> ([{"name": "A", "score": 95.0}], [{"name": "B", "error": "..."}])
    """
    # YOUR CODE HERE
    pass
