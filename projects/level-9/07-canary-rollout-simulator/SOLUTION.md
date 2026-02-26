# Solution: Level 9 / Project 07 - Canary Rollout Simulator

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
"""Canary Rollout Simulator — simulate canary deployments with rollback triggers."""

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


# WHY multi-stage rollouts instead of instant deploys? -- Each stage
# increases traffic gradually (e.g. 1% -> 5% -> 25% -> 100%). If the canary
# shows elevated errors at any stage, you roll back before most users are
# affected. The error_threshold is relative to baseline — accounting for
# the fact that some background error rate is normal.
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

    # WHY compare canary against baseline rather than absolute thresholds? --
    # A 2% error rate might be normal for this service. An absolute threshold
    # of 1% would always fail. Comparing deltas (canary minus baseline) isolates
    # the effect of the new code from background noise.
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

# WHY tightening thresholds at higher traffic? -- At 1% traffic, a slightly
# elevated error rate affects few users, so a wider threshold (0.02) is safe.
# At 100% traffic, even a small delta affects everyone, so the threshold
# tightens to 0.005. This is how production canary systems (Spinnaker, Argo)
# work.
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Delta-based comparison (canary vs baseline) | Isolates the effect of the new code from background noise; a service with 2% baseline error rate does not false-alarm | Absolute thresholds -- break when baseline error rates vary between services |
| Tightening thresholds at higher traffic percentages | At 1% traffic, a small regression affects few users; at 100%, the same regression affects everyone | Uniform threshold -- either too sensitive at low traffic (premature rollback) or too lenient at high traffic (late rollback) |
| Configurable canary metric functions | Allows injecting custom error and latency behaviors for testing specific scenarios (memory leak, gradual degradation) | Hardcoded noise model -- cannot simulate realistic failure modes |
| Seeded RNG for reproducibility | Same seed produces same rollout result, making tests deterministic and demos reproducible | System random -- non-deterministic; demos show different results each run |
| State machine for rollout phases | Clear progression through NOT_STARTED -> CANARY -> PROGRESSIVE -> COMPLETED (or ROLLED_BACK); prevents invalid state transitions | Boolean flags (is_rolled_back, is_complete) -- harder to reason about and prone to contradictory states |

## Alternative approaches

### Approach B: Statistical significance testing for canary analysis

```python
import math

class StatisticalCanaryAnalyzer:
    """Use chi-squared test to determine if the canary error rate
    is statistically significantly different from baseline, not just
    numerically different."""
    def is_significantly_worse(
        self, baseline_errors: int, baseline_total: int,
        canary_errors: int, canary_total: int,
        confidence: float = 0.95,
    ) -> bool:
        if baseline_total == 0 or canary_total == 0:
            return False
        p_baseline = baseline_errors / baseline_total
        p_canary = canary_errors / canary_total
        p_pooled = (baseline_errors + canary_errors) / (baseline_total + canary_total)
        se = math.sqrt(p_pooled * (1 - p_pooled) * (1/baseline_total + 1/canary_total))
        if se == 0:
            return False
        z = (p_canary - p_baseline) / se
        z_threshold = 1.645 if confidence == 0.95 else 2.326  # one-tailed
        return z > z_threshold
```

**Trade-off:** Statistical testing avoids reacting to random noise. A canary with 3 errors out of 100 requests is not statistically different from a baseline with 1 error out of 100 -- the delta could be random. Statistical tests require more data points (longer bake time per stage) but produce fewer false rollbacks. Use threshold-based comparison for learning; statistical testing for production canary systems handling millions of requests.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Negative canary error rate from `rng.gauss()` | Error rate becomes -0.003, which is not meaningful | Clamp with `max(0, canary_err)` before storing in MetricSnapshot |
| Empty stages list | `execute` returns COMPLETED immediately without any evaluation | Validate that stages list is non-empty, or return NOT_STARTED |
| Rollout re-execution after completion | `_phase` and `_snapshots` still hold state from previous run | Either reset state at the start of `execute` or make CanaryRollout single-use |
