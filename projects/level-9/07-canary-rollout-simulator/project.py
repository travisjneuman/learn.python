"""Canary Rollout Simulator — simulate canary deployments with rollback triggers.

Design rationale:
    Canary deployments route a small percentage of traffic to new code,
    comparing its error rate and latency against the stable version.
    This project simulates the rollout process with configurable stages,
    automatic promotion/rollback, and metric comparison.

Concepts practised:
    - state machine for deployment stages
    - statistical comparison (canary vs baseline)
    - configurable rollout strategy
    - automatic rollback triggers
    - dataclasses for deployment state
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# --- Domain types -------------------------------------------------------

class RolloutPhase(Enum):
    NOT_STARTED = "not_started"
    CANARY = "canary"
    PROGRESSIVE = "progressive"
    FULL = "full"
    ROLLED_BACK = "rolled_back"
    COMPLETED = "completed"


@dataclass
class RolloutStage:
    """A single stage in the canary rollout."""
    name: str
    traffic_pct: float  # % of traffic going to canary
    duration_steps: int  # number of evaluation steps
    error_threshold: float  # max allowed error rate difference vs baseline


@dataclass
class MetricSnapshot:
    """Metrics captured during a rollout stage."""
    stage_name: str
    canary_error_rate: float
    baseline_error_rate: float
    canary_latency_ms: float
    baseline_latency_ms: float
    traffic_pct: float

    @property
    def error_rate_delta(self) -> float:
        return self.canary_error_rate - self.baseline_error_rate

    @property
    def latency_delta_ms(self) -> float:
        return self.canary_latency_ms - self.baseline_latency_ms

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage_name,
            "canary_err": round(self.canary_error_rate, 4),
            "baseline_err": round(self.baseline_error_rate, 4),
            "error_delta": round(self.error_rate_delta, 4),
            "canary_lat_ms": round(self.canary_latency_ms, 1),
            "baseline_lat_ms": round(self.baseline_latency_ms, 1),
            "traffic_pct": self.traffic_pct,
        }


@dataclass
class RolloutResult:
    """Final result of a canary rollout."""
    phase: RolloutPhase
    stages_completed: int
    total_stages: int
    rollback_reason: str = ""
    snapshots: list[MetricSnapshot] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "phase": self.phase.value,
            "stages_completed": self.stages_completed,
            "total_stages": self.total_stages,
            "rollback_reason": self.rollback_reason,
            "snapshots": [s.to_dict() for s in self.snapshots],
        }


# --- Canary rollout engine ----------------------------------------------

class CanaryRollout:
    """Simulates a canary deployment with automatic promotion/rollback.

    The rollout progresses through configured stages. At each stage,
    canary metrics are compared against baseline. If the canary
    degrades beyond the threshold, an automatic rollback is triggered.
    """

    def __init__(
        self,
        stages: list[RolloutStage],
        latency_threshold_ms: float = 50.0,
    ) -> None:
        self._stages = stages
        self._latency_threshold = latency_threshold_ms
        self._phase = RolloutPhase.NOT_STARTED
        self._snapshots: list[MetricSnapshot] = []
        self._stages_completed = 0

    @property
    def phase(self) -> RolloutPhase:
        return self._phase

    def execute(
        self,
        baseline_error_rate: float,
        baseline_latency_ms: float,
        canary_error_fn: Any = None,
        canary_latency_fn: Any = None,
        rng: random.Random | None = None,
    ) -> RolloutResult:
        """Execute the full rollout simulation."""
        if rng is None:
            rng = random.Random()

        self._phase = RolloutPhase.CANARY

        for i, stage in enumerate(self._stages):
            # Simulate canary metrics for this stage
            if canary_error_fn:
                canary_err = canary_error_fn(stage, rng)
            else:
                canary_err = baseline_error_rate + rng.gauss(0, 0.005)

            if canary_latency_fn:
                canary_lat = canary_latency_fn(stage, rng)
            else:
                canary_lat = baseline_latency_ms + rng.gauss(0, 10)

            snapshot = MetricSnapshot(
                stage_name=stage.name,
                canary_error_rate=max(0, canary_err),
                baseline_error_rate=baseline_error_rate,
                canary_latency_ms=max(0, canary_lat),
                baseline_latency_ms=baseline_latency_ms,
                traffic_pct=stage.traffic_pct,
            )
            self._snapshots.append(snapshot)

            # Check rollback conditions
            if snapshot.error_rate_delta > stage.error_threshold:
                self._phase = RolloutPhase.ROLLED_BACK
                return RolloutResult(
                    phase=self._phase,
                    stages_completed=i,
                    total_stages=len(self._stages),
                    rollback_reason=f"Error rate delta {snapshot.error_rate_delta:.4f} "
                                    f"exceeds threshold {stage.error_threshold}",
                    snapshots=self._snapshots,
                )

            if snapshot.latency_delta_ms > self._latency_threshold:
                self._phase = RolloutPhase.ROLLED_BACK
                return RolloutResult(
                    phase=self._phase,
                    stages_completed=i,
                    total_stages=len(self._stages),
                    rollback_reason=f"Latency delta {snapshot.latency_delta_ms:.1f}ms "
                                    f"exceeds threshold {self._latency_threshold}ms",
                    snapshots=self._snapshots,
                )

            self._stages_completed = i + 1
            if stage.traffic_pct >= 50:
                self._phase = RolloutPhase.PROGRESSIVE

        self._phase = RolloutPhase.COMPLETED
        return RolloutResult(
            phase=self._phase,
            stages_completed=len(self._stages),
            total_stages=len(self._stages),
            snapshots=self._snapshots,
        )


# --- Default rollout strategy -------------------------------------------

def default_stages() -> list[RolloutStage]:
    """Standard canary rollout stages: 1% -> 5% -> 25% -> 50% -> 100%."""
    return [
        RolloutStage("canary-1pct", 1, 5, 0.02),
        RolloutStage("canary-5pct", 5, 5, 0.015),
        RolloutStage("progressive-25pct", 25, 5, 0.01),
        RolloutStage("progressive-50pct", 50, 5, 0.01),
        RolloutStage("full-100pct", 100, 3, 0.005),
    ]


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    stages = default_stages()
    rollout = CanaryRollout(stages, latency_threshold_ms=50)
    result = rollout.execute(
        baseline_error_rate=0.01,
        baseline_latency_ms=100,
        rng=random.Random(42),
    )
    return result.to_dict()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Canary rollout simulator")
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    print(json.dumps(run_demo(), indent=2))


if __name__ == "__main__":
    main()
