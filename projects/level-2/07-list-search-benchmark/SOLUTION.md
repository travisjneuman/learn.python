# List Search Benchmark — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""List Search Benchmark — complete annotated solution."""

from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path


def linear_search(data: list[int], target: int) -> int:
    """Find target by checking every element left to right. O(n)."""
    # WHY: enumerate gives us both the index and value in one pass.
    # Without it, we would need a separate counter variable.
    for idx, value in enumerate(data):
        if value == target:
            return idx
    return -1


def binary_search(data: list[int], target: int) -> int:
    """Find target in a SORTED list by halving the search space. O(log n).

    IMPORTANT: data must be sorted for this to work correctly.
    """
    low = 0
    high = len(data) - 1

    while low <= high:
        # WHY: Integer division (//) finds the middle index. Using (low+high)//2
        # is safe in Python (arbitrary precision ints), but in languages like C
        # or Java this can overflow — the safe form is low + (high - low) // 2.
        mid = (low + high) // 2

        if data[mid] == target:
            return mid
        elif data[mid] < target:
            # WHY: Target is larger than middle, so it must be in the right half.
            # We can safely discard the entire left half including mid.
            low = mid + 1
        else:
            # WHY: Target is smaller, so discard the right half.
            high = mid - 1

    return -1


def set_search(data_set: set[int], target: int) -> bool:
    """Check if target exists in a set. O(1) average."""
    # WHY: The `in` operator on a set uses a hash table lookup, which is
    # O(1) on average. The same `in` on a list would be O(n).
    return target in data_set


def time_search(search_func, *args, iterations: int = 100) -> float:
    """Time a search function over multiple iterations. Returns average microseconds."""
    total = 0.0
    for _ in range(iterations):
        # WHY: perf_counter gives the highest-resolution timer available.
        # time.time() has lower resolution on some platforms (especially Windows).
        start = time.perf_counter()
        search_func(*args)
        end = time.perf_counter()
        total += end - start

    # WHY: Convert seconds to microseconds (multiply by 1,000,000) and
    # average over iterations to reduce noise from OS scheduling.
    return (total / iterations) * 1_000_000


def generate_test_data(size: int, seed: int = 42) -> list[int]:
    """Generate a list of unique random integers."""
    # WHY: Fixed seed makes results reproducible. Without it, every run
    # would produce different numbers and different timings, making
    # comparisons meaningless.
    rng = random.Random(seed)
    # WHY: sample() from a range 10x the size ensures unique values with
    # room to spare. If range equalled size, it would just be a shuffle.
    return rng.sample(range(size * 10), size)


