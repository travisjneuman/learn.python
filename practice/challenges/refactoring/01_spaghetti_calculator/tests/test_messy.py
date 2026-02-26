"""Tests for the calculator.

These must pass before AND after your refactoring.

Run with:
    cd practice/challenges/refactoring/01_spaghetti_calculator
    python -m pytest tests/
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from messy import calc


def test_simple_addition():
    assert calc("3 + 4") == 7.0


def test_simple_subtraction():
    assert calc("10 - 3") == 7.0


def test_simple_multiplication():
    assert calc("3 * 4") == 12.0


def test_simple_division():
    assert calc("12 / 4") == 3.0


def test_operator_precedence():
    assert calc("3 + 4 * 2") == 11.0


def test_parentheses():
    assert calc("(3 + 4) * 2") == 14.0


def test_nested_parentheses():
    assert calc("((2 + 3) * (4 - 1))") == 15.0


def test_negative_number():
    assert calc("-5 + 3") == -2.0


def test_negative_in_parentheses():
    assert calc("-(3 + 4)") == -7.0


def test_decimal_numbers():
    assert abs(calc("3.5 + 1.5") - 5.0) < 1e-9


def test_complex_expression():
    assert abs(calc("2 * (3 + 4) - 1 / 2") - 13.5) < 1e-9


def test_single_number():
    assert calc("42") == 42.0


def test_whitespace_handling():
    assert calc("  3  +  4  ") == 7.0
