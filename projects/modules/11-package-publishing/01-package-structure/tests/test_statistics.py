"""Tests for the statistics module."""

import pytest
from mymath.statistics import mean, median, mode


def test_mean():
    assert mean([1, 2, 3, 4, 5]) == 3.0
    assert mean([10]) == 10.0


def test_mean_empty():
    with pytest.raises(ValueError):
        mean([])


def test_median_odd():
    assert median([1, 3, 5]) == 3


def test_median_even():
    assert median([1, 3, 5, 7]) == 4.0


def test_median_empty():
    with pytest.raises(ValueError):
        median([])


def test_mode():
    assert mode([1, 2, 2, 3, 3, 3]) == 3
    assert mode([7, 7, 7]) == 7


def test_mode_empty():
    with pytest.raises(ValueError):
        mode([])
