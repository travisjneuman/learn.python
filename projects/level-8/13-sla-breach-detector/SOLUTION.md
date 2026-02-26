# Solution: Level 8 / Project 13 - SLA Breach Detector

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
"""SLA Breach Detector -- monitor SLA metrics and detect breaches with alerting."""

from __future__ import annotations

import argparse
import json
import random
import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class SLAMetricType(Enum):
    AVAILABILITY = "availability"
    LATENCY = "latency"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    PAGE = "page"

# WHY separate SLA definitions from measurements? -- SLAs are contractual
# (99.9% uptime per month) while measurements are operational (actual uptime
# this minute). Keeping them separate lets you evaluate the same measurements
# against different SLA tiers (premium vs standard customers).
@dataclass
class SLADefinition:
    name: str
    metric_type: SLAMetricType
    target_value: float
    warning_threshold: float
    window_minutes: int = 60
    unit: str = "%"

@dataclass
class MetricDataPoint:
    timestamp: float
    value: float
    source: str = ""

@dataclass
class SLABreach:
    sla_name: str
    metric_type: SLAMetricType
    current_value: float
    target_value: float
    severity: AlertSeverity
    breach_start: float
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {"sla": self.sla_name, "metric": self.metric_type.value,
                "current": round(self.current_value, 4), "target": self.target_value,
                "severity": self.severity.value, "message": self.message}

@dataclass
class SLAStatus:
    sla_name: str
    current_value: float
    target_value: float
    margin: float  # positive = healthy
    in_breach: bool
    burn_rate: float  # rate of error budget consumption

    def to_dict(self) -> dict[str, Any]:
        return {"sla": self.sla_name, "current": round(self.current_value, 4),
                "target": self.target_value, "margin": round(self.margin, 4),
                "in_breach": self.in_breach, "burn_rate": round(self.burn_rate, 2)}

class SLATracker:
    """Tracks metrics for a single SLA using a sliding time window."""

    def __init__(self, sla: SLADefinition) -> None:
        self._sla = sla
        self._data: deque[MetricDataPoint] = deque()
        self._breaches: list[SLABreach] = []
        # WHY track _in_breach state? -- Hysteresis: only fire an alert on
        # the transition INTO breach, not on every check while breached.
        # This prevents alert storms during sustained outages.
        self._in_breach = False

    @property
    def sla(self) -> SLADefinition:
        return self._sla

    @property
    def breaches(self) -> list[SLABreach]:
        return list(self._breaches)

    def record(self, value: float, timestamp: float | None = None) -> None:
        ts = timestamp or time.time()
        self._data.append(MetricDataPoint(timestamp=ts, value=value))
        self._prune_window(ts)

    def current_value(self) -> float:
        if not self._data:
            return self._sla.target_value  # assume healthy with no data
        return sum(dp.value for dp in self._data) / len(self._data)

    def check(self, timestamp: float | None = None) -> SLABreach | None:
        ts = timestamp or time.time()
        current = self.current_value()
        sla = self._sla

        # WHY direction-aware comparison? -- Availability (higher is better)
        # breaches when current < target. Latency (lower is better) breaches
        # when current > target. The metric type determines the comparison.
        higher_is_better = sla.metric_type in (SLAMetricType.AVAILABILITY, SLAMetricType.THROUGHPUT)
        if higher_is_better:
            in_breach = current < sla.target_value
            in_warning = current < sla.warning_threshold
            margin = current - sla.target_value
        else:
            in_breach = current > sla.target_value
            in_warning = current > sla.warning_threshold
            margin = sla.target_value - current

        if in_breach and not self._in_breach:
            self._in_breach = True
            breach = SLABreach(
                sla_name=sla.name, metric_type=sla.metric_type,
                current_value=current, target_value=sla.target_value,
                severity=AlertSeverity.CRITICAL, breach_start=ts,
                message=f"{sla.name} breached: {current:.4f}{sla.unit} (target: {sla.target_value}{sla.unit})")
            self._breaches.append(breach)
            return breach
        if not in_breach:
            self._in_breach = False
        if in_warning and not in_breach:
            return SLABreach(
                sla_name=sla.name, metric_type=sla.metric_type,
                current_value=current, target_value=sla.target_value,
                severity=AlertSeverity.WARNING, breach_start=ts,
                message=f"{sla.name} approaching breach: {current:.4f}{sla.unit}")
        return None

    def status(self) -> SLAStatus:
        current = self.current_value()
        higher_is_better = self._sla.metric_type in (SLAMetricType.AVAILABILITY, SLAMetricType.THROUGHPUT)
        margin = (current - self._sla.target_value) if higher_is_better else (self._sla.target_value - current)
        error_budget = abs(self._sla.warning_threshold - self._sla.target_value)
        burn_rate = max(0, -margin) / error_budget if error_budget > 0 else 0.0
        return SLAStatus(sla_name=self._sla.name, current_value=current,
                         target_value=self._sla.target_value, margin=margin,
                         in_breach=self._in_breach, burn_rate=burn_rate)

    def _prune_window(self, now: float) -> None:
        cutoff = now - (self._sla.window_minutes * 60)
        while self._data and self._data[0].timestamp < cutoff:
            self._data.popleft()

