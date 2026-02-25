"""
Challenge: Caesar Cipher
Difficulty: Beginner
Concepts: strings, chr/ord, modular arithmetic, character classification
Time: 25 minutes

Implement a Caesar cipher that shifts letters by a given amount.
- Only shift alphabetic characters (a-z, A-Z).
- Preserve case: uppercase stays uppercase, lowercase stays lowercase.
- Non-alphabetic characters remain unchanged.
- Support both positive (encrypt) and negative (decrypt) shifts.

Examples:
    >>> caesar_cipher("abc", 1)
    'bcd'
    >>> caesar_cipher("xyz", 3)
    'abc'
    >>> caesar_cipher("Hello, World!", 13)
    'Uryyb, Jbeyq!'
"""


def caesar_cipher(text: str, shift: int) -> str:
    """Encrypt/decrypt text using a Caesar cipher with the given shift. Implement this function."""
    # Hint: Use ord() to get a character's number, add the shift with modulo 26, then chr() back.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Basic shift
    assert caesar_cipher("abc", 1) == "bcd", "Basic shift failed"
    # Test 2: Wrap around
    assert caesar_cipher("xyz", 3) == "abc", "Wrap around failed"
    # Test 3: Preserve case and punctuation
    assert caesar_cipher("Hello, World!", 13) == "Uryyb, Jbeyq!", "Preserve case failed"
    # Test 4: Decrypt (negative shift)
    assert caesar_cipher("bcd", -1) == "abc", "Decrypt failed"
    # Test 5: No shift
    assert caesar_cipher("test", 0) == "test", "No shift failed"
    # Test 6: Full rotation
    assert caesar_cipher("test", 26) == "test", "Full rotation failed"
    print("All tests passed!")
