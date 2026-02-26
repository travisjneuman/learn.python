# Solution: Level 8 / Project 06 - Response Time Profiler

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first -- it guides
> your thinking without giving away the answer.
>
> [Back to project README](./README.md)

---

## Complete solution

```python
"""Response Time Profiler -- profile function execution with percentile reporting."""

from __future__ import annotations

import argparse
import json
import math
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Callable, Generator


@dataclass
class TimingRecord:
    function_name: str
    duration_ms: float
    timestamp: float = field(default_factory=time.monotonic)


# WHY percentiles instead of just mean? -- Averages hide tail latency.
# A function averaging 10ms but hitting 5s at p99 means 1 in 100 users
# has a terrible experience. P99 reveals the worst case real users hit.
@dataclass
class ProfileReport:
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
            "function": self.function_name, "calls": self.call_count,
            "total_ms": round(self.total_ms, 3), "mean_ms": round(self.mean_ms, 3),
            "median_ms": round(self.median_ms, 3), "p90_ms": round(self.p90_ms, 3),
            "p95_ms": round(self.p95_ms, 3), "p99_ms": round(self.p99_ms, 3),
            "min_ms": round(self.min_ms, 3), "max_ms": round(self.max_ms, 3),
            "std_dev_ms": round(self.std_dev_ms, 3),
        }


# WHY linear interpolation for percentiles? -- Nearest-rank jumps between
# discrete values. Interpolation produces smoother estimates, especially
# important with small sample sizes where jumps would be large.
def percentile(sorted_values: list[float], pct: float) -> float:
    if not sorted_values:
        return 0.0
    if len(sorted_values) == 1:
        return sorted_values[0]
    rank = (pct / 100.0) * (len(sorted_values) - 1)
    lower = int(math.floor(rank))
    upper = min(lower + 1, len(sorted_values) - 1)
    weight = rank - lower
    return sorted_values[lower] + weight * (sorted_values[upper] - sorted_values[lower])


# WHY population std_dev (dividing by N)? -- We have all measurements,
# not a sample drawn from a larger population. Population variance is correct.
def std_dev(values: list[float], mean: float) -> float:
    if len(values) < 2:
        return 0.0
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return math.sqrt(variance)


class ResponseTimeProfiler:
    def __init__(self) -> None:
        self._records: dict[str, list[float]] = {}

    def record(self, name: str, duration_ms: float) -> None:
        if name not in self._records:
            self._records[name] = []
        self._records[name].append(duration_ms)

    @contextmanager
    def measure(self, name: str) -> Generator[None, None, None]:
        # WHY perf_counter? -- Highest resolution timer available, designed
        # for benchmarking. time.time() can have 15ms resolution on Windows.
        start = time.perf_counter()
        try:
            yield
        finally:
            # WHY record in finally? -- If the block raises, we still want
            # the timing. Failure latency is often the most interesting data.
            elapsed_ms = (time.perf_counter() - start) * 1000
            self.record(name, elapsed_ms)

    def track(self, func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed_ms = (time.perf_counter() - start) * 1000
                self.record(func.__name__, elapsed_ms)
        wrapper.__name__ = func.__name__
        wrapper.__wrapped__ = func
        return wrapper

    def report(self, name: str) -> ProfileReport:
        durations = self._records.get(name, [])
        if not durations:
            return ProfileReport(
                function_name=name, call_count=0, total_ms=0, mean_ms=0,
                median_ms=0, p90_ms=0, p95_ms=0, p99_ms=0,
                min_ms=0, max_ms=0, std_dev_ms=0,
            )
        sorted_d = sorted(durations)
        total = sum(sorted_d)
        mean = total / len(sorted_d)
        return ProfileReport(
            function_name=name, call_count=len(sorted_d), total_ms=total,
            mean_ms=mean, median_ms=percentile(sorted_d, 50),
            p90_ms=percentile(sorted_d, 90), p95_ms=percentile(sorted_d, 95),
            p99_ms=percentile(sorted_d, 99),
            min_ms=sorted_d[0], max_ms=sorted_d[-1],
            std_dev_ms=std_dev(sorted_d, mean),
        )

    def all_reports(self) -> list[ProfileReport]:
        return [self.report(name) for name in sorted(self._records)]

    def find_bottleneck(self) -> ProfileReport | None:
        # WHY p95 for bottleneck? -- p50 is too lenient (misses tail issues),
        # p99 can be noisy with few samples. p95 is the standard compromise.
        reports = self.all_reports()
        return max(reports, key=lambda r: r.p95_ms) if reports else None


def run_demo() -> dict[str, Any]:
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

    for _ in range(20):
        fast_operation()
        slow_operation()
        variable_operation()

    for _ in range(10):
        with profiler.measure("inline_block"):
            time.sleep(0.002)

    reports = profiler.all_reports()
    bottleneck = profiler.find_bottleneck()
    return {
        "profiles": [r.to_dict() for r in reports],
        "bottleneck": bottleneck.to_dict() if bottleneck else None,
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Response time profiler")
    parser.add_argument("--demo", action="store_true", default=True)
    parser.parse_args(argv)
    print(json.dumps(run_demo(), indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `time.perf_counter()` for measurement | Highest resolution timer; monotonic; designed for benchmarking | `time.time()` -- up to 15ms resolution on Windows, unsuitable for sub-ms work |
| Decorator + context manager dual API | Decorators profile whole functions; context managers profile arbitrary blocks | Decorator only -- loses ability to profile inline code sections |
| Linear interpolation for percentiles | Smoother estimates than nearest-rank, especially with small sample counts | Nearest-rank -- simpler but produces step-function jumps between values |
| P95 for bottleneck identification | Balances sensitivity and noise; p50 too lenient, p99 too noisy with few samples | Mean-based -- hides the tail latency that matters most to users |

## Alternative approaches

### Approach B: Histogram-based profiler (constant memory)

```python
class HistogramProfiler:
    """Count measurements per bucket instead of storing every value.
    O(1) memory per function regardless of call count."""
    BUCKETS = [1, 5, 10, 25, 50, 100, 250, 500, 1000, 5000]

    def __init__(self):
        self._counts: dict[str, list[int]] = {}

    def record(self, name: str, duration_ms: float):
        if name not in self._counts:
            self._counts[name] = [0] * (len(self.BUCKETS) + 1)
        for i, threshold in enumerate(self.BUCKETS):
            if duration_ms <= threshold:
                self._counts[name][i] += 1
                return
        self._counts[name][-1] += 1
```

**Trade-off:** Histograms use constant memory, ideal for production systems profiling millions of calls. You lose exact percentiles (only bucket-level estimates), but Prometheus and OpenTelemetry both use this approach because memory predictability matters more than precision at scale.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Timer resolution on Windows | `time.time()` has ~15ms resolution, making sub-ms measurements meaningless | Always use `time.perf_counter()` which has microsecond resolution on all platforms |
| GC pause during measurement | Python's garbage collector can inject 10-50ms pauses | Disable GC with `gc.disable()` for critical benchmarks, or accept noise in production profiling |
| Exception inside `measure()` block | Without `finally`, the timing is lost for the most interesting case | The `finally` clause ensures timing is recorded even when the block raises |
