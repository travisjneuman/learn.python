"""
Solution: Anagram Check

Approach: Normalize both strings by removing spaces and converting to
lowercase. Then count the frequency of each character in both strings
and compare the frequency dictionaries. If they match, the strings are
anagrams.
"""


def is_anagram(s1: str, s2: str) -> bool:
    # Normalize: remove spaces and lowercase
    clean1 = s1.replace(" ", "").lower()
    clean2 = s2.replace(" ", "").lower()

    # Build character frequency dictionaries
    def char_counts(s):
        counts = {}
        for char in s:
            counts[char] = counts.get(char, 0) + 1
        return counts

    return char_counts(clean1) == char_counts(clean2)


if __name__ == "__main__":
    assert is_anagram("listen", "silent") is True
    assert is_anagram("hello", "world") is False
    assert is_anagram("Astronomer", "Moon starer") is True
    assert is_anagram("", "") is True
    assert is_anagram("test", "test") is True
    assert is_anagram("aab", "abb") is False
    print("All tests passed!")