class SLABreachDetector:
    def __init__(self) -> None:
        self._trackers: dict[str, SLATracker] = {}

    def add_sla(self, sla: SLADefinition) -> None:
        self._trackers[sla.name] = SLATracker(sla)

    def record(self, sla_name: str, value: float, timestamp: float | None = None) -> None:
        if sla_name not in self._trackers:
            raise KeyError(f"Unknown SLA: {sla_name}")
        self._trackers[sla_name].record(value, timestamp)

    def check_all(self) -> list[SLABreach]:
        return [b for t in self._trackers.values() if (b := t.check()) is not None]

    def status_all(self) -> list[SLAStatus]:
        return [t.status() for t in self._trackers.values()]

    def all_breaches(self) -> list[SLABreach]:
        return [b for t in self._trackers.values() for b in t.breaches]

def run_demo() -> dict[str, Any]:
    detector = SLABreachDetector()
    detector.add_sla(SLADefinition(name="api-availability", metric_type=SLAMetricType.AVAILABILITY,
                                    target_value=99.9, warning_threshold=99.95, unit="%"))
    detector.add_sla(SLADefinition(name="api-latency-p99", metric_type=SLAMetricType.LATENCY,
                                    target_value=500, warning_threshold=400, unit="ms"))
    rng = random.Random(42)
    base_time = time.time()
    alerts: list[dict[str, Any]] = []
    for i in range(60):
        ts = base_time + i * 60
        detector.record("api-availability", rng.gauss(99.95, 0.05), ts)
        detector.record("api-latency-p99", rng.gauss(350, 80), ts)
        for b in detector.check_all():
            alerts.append(b.to_dict())
    return {"sla_status": [s.to_dict() for s in detector.status_all()],
            "total_breaches": len(detector.all_breaches()), "alerts": alerts[:10]}

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="SLA breach detector")
    parser.add_argument("--demo", action="store_true", default=True)
    parser.parse_args(argv)
    print(json.dumps(run_demo(), indent=2))

if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Hysteresis for breach detection | Only alert on transition into breach, preventing alert storms | Alert on every check -- floods incident channels during sustained outages |
| Direction-aware comparison | Availability (higher=better) and latency (lower=better) need opposite comparisons | Assume all metrics are same direction -- incorrect for mixed metric types |
| Burn rate calculation | Shows how fast error budget is being consumed; enables proactive response | Boolean breach only -- loses the velocity information that predicts future breaches |
| Time-windowed sliding data | Prunes old data points; SLA is measured over a rolling window, not all time | Cumulative -- never forgets old data, making recovery from past incidents impossible |

## Alternative approaches

### Approach B: Error budget-based SLO monitoring (Google SRE style)

```python
class ErrorBudgetMonitor:
    """Track remaining error budget instead of point-in-time SLA value.
    Google SRE approach: if budget is exhausted, freeze deployments."""
    def __init__(self, slo_target: float, window_days: int = 30):
        self.slo_target = slo_target  # e.g., 99.9%
        self.window_days = window_days
        self.total_budget = (1 - slo_target / 100) * window_days * 24 * 60  # minutes of downtime

    def remaining_budget_minutes(self, downtime_minutes: float) -> float:
        return self.total_budget - downtime_minutes
```

**Trade-off:** Error budget monitoring shifts focus from "are we in breach right now?" to "how much budget remains this month?" It enables proactive decisions (slow down releases when budget is low) but requires a longer time horizon and more sophisticated tracking than point-in-time breach detection.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| No data points recorded yet | `current_value()` returns the target value (assumes healthy) | This is intentional; alternative is to return "unknown" status |
| Warning threshold on wrong side of target | For latency: `warning_threshold=400` must be LESS than `target_value=500` | Validate threshold ordering matches metric direction at construction |
| SLA name not registered | `record()` raises KeyError -- fails fast rather than silently dropping data | This is correct behaviour; catch KeyError at the caller if needed |
