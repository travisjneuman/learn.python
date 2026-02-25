"""
Solution: Count Vowels

Approach: Convert the string to lowercase, then count characters that
appear in the vowel set "aeiou". Using a set for lookup is O(1) per check.
"""


def count_vowels(s: str) -> int:
    vowels = set("aeiou")
    count = 0
    for char in s.lower():
        if char in vowels:
            count += 1
    return count


if __name__ == "__main__":
    assert count_vowels("hello") == 2
    assert count_vowels("AEIOU") == 5
    assert count_vowels("rhythm") == 0
    assert count_vowels("") == 0
    assert count_vowels("Beautiful Day") == 6
    print("All tests passed!")
