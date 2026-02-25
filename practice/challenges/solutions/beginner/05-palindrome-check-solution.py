"""
Solution: Palindrome Check

Approach: Strip out all non-alphanumeric characters and convert to lowercase.
Then compare the cleaned string with its reverse. A two-pointer approach also
works: compare characters from both ends moving inward.
"""


def is_palindrome(s: str) -> bool:
    # Clean the string: keep only alphanumeric characters, lowercase.
    cleaned = ""
    for char in s.lower():
        if char.isalnum():
            cleaned += char

    # Compare with reverse using two pointers.
    left = 0
    right = len(cleaned) - 1
    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1
    return True


if __name__ == "__main__":
    assert is_palindrome("racecar") is True
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert is_palindrome("hello") is False
    assert is_palindrome("") is True
    assert is_palindrome("a") is True
    assert is_palindrome("Was it a car or a cat I saw?") is True
    print("All tests passed!")
