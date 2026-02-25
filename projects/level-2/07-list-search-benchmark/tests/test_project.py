"""Tests for List Search Benchmark.

Covers:
- Linear search correctness
- Binary search correctness
- Set search correctness
- Benchmark execution
- Edge cases
"""

import pytest

from project import (
    binary_search,
    generate_test_data,
    linear_search,
    run_benchmark,
    set_search,
)


def test_linear_search_found() -> None:
    """Linear search should return the correct index."""
    data = [10, 20, 30, 40, 50]
    assert linear_search(data, 30) == 2


def test_linear_search_not_found() -> None:
    """Linear search should return -1 for missing values."""
    data = [10, 20, 30]
    assert linear_search(data, 99) == -1


def test_binary_search_found() -> None:
    """Binary search should find elements in sorted data."""
    data = [10, 20, 30, 40, 50]
    assert binary_search(data, 40) == 3


def test_binary_search_not_found() -> None:
    """Binary search should return -1 for missing values."""
    data = [10, 20, 30, 40, 50]
    assert binary_search(data, 25) == -1


@pytest.mark.parametrize(
    "target,expected",
    [(10, 0), (50, 4), (30, 2), (99, -1)],
)
def test_binary_search_parametrized(target: int, expected: int) -> None:
    """Binary search should handle first, last, middle, and missing."""
    data = [10, 20, 30, 40, 50]
    assert binary_search(data, target) == expected


def test_set_search() -> None:
    """Set search should return True/False for membership."""
    data_set = {10, 20, 30}
    assert set_search(data_set, 20) is True
    assert set_search(data_set, 99) is False


def test_linear_search_empty_list() -> None:
    """Searching an empty list should return -1."""
    assert linear_search([], 5) == -1


def test_binary_search_empty_list() -> None:
    """Binary search on empty list should return -1."""
    assert binary_search([], 5) == -1


def test_generate_test_data_reproducible() -> None:
    """Same seed should produce identical data."""
    d1 = generate_test_data(100, seed=42)
    d2 = generate_test_data(100, seed=42)
    assert d1 == d2


def test_run_benchmark_returns_results() -> None:
    """Benchmark should return timing data for each size."""
    results = run_benchmark(sizes=[50, 100], iterations=5)
    assert len(results) == 2
    assert results[0]["size"] == 50
    assert "linear_found_us" in results[0]
    assert "binary_found_us" in results[0]
