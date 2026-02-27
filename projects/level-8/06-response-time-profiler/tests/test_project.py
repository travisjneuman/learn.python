"""Tests for Response Time Profiler.

Covers: percentile math, profiler recording, decorator, context manager, reports.
"""

from __future__ import annotations

import time

import pytest

from project import ProfileReport, ResponseTimeProfiler, percentile, std_dev


# --- Fixtures -----------------------------------------------------------

@pytest.fixture
def profiler() -> ResponseTimeProfiler:
    return ResponseTimeProfiler()


# --- Percentile math ----------------------------------------------------

class TestPercentile:
    @pytest.mark.parametrize("values,pct,expected", [
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 50, 5.5),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 90, 9.1),
        ([100], 99, 100),
    ])
    def test_percentile_computation(
        self, values: list[float], pct: float, expected: float,
    ) -> None:
        result = percentile(sorted(values), pct)
        assert abs(result - expected) < 0.2

    def test_empty_returns_zero(self) -> None:
        assert percentile([], 50) == 0.0


class TestStdDev:
    def test_identical_values(self) -> None:
        assert std_dev([5.0, 5.0, 5.0], 5.0) == 0.0

    def test_known_distribution(self) -> None:
        values = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
        mean = sum(values) / len(values)
        result = std_dev(values, mean)
        assert 1.5 < result < 2.5  # known std dev ~2.0


# --- Profiler recording -------------------------------------------------

class TestProfilerRecording:
    def test_record_and_report(self, profiler: ResponseTimeProfiler) -> None:
        profiler.record("func_a", 10.0)
        profiler.record("func_a", 20.0)
        profiler.record("func_a", 30.0)
        report = profiler.report("func_a")
        assert report.call_count == 3
        assert report.mean_ms == pytest.approx(20.0)
        assert report.min_ms == 10.0
        assert report.max_ms == 30.0

    def test_report_unknown_function(self, profiler: ResponseTimeProfiler) -> None:
        report = profiler.report("nonexistent")
        assert report.call_count == 0
        assert report.mean_ms == 0


# --- Decorator tracking -------------------------------------------------

class TestDecoratorTracking:
    def test_track_decorator(self, profiler: ResponseTimeProfiler) -> None:
        @profiler.track
        def sample() -> str:
            return "done"

        result = sample()
        assert result == "done"
        report = profiler.report("sample")
        assert report.call_count == 1
        assert report.total_ms > 0


# --- Context manager ----------------------------------------------------

@pytest.mark.slow
class TestContextManager:
    def test_measure_context(self, profiler: ResponseTimeProfiler) -> None:
        with profiler.measure("block"):
            time.sleep(0.005)
        report = profiler.report("block")
        assert report.call_count == 1
        assert report.mean_ms >= 3  # at least 3ms


# --- Bottleneck detection -----------------------------------------------

class TestBottleneck:
    def test_finds_slowest(self, profiler: ResponseTimeProfiler) -> None:
        profiler.record("fast", 1.0)
        profiler.record("slow", 100.0)
        profiler.record("medium", 50.0)
        bottleneck = profiler.find_bottleneck()
        assert bottleneck is not None
        assert bottleneck.function_name == "slow"

    def test_no_data_returns_none(self, profiler: ResponseTimeProfiler) -> None:
        assert profiler.find_bottleneck() is None
