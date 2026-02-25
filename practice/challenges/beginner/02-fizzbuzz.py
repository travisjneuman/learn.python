"""
Challenge: FizzBuzz
Difficulty: Beginner
Concepts: loops, conditionals, modulo operator, list building
Time: 15 minutes

Given an integer n, return a list of strings from 1 to n where:
- Multiples of 3 are replaced with "Fizz"
- Multiples of 5 are replaced with "Buzz"
- Multiples of both 3 and 5 are replaced with "FizzBuzz"
- All other numbers are converted to their string representation

Examples:
    >>> fizzbuzz(5)
    ['1', '2', 'Fizz', '4', 'Buzz']
    >>> fizzbuzz(15)[-1]
    'FizzBuzz'
"""


def fizzbuzz(n: int) -> list[str]:
    """Return FizzBuzz sequence from 1 to n. Implement this function."""
    # Hint: Check divisibility by 15 (both) before checking 3 or 5 individually.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Small range
    assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"], "Small range failed"
    # Test 2: FizzBuzz at 15
    result = fizzbuzz(15)
    assert result[14] == "FizzBuzz", "FizzBuzz at 15 failed"
    assert result[2] == "Fizz", "Fizz at 3 failed"
    assert result[4] == "Buzz", "Buzz at 5 failed"
    # Test 3: Single element
    assert fizzbuzz(1) == ["1"], "Single element failed"
    # Test 4: Length check
    assert len(fizzbuzz(20)) == 20, "Length check failed"
    print("All tests passed!")