def run_benchmark(
    sizes: list[int] | None = None,
    iterations: int = 100,
) -> list[dict]:
    """Run search benchmarks across multiple list sizes."""
    if sizes is None:
        sizes = [100, 1000, 5000, 10000, 50000]

    results: list[dict] = []

    for size in sizes:
        data = generate_test_data(size)
        sorted_data = sorted(data)
        # WHY: Pick a target that definitely exists (middle of sorted data)
        # and one that definitely does not (-1, since all values are positive).
        # This lets us measure both hit and miss performance.
        existing_target = sorted_data[size // 2]
        missing_target = -1

        # WHY: Linear search runs on unsorted data — it does not need sorting.
        linear_found = time_search(
            linear_search, data, existing_target, iterations=iterations
        )
        linear_miss = time_search(
            linear_search, data, missing_target, iterations=iterations
        )

        # WHY: Binary search requires sorted data. Using sorted_data here.
        binary_found = time_search(
            binary_search, sorted_data, existing_target, iterations=iterations
        )
        binary_miss = time_search(
            binary_search, sorted_data, missing_target, iterations=iterations
        )

        # WHY: Set construction is O(n), but each lookup is O(1). We build
        # the set once outside the timing loop to measure only the lookup cost.
        data_set = set(data)
        set_found = time_search(
            set_search, data_set, existing_target, iterations=iterations
        )
        set_miss = time_search(
            set_search, data_set, missing_target, iterations=iterations
        )

        results.append({
            "size": size,
            "linear_found_us": round(linear_found, 2),
            "linear_miss_us": round(linear_miss, 2),
            "binary_found_us": round(binary_found, 2),
            "binary_miss_us": round(binary_miss, 2),
            "set_found_us": round(set_found, 2),
            "set_miss_us": round(set_miss, 2),
        })

    return results


def format_results(results: list[dict]) -> str:
    """Format benchmark results as a readable table."""
    lines = [
        f"{'Size':>8} | {'Linear(hit)':>12} | {'Linear(miss)':>12} | "
        f"{'Binary(hit)':>12} | {'Binary(miss)':>12} | "
        f"{'Set(hit)':>10} | {'Set(miss)':>10}",
        "-" * 90,
    ]
    for r in results:
        lines.append(
            f"{r['size']:>8} | {r['linear_found_us']:>10.2f}us | "
            f"{r['linear_miss_us']:>10.2f}us | {r['binary_found_us']:>10.2f}us | "
            f"{r['binary_miss_us']:>10.2f}us | {r['set_found_us']:>8.2f}us | "
            f"{r['set_miss_us']:>8.2f}us"
        )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="List search benchmark")
    parser.add_argument(
        "--sizes", nargs="+", type=int, default=[100, 1000, 5000, 10000],
        help="List sizes to benchmark",
    )
    parser.add_argument(
        "--iterations", type=int, default=50,
        help="Number of iterations per measurement",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    return parser.parse_args()


def main() -> None:
    """Entry point: run benchmarks and display results."""
    args = parse_args()
    results = run_benchmark(sizes=args.sizes, iterations=args.iterations)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("=== Search Algorithm Benchmark ===\n")
        print(format_results(results))
        print("\nAll times in microseconds (us). Lower is faster.")
        print("Binary search requires sorted data. Set search requires set construction.")


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Three search algorithms | Linear (O(n)), binary (O(log n)), and set (O(1)) represent the three most important complexity classes for searching. Seeing them side by side makes Big-O tangible instead of abstract. |
| Fixed random seed | Reproducibility is essential for benchmarks. Without a fixed seed, results would change every run, making it impossible to know if a code change improved or worsened performance. |
| `time.perf_counter()` over `time.time()` | `perf_counter` has nanosecond resolution on modern systems. `time.time()` may only have millisecond resolution on Windows, which is too coarse for fast operations. |
| Averaging over many iterations | A single timing measurement is noisy due to OS scheduling, CPU cache effects, and garbage collection. Averaging smooths out these artifacts. |
| Measuring both hit and miss | Miss cases reveal worst-case behavior. Linear search's miss is always O(n) (must check every element). Binary search's miss is still O(log n). Set's miss is still O(1). |

## Alternative Approaches

### Using Python's `bisect` module for binary search

```python
import bisect

def bisect_search(sorted_data, target):
    idx = bisect.bisect_left(sorted_data, target)
    if idx < len(sorted_data) and sorted_data[idx] == target:
        return idx
    return -1
```

`bisect` is a C-implemented binary search in the standard library. It is faster than a pure-Python implementation and is what you should use in production. The manual implementation here teaches the algorithm itself.

### Using `timeit` module instead of manual timing

```python
import timeit

time_us = timeit.timeit(
    lambda: linear_search(data, target),
    number=100
) / 100 * 1_000_000
```

`timeit` automatically handles garbage collection suppression and other timing best practices. The manual approach here makes the timing mechanics visible for learning.

## Common Pitfalls

1. **Running binary search on unsorted data** — Binary search assumes sorted input. On unsorted data it may return wrong answers or miss elements that are present. Always verify data is sorted before using binary search, or sort it first (but remember sorting itself is O(n log n)).

2. **Forgetting set construction cost** — Set lookup is O(1), but building the set from a list is O(n). If you only search once, the total cost is O(n) + O(1) = O(n), same as linear search. Sets only win when you search the same data multiple times.

3. **Benchmarking with too few iterations** — A single measurement on a microsecond-scale operation is dominated by noise. Use at least 50-100 iterations and report the average. For sub-microsecond operations, you may need thousands of iterations.
