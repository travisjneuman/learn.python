"""
Solution: Word Frequency

Approach: Lowercase the text and split on whitespace. Iterate through the
words and build a dictionary, incrementing counts for each word. The
.split() method without arguments splits on any whitespace and ignores
extra spaces.
"""


def word_frequency(text: str) -> dict[str, int]:
    counts = {}
    for word in text.lower().split():
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts


if __name__ == "__main__":
    assert word_frequency("the cat and the dog") == {"the": 2, "cat": 1, "and": 1, "dog": 1}
    assert word_frequency("Hello hello HELLO") == {"hello": 3}
    assert word_frequency("Python") == {"python": 1}
    assert word_frequency("") == {}
    result = word_frequency("a  b  a")
    assert result == {"a": 2, "b": 1}
    print("All tests passed!")
