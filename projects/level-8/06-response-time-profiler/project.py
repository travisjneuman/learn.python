"""Response Time Profiler — profile function execution with percentile reporting.

Design rationale:
    Understanding where time is spent is essential for optimization.
    This project builds a profiling toolkit that measures function execution
    times, computes percentile distributions (p50, p90, p99), and identifies
    bottlenecks — the same approach used by APM tools like New Relic and Datadog.

Concepts practised:
    - context managers for timing blocks
    - decorator-based profiling
    - percentile calculation (p50, p90, p95, p99)
    - dataclasses for profile results
    - statistical distribution analysis
"""

from __future__ import annotations

import argparse
import json
import math
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Callable, Generator


# --- Domain types -------------------------------------------------------

@dataclass
class TimingRecord:
    """A single execution timing measurement."""
    function_name: str
    duration_ms: float
    timestamp: float = field(default_factory=time.monotonic)


# WHY percentiles (p90, p95, p99) instead of just mean? -- Averages hide
# tail latency. If 99% of requests take 10ms but 1% take 5000ms, the mean
# looks fine but users in that 1% have a terrible experience. P99 reveals
# the worst-case that real users actually hit — the metric APM tools like
# Datadog and New Relic prioritize.
@dataclass
class ProfileReport:
    """Statistical summary of timings for one function."""
    function_name: str
    call_count: int
    total_ms: float
    mean_ms: float
    median_ms: float
    p90_ms: float
    p95_ms: float
    p99_ms: float
    min_ms: float
    max_ms: float
    std_dev_ms: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": self.function_name,
            "calls": self.call_count,
            "total_ms": round(self.total_ms, 3),
            "mean_ms": round(self.mean_ms, 3),
            "median_ms": round(self.median_ms, 3),
            "p90_ms": round(self.p90_ms, 3),
            "p95_ms": round(self.p95_ms, 3),
            "p99_ms": round(self.p99_ms, 3),
            "min_ms": round(self.min_ms, 3),
            "max_ms": round(self.max_ms, 3),
            "std_dev_ms": round(self.std_dev_ms, 3),
        }


# --- Statistical helpers ------------------------------------------------

def percentile(sorted_values: list[float], pct: float) -> float:
    """Compute percentile using linear interpolation method."""
    if not sorted_values:
        return 0.0
    if len(sorted_values) == 1:
        return sorted_values[0]
    rank = (pct / 100.0) * (len(sorted_values) - 1)
    lower = int(math.floor(rank))
    upper = min(lower + 1, len(sorted_values) - 1)
    weight = rank - lower
    return sorted_values[lower] + weight * (sorted_values[upper] - sorted_values[lower])


def std_dev(values: list[float], mean: float) -> float:
    """Population standard deviation."""
    if len(values) < 2:
        return 0.0
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return math.sqrt(variance)


# --- Profiler -----------------------------------------------------------

class ResponseTimeProfiler:
    """Collects timing data and generates statistical reports.

    Usage:
        profiler = ResponseTimeProfiler()

        @profiler.track
        def my_function():
            ...

        # Or use context manager:
        with profiler.measure("operation_name"):
            ...

        report = profiler.report("my_function")
    """

    def __init__(self) -> None:
        self._records: dict[str, list[float]] = {}

    def record(self, name: str, duration_ms: float) -> None:
        """Record a timing measurement."""
        if name not in self._records:
            self._records[name] = []
        self._records[name].append(duration_ms)

    @contextmanager
    def measure(self, name: str) -> Generator[None, None, None]:
        """Context manager that times the enclosed block."""
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            self.record(name, elapsed_ms)

    def track(self, func: Callable) -> Callable:
        """Decorator that automatically profiles a function."""
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed_ms = (time.perf_counter() - start) * 1000
                self.record(func.__name__, elapsed_ms)
        wrapper.__name__ = func.__name__
        wrapper.__wrapped__ = func  # type: ignore[attr-defined]
        return wrapper

    def report(self, name: str) -> ProfileReport:
        """Generate a statistical report for a profiled function."""
        durations = self._records.get(name, [])
        if not durations:
            return ProfileReport(
                function_name=name, call_count=0,
                total_ms=0, mean_ms=0, median_ms=0,
                p90_ms=0, p95_ms=0, p99_ms=0,
                min_ms=0, max_ms=0, std_dev_ms=0,
            )

        sorted_d = sorted(durations)
        count = len(sorted_d)
        total = sum(sorted_d)
        mean = total / count

        return ProfileReport(
            function_name=name,
            call_count=count,
            total_ms=total,
            mean_ms=mean,
            median_ms=percentile(sorted_d, 50),
            p90_ms=percentile(sorted_d, 90),
            p95_ms=percentile(sorted_d, 95),
            p99_ms=percentile(sorted_d, 99),
            min_ms=sorted_d[0],
            max_ms=sorted_d[-1],
            std_dev_ms=std_dev(sorted_d, mean),
        )

    def all_reports(self) -> list[ProfileReport]:
        """Generate reports for all tracked functions."""
        return [self.report(name) for name in sorted(self._records)]

    def names(self) -> list[str]:
        """Return names of all profiled functions."""
        return sorted(self._records.keys())

    def find_bottleneck(self) -> ProfileReport | None:
        """Identify the function with the highest p95 latency."""
        reports = self.all_reports()
        if not reports:
            return None
        return max(reports, key=lambda r: r.p95_ms)


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    """Demonstrate profiling with simulated workloads."""
    profiler = ResponseTimeProfiler()

    @profiler.track
    def fast_operation() -> None:
        time.sleep(0.001)

    @profiler.track
    def slow_operation() -> None:
        time.sleep(0.005)

    @profiler.track
    def variable_operation() -> None:
        import random
        time.sleep(random.uniform(0.001, 0.01))

    # Run each function multiple times
    for _ in range(20):
        fast_operation()
        slow_operation()
        variable_operation()

    # Also demonstrate context manager
    for _ in range(10):
        with profiler.measure("inline_block"):
            time.sleep(0.002)

    reports = profiler.all_reports()
    bottleneck = profiler.find_bottleneck()

    return {
        "profiles": [r.to_dict() for r in reports],
        "bottleneck": bottleneck.to_dict() if bottleneck else None,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Response time profiler")
    parser.add_argument("--demo", action="store_true", default=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    output = run_demo()
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
