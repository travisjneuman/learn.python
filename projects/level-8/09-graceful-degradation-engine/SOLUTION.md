# Solution: Level 8 / Project 09 - Graceful Degradation Engine

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first -- it guides
> your thinking without giving away the answer.
>
> [Back to project README](./README.md)

---

## Complete solution

```python
"""Graceful Degradation Engine -- degrade service levels based on error rates."""

from __future__ import annotations

import argparse
import json
import random
import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

# WHY three circuit states? -- CLOSED = normal, OPEN = rejecting all,
# HALF_OPEN = probing recovery. Without HALF_OPEN, a transient error
# keeps the circuit open forever. HALF_OPEN lets limited requests
# through to test if the dependency recovered.
class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class ServiceTier(Enum):
    FULL = "full"
    REDUCED = "reduced"
    MINIMAL = "minimal"
    OFFLINE = "offline"

@dataclass
class DegradationConfig:
    error_rate_reduced: float = 0.10
    error_rate_minimal: float = 0.30
    error_rate_offline: float = 0.50
    window_size: int = 100
    recovery_wait_seconds: float = 30
    half_open_max_requests: int = 5

@dataclass
class ServiceStatus:
    circuit_state: CircuitState
    service_tier: ServiceTier
    error_rate: float
    total_requests: int
    total_errors: int
    features_enabled: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "circuit_state": self.circuit_state.value,
            "service_tier": self.service_tier.value,
            "error_rate": round(self.error_rate, 4),
            "total_requests": self.total_requests,
            "total_errors": self.total_errors,
            "features_enabled": self.features_enabled,
        }

TIER_FEATURES: dict[ServiceTier, list[str]] = {
    ServiceTier.FULL: ["search", "recommendations", "analytics", "exports",
                       "notifications", "real_time_updates"],
    ServiceTier.REDUCED: ["search", "recommendations", "notifications"],
    ServiceTier.MINIMAL: ["search"],
    ServiceTier.OFFLINE: [],
}

class SlidingWindowTracker:
    """WHY sliding window? -- Cumulative counters never forget: an incident
    at 3 AM still depresses the rate at 3 PM. A sliding window (deque with
    maxlen) only considers the last N requests, so recovery happens naturally."""

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
        if not self._window:
            return 0.0
        return sum(1 for ok in self._window if not ok) / len(self._window)

    @property
    def total_requests(self) -> int:
        return self._total_requests

    @property
    def total_errors(self) -> int:
        return self._total_errors

class GracefulDegradationEngine:
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
        self._tracker.record_success()
        if self._circuit_state == CircuitState.HALF_OPEN:
            self._half_open_count += 1
            if self._half_open_count >= self._config.half_open_max_requests:
                self._transition_to(CircuitState.CLOSED, ServiceTier.FULL)
        else:
            self._evaluate_tier()

    def record_failure(self) -> None:
        self._tracker.record_failure()
        if self._circuit_state == CircuitState.HALF_OPEN:
            # WHY re-open immediately? -- A failure during recovery testing
            # means the dependency is still broken. Keep the circuit open.
            self._transition_to(CircuitState.OPEN, ServiceTier.OFFLINE)
        else:
            self._evaluate_tier()

    def should_allow_request(self) -> bool:
        if self._circuit_state == CircuitState.CLOSED:
            return True
        if self._circuit_state == CircuitState.OPEN:
            elapsed = time.monotonic() - self._last_state_change
            if elapsed >= self._config.recovery_wait_seconds:
                self._transition_to(CircuitState.HALF_OPEN, ServiceTier.MINIMAL)
                self._half_open_count = 0
                return True
            return False
        return self._half_open_count < self._config.half_open_max_requests

    def _evaluate_tier(self) -> None:
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
            circuit_state=self._circuit_state, service_tier=self._service_tier,
            error_rate=self._tracker.error_rate,
            total_requests=self._tracker.total_requests,
            total_errors=self._tracker.total_errors,
            features_enabled=self.features)

    def force_recovery(self) -> None:
        self._transition_to(CircuitState.CLOSED, ServiceTier.FULL)

def run_demo() -> dict[str, Any]:
    engine = GracefulDegradationEngine(DegradationConfig(window_size=20))
    timeline, rng = [], random.Random(42)
    for i in range(30):
        if engine.should_allow_request():
            engine.record_failure() if rng.random() < 0.05 else engine.record_success()
        if i % 10 == 0:
            timeline.append({"step": i, **engine.status().to_dict()})
    for i in range(30, 60):
        if engine.should_allow_request():
            engine.record_failure() if rng.random() < 0.40 else engine.record_success()
        if i % 10 == 0:
            timeline.append({"step": i, **engine.status().to_dict()})
    engine.force_recovery()
    for i in range(60, 80):
        if engine.should_allow_request():
            engine.record_failure() if rng.random() < 0.02 else engine.record_success()
        if i % 10 == 0:
            timeline.append({"step": i, **engine.status().to_dict()})
    return {"final_status": engine.status().to_dict(), "timeline": timeline}

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Graceful degradation engine")
    parser.add_argument("--window", type=int, default=20)
    parser.parse_args(argv)
    print(json.dumps(run_demo(), indent=2))

if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Sliding window with `deque(maxlen=N)` | Auto-evicts old entries; system recovers as good requests push bad ones out | Cumulative counters -- never forget old errors, requiring manual resets |
| Progressive tier degradation | Preserves core features under stress; disable non-essentials first | Binary on/off -- either full service or total outage, no middle ground |
| HALF_OPEN requires N consecutive successes | Single success could be a fluke; N confirms genuine recovery | Single-request probe -- one lucky request could reopen full traffic prematurely |
| Feature flags tied to tiers | Makes degradation visible: each tier explicitly lists enabled features | Dynamic feature negotiation -- flexible but harder to reason about during incidents |

## Alternative approaches

### Approach B: Exponential backoff for recovery probing

```python
class BackoffRecovery:
    """Double the wait between HALF_OPEN probes after each failure.
    Prevents hammering a struggling dependency with recovery attempts."""
    def __init__(self, base_wait: float = 5.0, max_wait: float = 300.0):
        self.base_wait = base_wait
        self.max_wait = max_wait
        self.failures = 0

    def next_wait(self) -> float:
        wait = min(self.base_wait * (2 ** self.failures), self.max_wait)
        return wait + random.uniform(0, wait * 0.1)  # jitter
```

**Trade-off:** Exponential backoff prevents overwhelming a failing dependency. The cost is slower recovery -- if the dependency fixes in 2 seconds but the backoff is at 60 seconds, users wait unnecessarily. Fixed waits recover faster but risk hammering a struggling service.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Window size too small (5) | One bad request = 20% error rate, triggering premature degradation | Use 50-100 to smooth out noise from individual requests |
| Skipping `should_allow_request()` | Requests hit a broken dependency during OPEN state, worsening the outage | Always gate through `should_allow_request()` before calling dependencies |
| `force_recovery()` while dependency is still down | Floods the broken service with full traffic immediately | Prefer HALF_OPEN probing over force_recovery() in production |
