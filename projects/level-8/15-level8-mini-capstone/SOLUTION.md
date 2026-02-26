# Solution: Level 8 / Project 15 - Level 8 Mini Capstone

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first -- it guides
> your thinking without giving away the answer.
>
> [Back to project README](./README.md)

---

## Complete solution

```python
"""Level 8 Mini Capstone -- full observability platform integrating KPIs,
profiling, SLA monitoring, and fault injection from the entire level."""

from __future__ import annotations

import argparse
import json
import math
import random
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class ServiceHealth(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    DOWN = "down"

# WHY raw latency samples instead of pre-computed averages? -- Keeping
# individual measurements lets you compute any statistic after the fact:
# mean, percentiles, histograms. Pre-computing averages loses the
# distribution shape, making tail latency invisible.
@dataclass
class ServiceMetrics:
    name: str
    latency_ms: list[float] = field(default_factory=list)
    error_count: int = 0
    success_count: int = 0
    uptime_checks: int = 0
    uptime_passes: int = 0

    @property
    def request_count(self) -> int:
        return self.error_count + self.success_count

    @property
    def error_rate(self) -> float:
        return self.error_count / self.request_count if self.request_count else 0.0

    @property
    def availability(self) -> float:
        return self.uptime_passes / self.uptime_checks * 100 if self.uptime_checks else 100.0

    @property
    def p50_latency(self) -> float:
        return _percentile(self.latency_ms, 50)

    @property
    def p95_latency(self) -> float:
        return _percentile(self.latency_ms, 95)

    @property
    def p99_latency(self) -> float:
        return _percentile(self.latency_ms, 99)

    # WHY multi-signal health classification? -- A service can be unhealthy
    # for different reasons: high error rate, high latency, or low availability.
    # Checking all three signals prevents blind spots.
    def health(self) -> ServiceHealth:
        if self.availability < 95:
            return ServiceHealth.DOWN
        if self.error_rate > 0.10 or self.p99_latency > 1000:
            return ServiceHealth.CRITICAL
        if self.error_rate > 0.05 or self.p99_latency > 500:
            return ServiceHealth.DEGRADED
        return ServiceHealth.HEALTHY

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name, "requests": self.request_count,
            "error_rate_pct": round(self.error_rate * 100, 2),
            "availability_pct": round(self.availability, 2),
            "p50_ms": round(self.p50_latency, 1),
            "p95_ms": round(self.p95_latency, 1),
            "p99_ms": round(self.p99_latency, 1),
            "health": self.health().value,
        }

@dataclass
class Alert:
    service: str
    severity: str
    message: str
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {"service": self.service, "severity": self.severity, "message": self.message}

@dataclass
class PlatformReport:
    services: list[ServiceMetrics]
    alerts: list[Alert]
    overall_health: ServiceHealth

    def to_dict(self) -> dict[str, Any]:
        return {
            "overall_health": self.overall_health.value,
            "service_count": len(self.services),
            "alert_count": len(self.alerts),
            "services": [s.to_dict() for s in self.services],
            "alerts": [a.to_dict() for a in self.alerts[:20]],
            "summary": {
                "healthy": sum(1 for s in self.services if s.health() == ServiceHealth.HEALTHY),
                "degraded": sum(1 for s in self.services if s.health() == ServiceHealth.DEGRADED),
                "critical": sum(1 for s in self.services if s.health() == ServiceHealth.CRITICAL),
                "down": sum(1 for s in self.services if s.health() == ServiceHealth.DOWN),
            },
        }

def _percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    idx = max(0, math.ceil(pct / 100 * len(s)) - 1)
    return s[idx]

class ObservabilityPlatform:
    """WHY a unified platform? -- This capstone integrates the entire level:
    metrics collection (project 01), profiling (06), alerting (13), and
    health classification (09). A single platform object coordinates
    all subsystems, just like Datadog or Grafana in production."""

    def __init__(self, service_names: list[str]) -> None:
        self._metrics = {name: ServiceMetrics(name=name) for name in service_names}
        self._alerts: list[Alert] = []

    def record_request(self, service: str, latency_ms: float, success: bool) -> None:
        metrics = self._metrics.get(service)
        if not metrics:
            return
        metrics.latency_ms.append(latency_ms)
        if success:
            metrics.success_count += 1
        else:
            metrics.error_count += 1

    def record_health_check(self, service: str, passed: bool) -> None:
        metrics = self._metrics.get(service)
        if not metrics:
            return
        metrics.uptime_checks += 1
        if passed:
            metrics.uptime_passes += 1

    def evaluate_alerts(self) -> list[Alert]:
        new_alerts: list[Alert] = []
        for metrics in self._metrics.values():
            health = metrics.health()
            if health == ServiceHealth.CRITICAL:
                alert = Alert(service=metrics.name, severity="critical",
                              message=f"{metrics.name}: error_rate={metrics.error_rate:.1%}, p99={metrics.p99_latency:.0f}ms")
                new_alerts.append(alert)
                self._alerts.append(alert)
            elif health == ServiceHealth.DEGRADED:
                alert = Alert(service=metrics.name, severity="warning",
                              message=f"{metrics.name}: degraded performance")
                new_alerts.append(alert)
                self._alerts.append(alert)
            elif health == ServiceHealth.DOWN:
                alert = Alert(service=metrics.name, severity="page",
                              message=f"{metrics.name}: service DOWN, availability={metrics.availability:.1f}%")
                new_alerts.append(alert)
                self._alerts.append(alert)
        return new_alerts

    # WHY worst-status-wins? -- A platform with one DOWN service is not
    # healthy overall. The worst individual health determines the platform state.
    def report(self) -> PlatformReport:
        services = list(self._metrics.values())
        healths = [s.health() for s in services]
        if ServiceHealth.DOWN in healths:
            overall = ServiceHealth.DOWN
        elif ServiceHealth.CRITICAL in healths:
            overall = ServiceHealth.CRITICAL
        elif ServiceHealth.DEGRADED in healths:
            overall = ServiceHealth.DEGRADED
        else:
            overall = ServiceHealth.HEALTHY
        return PlatformReport(services=services, alerts=self._alerts, overall_health=overall)

def run_simulation(num_requests: int = 200, seed: int = 42) -> dict[str, Any]:
    rng = random.Random(seed)
    profiles = {
        "api-gateway": {"latency_base": 50, "error_prob": 0.02, "down_prob": 0.0},
        "user-service": {"latency_base": 30, "error_prob": 0.01, "down_prob": 0.0},
        "payment-service": {"latency_base": 200, "error_prob": 0.08, "down_prob": 0.01},
        "search-service": {"latency_base": 100, "error_prob": 0.03, "down_prob": 0.0},
        "notification-svc": {"latency_base": 80, "error_prob": 0.15, "down_prob": 0.02},
    }
    platform = ObservabilityPlatform(list(profiles.keys()))
    for _ in range(num_requests):
        for svc_name, profile in profiles.items():
            latency = max(1, rng.gauss(profile["latency_base"], profile["latency_base"] * 0.3))
            success = rng.random() > profile["error_prob"]
            platform.record_request(svc_name, latency, success)
            platform.record_health_check(svc_name, rng.random() > profile["down_prob"])
    platform.evaluate_alerts()
    return platform.report().to_dict()

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Level 8 Capstone: Observability Platform")
    parser.add_argument("--requests", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args(argv)
    print(json.dumps(run_simulation(num_requests=args.requests, seed=args.seed), indent=2))

if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Raw latency samples stored per service | Enables computing any statistic (mean, percentiles, histograms) after collection | Pre-aggregated averages -- loses distribution shape, hides tail latency |
| Multi-signal health (error rate + latency + availability) | A service can be unhealthy for different reasons; checking all three prevents blind spots | Single-metric health -- misses problems visible only in other dimensions |
| Worst-status-wins for overall health | One DOWN service means the platform needs attention regardless of others | Majority voting -- hides critical issues when most services are healthy |
| Service profiles with configurable error/latency | Realistic simulation where each service has different characteristics | Uniform profiles -- oversimplifies; real systems have heterogeneous services |
| Unified platform class | Single coordination point for metrics, health checks, and alerts | Separate systems -- harder to get a holistic view of platform health |

## Alternative approaches

### Approach B: Event-driven architecture with pub/sub

```python
class EventBus:
    """Instead of direct method calls, emit events that multiple
    subscribers process. Enables adding new alert channels without
    modifying the platform."""
    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable):
        self._subscribers[event_type].append(handler)

    def emit(self, event_type: str, data: dict):
        for handler in self._subscribers[event_type]:
            handler(data)
```

**Trade-off:** Event-driven architecture decouples metric collection from alerting, enabling multiple alert channels (Slack, PagerDuty, email) without modifying the core platform. The tradeoff is increased complexity and harder debugging (events flow through multiple handlers). Use direct method calls for simple systems, event-driven for platforms with multiple consumers.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Service with zero requests | `error_rate` divides by zero | Guard with `if self.request_count else 0.0` |
| Latency list grows unbounded | Memory grows linearly with request count over long-running simulations | Add a sliding window or periodic aggregation to bound memory usage |
| Alert fatigue from repeated alerts | `evaluate_alerts()` fires alerts for every degraded service on every call | Add hysteresis: only alert on state transitions, not on every evaluation |
