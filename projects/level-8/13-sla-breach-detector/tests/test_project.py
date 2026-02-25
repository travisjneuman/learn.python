"""Tests for SLA Breach Detector.

Covers: SLA tracking, breach detection, multi-SLA monitoring, and status reporting.
"""

from __future__ import annotations

import time

import pytest

from project import (
    AlertSeverity,
    SLABreach,
    SLABreachDetector,
    SLADefinition,
    SLAMetricType,
    SLATracker,
)


# --- Fixtures -----------------------------------------------------------

@pytest.fixture
def availability_sla() -> SLADefinition:
    return SLADefinition(
        name="uptime", metric_type=SLAMetricType.AVAILABILITY,
        target_value=99.9, warning_threshold=99.95, unit="%",
    )


@pytest.fixture
def latency_sla() -> SLADefinition:
    return SLADefinition(
        name="p99-latency", metric_type=SLAMetricType.LATENCY,
        target_value=500, warning_threshold=400, unit="ms",
    )


# --- SLATracker ---------------------------------------------------------

class TestSLATracker:
    def test_healthy_no_breach(self, availability_sla: SLADefinition) -> None:
        tracker = SLATracker(availability_sla)
        ts = time.time()
        for i in range(10):
            tracker.record(99.99, ts + i)
        breach = tracker.check(ts + 10)
        assert breach is None

    def test_breach_detected(self, availability_sla: SLADefinition) -> None:
        tracker = SLATracker(availability_sla)
        ts = time.time()
        for i in range(10):
            tracker.record(99.5, ts + i)  # below 99.9 target
        breach = tracker.check(ts + 10)
        assert breach is not None
        assert breach.severity == AlertSeverity.CRITICAL

    def test_warning_before_breach(self, availability_sla: SLADefinition) -> None:
        tracker = SLATracker(availability_sla)
        ts = time.time()
        for i in range(10):
            tracker.record(99.92, ts + i)  # between warning and target
        breach = tracker.check(ts + 10)
        assert breach is not None
        assert breach.severity == AlertSeverity.WARNING

    def test_latency_breach_higher_is_worse(self, latency_sla: SLADefinition) -> None:
        tracker = SLATracker(latency_sla)
        ts = time.time()
        for i in range(10):
            tracker.record(600, ts + i)  # above 500ms target
        breach = tracker.check(ts + 10)
        assert breach is not None


# --- Status reporting ---------------------------------------------------

class TestSLAStatus:
    @pytest.mark.parametrize("values,expected_breach", [
        ([99.99, 99.98, 99.97], False),
        ([99.5, 99.4, 99.3], True),
    ])
    def test_status_breach_flag(
        self, availability_sla: SLADefinition,
        values: list[float], expected_breach: bool,
    ) -> None:
        tracker = SLATracker(availability_sla)
        ts = time.time()
        for i, v in enumerate(values):
            tracker.record(v, ts + i)
        tracker.check(ts + len(values))
        status = tracker.status()
        assert status.in_breach == expected_breach


# --- Multi-SLA detector -------------------------------------------------

class TestSLABreachDetector:
    def test_add_and_record(self) -> None:
        detector = SLABreachDetector()
        sla = SLADefinition(
            name="test", metric_type=SLAMetricType.AVAILABILITY,
            target_value=99.9, warning_threshold=99.95,
        )
        detector.add_sla(sla)
        detector.record("test", 99.99)
        statuses = detector.status_all()
        assert len(statuses) == 1

    def test_unknown_sla_raises(self) -> None:
        detector = SLABreachDetector()
        with pytest.raises(KeyError, match="Unknown SLA"):
            detector.record("nonexistent", 50.0)

    def test_check_all_returns_breaches(self) -> None:
        detector = SLABreachDetector()
        detector.add_sla(SLADefinition(
            name="bad", metric_type=SLAMetricType.AVAILABILITY,
            target_value=99.9, warning_threshold=99.95,
        ))
        ts = time.time()
        for i in range(5):
            detector.record("bad", 90.0, ts + i)
        breaches = detector.check_all()
        assert len(breaches) > 0
