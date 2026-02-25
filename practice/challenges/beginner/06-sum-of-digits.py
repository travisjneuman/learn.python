"""
Challenge: Sum of Digits
Difficulty: Beginner
Concepts: integers, modulo, floor division, loops
Time: 10 minutes

Given a non-negative integer, return the sum of its digits.
Do not convert the integer to a string -- use arithmetic only.

Examples:
    >>> sum_of_digits(123)
    6
    >>> sum_of_digits(9999)
    36
"""


def sum_of_digits(n: int) -> int:
    """Sum all digits of a non-negative integer using arithmetic. Implement this function."""
    # Hint: Use n % 10 to get the last digit and n // 10 to remove it.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Basic number
    assert sum_of_digits(123) == 6, "Basic number failed"
    # Test 2: All nines
    assert sum_of_digits(9999) == 36, "All nines failed"
    # Test 3: Zero
    assert sum_of_digits(0) == 0, "Zero failed"
    # Test 4: Single digit
    assert sum_of_digits(7) == 7, "Single digit failed"
    # Test 5: Large number
    assert sum_of_digits(10001) == 2, "Large number failed"
    print("All tests passed!")
