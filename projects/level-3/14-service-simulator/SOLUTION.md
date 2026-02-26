# Service Simulator — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Level 3 project: Service Simulator."""

from __future__ import annotations

import argparse
import json
import logging
import random
import time
from dataclasses import dataclass, field, asdict
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ServiceResponse:
    """Simulated HTTP response."""
    status_code: int
    body: dict = field(default_factory=dict)
    headers: dict = field(default_factory=dict)
    latency_ms: float = 0.0
    error: Optional[str] = None


@dataclass
class ServiceConfig:
    """Configuration for the simulated service.

    WHY: all probabilities are explicit and configurable. This lets
    tests create services with 100% failure rate or 100% success
    rate to verify specific code paths.
    """
    success_rate: float = 0.8
    timeout_rate: float = 0.05
    error_rate: float = 0.1
    rate_limit_rate: float = 0.05
    min_latency_ms: float = 10.0
    max_latency_ms: float = 500.0
    seed: Optional[int] = None


@dataclass
class RequestLog:
    """Log of all requests made to the service."""
    total_requests: int = 0
    successes: int = 0
    errors: int = 0
    timeouts: int = 0
    rate_limits: int = 0
    avg_latency_ms: float = 0.0


class SimulatedService:
    """A simulated HTTP service with configurable failure modes.

    WHY: using a class (instead of standalone functions) groups the
    service state (config, RNG, request count) with its behaviour
    (request, get_log). Each SimulatedService instance is an
    independent service with its own configuration.
    """

    def __init__(self, config: Optional[ServiceConfig] = None) -> None:
        self.config = config or ServiceConfig()
        # WHY: random.Random(seed) creates an independent RNG that
        # does not affect the global random state. With a fixed seed,
        # the sequence of responses is DETERMINISTIC — essential
        # for reproducible tests.
        self._rng = random.Random(self.config.seed)
        self._request_count = 0
        self._latencies: list[float] = []

    def _random_latency(self) -> float:
        """Generate a random latency within configured bounds."""
        return round(
            self._rng.uniform(self.config.min_latency_ms,
                              self.config.max_latency_ms), 2
        )

    def request(self, method: str = "GET", path: str = "/") -> ServiceResponse:
        """Make a simulated request to the service.

        WHY: the random roll determines the outcome. Probabilities
        are checked in priority order: timeout first (most severe),
        then rate limit, then server error. Success is the default
        if none of the failure conditions trigger.
        """
        self._request_count += 1
        latency = self._random_latency()
        self._latencies.append(latency)

        # WHY: a single random number [0, 1) is compared against
        # cumulative probability thresholds. This ensures the rates
        # are respected without multiple random calls.
        roll = self._rng.random()

        # Check failure modes in priority order.
        if roll < self.config.timeout_rate:
            logger.warning("Request %d: Timeout on %s %s",
                           self._request_count, method, path)
            return ServiceResponse(
                status_code=504,
                latency_ms=self.config.max_latency_ms,
                error="Gateway Timeout",
            )

        if roll < self.config.timeout_rate + self.config.rate_limit_rate:
            logger.warning("Request %d: Rate limited", self._request_count)
            return ServiceResponse(
                status_code=429,
                body={"message": "Too Many Requests"},
                # WHY: real rate-limit responses include Retry-After
                # to tell the client when to try again.
                headers={"Retry-After": "60"},
                latency_ms=latency,
            )

        if roll < (self.config.timeout_rate +
                   self.config.rate_limit_rate +
                   self.config.error_rate):
            logger.error("Request %d: Server error on %s %s",
                         self._request_count, method, path)
            return ServiceResponse(
                status_code=500,
                body={"error": "Internal Server Error"},
                latency_ms=latency,
                error="Internal Server Error",
            )

        # Success.
        logger.info("Request %d: %s %s -> 200",
                     self._request_count, method, path)
        return ServiceResponse(
            status_code=200,
            body={"message": "OK", "path": path, "method": method},
            latency_ms=latency,
        )

    def get_log(self) -> RequestLog:
        """Get a summary of all requests made."""
        return RequestLog(
            total_requests=self._request_count,
            successes=sum(1 for l in self._latencies if True),
            avg_latency_ms=(round(sum(self._latencies) / len(self._latencies), 2)
                            if self._latencies else 0.0),
        )


