"""Level 5 / Project 11 — Retry Backoff Runner.

A configurable retry mechanism with exponential backoff and jitter.
Wraps any callable and retries on specified exception types.

Concepts practiced:
- Exponential backoff with configurable factor and cap
- Jitter to prevent thundering-herd problems
- Higher-order functions (wrapping callables)
- Structured attempt logging for observability
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
    """Set up logging so every retry attempt is traceable."""
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

    Uses exponential backoff: delay = base * factor^(attempt-1).
    The result is capped at *max_delay* to prevent unbounded waits.
    When *jitter* is True a random factor between 0.5 and 1.0 is
    applied to spread out retries from concurrent clients.
    """
    delay = min(base_delay * (backoff_factor ** (attempt - 1)), max_delay)
    if jitter:
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

    Returns ``(result, attempt_log)`` on success.
    Raises the last caught exception if all retries are exhausted.

    Each entry in *attempt_log* records the attempt number, status,
    any error message, and the delay before the next attempt.
    """
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
                attempt,
                max_retries,
                exc,
                delay,
            )
            if attempt < max_retries:
                time.sleep(delay)

    # All retries exhausted — re-raise the last exception.
    raise last_exc  # type: ignore[misc]


# ---------- test harness ----------


def create_flaky_function(fail_count: int = 2) -> Callable[..., Any]:
    """Create a function that fails *fail_count* times then succeeds.

    Useful for testing the retry mechanism with a controlled number
    of failures before eventual success.
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
    """Execute a retry demo: create a flaky function and retry it."""
    func = create_flaky_function(fail_count=fail_count)
    try:
        result, attempt_log = retry_with_backoff(
            func,
            max_retries=max_retries,
            base_delay=base_delay,
            jitter=False,
        )
        status = "success"
    except Exception as exc:
        result = None
        attempt_log = [{"error": str(exc)}]
        status = "failed"

    total_delay = sum(
        entry.get("delay_seconds", 0) for entry in attempt_log
    )
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
    logging.info(
        "Retry run: %s after %d attempts (total delay: %.3fs)",
        status,
        len(attempt_log),
        total_delay,
    )
    return report


# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the retry runner."""
    parser = argparse.ArgumentParser(
        description="Retry with exponential backoff",
    )
    parser.add_argument("--output", default="data/retry_report.json", help="Output report path")
    parser.add_argument("--max-retries", type=int, default=5, help="Maximum retry attempts")
    parser.add_argument("--fail-count", type=int, default=2, help="Simulated failures before success")
    parser.add_argument("--base-delay", type=float, default=0.1, help="Base delay in seconds")
    return parser.parse_args()


def main() -> None:
    """Entry point: configure logging, parse args, run the retry demo."""
    configure_logging()
    args = parse_args()
    report = run(Path(args.output), args.max_retries, args.fail_count, args.base_delay)
    print(
        f"{report['status'].capitalize()} after {report['total_attempts']} attempts "
        f"(total delay: {report['total_delay_seconds']}s)"
    )


if __name__ == "__main__":
    main()
