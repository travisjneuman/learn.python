"""Graceful Degradation Engine — degrade service levels based on error rates.

Design rationale:
    Production systems must degrade gracefully rather than fail completely.
    This project implements a circuit-breaker-style degradation engine that
    monitors error rates and progressively reduces service quality — the
    same pattern used by Netflix, AWS, and every major cloud platform.

Concepts practised:
    - circuit breaker pattern (closed, open, half-open)
    - sliding window error rate calculation
    - service level tiers with feature flags
    - state machine transitions
    - dataclasses for configuration and status
"""

from __future__ import annotations

import argparse
import json
import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# --- Domain types -------------------------------------------------------

# WHY a three-state circuit breaker? -- CLOSED (normal), OPEN (rejecting),
# and HALF_OPEN (probing recovery) prevent cascading failures. Without
# HALF_OPEN, the system would stay OPEN forever after a transient error.
# HALF_OPEN lets a single request through to test if the dependency recovered.
class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # normal operation
    OPEN = "open"          # all requests rejected
    HALF_OPEN = "half_open"  # testing if recovery is possible


class ServiceTier(Enum):
    """Degradation levels from full to minimal."""
    FULL = "full"
    REDUCED = "reduced"
    MINIMAL = "minimal"
    OFFLINE = "offline"


@dataclass
class DegradationConfig:
    """Thresholds for triggering degradation transitions."""
    error_rate_reduced: float = 0.10   # 10% errors -> reduced
    error_rate_minimal: float = 0.30   # 30% errors -> minimal
    error_rate_offline: float = 0.50   # 50% errors -> offline
    window_size: int = 100             # sliding window size
    recovery_wait_seconds: float = 30  # time before attempting recovery
    half_open_max_requests: int = 5    # test requests in half-open state


@dataclass
class ServiceStatus:
    """Current status of the degradation engine."""
    circuit_state: CircuitState
    service_tier: ServiceTier
    error_rate: float
    total_requests: int
    total_errors: int
    features_enabled: list[str]
    last_state_change: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "circuit_state": self.circuit_state.value,
            "service_tier": self.service_tier.value,
            "error_rate": round(self.error_rate, 4),
            "total_requests": self.total_requests,
            "total_errors": self.total_errors,
            "features_enabled": self.features_enabled,
        }


# --- Feature flags per tier ---------------------------------------------

TIER_FEATURES: dict[ServiceTier, list[str]] = {
    ServiceTier.FULL: [
        "search", "recommendations", "analytics", "exports",
        "notifications", "real_time_updates",
    ],
    ServiceTier.REDUCED: [
        "search", "recommendations", "notifications",
    ],
    ServiceTier.MINIMAL: [
        "search",
    ],
    ServiceTier.OFFLINE: [],
}


# --- Sliding window tracker ---------------------------------------------

class SlidingWindowTracker:
    """Tracks success/failure within a sliding window of fixed size."""

    def __init__(self, window_size: int = 100) -> None:
        self._window: deque[bool] = deque(maxlen=window_size)
        self._total_requests = 0
        self._total_errors = 0

    def record_success(self) -> None:
        self._window.append(True)
        self._total_requests += 1

    def record_failure(self) -> None:
        self._window.append(False)
        self._total_requests += 1
        self._total_errors += 1

    @property
    def error_rate(self) -> float:
        """Current error rate within the sliding window."""
        if not self._window:
            return 0.0
        failures = sum(1 for ok in self._window if not ok)
        return failures / len(self._window)

    @property
    def total_requests(self) -> int:
        return self._total_requests

    @property
    def total_errors(self) -> int:
        return self._total_errors

    @property
    def window_fill(self) -> int:
        return len(self._window)


# --- Degradation engine -------------------------------------------------

