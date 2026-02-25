"""Tests for the calculator module."""

import pytest
from mymath.calculator import add, subtract, multiply, divide


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract():
    assert subtract(10, 4) == 6
    assert subtract(0, 5) == -5


def test_multiply():
    assert multiply(3, 7) == 21
    assert multiply(0, 100) == 0
    assert multiply(-2, 3) == -6


def test_divide():
    assert divide(15, 4) == 3.75
    assert divide(10, 2) == 5.0


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
