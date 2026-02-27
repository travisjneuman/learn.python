"""Tests for Temperature Converter."""

import pytest

from project import celsius_to_fahrenheit, convert_temperature, kelvin_to_celsius


def test_boiling_point_c_to_f() -> None:
    """Water boils at 100 C which is 212 F."""
    assert celsius_to_fahrenheit(100) == 212.0


def test_freezing_point_c_to_f() -> None:
    """Water freezes at 0 C which is 32 F."""
    assert celsius_to_fahrenheit(0) == 32.0


def test_convert_round_trip() -> None:
    """Converting C->F->C should return the original value."""
    original = 37.0
    f_value = convert_temperature(original, "C", "F")
    back = convert_temperature(f_value, "F", "C")
    assert abs(back - original) < 0.01


def test_negative_kelvin_raises() -> None:
    """Kelvin cannot be negative -- that is below absolute zero."""
    with pytest.raises(ValueError, match="Kelvin cannot be negative"):
        kelvin_to_celsius(-1)


def test_unknown_unit_raises() -> None:
    """An unsupported unit letter should raise ValueError."""
    with pytest.raises(ValueError, match="Unknown unit"):
        convert_temperature(100, "X", "C")


def test_freezing_point_boundary() -> None:
    """0 C (freezing point of water) converts to 32 F and 273.15 K."""
    assert convert_temperature(0, "C", "F") == 32.0
    assert convert_temperature(0, "C", "K") == 273.15


def test_boiling_point_boundary() -> None:
    """100 C (boiling point of water) converts to 212 F and 373.15 K."""
    assert convert_temperature(100, "C", "F") == 212.0
    assert convert_temperature(100, "C", "K") == 373.15


def test_absolute_zero_boundary() -> None:
    """Absolute zero (-273.15 C) converts to -459.67 F and 0 K.

    This is the lowest possible temperature.  The Kelvin value must be
    exactly 0 (within floating-point rounding).
    """
    assert convert_temperature(-273.15, "C", "K") == 0.0
    assert convert_temperature(-273.15, "C", "F") == -459.67