class GracefulDegradationEngine:
    """Manages service degradation based on error rates.

    The engine acts as a circuit breaker with progressive degradation:
    1. CLOSED + FULL: Normal operation, all features enabled.
    2. CLOSED + REDUCED: High error rate, non-essential features disabled.
    3. CLOSED + MINIMAL: Very high errors, only core features remain.
    4. OPEN + OFFLINE: Error rate critical, all requests rejected.
    5. HALF_OPEN: Testing recovery with limited requests.
    """

    def __init__(self, config: DegradationConfig | None = None) -> None:
        self._config = config or DegradationConfig()
        self._tracker = SlidingWindowTracker(self._config.window_size)
        self._circuit_state = CircuitState.CLOSED
        self._service_tier = ServiceTier.FULL
        self._last_state_change = time.monotonic()
        self._half_open_count = 0

    @property
    def circuit_state(self) -> CircuitState:
        return self._circuit_state

    @property
    def service_tier(self) -> ServiceTier:
        return self._service_tier

    @property
    def features(self) -> list[str]:
        return TIER_FEATURES[self._service_tier]

    def record_success(self) -> None:
        """Record a successful request."""
        self._tracker.record_success()
        if self._circuit_state == CircuitState.HALF_OPEN:
            self._half_open_count += 1
            if self._half_open_count >= self._config.half_open_max_requests:
                self._transition_to(CircuitState.CLOSED, ServiceTier.FULL)
        else:
            self._evaluate_tier()

    def record_failure(self) -> None:
        """Record a failed request."""
        self._tracker.record_failure()
        if self._circuit_state == CircuitState.HALF_OPEN:
            self._transition_to(CircuitState.OPEN, ServiceTier.OFFLINE)
        else:
            self._evaluate_tier()

    def should_allow_request(self) -> bool:
        """Decide whether to allow the next request through."""
        if self._circuit_state == CircuitState.CLOSED:
            return True
        if self._circuit_state == CircuitState.OPEN:
            elapsed = time.monotonic() - self._last_state_change
            if elapsed >= self._config.recovery_wait_seconds:
                self._transition_to(CircuitState.HALF_OPEN, ServiceTier.MINIMAL)
                self._half_open_count = 0
                return True
            return False
        # Half-open: allow limited requests
        return self._half_open_count < self._config.half_open_max_requests

    def _evaluate_tier(self) -> None:
        """Evaluate error rate and adjust service tier."""
        rate = self._tracker.error_rate
        cfg = self._config

        if rate >= cfg.error_rate_offline:
            self._transition_to(CircuitState.OPEN, ServiceTier.OFFLINE)
        elif rate >= cfg.error_rate_minimal:
            self._set_tier(ServiceTier.MINIMAL)
        elif rate >= cfg.error_rate_reduced:
            self._set_tier(ServiceTier.REDUCED)
        else:
            self._set_tier(ServiceTier.FULL)

    def _set_tier(self, tier: ServiceTier) -> None:
        if self._service_tier != tier:
            self._service_tier = tier
            self._last_state_change = time.monotonic()

    def _transition_to(self, state: CircuitState, tier: ServiceTier) -> None:
        self._circuit_state = state
        self._service_tier = tier
        self._last_state_change = time.monotonic()

    def status(self) -> ServiceStatus:
        return ServiceStatus(
            circuit_state=self._circuit_state,
            service_tier=self._service_tier,
            error_rate=self._tracker.error_rate,
            total_requests=self._tracker.total_requests,
            total_errors=self._tracker.total_errors,
            features_enabled=self.features,
        )

    def force_recovery(self) -> None:
        """Manually force recovery to full service."""
        self._transition_to(CircuitState.CLOSED, ServiceTier.FULL)


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    """Simulate a degradation scenario."""
    engine = GracefulDegradationEngine(DegradationConfig(window_size=20))
    timeline: list[dict[str, Any]] = []

    import random
    rng = random.Random(42)

    # Phase 1: Normal operation (low error rate)
    for i in range(30):
        if engine.should_allow_request():
            if rng.random() < 0.05:
                engine.record_failure()
            else:
                engine.record_success()
        if i % 10 == 0:
            timeline.append({"step": i, **engine.status().to_dict()})

    # Phase 2: Spike in errors
    for i in range(30, 60):
        if engine.should_allow_request():
            if rng.random() < 0.40:
                engine.record_failure()
            else:
                engine.record_success()
        if i % 10 == 0:
            timeline.append({"step": i, **engine.status().to_dict()})

    # Phase 3: Recovery
    engine.force_recovery()
    for i in range(60, 80):
        if engine.should_allow_request():
            if rng.random() < 0.02:
                engine.record_failure()
            else:
                engine.record_success()
        if i % 10 == 0:
            timeline.append({"step": i, **engine.status().to_dict()})

    return {
        "final_status": engine.status().to_dict(),
        "timeline": timeline,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Graceful degradation engine")
    parser.add_argument("--window", type=int, default=20, help="Sliding window size")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    output = run_demo()
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
