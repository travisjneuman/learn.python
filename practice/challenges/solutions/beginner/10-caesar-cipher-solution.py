"""
Solution: Caesar Cipher

Approach: For each character, check if it is alphabetic. If so, determine
its base ('a' for lowercase, 'A' for uppercase), shift its position within
the 26-letter alphabet using modular arithmetic, and convert back to a char.
Non-alphabetic characters pass through unchanged.
"""


def caesar_cipher(text: str, shift: int) -> str:
    result = ""
    for char in text:
        if char.isalpha():
            # Determine the base: 'a' (97) for lowercase, 'A' (65) for uppercase
            base = ord("a") if char.islower() else ord("A")
            # Shift within the 0-25 range, wrap with modulo 26
            shifted = (ord(char) - base + shift) % 26
            result += chr(base + shifted)
        else:
            # Non-alphabetic characters are unchanged
            result += char
    return result


if __name__ == "__main__":
    assert caesar_cipher("abc", 1) == "bcd"
    assert caesar_cipher("xyz", 3) == "abc"
    assert caesar_cipher("Hello, World!", 13) == "Uryyb, Jbeyq!"
    assert caesar_cipher("bcd", -1) == "abc"
    assert caesar_cipher("test", 0) == "test"
    assert caesar_cipher("test", 26) == "test"
    print("All tests passed!")
