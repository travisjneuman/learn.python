"""
Solution: FizzBuzz

Approach: Iterate from 1 to n. Check divisibility by 15 first (both 3 and 5),
then by 3, then by 5. The order matters because 15 is divisible by both.
"""


def fizzbuzz(n: int) -> list[str]:
    result = []
    for i in range(1, n + 1):
        # Check the combined case first -- a number divisible by both 3 and 5
        # is also divisible by 15.
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result


if __name__ == "__main__":
    assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]
    result = fizzbuzz(15)
    assert result[14] == "FizzBuzz"
    assert result[2] == "Fizz"
    assert result[4] == "Buzz"
    assert fizzbuzz(1) == ["1"]
    assert len(fizzbuzz(20)) == 20
    print("All tests passed!")
