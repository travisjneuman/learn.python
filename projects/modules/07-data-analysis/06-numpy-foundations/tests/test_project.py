"""Tests for NumPy Foundations project."""

import numpy as np
import pytest

from project import (
    create_basic_arrays,
    broadcasting_demo,
    vectorized_operations,
    statistical_summary,
)


def test_create_basic_arrays():
    grades, zeros, ones, sequence, even_spaced = create_basic_arrays()
    assert len(grades) == 5
    assert np.all(zeros == 0)
    assert ones.shape == (3, 4)
    assert np.all(ones == 1)
    assert list(sequence) == [0, 2, 4, 6, 8]
    assert len(even_spaced) == 5
    assert even_spaced[0] == pytest.approx(0.0)
    assert even_spaced[-1] == pytest.approx(1.0)


def test_broadcasting_discount():
    discounted, with_tax, normalized = broadcasting_demo()
    assert discounted[0] == pytest.approx(9.0)
    assert discounted[-1] == pytest.approx(45.0)


def test_broadcasting_tax():
    discounted, with_tax, normalized = broadcasting_demo()
    assert with_tax[0] == pytest.approx(10.5)  # 10 * 1.05


def test_vectorized_sqrt():
    roots, squared, clipped, large = vectorized_operations()
    assert roots[0] == pytest.approx(2.0)
    assert roots[1] == pytest.approx(3.0)


def test_vectorized_clip():
    roots, squared, clipped, large = vectorized_operations()
    assert np.all(clipped >= 10)
    assert np.all(clipped <= 50)


def test_vectorized_filter():
    roots, squared, clipped, large = vectorized_operations()
    assert all(v > 20 for v in large)


def test_statistical_summary():
    values = np.array([10, 20, 30, 40, 50])
    stats = statistical_summary(values)
    assert stats["count"] == 5
    assert stats["mean"] == pytest.approx(30.0)
    assert stats["min"] == pytest.approx(10.0)
    assert stats["max"] == pytest.approx(50.0)
    assert stats["median"] == pytest.approx(30.0)
    assert stats["sum"] == pytest.approx(150.0)


def test_statistical_summary_single():
    values = np.array([42])
    stats = statistical_summary(values)
    assert stats["mean"] == pytest.approx(42.0)
    assert stats["std"] == pytest.approx(0.0)
