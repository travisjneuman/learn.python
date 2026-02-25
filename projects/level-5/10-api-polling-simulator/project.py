"""Level 5 / Project 10 — API Polling Simulator.

Simulates polling an API endpoint at regular intervals with rate
limiting and exponential backoff on errors.  Uses a mock API that
returns randomised results to simulate real-world behaviour.

Concepts practiced:
- Exponential backoff with jitter for rate-limit handling
- Mock objects for deterministic testing
- Time-based polling loops with configurable limits
- Structured result collection and reporting
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
    """Set up logging so every poll attempt is traceable."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


# ---------- mock API ----------


class MockAPI:
    """Simulates an unreliable API with configurable failure rate.

    The random number generator is seeded so that results are
    deterministic for testing, while still demonstrating realistic
    failure patterns.
    """

    def __init__(self, failure_rate: float = 0.2, seed: int | None = None) -> None:
        self.failure_rate = max(0.0, min(1.0, failure_rate))
        self.call_count = 0
        self.rng = random.Random(seed)

    def get_status(self) -> dict:
        """Simulate a single API call.

        Returns a success dict or raises ConnectionError to
        simulate intermittent failures.
        """
        self.call_count += 1
        roll = self.rng.random()

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

    The delay doubles with each consecutive failure but is capped at
    *max_delay*.  Jitter adds a small random component to prevent
    multiple clients from retrying in lockstep (thundering herd).
    """
    delay = min(base_delay * (2 ** attempt), max_delay)
    if jitter:
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

    Returns (results, errors) where *results* contains successful
    responses and *errors* contains failure records.  Polling stops
    early if *max_retries* consecutive failures occur.
    """
    results: list[dict] = []
    errors: list[dict] = []
    consecutive_failures = 0

    for poll_num in range(1, max_polls + 1):
        try:
            response = api.get_status()
            results.append({"poll": poll_num, **response})
            consecutive_failures = 0
            logging.info("Poll %d: %s", poll_num, response)
        except ConnectionError as exc:
            consecutive_failures += 1
            errors.append({
                "poll": poll_num,
                "error": str(exc),
                "retry": consecutive_failures,
            })
            logging.warning(
                "Poll %d failed (attempt %d): %s",
                poll_num,
                consecutive_failures,
                exc,
            )

            if consecutive_failures >= max_retries:
                logging.error("Max retries (%d) reached — stopping early", max_retries)
                break

            delay = calculate_backoff(consecutive_failures, base_delay, max_delay)
            time.sleep(delay)
            continue

        # Short pause between successful polls (rate limiting).
        time.sleep(base_delay)

    return results, errors


# ---------- pipeline ----------


def run(
    output_path: Path,
    max_polls: int = 10,
    failure_rate: float = 0.2,
    seed: int | None = 42,
) -> dict:
    """Execute a full polling session and write the report."""
    api = MockAPI(failure_rate=failure_rate, seed=seed)
    results, errors = poll_with_backoff(api, max_polls=max_polls, base_delay=0.01)

    report = {
        "total_polls_attempted": len(results) + len(errors),
        "successful": len(results),
        "failed": len(errors),
        "success_rate": round(len(results) / max(1, len(results) + len(errors)), 2),
        "results": results,
        "errors": errors,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logging.info(
        "Polling complete: %d successful, %d failed out of %d attempted",
        len(results),
        len(errors),
        report["total_polls_attempted"],
    )
    return report


# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the polling simulator."""
    parser = argparse.ArgumentParser(
        description="Simulate API polling with exponential backoff",
    )
    parser.add_argument("--output", default="data/poll_results.json", help="Output report path")
    parser.add_argument("--max-polls", type=int, default=10, help="Maximum poll attempts")
    parser.add_argument("--failure-rate", type=float, default=0.2, help="Simulated failure rate 0-1")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed for reproducibility")
    return parser.parse_args()


def main() -> None:
    """Entry point: configure logging, parse args, run the poller."""
    configure_logging()
    args = parse_args()
    report = run(Path(args.output), args.max_polls, args.failure_rate, args.seed)
    print(
        f"Polling complete: {report['successful']} successful, "
        f"{report['failed']} failed"
    )


if __name__ == "__main__":
    main()
