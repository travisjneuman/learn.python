"""
Solution: Sum of Digits

Approach: Repeatedly extract the last digit using modulo 10, then remove
it using integer (floor) division by 10. Accumulate the sum until the
number reaches 0.
"""


def sum_of_digits(n: int) -> int:
    total = 0
    while n > 0:
        total += n % 10   # extract last digit
        n = n // 10        # remove last digit
    return total


if __name__ == "__main__":
    assert sum_of_digits(123) == 6
    assert sum_of_digits(9999) == 36
    assert sum_of_digits(0) == 0
    assert sum_of_digits(7) == 7
    assert sum_of_digits(10001) == 2
    print("All tests passed!")
