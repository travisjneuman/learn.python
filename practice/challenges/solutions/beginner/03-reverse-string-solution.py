"""
Solution: Reverse String

Approach: Build the result by iterating through the string and prepending
each character to an accumulator. This avoids the [::-1] slice shortcut.
"""


def reverse_string(s: str) -> str:
    # Start with an empty result and prepend each character.
    # Alternatively, iterate backwards using range(len(s) - 1, -1, -1).
    result = ""
    for char in s:
        result = char + result
    return result


if __name__ == "__main__":
    assert reverse_string("hello") == "olleh"
    assert reverse_string("racecar") == "racecar"
    assert reverse_string("") == ""
    assert reverse_string("x") == "x"
    assert reverse_string("hi there!") == "!ereht ih"
    print("All tests passed!")
