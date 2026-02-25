"""Tests for CLI Arguments Workbench.

Uses pytest fixtures and parametrize to validate argparse patterns,
custom types, and conversion functions.
"""

import json
from pathlib import Path

import pytest

from project import (
    ConversionResult,
    batch_convert,
    build_parser,
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    kg_to_lbs,
    km_to_miles,
    lbs_to_kg,
    miles_to_km,
    positive_float,
)


# --- Custom type tests ---

def test_positive_float_accepts_positive() -> None:
    """positive_float should accept valid positive numbers."""
    assert positive_float("3.14") == 3.14
    assert positive_float("1") == 1.0


def test_positive_float_rejects_zero_and_negative() -> None:
    """positive_float should reject zero and negative values."""
    import argparse
    with pytest.raises(argparse.ArgumentTypeError):
        positive_float("0")
    with pytest.raises(argparse.ArgumentTypeError):
        positive_float("-5")


def test_positive_float_rejects_non_numeric() -> None:
    """positive_float should reject non-numeric strings."""
    import argparse
    with pytest.raises(argparse.ArgumentTypeError):
        positive_float("abc")


# --- Conversion function tests ---

@pytest.mark.parametrize("celsius,expected_f", [
    (0, 32.0),
    (100, 212.0),
    (-40, -40.0),
])
def test_celsius_to_fahrenheit(celsius: float, expected_f: float) -> None:
    """Verify C-to-F conversions against known values."""
    result = celsius_to_fahrenheit(celsius)
    assert isinstance(result, ConversionResult)
    assert result.output_value == expected_f
    assert result.input_unit == "C"
    assert result.output_unit == "F"


@pytest.mark.parametrize("fahrenheit,expected_c", [
    (32, 0.0),
    (212, 100.0),
    (-40, -40.0),
])
def test_fahrenheit_to_celsius(fahrenheit: float, expected_c: float) -> None:
    """Verify F-to-C conversions against known values."""
    result = fahrenheit_to_celsius(fahrenheit)
    assert result.output_value == expected_c


def test_km_to_miles() -> None:
    """1 km should be approximately 0.621371 miles."""
    result = km_to_miles(1.0)
    assert result.output_value == 0.6214
    assert result.output_unit == "mi"


def test_miles_to_km() -> None:
    """1 mile should be approximately 1.6093 km."""
    result = miles_to_km(1.0)
    assert abs(result.output_value - 1.6093) < 0.001


def test_kg_to_lbs() -> None:
    """1 kg should be approximately 2.2046 lbs."""
    result = kg_to_lbs(1.0)
    assert result.output_value == 2.2046


def test_lbs_to_kg() -> None:
    """1 lb should be approximately 0.4536 kg."""
    result = lbs_to_kg(1.0)
    assert abs(result.output_value - 0.4536) < 0.001


# --- Batch conversion tests ---

def test_batch_convert_valid() -> None:
    """Batch convert should process a list of operations."""
    ops = [
        {"category": "temp", "conversion": "c-to-f", "value": 100},
        {"category": "dist", "conversion": "km-to-mi", "value": 10},
    ]
    results = batch_convert(ops)
    assert len(results) == 2
    assert results[0]["output_value"] == 212.0
    assert results[1]["output_unit"] == "mi"


def test_batch_convert_unknown_operation() -> None:
    """Unknown category/conversion should produce an error dict."""
    ops = [{"category": "volume", "conversion": "l-to-gal", "value": 1}]
    results = batch_convert(ops)
    assert "error" in results[0]


# --- Parser tests ---

def test_parser_temp_subcommand() -> None:
    """Parser should accept temp subcommand with mutually exclusive args."""
    parser = build_parser()
    args = parser.parse_args(["temp", "--c-to-f", "100"])
    assert args.command == "temp"
    assert args.c_to_f == 100.0


def test_parser_json_flag() -> None:
    """Parser should accept --json flag."""
    parser = build_parser()
    args = parser.parse_args(["--json", "temp", "--f-to-c", "212"])
    assert args.json is True


# --- Dataclass tests ---

def test_conversion_result_dataclass() -> None:
    """ConversionResult should be a proper dataclass."""
    r = ConversionResult(100, "C", 212.0, "F", "F = C * 9/5 + 32")
    assert r.input_value == 100
    assert r.formula == "F = C * 9/5 + 32"
