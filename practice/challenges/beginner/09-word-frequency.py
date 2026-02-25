"""
Challenge: Word Frequency
Difficulty: Beginner
Concepts: strings, dictionaries, splitting, case normalization
Time: 20 minutes

Count the frequency of each word in a text string. Words should be
compared case-insensitively. Return a dictionary mapping lowercase
words to their counts. Split on whitespace only.

Examples:
    >>> word_frequency("the cat and the dog")
    {'the': 2, 'cat': 1, 'and': 1, 'dog': 1}
    >>> word_frequency("Hello hello HELLO")
    {'hello': 3}
"""


def word_frequency(text: str) -> dict[str, int]:
    """Count word frequencies in text (case-insensitive). Implement this function."""
    # Hint: Use .lower().split() to get normalized words, then build a dict with counts.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Basic sentence
    assert word_frequency("the cat and the dog") == {"the": 2, "cat": 1, "and": 1, "dog": 1}, "Basic sentence failed"
    # Test 2: Case insensitive
    assert word_frequency("Hello hello HELLO") == {"hello": 3}, "Case insensitive failed"
    # Test 3: Single word
    assert word_frequency("Python") == {"python": 1}, "Single word failed"
    # Test 4: Empty string
    assert word_frequency("") == {}, "Empty string failed"
    # Test 5: Multiple spaces
    result = word_frequency("a  b  a")
    assert result == {"a": 2, "b": 1}, "Multiple spaces failed"
    print("All tests passed!")
