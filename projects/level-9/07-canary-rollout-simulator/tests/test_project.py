"""Tests for Canary Rollout Simulator.

Covers: rollout stages, metric snapshots, rollback triggers, and successful completion.
"""

from __future__ import annotations

import random

import pytest

from project import (
    CanaryRollout,
    MetricSnapshot,
    RolloutPhase,
    RolloutStage,
    default_stages,
)


# --- MetricSnapshot -----------------------------------------------------

class TestMetricSnapshot:
    def test_error_rate_delta(self) -> None:
        snap = MetricSnapshot("s", 0.05, 0.02, 100, 100, 10)
        assert snap.error_rate_delta == pytest.approx(0.03)

    def test_latency_delta(self) -> None:
        snap = MetricSnapshot("s", 0.01, 0.01, 150, 100, 10)
        assert snap.latency_delta_ms == pytest.approx(50)


# --- Successful rollout -------------------------------------------------

class TestSuccessfulRollout:
    def test_completes_all_stages(self) -> None:
        stages = [
            RolloutStage("s1", 5, 3, 0.1),
            RolloutStage("s2", 50, 3, 0.1),
            RolloutStage("s3", 100, 3, 0.1),
        ]
        rollout = CanaryRollout(stages, latency_threshold_ms=100)
        result = rollout.execute(
            baseline_error_rate=0.01, baseline_latency_ms=50,
            rng=random.Random(42),
        )
        assert result.phase == RolloutPhase.COMPLETED
        assert result.stages_completed == 3

    def test_default_stages_structure(self) -> None:
        stages = default_stages()
        assert len(stages) == 5
        assert stages[0].traffic_pct < stages[-1].traffic_pct


# --- Rollback on error rate ---------------------------------------------

class TestRollbackOnErrors:
    def test_rollback_on_high_error_rate(self) -> None:
        stages = [RolloutStage("s1", 5, 3, 0.01)]
        rollout = CanaryRollout(stages)

        # Force canary to have much higher error rate
        def bad_errors(stage, rng):
            return 0.10  # 10% vs 1% baseline

        result = rollout.execute(
            baseline_error_rate=0.01, baseline_latency_ms=50,
            canary_error_fn=bad_errors, rng=random.Random(0),
        )
        assert result.phase == RolloutPhase.ROLLED_BACK
        assert "Error rate" in result.rollback_reason


# --- Rollback on latency ------------------------------------------------

class TestRollbackOnLatency:
    def test_rollback_on_high_latency(self) -> None:
        stages = [RolloutStage("s1", 5, 3, 1.0)]  # lenient error threshold
        rollout = CanaryRollout(stages, latency_threshold_ms=20)

        def slow_latency(stage, rng):
            return 200  # 200ms vs 50ms baseline

        result = rollout.execute(
            baseline_error_rate=0.01, baseline_latency_ms=50,
            canary_latency_fn=slow_latency, rng=random.Random(0),
        )
        assert result.phase == RolloutPhase.ROLLED_BACK
        assert "Latency" in result.rollback_reason


# --- Serialization ------------------------------------------------------

class TestSerialization:
    def test_result_to_dict(self) -> None:
        stages = [RolloutStage("s1", 5, 3, 0.1)]
        rollout = CanaryRollout(stages)
        result = rollout.execute(0.01, 50, rng=random.Random(0))
        d = result.to_dict()
        assert "phase" in d
        assert "snapshots" in d

    @pytest.mark.parametrize("seed", [0, 42, 123])
    def test_deterministic_with_seed(self, seed: int) -> None:
        stages = [RolloutStage("s1", 5, 3, 0.1)]
        r1 = CanaryRollout(stages).execute(0.01, 50, rng=random.Random(seed))
        r2 = CanaryRollout(stages).execute(0.01, 50, rng=random.Random(seed))
        assert r1.phase == r2.phase