def retry_request(
    service: SimulatedService,
    method: str = "GET",
    path: str = "/",
    max_retries: int = 3,
) -> tuple[ServiceResponse, int]:
    """Make a request with retry logic.

    WHY: transient failures (5xx, 429) are common in distributed
    systems. Retry logic with a maximum attempt count prevents
    both giving up too early and retrying forever.
    """
    for attempt in range(1, max_retries + 1):
        response = service.request(method, path)

        # WHY: 2xx means success — stop retrying.
        if response.status_code < 400:
            return response, attempt

        # WHY: 5xx (server error) and 429 (rate limit) are TRANSIENT —
        # the next attempt might succeed. 4xx (except 429) are CLIENT
        # errors that retrying will not fix.
        if response.status_code == 429 or response.status_code >= 500:
            logger.info("Attempt %d/%d failed (%d), retrying...",
                        attempt, max_retries, response.status_code)
            continue

        # 4xx (except 429) — don't retry.
        return response, attempt

    return response, max_retries


def run_load_test(
    service: SimulatedService,
    num_requests: int,
    path: str = "/api/data",
) -> dict:
    """Run multiple requests and collect statistics.

    WHY: load testing reveals the distribution of responses under
    realistic conditions. The status code histogram shows whether
    the configured rates match expectations.
    """
    results: dict[int, int] = {}

    for _ in range(num_requests):
        response = service.request("GET", path)
        results[response.status_code] = results.get(response.status_code, 0) + 1

    return {
        "total_requests": num_requests,
        "by_status": results,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Service simulator")

    sub = parser.add_subparsers(dest="command")

    single = sub.add_parser("request", help="Make a single request")
    single.add_argument("--method", default="GET")
    single.add_argument("--path", default="/api/data")
    single.add_argument("--seed", type=int, default=None)

    load = sub.add_parser("load", help="Run a load test")
    load.add_argument("--count", type=int, default=100)
    load.add_argument("--seed", type=int, default=None)
    load.add_argument("--json", action="store_true")

    retry = sub.add_parser("retry", help="Request with retries")
    retry.add_argument("--max-retries", type=int, default=3)
    retry.add_argument("--seed", type=int, default=None)

    parser.add_argument("--log-level", default="INFO")
    return parser


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "request":
        service = SimulatedService(ServiceConfig(seed=args.seed))
        response = service.request(args.method, args.path)
        print(json.dumps(asdict(response), indent=2))

    elif args.command == "load":
        service = SimulatedService(ServiceConfig(seed=args.seed))
        results = run_load_test(service, args.count)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"Load test: {results['total_requests']} requests")
            for code, count in sorted(results["by_status"].items()):
                print(f"  {code}: {count}")

    elif args.command == "retry":
        service = SimulatedService(ServiceConfig(seed=args.seed))
        response, attempts = retry_request(
            service, max_retries=args.max_retries)
        print(f"Status: {response.status_code} after {attempts} attempt(s)")
        print(json.dumps(asdict(response), indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| `random.Random(seed)` instance vs global `random` | An instance-level RNG is isolated — setting a seed produces deterministic results without affecting other code that uses `random`. Essential for reproducible tests. |
| Cumulative probability thresholds | One `random()` call determines the outcome by checking against cumulative boundaries (timeout, then +rate_limit, then +error). Simpler and faster than multiple independent random calls. |
| Retry only on 5xx and 429 | 4xx errors (except 429) are client mistakes — retrying the same request will get the same error. 5xx and 429 are transient — the next attempt might succeed. |
| Class for SimulatedService | Encapsulates state (config, RNG, counters) with behaviour (request, get_log). Each instance is an independent service, allowing tests to create multiple services with different configs. |
| Status codes follow real HTTP conventions | 200=success, 429=rate limited, 500=server error, 504=timeout. Using real codes teaches the HTTP status code system in context. |

## Alternative Approaches

### Adding exponential backoff to retries

```python
import time

def retry_with_backoff(service, max_retries=3, base_delay=0.1):
    for attempt in range(1, max_retries + 1):
        response = service.request()
        if response.status_code < 400:
            return response, attempt
        if response.status_code in (429, 500, 502, 503, 504):
            delay = base_delay * (2 ** (attempt - 1))  # 0.1, 0.2, 0.4...
            time.sleep(delay)
            continue
        return response, attempt
    return response, max_retries
```

**Trade-off:** Exponential backoff prevents overwhelming an already-struggling service. Real production code always uses it. But `time.sleep()` makes tests slow — the simulation approach (no actual sleeping) keeps tests fast while teaching the concept.

## Common Pitfalls

1. **Rates summing to more than 1.0** — If `timeout_rate=0.5` and `error_rate=0.6`, no request would ever succeed because the failure thresholds cover the entire [0, 1) range. Validate that rates sum to at most 1.0.

2. **Using global `random` in tests** — `random.random()` depends on global state that other tests or libraries might change. Always use `random.Random(seed)` for an isolated, reproducible RNG in tests.

3. **Retrying on 4xx client errors** — A 400 Bad Request or 403 Forbidden will return the same error every time you retry. Only retry on transient failures (5xx, 429). The `retry_request` function correctly skips 4xx errors.
