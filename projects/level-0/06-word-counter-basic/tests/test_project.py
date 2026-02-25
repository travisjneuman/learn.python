"""Tests for Word Counter Basic."""

from project import analyse_text, count_lines, count_words, word_frequencies


def test_count_words_simple() -> None:
    """Counting words in a simple sentence."""
    assert count_words("hello world") == 2
    assert count_words("one") == 1
    assert count_words("") == 0


def test_count_lines() -> None:
    """Line counting should handle single and multi-line text."""
    assert count_lines("line one\nline two\nline three") == 3
    assert count_lines("single line") == 1
    assert count_lines("") == 0


def test_word_frequencies_normalises_case() -> None:
    """'The' and 'the' should be counted as the same word."""
    freq = word_frequencies("The the THE")
    assert freq["the"] == 3


def test_word_frequencies_strips_punctuation() -> None:
    """Punctuation at word boundaries should be removed."""
    freq = word_frequencies("hello, hello! Hello.")
    assert freq["hello"] == 3


def test_analyse_text_returns_all_keys() -> None:
    """The summary should contain all expected keys."""
    result = analyse_text("Python is great. Python is fun.")
    assert "lines" in result
    assert "words" in result
    assert "characters" in result
    assert "unique_words" in result
    assert "top_words" in result
    assert result["words"] == 6
