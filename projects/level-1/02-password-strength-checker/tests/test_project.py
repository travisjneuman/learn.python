"""Tests for Password Strength Checker."""

from project import check_character_variety, check_common, check_length, score_password


def test_check_length_short() -> None:
    assert check_length("abc") == 0


def test_check_length_long() -> None:
    assert check_length("a" * 16) == 3


def test_character_variety_all_types() -> None:
    result = check_character_variety("Abc1!")
    assert result["uppercase"] is True
    assert result["lowercase"] is True
    assert result["digit"] is True
    assert result["special"] is True


def test_common_password_detected() -> None:
    assert check_common("password") is True
    assert check_common("PASSWORD") is True
    assert check_common("xK9#mP2z") is False


def test_score_strong_password() -> None:
    result = score_password("MyStr0ng!Pass#2024")
    assert result["strength"] == "strong"
    assert result["total_score"] >= 7
