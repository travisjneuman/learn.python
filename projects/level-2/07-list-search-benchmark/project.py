"""Level 2 project: List Search Benchmark.

Heavily commented beginner-friendly script:
- implement linear search and binary search,
- time each approach on lists of increasing size,
- compare performance to understand Big-O in practice.

Skills practiced: sorting with key, enumerate, nested data structures,
try/except, list comprehensions, time measurement.
"""

from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path


def linear_search(data: list[int], target: int) -> int:
    """Find target in data by checking every element left to right.

    Time complexity: O(n) — worst case checks every element.

    Returns:
        The index of target, or -1 if not found.
    """
    for idx, value in enumerate(data):
        if value == target:
            return idx
    return -1


def binary_search(data: list[int], target: int) -> int:
    """Find target in a SORTED list by halving the search space.

    Time complexity: O(log n) — cuts the problem in half each step.
    IMPORTANT: data must be sorted for this to work correctly.

    Returns:
        The index of target in the sorted list, or -1 if not found.
    """
    low = 0
    high = len(data) - 1

    while low <= high:
        # Find the middle index.
        mid = (low + high) // 2

        if data[mid] == target:
            return mid
        elif data[mid] < target:
            # Target is in the right half.
            low = mid + 1
        else:
            # Target is in the left half.
            high = mid - 1

    return -1


def set_search(data_set: set[int], target: int) -> bool:
    """Check if target exists in a set.

    Time complexity: O(1) average — hash table lookup.
    But building the set is O(n), so this only wins
    when you search the same data many times.
    """
    return target in data_set


def time_search(search_func, *args, iterations: int = 100) -> float:
    """Time a search function over multiple iterations.

    Returns the average time in microseconds.

    Using time.perf_counter() for high-resolution timing.
    """
    total = 0.0
    for _ in range(iterations):
        start = time.perf_counter()
        search_func(*args)
        end = time.perf_counter()
        total += end - start

    # Convert seconds to microseconds and return average.
    return (total / iterations) * 1_000_000


def generate_test_data(size: int, seed: int = 42) -> list[int]:
    """Generate a list of unique random integers.

    Using a fixed seed so results are reproducible across runs.
    """
    rng = random.Random(seed)
    return rng.sample(range(size * 10), size)


def run_benchmark(
    sizes: list[int] | None = None,
    iterations: int = 100,
) -> list[dict]:
    """Run search benchmarks across multiple list sizes.

    For each size, times linear search, binary search, and set lookup.
    Returns a list of result dicts with timing data.
    """
    if sizes is None:
        sizes = [100, 1000, 5000, 10000, 50000]

    results: list[dict] = []

    for size in sizes:
        data = generate_test_data(size)
        # Pick a target that exists (middle element) and one that does not.
        sorted_data = sorted(data)
        existing_target = sorted_data[size // 2]
        missing_target = -1  # guaranteed not in data (all positive)

        # Time linear search (needs unsorted data).
        linear_found = time_search(
            linear_search, data, existing_target, iterations=iterations
        )
        linear_miss = time_search(
            linear_search, data, missing_target, iterations=iterations
        )

        # Time binary search (needs sorted data).
        binary_found = time_search(
            binary_search, sorted_data, existing_target, iterations=iterations
        )
        binary_miss = time_search(
            binary_search, sorted_data, missing_target, iterations=iterations
        )

        # Time set search (needs a set).
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
        "--sizes",
        nargs="+",
        type=int,
        default=[100, 1000, 5000, 10000],
        help="List sizes to benchmark",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=50,
        help="Number of iterations per measurement",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )
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
