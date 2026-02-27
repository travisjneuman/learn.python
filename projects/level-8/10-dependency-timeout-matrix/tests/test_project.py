"""Tests for Dependency Timeout Matrix.

Covers: dependency checks, timeout enforcement, matrix building, and analysis.
"""

from __future__ import annotations

import time

import pytest

from project import (
    DependencyChecker,
    DependencyConfig,
    HealthStatus,
    TimeoutMatrix,
    analyze_matrix,
    build_timeout_matrix,
)


# --- DependencyConfig ---------------------------------------------------

class TestDependencyConfig:
    def test_config_defaults(self) -> None:
        config = DependencyConfig(name="db", timeout_seconds=1.0)
        assert config.critical is True
        assert config.retry_count == 1


# --- DependencyChecker --------------------------------------------------

@pytest.mark.slow
class TestDependencyChecker:
    def test_healthy_check(self) -> None:
        checker = DependencyChecker()
        config = DependencyConfig(name="fast", timeout_seconds=1.0)
        result = checker.check(config, simulate_fn=lambda n: time.sleep(0.01) or 0.01)
        assert result.status == HealthStatus.HEALTHY
        assert result.timed_out is False

    def test_timeout_check(self) -> None:
        checker = DependencyChecker()
        config = DependencyConfig(name="slow", timeout_seconds=0.05)

        def slow_fn(name: str) -> float:
            time.sleep(1.0)
            return 1.0

        result = checker.check(config, simulate_fn=slow_fn)
        assert result.status == HealthStatus.TIMEOUT
        assert result.timed_out is True

    def test_error_check(self) -> None:
        checker = DependencyChecker()
        config = DependencyConfig(name="broken", timeout_seconds=1.0)

        def error_fn(name: str) -> float:
            raise ConnectionError("refused")

        result = checker.check(config, simulate_fn=error_fn)
        assert result.status == HealthStatus.ERROR
        assert "refused" in result.error_message

    @pytest.mark.parametrize("retry_count,expected_retries", [
        (1, 1),
        (3, 3),
    ])
    def test_retry_behavior(self, retry_count: int, expected_retries: int) -> None:
        checker = DependencyChecker()
        config = DependencyConfig(
            name="flaky", timeout_seconds=0.05, retry_count=retry_count,
        )

        def slow_fn(name: str) -> float:
            time.sleep(1.0)
            return 1.0

        result = checker.check(config, simulate_fn=slow_fn)
        assert result.retries_used == expected_retries


# --- Matrix building ----------------------------------------------------

@pytest.mark.slow
class TestTimeoutMatrix:
    def test_matrix_dimensions(self) -> None:
        deps = [
            DependencyConfig(name="svc-a", timeout_seconds=1.0),
            DependencyConfig(name="svc-b", timeout_seconds=1.0),
        ]
        timeouts = [0.5, 1.0]

        def fast_fn(name: str) -> float:
            time.sleep(0.01)
            return 0.01

        matrix = build_timeout_matrix(deps, timeouts, simulate_fn=fast_fn)
        assert len(matrix.results) == 2  # 2 timeout values
        assert len(matrix.results[0]) == 2  # 2 dependencies per row

    def test_matrix_to_dict(self) -> None:
        deps = [DependencyConfig(name="svc", timeout_seconds=1.0)]

        def fast_fn(name: str) -> float:
            time.sleep(0.001)
            return 0.001

        matrix = build_timeout_matrix(deps, [0.5], simulate_fn=fast_fn)
        d = matrix.to_dict()
        assert "matrix" in d
        assert "dependencies" in d


# --- Analysis -----------------------------------------------------------

@pytest.mark.slow
class TestAnalyzeMatrix:
    def test_finds_minimum_passing_timeout(self) -> None:
        deps = [DependencyConfig(name="svc", timeout_seconds=1.0)]

        def fast_fn(name: str) -> float:
            time.sleep(0.01)
            return 0.01

        matrix = build_timeout_matrix(deps, [0.05, 0.1, 0.5], simulate_fn=fast_fn)
        analysis = analyze_matrix(matrix)
        assert "svc" in analysis
        assert analysis["svc"]["min_passing_timeout"] is not None
