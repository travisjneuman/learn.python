"""
Challenge 05: Type Narrowing
Difficulty: Level 7
Topic: Use TypeGuard and type narrowing patterns

Write type guard functions that narrow union types so that downstream code
can safely assume a specific type. This challenge focuses on runtime checks
that also inform static type checkers.

Concepts: TypeGuard, isinstance, Union types, type narrowing.
Review: concepts/types-and-conversions.md

Instructions:
    1. Implement `is_string_list` — a TypeGuard that checks whether a value
       is a list[str].
    2. Implement `is_positive_int` — a TypeGuard for positive integers
       (must be int, not bool, and > 0).
    3. Implement `safe_process` — uses the guards to process mixed input.
"""

from typing import TypeGuard


def is_string_list(value: object) -> TypeGuard[list[str]]:
    """Return True if *value* is a list where every element is a str."""
    # YOUR CODE HERE
    ...


def is_positive_int(value: object) -> TypeGuard[int]:
    """Return True if *value* is an int (not bool) greater than zero."""
    # YOUR CODE HERE
    ...


def safe_process(data: object) -> str:
    """Process *data* and return a descriptive string.

    Rules:
    - If data is a list of strings, return them joined with ", ".
    - If data is a positive int, return "positive:<value>".
    - If data is a dict, return "keys:" followed by sorted keys joined with ",".
    - Otherwise return "unknown".
    """
    # YOUR CODE HERE
    ...


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- is_string_list ---
    assert is_string_list(["a", "b", "c"]) is True
    assert is_string_list([]) is True  # empty list qualifies
    assert is_string_list([1, 2, 3]) is False
    assert is_string_list(["a", 1]) is False
    assert is_string_list("not a list") is False
    assert is_string_list(None) is False

    # --- is_positive_int ---
    assert is_positive_int(5) is True
    assert is_positive_int(1) is True
    assert is_positive_int(0) is False
    assert is_positive_int(-3) is False
    assert is_positive_int(True) is False  # bool is a subclass of int
    assert is_positive_int(3.14) is False
    assert is_positive_int("5") is False

    # --- safe_process ---
    assert safe_process(["hello", "world"]) == "hello, world"
    assert safe_process([]) == ""
    assert safe_process(42) == "positive:42"
    assert safe_process({"b": 1, "a": 2}) == "keys:a,b"
    assert safe_process(-5) == "unknown"
    assert safe_process(True) == "unknown"
    assert safe_process(3.14) == "unknown"
    assert safe_process(None) == "unknown"

    print("All tests passed.")
