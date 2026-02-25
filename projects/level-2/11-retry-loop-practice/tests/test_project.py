"""Tests for Retry Loop Practice.

Covers:
- Retry succeeds on first try
- Retry succeeds after failures
- Retry exhausts all attempts
- Countdown function (deterministic)
- Summary statistics
"""

import pytest

from project import (
    make_countdown_function,
    make_flaky_function,
    retry_no_sleep,
    summarise_retry_results,
)


def test_retry_immediate_success() -> None:
    """A function that always succeeds should need only 1 attempt."""
    func = lambda: "done"
    result = retry_no_sleep(func, max_attempts=3)
    assert result["success"] is True
    assert result["total_attempts"] == 1
    assert result["result"] == "done"


def test_retry_succeeds_after_failures() -> None:
    """Countdown function should succeed after N failures."""
    func = make_countdown_function(failures_before_success=2)
    result = retry_no_sleep(func, max_attempts=5)
    assert result["success"] is True
    assert result["total_attempts"] == 3  # 2 failures + 1 success


def test_retry_exhausts_attempts() -> None:
    """If function always fails, all attempts should be used."""
    func = lambda: (_ for _ in ()).throw(ConnectionError("always fails"))
    result = retry_no_sleep(func, max_attempts=3)
    assert result["success"] is False
    assert result["total_attempts"] == 3


def test_retry_catches_specific_exceptions() -> None:
    """Retry should only catch the specified exception types."""
    func = lambda: (_ for _ in ()).throw(ValueError("wrong type"))
    # Only catching ConnectionError — ValueError should not be retried.
    with pytest.raises(ValueError):
        retry_no_sleep(func, max_attempts=3, exceptions=(ConnectionError,))


def test_countdown_function() -> None:
    """Countdown should fail exactly N times then succeed."""
    func = make_countdown_function(failures_before_success=3)

    # First 3 calls should raise.
    for _ in range(3):
        with pytest.raises(ConnectionError):
            func()

    # 4th call should succeed.
    result = func()
    assert "Success" in result


@pytest.mark.parametrize(
    "failures,max_attempts,expected_success",
    [
        (0, 3, True),    # immediate success
        (2, 3, True),    # succeeds on 3rd try
        (5, 3, False),   # not enough attempts
        (2, 2, False),   # just barely not enough
    ],
)
def test_retry_parametrized(
    failures: int, max_attempts: int, expected_success: bool
) -> None:
    """Retry should succeed iff max_attempts > failures."""
    func = make_countdown_function(failures_before_success=failures)
    result = retry_no_sleep(func, max_attempts=max_attempts)
    assert result["success"] is expected_success


def test_flaky_function_deterministic() -> None:
    """Same seed should produce same sequence of failures."""
    func1 = make_flaky_function(failure_rate=0.5, seed=42)
    func2 = make_flaky_function(failure_rate=0.5, seed=42)

    results1 = []
    results2 = []
    for _ in range(10):
        try:
            func1()
            results1.append(True)
        except ConnectionError:
            results1.append(False)
        try:
            func2()
            results2.append(True)
        except ConnectionError:
            results2.append(False)

    assert results1 == results2


def test_summarise_results() -> None:
    """Summary should report correct counts and rates."""
    results = [
        {"success": True, "total_attempts": 1},
        {"success": False, "total_attempts": 3},
        {"success": True, "total_attempts": 2},
    ]
    summary = summarise_retry_results(results)
    assert summary["total_operations"] == 3
    assert summary["successes"] == 2
    assert summary["failures"] == 1
    assert summary["success_rate"] == 66.7
