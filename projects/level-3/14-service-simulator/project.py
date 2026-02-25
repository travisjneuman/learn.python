"""Level 3 project: Service Simulator.

Simulates HTTP service responses (success, error, timeout, rate limit)
without making real network calls. Useful for testing retry logic.

Skills practiced: dataclasses, typing basics, logging, random
simulation, HTTP status codes, error handling patterns.
"""

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
    """Configuration for the simulated service."""
    success_rate: float = 0.8     # 0.0 to 1.0
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

    This class demonstrates encapsulating state and behaviour.
    """

    def __init__(self, config: Optional[ServiceConfig] = None) -> None:
        self.config = config or ServiceConfig()
        self._rng = random.Random(self.config.seed)
        self._request_count = 0
        self._latencies: list[float] = []

    def _random_latency(self) -> float:
        """Generate a random latency within configured bounds."""
        return round(
            self._rng.uniform(self.config.min_latency_ms, self.config.max_latency_ms), 2
        )

    def request(self, method: str = "GET", path: str = "/") -> ServiceResponse:
        """Make a simulated request to the service.

        Returns a ServiceResponse based on configured probabilities.
        """
        self._request_count += 1
        latency = self._random_latency()
        self._latencies.append(latency)

        roll = self._rng.random()

        # Check failure modes in priority order.
        if roll < self.config.timeout_rate:
            logger.warning("Request %d: Timeout on %s %s", self._request_count, method, path)
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
                headers={"Retry-After": "60"},
                latency_ms=latency,
            )

        if roll < self.config.timeout_rate + self.config.rate_limit_rate + self.config.error_rate:
            logger.error("Request %d: Server error on %s %s", self._request_count, method, path)
            return ServiceResponse(
                status_code=500,
                body={"error": "Internal Server Error"},
                latency_ms=latency,
                error="Internal Server Error",
            )

        # Success.
        logger.info("Request %d: %s %s -> 200", self._request_count, method, path)
        return ServiceResponse(
            status_code=200,
            body={"message": "OK", "path": path, "method": method},
            latency_ms=latency,
        )

    def get_log(self) -> RequestLog:
        """Get a summary of all requests made."""
        return RequestLog(
            total_requests=self._request_count,
            successes=sum(1 for l in self._latencies if True),  # Placeholder.
            avg_latency_ms=round(sum(self._latencies) / len(self._latencies), 2)
            if self._latencies else 0.0,
        )


def retry_request(
    service: SimulatedService,
    method: str = "GET",
    path: str = "/",
    max_retries: int = 3,
) -> tuple[ServiceResponse, int]:
    """Make a request with retry logic.

    Retries on 5xx errors and 429 (rate limit).
    Returns the final response and the number of attempts.
    """
    for attempt in range(1, max_retries + 1):
        response = service.request(method, path)

        if response.status_code < 400:
            return response, attempt

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
    """Run multiple requests and collect statistics."""
    results: dict[int, int] = {}

    for _ in range(num_requests):
        response = service.request("GET", path)
        results[response.status_code] = results.get(response.status_code, 0) + 1

    return {
        "total_requests": num_requests,
        "by_status": results,
    }


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser."""
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
    """Entry point."""
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
        response, attempts = retry_request(service, max_retries=args.max_retries)
        print(f"Status: {response.status_code} after {attempts} attempt(s)")
        print(json.dumps(asdict(response), indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
