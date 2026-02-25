"""Level 2 project: Retry Loop Practice.

Heavily commented beginner-friendly script:
- implement retry logic with configurable attempts and backoff,
- simulate unreliable operations that fail randomly,
- log each attempt with timing and outcome.

Skills practiced: try/except, nested data structures, enumerate,
list comprehensions, sorting with key, time measurement.
"""

from __future__ import annotations

import argparse
import json
import random
import time


def retry(
    func,
    max_attempts: int = 3,
    delay: float = 0.1,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,),
) -> dict:
    """Retry a function up to max_attempts times with exponential backoff.

    Each failed attempt waits longer before retrying:
        attempt 1: delay seconds
        attempt 2: delay * backoff_factor seconds
        attempt 3: delay * backoff_factor^2 seconds

    Args:
        func: Callable to retry (takes no arguments).
        max_attempts: Maximum number of tries.
        delay: Initial delay between retries (seconds).
        backoff_factor: Multiplier for delay after each failure.
        exceptions: Tuple of exception types to catch and retry.

    Returns:
        A dict with success status, result, and attempt history.
    """
    attempts: list[dict] = []
    current_delay = delay

    for attempt_num in range(1, max_attempts + 1):
        start = time.perf_counter()

        try:
            result = func()
            elapsed = time.perf_counter() - start

            attempts.append({
                "attempt": attempt_num,
                "success": True,
                "elapsed_ms": round(elapsed * 1000, 2),
            })

            return {
                "success": True,
                "result": result,
                "total_attempts": attempt_num,
                "attempts": attempts,
            }

        except exceptions as exc:
            elapsed = time.perf_counter() - start

            attempts.append({
                "attempt": attempt_num,
                "success": False,
                "error": str(exc),
                "error_type": type(exc).__name__,
                "elapsed_ms": round(elapsed * 1000, 2),
            })

            # Only wait if we have more attempts remaining.
            if attempt_num < max_attempts:
                time.sleep(current_delay)
                current_delay *= backoff_factor

    return {
        "success": False,
        "result": None,
        "total_attempts": max_attempts,
        "attempts": attempts,
        "error": "All retry attempts exhausted",
    }


def retry_no_sleep(
    func,
    max_attempts: int = 3,
    exceptions: tuple = (Exception,),
) -> dict:
    """Retry without sleep — useful for testing (no real delays).

    Same logic as retry() but without time.sleep calls.
    """
    attempts: list[dict] = []

    for attempt_num in range(1, max_attempts + 1):
        try:
            result = func()
            attempts.append({"attempt": attempt_num, "success": True})
            return {
                "success": True,
                "result": result,
                "total_attempts": attempt_num,
                "attempts": attempts,
            }
        except exceptions as exc:
            attempts.append({
                "attempt": attempt_num,
                "success": False,
                "error": str(exc),
            })

    return {
        "success": False,
        "result": None,
        "total_attempts": max_attempts,
        "attempts": attempts,
    }


def make_flaky_function(
    failure_rate: float = 0.5,
    error_type: type = ConnectionError,
    success_value: str = "OK",
    seed: int | None = None,
) -> callable:
    """Create a function that randomly fails at the given rate.

    This simulates an unreliable network call, database query, or API.

    Args:
        failure_rate: Probability of failure (0.0 to 1.0).
        error_type: Exception type to raise on failure.
        success_value: Value to return on success.
        seed: Optional random seed for reproducibility.

    Returns:
        A callable that may raise an exception.
    """
    rng = random.Random(seed)

    def flaky():
        if rng.random() < failure_rate:
            raise error_type("Simulated failure — service unavailable")
        return success_value

    return flaky


def make_countdown_function(failures_before_success: int = 2) -> callable:
    """Create a function that fails a fixed number of times then succeeds.

    Useful for deterministic testing — you know exactly when it will work.
    """
    # Use a mutable list to track state across calls (closure pattern).
    call_count = [0]

    def countdown():
        call_count[0] += 1
        if call_count[0] <= failures_before_success:
            raise ConnectionError(
                f"Attempt {call_count[0]}/{failures_before_success + 1}: not yet"
            )
        return f"Success on attempt {call_count[0]}"

    return countdown


def summarise_retry_results(results: list[dict]) -> dict:
    """Summarise multiple retry results.

    Useful when running retries across many operations.
    """
    successes = [r for r in results if r["success"]]
    failures = [r for r in results if not r["success"]]

    avg_attempts = (
        sum(r["total_attempts"] for r in results) / len(results) if results else 0
    )

    return {
        "total_operations": len(results),
        "successes": len(successes),
        "failures": len(failures),
        "success_rate": round(len(successes) / len(results) * 100, 1) if results else 0,
        "avg_attempts": round(avg_attempts, 2),
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Retry loop practice")
    parser.add_argument(
        "--attempts", type=int, default=5, help="Max retry attempts"
    )
    parser.add_argument(
        "--failure-rate", type=float, default=0.6, help="Probability of failure (0-1)"
    )
    parser.add_argument(
        "--operations", type=int, default=10, help="Number of operations to simulate"
    )
    parser.add_argument(
        "--delay", type=float, default=0.01, help="Initial delay between retries"
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed for reproducibility"
    )
    return parser.parse_args()


def main() -> None:
    """Entry point: simulate unreliable operations with retry logic."""
    args = parse_args()

    print(f"Simulating {args.operations} operations "
          f"(failure_rate={args.failure_rate}, max_attempts={args.attempts})\n")

    results: list[dict] = []

    for i in range(args.operations):
        func = make_flaky_function(
            failure_rate=args.failure_rate,
            seed=args.seed + i,
        )
        result = retry(func, max_attempts=args.attempts, delay=args.delay)

        status = "OK" if result["success"] else "FAILED"
        print(f"  Operation {i + 1}: {status} (attempts: {result['total_attempts']})")
        results.append(result)

    summary = summarise_retry_results(results)
    print(f"\n=== Summary ===")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
