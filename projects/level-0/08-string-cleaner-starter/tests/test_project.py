"""Tests for String Cleaner Starter."""

from project import clean_string, collapse_spaces, normalise_case, remove_special_characters


def test_clean_string_full_pipeline() -> None:
    """The full pipeline should strip, lowercase, remove specials, collapse spaces."""
    result = clean_string("  Hello,   WORLD!!!  ")
    assert result == "hello world"


def test_normalise_case() -> None:
    """All characters should be lowered."""
    assert normalise_case("HeLLo WoRLd") == "hello world"


def test_remove_special_characters() -> None:
    """Only letters, digits, and spaces should remain."""
    assert remove_special_characters("price: $9.99!") == "price 999"
    assert remove_special_characters("a-b_c") == "abc"


def test_collapse_spaces() -> None:
    """Multiple spaces should become one."""
    assert collapse_spaces("a  b   c    d") == "a b c d"


def test_clean_string_already_clean() -> None:
    """A string that is already clean should be unchanged."""
    assert clean_string("hello world") == "hello world"
