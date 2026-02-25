"""Tests for Date Difference Helper."""

import pytest

from project import add_days, day_of_week, days_between, parse_date


def test_days_between_same_date() -> None:
    assert days_between("2024-01-01", "2024-01-01") == 0


def test_days_between_one_week() -> None:
    assert days_between("2024-01-01", "2024-01-08") == 7


def test_days_between_reversed() -> None:
    """Order should not matter -- result is always positive."""
    assert days_between("2024-12-31", "2024-01-01") == 365


def test_add_days() -> None:
    assert add_days("2024-01-01", 30) == "2024-01-31"
    assert add_days("2024-03-01", -1) == "2024-02-29"  # 2024 is a leap year


def test_day_of_week() -> None:
    assert day_of_week("2024-01-01") == "Monday"


def test_parse_date_invalid() -> None:
    with pytest.raises(ValueError):
        parse_date("not-a-date")
