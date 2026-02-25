"""Tests for Level 0 Mini Toolkit."""

from project import clean_string, count_words, find_duplicates, run_tool


def test_count_words() -> None:
    """Word count should return correct counts."""
    result = count_words("hello world\ngoodbye world")
    assert result["words"] == 4
    assert result["lines"] == 2


def test_find_duplicates() -> None:
    """Duplicate lines should be detected with correct counts."""
    lines = ["alpha", "beta", "alpha", "gamma", "beta", "beta"]
    dupes = find_duplicates(lines)
    texts = {d["text"]: d["count"] for d in dupes}
    assert texts["alpha"] == 2
    assert texts["beta"] == 3
    assert "gamma" not in texts


def test_clean_string() -> None:
    """Cleaning should strip, lowercase, and remove specials."""
    assert clean_string("  Hello, World!!!  ") == "hello world"


def test_run_tool_wordcount() -> None:
    """The wordcount tool should return a result dict."""
    result = run_tool("wordcount", "one two three")
    assert result["tool"] == "wordcount"
    assert result["result"]["words"] == 3


def test_run_tool_unknown() -> None:
    """An unknown tool name should return an error."""
    result = run_tool("nope", "text")
    assert "error" in result
