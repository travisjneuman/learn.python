"""Tests for Terminal Hello Lab.

These tests verify that the greeting and banner functions
produce correct output without needing to run the full script.
"""

from project import build_banner, build_info_card, greet


def test_greet_includes_name() -> None:
    """The greeting should contain the name that was passed in."""
    result = greet("Ada")
    assert "Ada" in result
    assert "Hello" in result


def test_greet_different_names() -> None:
    """greet() should work for any name, not just one hard-coded value."""
    for name in ["Bob", "Zara", "0xCAFE"]:
        result = greet(name)
        assert name in result


def test_build_banner_contains_title() -> None:
    """The banner should contain the title text we passed."""
    banner = build_banner("MY TITLE")
    assert "MY TITLE" in banner
    # Banner has three lines: top border, title, bottom border.
    lines = banner.split("\n")
    assert len(lines) == 3


def test_build_banner_respects_width() -> None:
    """The border lines should match the requested width."""
    banner = build_banner("HI", width=20)
    lines = banner.split("\n")
    # First and last lines are the border.
    assert len(lines[0]) == 20
    assert len(lines[2]) == 20


def test_build_info_card_structure() -> None:
    """The info card dict should have all expected keys."""
    card = build_info_card("Test", "Python", 5)
    assert card["name"] == "Test"
    assert card["language"] == "Python"
    assert card["learning_day"] == 5
    assert "Test" in card["greeting"]
