# Retry Loop Practice — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Retry Loop Practice — complete annotated solution."""

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
    """Retry a function with exponential backoff.

    Delay pattern: attempt 1 waits `delay`, attempt 2 waits `delay * backoff_factor`,
    attempt 3 waits `delay * backoff_factor^2`, etc.
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

            # WHY: Return immediately on success. There is no reason to
            # keep retrying once the operation succeeds.
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

            # WHY: Only sleep if more attempts remain. Sleeping after the
            # last failure wastes time with no benefit.
            if attempt_num < max_attempts:
                time.sleep(current_delay)
                # WHY: Exponential backoff — each wait is longer than the last.
                # This prevents overwhelming a struggling service with rapid
                # retries (the "thundering herd" problem).
                current_delay *= backoff_factor

    # WHY: If we exit the loop, all attempts failed.
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
    """Retry without sleep — useful for testing (no real delays)."""
    # WHY: Tests should run in milliseconds, not seconds. This version
    # has the same retry logic but skips time.sleep, making it suitable
    # for unit tests that verify retry behavior.
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

    Simulates an unreliable network call, database query, or API.
    """
    # WHY: Using a local Random instance with a seed makes the "randomness"
    # reproducible — essential for testing. Global random.random() would
    # produce different results every run.
    rng = random.Random(seed)

    def flaky():
        # WHY: rng.random() returns a float in [0, 1). If it is below
        # the failure_rate, we simulate a failure. A rate of 0.6 means
        # 60% of calls fail.
        if rng.random() < failure_rate:
            raise error_type("Simulated failure — service unavailable")
        return success_value

    return flaky


def make_countdown_function(failures_before_success: int = 2) -> callable:
    """Create a function that fails a fixed number of times then succeeds.

    Useful for deterministic testing — you know exactly when it will work.
    """
    # WHY: Using a mutable list [0] instead of a plain integer because
    # closures can read outer variables but cannot reassign them without
    # the `nonlocal` keyword. A list is mutable, so call_count[0] += 1
    # works. This is the closure-with-mutable-state pattern.
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
    """Summarise multiple retry results."""
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
    parser.add_argument("--attempts", type=int, default=5, help="Max retry attempts")
    parser.add_argument(
        "--failure-rate", type=float, default=0.6, help="Probability of failure (0-1)"
    )
    parser.add_argument("--operations", type=int, default=10, help="Number of operations")
    parser.add_argument("--delay", type=float, default=0.01, help="Initial retry delay")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    return parser.parse_args()


def main() -> None:
    """Entry point: simulate unreliable operations with retry logic."""
    args = parse_args()

    print(f"Simulating {args.operations} operations "
          f"(failure_rate={args.failure_rate}, max_attempts={args.attempts})\n")

    results: list[dict] = []

    for i in range(args.operations):
        # WHY: seed + i gives each operation a different but reproducible
        # random sequence. Without this, all operations would have identical
        # failure patterns.
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
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Exponential backoff | Each retry waits longer than the last (0.1s, 0.2s, 0.4s, ...). This gives struggling services time to recover instead of hammering them with rapid retries, which would make the problem worse. |
| Configurable exception types | Not all exceptions should trigger a retry. A `ConnectionError` (network down) is worth retrying; a `ValueError` (bad input) will fail every time. Letting callers specify which exceptions to catch prevents wasteful retries. |
| Separate `retry_no_sleep` for testing | Tests should be fast and deterministic. A retry function that sleeps 0.1s per attempt would make a test suite unbearably slow. The no-sleep version preserves retry logic without the wait. |
| Closure pattern in `make_countdown_function` | The mutable `call_count = [0]` lets the inner function track state across calls without using a class. This is a lightweight alternative to creating a full class with `__init__` and `__call__`. |
| Deterministic seed per operation | `seed + i` ensures each simulated operation has a unique but reproducible failure pattern. This makes debugging possible — you can re-run and get the same results. |

## Alternative Approaches

### Using a decorator for retry

```python
import functools

def with_retry(max_attempts=3, delay=0.1, backoff=2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts:
                        raise
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

@with_retry(max_attempts=5)
def call_api():
    # ... might fail
    pass
```

A decorator applies retry logic transparently — the caller does not even know retries happen. This is elegant for production code but harder to test and debug. The explicit function-call approach in this project makes the retry mechanics visible.

### Using the `tenacity` library

For production retry logic, the `tenacity` library provides battle-tested retry decorators with features like jitter, conditional retries, and callback hooks. The manual implementation here teaches the core algorithm that libraries like `tenacity` build upon.

## Common Pitfalls

1. **Retrying non-transient errors** — Retrying a `ValueError` from bad input is pointless — it will fail the same way every time. Only retry errors that might succeed on the next attempt (network timeouts, rate limits, temporary server errors).

2. **No backoff (constant delay)** — Retrying every 0.1 seconds puts constant pressure on a failing service. Exponential backoff gives the service progressively more recovery time. Adding random jitter (small random variation to the delay) further prevents multiple clients from retrying in sync.

3. **Closure variable reassignment trap** — Writing `count = 0` and then `count += 1` inside a closure causes `UnboundLocalError`. Python sees the assignment and treats `count` as a local variable. The fix is either `nonlocal count` (Python 3) or the mutable-container trick `count = [0]` used in this project.
