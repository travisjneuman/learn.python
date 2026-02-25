"""SLA Breach Detector — monitor SLA metrics and detect breaches with alerting.

Design rationale:
    Service Level Agreements define contractual performance guarantees.
    Detecting breaches early prevents penalties and customer churn.
    This project builds an SLA monitoring engine that tracks metrics
    against SLA targets, detects breaches in real-time, and generates
    alerts — the pattern behind every uptime monitoring tool.

Concepts practised:
    - dataclasses for SLA definitions and breach records
    - time-window aggregation for SLA calculations
    - threshold detection with hysteresis
    - alert severity escalation
    - reporting with burn-rate analysis
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


@dataclass
class SLADefinition:
    """Defines an SLA target for a specific metric."""
    name: str
    metric_type: SLAMetricType
    target_value: float       # e.g., 99.9 for availability
    warning_threshold: float  # e.g., 99.95 — warn before breach
    window_minutes: int = 60  # measurement window
    unit: str = "%"


@dataclass
class MetricDataPoint:
    """A single metric measurement."""
    timestamp: float
    value: float
    source: str = ""


@dataclass
class SLABreach:
    """Record of an SLA breach event."""
    sla_name: str
    metric_type: SLAMetricType
    current_value: float
    target_value: float
    severity: AlertSeverity
    breach_start: float
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "sla": self.sla_name,
            "metric": self.metric_type.value,
            "current": round(self.current_value, 4),
            "target": self.target_value,
            "severity": self.severity.value,
            "message": self.message,
        }


@dataclass
class SLAStatus:
    """Current status of a single SLA."""
    sla_name: str
    current_value: float
    target_value: float
    margin: float  # how far from breach (positive = healthy)
    in_breach: bool
    burn_rate: float  # rate at which error budget is consumed

    def to_dict(self) -> dict[str, Any]:
        return {
            "sla": self.sla_name,
            "current": round(self.current_value, 4),
            "target": self.target_value,
            "margin": round(self.margin, 4),
            "in_breach": self.in_breach,
            "burn_rate": round(self.burn_rate, 2),
        }


# --- SLA Tracker --------------------------------------------------------

class SLATracker:
    """Tracks metrics for a single SLA definition.

    Maintains a sliding window of data points and computes the
    current SLA value. Detects breaches when the value drops
    below the target.
    """

    def __init__(self, sla: SLADefinition) -> None:
        self._sla = sla
        self._data: deque[MetricDataPoint] = deque()
        self._breaches: list[SLABreach] = []
        self._in_breach = False

    @property
    def sla(self) -> SLADefinition:
        return self._sla

    @property
    def breaches(self) -> list[SLABreach]:
        return list(self._breaches)

    def record(self, value: float, timestamp: float | None = None) -> None:
        """Record a new metric data point."""
        ts = timestamp or time.time()
        self._data.append(MetricDataPoint(timestamp=ts, value=value))
        self._prune_window(ts)

    def current_value(self) -> float:
        """Compute the current SLA value from the measurement window."""
        if not self._data:
            return self._sla.target_value  # assume healthy when no data
        values = [dp.value for dp in self._data]
        # For availability/error_rate: use mean
        return sum(values) / len(values)

    def check(self, timestamp: float | None = None) -> SLABreach | None:
        """Check current value against SLA and return breach if detected."""
        ts = timestamp or time.time()
        current = self.current_value()
        sla = self._sla

        # Determine if metric is "lower is better" or "higher is better"
        higher_is_better = sla.metric_type in (
            SLAMetricType.AVAILABILITY, SLAMetricType.THROUGHPUT,
        )

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
            severity = AlertSeverity.CRITICAL
            breach = SLABreach(
                sla_name=sla.name,
                metric_type=sla.metric_type,
                current_value=current,
                target_value=sla.target_value,
                severity=severity,
                breach_start=ts,
                message=f"{sla.name} breached: {current:.4f}{sla.unit} "
                        f"(target: {sla.target_value}{sla.unit})",
            )
            self._breaches.append(breach)
            return breach

        if not in_breach:
            self._in_breach = False

        if in_warning and not in_breach:
            return SLABreach(
                sla_name=sla.name,
                metric_type=sla.metric_type,
                current_value=current,
                target_value=sla.target_value,
                severity=AlertSeverity.WARNING,
                breach_start=ts,
                message=f"{sla.name} approaching breach: {current:.4f}{sla.unit}",
            )

        return None

    def status(self) -> SLAStatus:
        """Get current SLA status."""
        current = self.current_value()
        higher_is_better = self._sla.metric_type in (
            SLAMetricType.AVAILABILITY, SLAMetricType.THROUGHPUT,
        )
        if higher_is_better:
            margin = current - self._sla.target_value
        else:
            margin = self._sla.target_value - current

        # Burn rate: how fast we're consuming error budget (1.0 = normal burn)
        error_budget = abs(self._sla.warning_threshold - self._sla.target_value)
        if error_budget > 0:
            burn_rate = max(0, -margin) / error_budget
        else:
            burn_rate = 0.0

        return SLAStatus(
            sla_name=self._sla.name,
            current_value=current,
            target_value=self._sla.target_value,
            margin=margin,
            in_breach=self._in_breach,
            burn_rate=burn_rate,
        )

    def _prune_window(self, now: float) -> None:
        """Remove data points outside the measurement window."""
        cutoff = now - (self._sla.window_minutes * 60)
        while self._data and self._data[0].timestamp < cutoff:
            self._data.popleft()


# --- Multi-SLA monitor --------------------------------------------------

class SLABreachDetector:
    """Monitors multiple SLAs and aggregates breach detection."""

    def __init__(self) -> None:
        self._trackers: dict[str, SLATracker] = {}

    def add_sla(self, sla: SLADefinition) -> None:
        self._trackers[sla.name] = SLATracker(sla)

    def record(self, sla_name: str, value: float, timestamp: float | None = None) -> None:
        if sla_name not in self._trackers:
            raise KeyError(f"Unknown SLA: {sla_name}")
        self._trackers[sla_name].record(value, timestamp)

    def check_all(self) -> list[SLABreach]:
        """Check all SLAs and return any breaches."""
        breaches: list[SLABreach] = []
        for tracker in self._trackers.values():
            breach = tracker.check()
            if breach:
                breaches.append(breach)
        return breaches

    def status_all(self) -> list[SLAStatus]:
        return [t.status() for t in self._trackers.values()]

    def all_breaches(self) -> list[SLABreach]:
        breaches: list[SLABreach] = []
        for t in self._trackers.values():
            breaches.extend(t.breaches)
        return breaches


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    """Simulate SLA monitoring with breach detection."""
    detector = SLABreachDetector()

    detector.add_sla(SLADefinition(
        name="api-availability", metric_type=SLAMetricType.AVAILABILITY,
        target_value=99.9, warning_threshold=99.95, unit="%",
    ))
    detector.add_sla(SLADefinition(
        name="api-latency-p99", metric_type=SLAMetricType.LATENCY,
        target_value=500, warning_threshold=400, unit="ms",
    ))

    import random
    rng = random.Random(42)
    base_time = time.time()

    alerts: list[dict[str, Any]] = []
    for i in range(60):
        ts = base_time + i * 60  # 1 minute intervals
        avail = rng.gauss(99.95, 0.05)
        latency = rng.gauss(350, 80)

        detector.record("api-availability", avail, ts)
        detector.record("api-latency-p99", latency, ts)

        breaches = detector.check_all()
        for b in breaches:
            alerts.append(b.to_dict())

    return {
        "sla_status": [s.to_dict() for s in detector.status_all()],
        "total_breaches": len(detector.all_breaches()),
        "alerts": alerts[:10],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SLA breach detector")
    parser.add_argument("--demo", action="store_true", default=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    print(json.dumps(run_demo(), indent=2))


if __name__ == "__main__":
    main()
