# API Polling Simulator — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 5 / Project 10 — API Polling Simulator.

Simulates polling an API endpoint at regular intervals with rate
limiting and exponential backoff on errors.
"""

from __future__ import annotations

import argparse
import json
import logging
import random
import time
from pathlib import Path

# ---------- logging ----------

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- mock API ----------

class MockAPI:
    """Simulates an unreliable API with configurable failure rate.

    WHY a mock? -- Testing against a real API is slow, costs money,
    and produces non-deterministic results. A mock with a seeded RNG
    gives reproducible failures for testing while demonstrating
    realistic error patterns.
    """

    def __init__(self, failure_rate: float = 0.2, seed: int | None = None) -> None:
        # WHY: Clamp failure_rate to [0, 1] to prevent invalid probabilities.
        self.failure_rate = max(0.0, min(1.0, failure_rate))
        self.call_count = 0
        # WHY: A separate Random instance (not the global random) ensures
        # the mock's behavior is isolated from other random calls.
        self.rng = random.Random(seed)

    def get_status(self) -> dict:
        """Simulate a single API call."""
        self.call_count += 1
        roll = self.rng.random()

        # WHY: ConnectionError is a real Python exception that HTTP libraries
        # raise on network failures, making the simulation realistic.
        if roll < self.failure_rate:
            raise ConnectionError(
                f"API unavailable (call #{self.call_count}, roll={roll:.3f})"
            )

        return {
            "status": "ok",
            "value": self.rng.randint(1, 100),
            "call_number": self.call_count,
        }

# ---------- polling engine ----------

def calculate_backoff(
    attempt: int,
    base_delay: float,
    max_delay: float,
    jitter: bool = True,
) -> float:
    """Calculate the delay before the next retry using exponential backoff.

    WHY exponential (2^n) instead of linear? -- Doubling the wait time
    gives the overloaded server progressively more breathing room.
    Linear backoff (adding a fixed amount) recovers too aggressively.
    """
    delay = min(base_delay * (2 ** attempt), max_delay)
    if jitter:
        # WHY jitter? -- Without randomness, 100 clients that failed at
        # the same moment would all retry at the exact same time (thundering
        # herd), overwhelming the server again. Jitter spreads retries out.
        delay += delay * 0.1 * random.random()
    return delay


def poll_with_backoff(
    api: MockAPI,
    max_polls: int = 10,
    base_delay: float = 0.01,
    max_delay: float = 1.0,
    max_retries: int = 3,
) -> tuple[list[dict], list[dict]]:
    """Poll the API up to *max_polls* times with exponential backoff.

    Returns (results, errors). Polling stops early if *max_retries*
    consecutive failures occur.
    """
    results: list[dict] = []
    errors: list[dict] = []
    consecutive_failures = 0

    for poll_num in range(1, max_polls + 1):
        try:
            response = api.get_status()
            results.append({"poll": poll_num, **response})
            # WHY: Reset consecutive failures on success. Only consecutive
            # failures trigger early stop — intermittent failures are normal.
            consecutive_failures = 0
            logging.info("Poll %d: %s", poll_num, response)
        except ConnectionError as exc:
            consecutive_failures += 1
            errors.append({
                "poll": poll_num,
                "error": str(exc),
                "retry": consecutive_failures,
            })
            logging.warning("Poll %d failed (attempt %d): %s",
                            poll_num, consecutive_failures, exc)

            # WHY: Stop early after too many consecutive failures. The API
            # is likely down, not just flaky, and continuing wastes resources.
            if consecutive_failures >= max_retries:
                logging.error("Max retries (%d) reached — stopping early", max_retries)
                break

            delay = calculate_backoff(consecutive_failures, base_delay, max_delay)
            time.sleep(delay)
            continue

        # WHY: Short pause between successful polls to respect rate limits.
        time.sleep(base_delay)

    return results, errors

# ---------- pipeline ----------

def run(
    output_path: Path,
    max_polls: int = 10,
    failure_rate: float = 0.2,
    seed: int | None = 42,
) -> dict:
    api = MockAPI(failure_rate=failure_rate, seed=seed)
    results, errors = poll_with_backoff(api, max_polls=max_polls, base_delay=0.01)

    report = {
        "total_polls_attempted": len(results) + len(errors),
        "successful": len(results),
        "failed": len(errors),
        # WHY: max(1, ...) prevents division by zero when no polls run.
        "success_rate": round(len(results) / max(1, len(results) + len(errors)), 2),
        "results": results,
        "errors": errors,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info("Polling complete: %d successful, %d failed out of %d attempted",
                 len(results), len(errors), report["total_polls_attempted"])
    return report

# ---------- CLI ----------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulate API polling with exponential backoff")
    parser.add_argument("--output", default="data/poll_results.json")
    parser.add_argument("--max-polls", type=int, default=10)
    parser.add_argument("--failure-rate", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()

def main() -> None:
    configure_logging()
    args = parse_args()
    report = run(Path(args.output), args.max_polls, args.failure_rate, args.seed)
    print(f"Polling complete: {report['successful']} successful, "
          f"{report['failed']} failed")

if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Exponential backoff (2^n) with max cap | Doubling the delay gives the server progressively more recovery time. The cap prevents unbounded waits (e.g., 2^20 = 1,048,576 seconds). |
| Jitter on retry delays | Without jitter, all clients that failed simultaneously retry at the same moment, causing a "thundering herd" that overwhelms the server again. Random jitter spreads retries across time. |
| Seeded RNG for the MockAPI | A fixed seed produces the same sequence of successes/failures every run, making tests deterministic. Change the seed to explore different failure patterns. |
| Stop after N consecutive failures | Intermittent failures are normal (bad network packet). But 3+ consecutive failures suggest the API is down, not just flaky. Stopping early avoids wasting time and resources. |

## Alternative Approaches

### Using a decorator for retry logic

```python
import functools

def retry(max_retries=3, base_delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(base_delay * (2 ** attempt))
        return wrapper
    return decorator

@retry(max_retries=3)
def call_api():
    return api.get_status()
```

A decorator separates retry logic from business logic. Libraries like `tenacity` and `backoff` provide production-grade retry decorators with configurable backoff strategies, jitter, and exception filtering.

## Common Pitfalls

1. **No maximum delay cap** — Without a cap, exponential backoff can grow to absurd values (2^10 = 1024 seconds = 17 minutes between retries). Always set a `max_delay`.
2. **Retrying on all exceptions** — Not all errors are retryable. A `404 Not Found` will never succeed on retry; a `429 Too Many Requests` or `503 Service Unavailable` will. Filter retry-eligible exceptions.
3. **Fixed-interval polling without backoff** — Polling every 5 seconds regardless of failures keeps hammering a struggling server. Exponential backoff gives the server time to recover.
