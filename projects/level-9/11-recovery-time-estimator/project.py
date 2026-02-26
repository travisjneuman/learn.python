"""Recovery Time Estimator — model and predict service recovery times.

Design rationale:
    When systems fail, stakeholders need realistic recovery time estimates.
    This project models recovery processes as phases (detect, diagnose,
    fix, verify, deploy) and estimates total recovery time based on
    historical data, team capacity, and incident complexity.

Concepts practised:
    - Monte Carlo simulation for time estimation
    - dataclasses with computed properties
    - statistical modeling (percentiles, confidence intervals)
    - strategy pattern for estimation methods
    - enum-based complexity classification
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


# --- Domain types -------------------------------------------------------

class Severity(Enum):
    SEV1 = "sev1"  # Critical outage
    SEV2 = "sev2"  # Major degradation
    SEV3 = "sev3"  # Minor impact
    SEV4 = "sev4"  # Cosmetic / low priority


class RecoveryPhase(Enum):
    DETECTION = "detection"
    DIAGNOSIS = "diagnosis"
    FIX = "fix"
    VERIFICATION = "verification"
    DEPLOYMENT = "deployment"


# WHY three-point estimates (min, expected, max)? -- Recovery times are
# uncertain. Three-point estimates feed Monte Carlo simulation: randomly
# sampling between min and max across all phases produces a probability
# distribution of total recovery time. This gives stakeholders confidence
# intervals ("90% chance of recovery within 45 min") instead of false
# precision from a single number.
@dataclass(frozen=True)
class PhaseEstimate:
    """Time estimate for a single recovery phase."""
    phase: RecoveryPhase
    min_minutes: float
    expected_minutes: float
    max_minutes: float

    @property
    def range_width(self) -> float:
        return self.max_minutes - self.min_minutes


@dataclass
class IncidentProfile:
    """Describes an incident for recovery estimation."""
    incident_id: str
    severity: Severity
    affected_services: list[str] = field(default_factory=list)
    has_runbook: bool = False
    team_size: int = 1
    is_novel: bool = False  # Never seen this type before?


@dataclass
class RecoveryEstimate:
    """Complete recovery time estimate with confidence intervals."""
    incident_id: str
    phase_estimates: list[PhaseEstimate] = field(default_factory=list)
    simulated_totals: list[float] = field(default_factory=list)

    @property
    def total_expected(self) -> float:
        return sum(p.expected_minutes for p in self.phase_estimates)

    @property
    def p50(self) -> float:
        return _percentile(self.simulated_totals, 50)

    @property
    def p90(self) -> float:
        return _percentile(self.simulated_totals, 90)

    @property
    def p99(self) -> float:
        return _percentile(self.simulated_totals, 99)

    def to_dict(self) -> dict[str, Any]:
        return {
            "incident_id": self.incident_id,
            "total_expected_minutes": round(self.total_expected, 1),
            "p50_minutes": round(self.p50, 1),
            "p90_minutes": round(self.p90, 1),
            "p99_minutes": round(self.p99, 1),
            "phases": [
                {
                    "phase": p.phase.value,
                    "min": p.min_minutes,
                    "expected": p.expected_minutes,
                    "max": p.max_minutes,
                }
                for p in self.phase_estimates
            ],
        }


# --- Helpers ------------------------------------------------------------

def _percentile(data: list[float], pct: float) -> float:
    """Calculate percentile from a sorted list."""
    if not data:
        return 0.0
    sorted_data = sorted(data)
    k = (len(sorted_data) - 1) * (pct / 100)
    f = int(k)
    c = f + 1
    if c >= len(sorted_data):
        return sorted_data[-1]
    return sorted_data[f] + (k - f) * (sorted_data[c] - sorted_data[f])


def _triangular_sample(low: float, mode: float, high: float, rng: random.Random) -> float:
    """Sample from triangular distribution — models 3-point estimates."""
    return rng.triangular(low, high, mode)


# --- Estimation engine --------------------------------------------------

# Severity multipliers — higher severity = faster response but harder fix
SEVERITY_MULTIPLIERS: dict[Severity, dict[RecoveryPhase, float]] = {
    Severity.SEV1: {
        RecoveryPhase.DETECTION: 0.5,   # Faster detection (alerts fire)
        RecoveryPhase.DIAGNOSIS: 1.2,   # Harder to diagnose under pressure
        RecoveryPhase.FIX: 1.0,
        RecoveryPhase.VERIFICATION: 1.3,  # More thorough verification needed
        RecoveryPhase.DEPLOYMENT: 0.8,    # Expedited deployment
    },
    Severity.SEV2: {p: 1.0 for p in RecoveryPhase},
    Severity.SEV3: {
        RecoveryPhase.DETECTION: 2.0,   # Slower detection
        RecoveryPhase.DIAGNOSIS: 0.8,
        RecoveryPhase.FIX: 0.8,
        RecoveryPhase.VERIFICATION: 0.7,
        RecoveryPhase.DEPLOYMENT: 1.2,  # Waits for normal deploy window
    },
    Severity.SEV4: {p: 1.5 for p in RecoveryPhase},
}

# Base estimates per phase (minutes): (min, expected, max)
BASE_ESTIMATES: dict[RecoveryPhase, tuple[float, float, float]] = {
    RecoveryPhase.DETECTION: (2, 10, 60),
    RecoveryPhase.DIAGNOSIS: (10, 30, 120),
    RecoveryPhase.FIX: (15, 45, 180),
    RecoveryPhase.VERIFICATION: (5, 15, 60),
    RecoveryPhase.DEPLOYMENT: (5, 20, 90),
}


# EstimationStrategy type: takes an IncidentProfile, returns phase estimates
EstimationStrategy = Callable[[IncidentProfile], list[PhaseEstimate]]


def default_estimation_strategy(profile: IncidentProfile) -> list[PhaseEstimate]:
    """Estimate recovery phases based on severity and incident attributes."""
    multipliers = SEVERITY_MULTIPLIERS[profile.severity]
    estimates: list[PhaseEstimate] = []

    for phase in RecoveryPhase:
        base_min, base_exp, base_max = BASE_ESTIMATES[phase]
        m = multipliers[phase]

        # Adjust for incident attributes
        if profile.has_runbook and phase in (RecoveryPhase.DIAGNOSIS, RecoveryPhase.FIX):
            m *= 0.6  # Runbooks cut diagnosis/fix time significantly

        if profile.is_novel and phase == RecoveryPhase.DIAGNOSIS:
            m *= 2.0  # Novel incidents take much longer to diagnose

        # More affected services = longer verification and deployment
        service_factor = 1 + 0.1 * max(0, len(profile.affected_services) - 1)
        if phase in (RecoveryPhase.VERIFICATION, RecoveryPhase.DEPLOYMENT):
            m *= service_factor

        # Larger teams can parallelize diagnosis
        if profile.team_size > 1 and phase == RecoveryPhase.DIAGNOSIS:
            m *= max(0.4, 1.0 / (profile.team_size ** 0.5))

        estimates.append(PhaseEstimate(
            phase=phase,
            min_minutes=round(base_min * m, 1),
            expected_minutes=round(base_exp * m, 1),
            max_minutes=round(base_max * m, 1),
        ))

    return estimates


class RecoveryTimeEstimator:
    """Estimates incident recovery time using phase-based modeling."""

    def __init__(
        self,
        strategy: EstimationStrategy = default_estimation_strategy,
        simulation_runs: int = 1000,
        seed: int | None = None,
    ) -> None:
        self._strategy = strategy
        self._simulation_runs = simulation_runs
        self._rng = random.Random(seed)

    def estimate(self, profile: IncidentProfile) -> RecoveryEstimate:
        """Generate a recovery estimate with Monte Carlo simulation."""
        phase_estimates = self._strategy(profile)
        simulated = self._simulate(phase_estimates)
        return RecoveryEstimate(
            incident_id=profile.incident_id,
            phase_estimates=phase_estimates,
            simulated_totals=simulated,
        )

    def _simulate(self, phases: list[PhaseEstimate]) -> list[float]:
        """Run Monte Carlo simulation sampling from triangular distributions."""
        totals: list[float] = []
        for _ in range(self._simulation_runs):
            total = sum(
                _triangular_sample(p.min_minutes, p.expected_minutes, p.max_minutes, self._rng)
                for p in phases
            )
            totals.append(total)
        return totals

    def compare_scenarios(
        self, base: IncidentProfile, improved: IncidentProfile,
    ) -> dict[str, Any]:
        """Compare two incident profiles to show improvement potential."""
        base_est = self.estimate(base)
        improved_est = self.estimate(improved)
        return {
            "base_p50": round(base_est.p50, 1),
            "improved_p50": round(improved_est.p50, 1),
            "improvement_pct": round(
                (1 - improved_est.p50 / base_est.p50) * 100, 1
            ) if base_est.p50 > 0 else 0,
            "base_p90": round(base_est.p90, 1),
            "improved_p90": round(improved_est.p90, 1),
        }


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    estimator = RecoveryTimeEstimator(seed=42, simulation_runs=500)

    sev1_no_runbook = IncidentProfile(
        "INC-001", Severity.SEV1, ["api", "db", "cache"],
        has_runbook=False, team_size=3, is_novel=True,
    )
    sev2_with_runbook = IncidentProfile(
        "INC-002", Severity.SEV2, ["api"],
        has_runbook=True, team_size=2,
    )

    est1 = estimator.estimate(sev1_no_runbook)
    est2 = estimator.estimate(sev2_with_runbook)
    comparison = estimator.compare_scenarios(sev1_no_runbook, sev2_with_runbook)

    return {
        "sev1_novel": est1.to_dict(),
        "sev2_runbook": est2.to_dict(),
        "comparison": comparison,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recovery time estimator")
    parser.add_argument("--demo", action="store_true", default=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    print(json.dumps(run_demo(), indent=2))


if __name__ == "__main__":
    main()
