# Retry Backoff Runner — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 5 / Project 11 — Retry Backoff Runner.

A configurable retry mechanism with exponential backoff and jitter.
Wraps any callable and retries on specified exception types.
"""

from __future__ import annotations

import argparse
import json
import logging
import random
import time
from pathlib import Path
from typing import Any, Callable

# ---------- logging ----------

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- retry engine ----------

def compute_delay(
    attempt: int,
    base_delay: float,
    backoff_factor: float,
    max_delay: float,
    jitter: bool,
) -> float:
    """Calculate the delay before the next retry.

    WHY exponential backoff? -- delay = base * factor^(attempt-1).
    With base=1 and factor=2: delays are 1, 2, 4, 8, 16...
    This gives an overloaded system progressively more recovery time.
    """
    delay = min(base_delay * (backoff_factor ** (attempt - 1)), max_delay)
    if jitter:
        # WHY: Multiplying by a random factor between 0.5 and 1.0
        # (instead of 0.0 and 1.0) ensures the delay is always at least
        # half the computed value. Full jitter (0.0-1.0) can produce
        # near-zero delays that defeat the purpose of backoff.
        delay = delay * (0.5 + random.random() * 0.5)
    return round(delay, 4)


def retry_with_backoff(
    func: Callable[..., Any],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    retry_on: tuple[type, ...] = (Exception,),
) -> tuple[object, list[dict]]:
    """Execute *func* with retry and exponential backoff.

    Returns (result, attempt_log) on success.
    Raises the last caught exception if all retries are exhausted.
    """
    # WHY: Validate inputs upfront. Negative delays or zero retries
    # would cause confusing behavior downstream.
    if max_retries < 1:
        raise ValueError("max_retries must be at least 1")
    if base_delay < 0:
        raise ValueError("base_delay must be non-negative")

    attempt_log: list[dict] = []
    last_exc: Exception | None = None

    for attempt in range(1, max_retries + 1):
        try:
            result = func()
            attempt_log.append({"attempt": attempt, "status": "success"})
            logging.info("Attempt %d succeeded", attempt)
            return result, attempt_log
        except retry_on as exc:
            # WHY: Only catch the exception types listed in retry_on.
            # A KeyboardInterrupt or SystemExit should not be retried.
            last_exc = exc
            delay = compute_delay(attempt, base_delay, backoff_factor, max_delay, jitter)
            attempt_log.append({
                "attempt": attempt,
                "status": "failed",
                "error": str(exc),
                "delay_seconds": delay,
            })
            logging.warning(
                "Attempt %d/%d failed: %s (retrying in %.3fs)",
                attempt, max_retries, exc, delay,
            )
            # WHY: Do not sleep after the final attempt — there is
            # nothing to wait for, and it wastes time.
            if attempt < max_retries:
                time.sleep(delay)

    # WHY: Re-raise the last exception so the caller knows what went
    # wrong. The attempt_log is lost here, which is why the caller
    # should wrap this in try/except if they need the log.
    raise last_exc  # type: ignore[misc]

# ---------- test harness ----------

def create_flaky_function(fail_count: int = 2) -> Callable[..., Any]:
    """Create a function that fails *fail_count* times then succeeds.

    WHY a closure with mutable state? -- The function needs to remember
    how many times it has been called. Using a dict ({"calls": 0})
    instead of a plain int works around Python's closure scoping:
    closures can read but not rebind outer variables, but they CAN
    mutate a dict's contents.
    """
    state = {"calls": 0}

    def flaky() -> dict:
        state["calls"] += 1
        if state["calls"] <= fail_count:
            raise ConnectionError(f"Simulated failure #{state['calls']}")
        return {"result": "success", "total_calls": state["calls"]}

    return flaky

# ---------- pipeline ----------

def run(
    output_path: Path,
    max_retries: int = 5,
    fail_count: int = 2,
    base_delay: float = 0.01,
) -> dict:
    func = create_flaky_function(fail_count=fail_count)
    try:
        result, attempt_log = retry_with_backoff(
            func, max_retries=max_retries, base_delay=base_delay, jitter=False,
        )
        status = "success"
    except Exception as exc:
        result = None
        attempt_log = [{"error": str(exc)}]
        status = "failed"

    total_delay = sum(entry.get("delay_seconds", 0) for entry in attempt_log)
    report = {
        "status": status,
        "result": result,
        "attempts": attempt_log,
        "total_attempts": len(attempt_log),
        "total_delay_seconds": round(total_delay, 3),
        "max_retries": max_retries,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info("Retry run: %s after %d attempts (total delay: %.3fs)",
                 status, len(attempt_log), total_delay)
    return report

# ---------- CLI ----------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retry with exponential backoff")
    parser.add_argument("--output", default="data/retry_report.json")
    parser.add_argument("--max-retries", type=int, default=5)
    parser.add_argument("--fail-count", type=int, default=2)
    parser.add_argument("--base-delay", type=float, default=0.1)
    return parser.parse_args()

def main() -> None:
    configure_logging()
    args = parse_args()
    report = run(Path(args.output), args.max_retries, args.fail_count, args.base_delay)
    print(f"{report['status'].capitalize()} after {report['total_attempts']} attempts "
          f"(total delay: {report['total_delay_seconds']}s)")

if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| `retry_on` parameter for selective exception handling | Not all exceptions are retryable. A `ValueError` (bad input) will never succeed on retry, but a `ConnectionError` (network glitch) might. Filtering by exception type prevents wasting retries on permanent failures. |
| Jitter range 0.5-1.0 instead of 0.0-1.0 | Full jitter (0.0-1.0) can produce near-zero delays, which defeats the purpose of backing off. Half-jitter ensures the minimum delay is always at least 50% of the computed backoff. |
| Closure with dict for flaky function state | Python closures can read outer variables but cannot reassign them (without `nonlocal`). Using a mutable dict (`state["calls"]`) sidesteps this limitation and is a common Python pattern. |
| Re-raise last exception on exhaustion | The caller needs to know *what* went wrong. Returning `None` would hide the error. Re-raising lets the caller decide whether to log, retry at a higher level, or abort. |

## Alternative Approaches

### Using the `tenacity` library

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=60),
)
def call_api():
    return requests.get("https://api.example.com/status").json()
```

`tenacity` is the production standard for Python retry logic. It supports dozens of backoff strategies, custom stop conditions, and callback hooks. Building the retry engine manually teaches the underlying algorithm.

## Common Pitfalls

1. **Retrying on `KeyboardInterrupt`** — If `retry_on=(Exception,)`, pressing Ctrl+C during a retry loop is caught and retried. Use `retry_on=(ConnectionError, TimeoutError)` to only retry transient errors.
2. **No maximum delay cap** — Without `max_delay`, exponential growth produces absurd waits. With `factor=2` and `base=1`: attempt 20 would wait 2^19 = 524,288 seconds (6 days). Always cap the delay.
3. **Sleeping after the last attempt** — If all retries fail, sleeping before re-raising the exception wastes time. The `if attempt < max_retries` guard skips the final sleep.
