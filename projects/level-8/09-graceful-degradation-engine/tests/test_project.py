"""Tests for Graceful Degradation Engine.

Covers: sliding window, tier transitions, circuit breaker states, and features.
"""

from __future__ import annotations

import pytest

from project import (
    CircuitState,
    DegradationConfig,
    GracefulDegradationEngine,
    ServiceTier,
    SlidingWindowTracker,
    TIER_FEATURES,
)


# --- Fixtures -----------------------------------------------------------

@pytest.fixture
def engine() -> GracefulDegradationEngine:
    return GracefulDegradationEngine(DegradationConfig(window_size=10))


# --- SlidingWindowTracker -----------------------------------------------

class TestSlidingWindow:
    def test_error_rate_empty(self) -> None:
        tracker = SlidingWindowTracker(window_size=10)
        assert tracker.error_rate == 0.0

    def test_error_rate_calculation(self) -> None:
        tracker = SlidingWindowTracker(window_size=10)
        for _ in range(7):
            tracker.record_success()
        for _ in range(3):
            tracker.record_failure()
        assert tracker.error_rate == pytest.approx(0.3)

    def test_window_slides(self) -> None:
        tracker = SlidingWindowTracker(window_size=5)
        # Fill with failures
        for _ in range(5):
            tracker.record_failure()
        assert tracker.error_rate == 1.0
        # Push successes through — old failures slide out
        for _ in range(5):
            tracker.record_success()
        assert tracker.error_rate == 0.0


# --- Service tier transitions -------------------------------------------

class TestTierTransitions:
    @pytest.mark.parametrize("failures,expected_tier", [
        (0, ServiceTier.FULL),
        (1, ServiceTier.REDUCED),     # 10% of 10
        (3, ServiceTier.MINIMAL),     # 30% of 10
        (5, ServiceTier.OFFLINE),     # 50% of 10
    ])
    def test_tier_based_on_error_rate(
        self, failures: int, expected_tier: ServiceTier,
    ) -> None:
        engine = GracefulDegradationEngine(DegradationConfig(window_size=10))
        successes = 10 - failures
        for _ in range(successes):
            engine.record_success()
        for _ in range(failures):
            engine.record_failure()
        assert engine.service_tier == expected_tier


# --- Circuit breaker states ---------------------------------------------

class TestCircuitBreaker:
    def test_starts_closed(self, engine: GracefulDegradationEngine) -> None:
        assert engine.circuit_state == CircuitState.CLOSED

    def test_opens_on_high_errors(self, engine: GracefulDegradationEngine) -> None:
        for _ in range(5):
            engine.record_success()
        for _ in range(5):
            engine.record_failure()
        assert engine.circuit_state == CircuitState.OPEN

    def test_open_circuit_blocks_requests(self) -> None:
        engine = GracefulDegradationEngine(
            DegradationConfig(window_size=10, recovery_wait_seconds=999)
        )
        # Force open
        for _ in range(10):
            engine.record_failure()
        assert engine.should_allow_request() is False

    def test_force_recovery(self, engine: GracefulDegradationEngine) -> None:
        for _ in range(10):
            engine.record_failure()
        assert engine.circuit_state == CircuitState.OPEN
        engine.force_recovery()
        assert engine.circuit_state == CircuitState.CLOSED
        assert engine.service_tier == ServiceTier.FULL


# --- Feature flags ------------------------------------------------------

class TestFeatures:
    def test_full_tier_has_all_features(self) -> None:
        engine = GracefulDegradationEngine()
        assert len(engine.features) == len(TIER_FEATURES[ServiceTier.FULL])

    def test_offline_tier_has_no_features(self) -> None:
        assert len(TIER_FEATURES[ServiceTier.OFFLINE]) == 0

    def test_reduced_tier_subset_of_full(self) -> None:
        full = set(TIER_FEATURES[ServiceTier.FULL])
        reduced = set(TIER_FEATURES[ServiceTier.REDUCED])
        assert reduced.issubset(full)


# --- Status reporting ---------------------------------------------------

class TestStatus:
    def test_status_dict_has_required_fields(self, engine: GracefulDegradationEngine) -> None:
        status = engine.status().to_dict()
        assert "circuit_state" in status
        assert "service_tier" in status
        assert "error_rate" in status
        assert "features_enabled" in status
