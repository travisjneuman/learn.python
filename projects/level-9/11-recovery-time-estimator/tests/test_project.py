"""Tests for Recovery Time Estimator.

Covers: phase estimation, severity multipliers, Monte Carlo simulation,
scenario comparison, and incident profile attributes.
"""

from __future__ import annotations

import pytest

from project import (
    IncidentProfile,
    PhaseEstimate,
    RecoveryPhase,
    RecoveryTimeEstimator,
    Severity,
    _percentile,
    default_estimation_strategy,
)


# --- Fixtures -----------------------------------------------------------

@pytest.fixture
def estimator() -> RecoveryTimeEstimator:
    return RecoveryTimeEstimator(seed=42, simulation_runs=200)


@pytest.fixture
def sev1_profile() -> IncidentProfile:
    return IncidentProfile(
        "INC-001", Severity.SEV1, ["api", "db"],
        has_runbook=False, team_size=2, is_novel=False,
    )


@pytest.fixture
def sev3_profile() -> IncidentProfile:
    return IncidentProfile(
        "INC-002", Severity.SEV3, ["ui"],
        has_runbook=True, team_size=1,
    )


# --- Percentile helper --------------------------------------------------

class TestPercentile:
    def test_p50_of_range(self) -> None:
        data = list(range(1, 101))
        assert _percentile(data, 50) == pytest.approx(50.5, abs=0.5)

    def test_p0_and_p100(self) -> None:
        data = [10.0, 20.0, 30.0]
        assert _percentile(data, 0) == 10.0
        assert _percentile(data, 100) == 30.0

    def test_empty_returns_zero(self) -> None:
        assert _percentile([], 50) == 0.0


# --- Phase estimation ---------------------------------------------------

class TestPhaseEstimation:
    def test_all_phases_present(self, sev1_profile: IncidentProfile) -> None:
        phases = default_estimation_strategy(sev1_profile)
        phase_names = {p.phase for p in phases}
        assert phase_names == set(RecoveryPhase)

    def test_min_less_than_expected_less_than_max(self, sev1_profile: IncidentProfile) -> None:
        phases = default_estimation_strategy(sev1_profile)
        for p in phases:
            assert p.min_minutes <= p.expected_minutes <= p.max_minutes

    def test_runbook_reduces_diagnosis_time(self) -> None:
        without = IncidentProfile("a", Severity.SEV2, [], has_runbook=False)
        with_rb = IncidentProfile("b", Severity.SEV2, [], has_runbook=True)
        phases_without = {p.phase: p for p in default_estimation_strategy(without)}
        phases_with = {p.phase: p for p in default_estimation_strategy(with_rb)}
        assert phases_with[RecoveryPhase.DIAGNOSIS].expected_minutes < \
               phases_without[RecoveryPhase.DIAGNOSIS].expected_minutes

    def test_novel_incident_increases_diagnosis(self) -> None:
        normal = IncidentProfile("a", Severity.SEV2, [], is_novel=False)
        novel = IncidentProfile("b", Severity.SEV2, [], is_novel=True)
        phases_normal = {p.phase: p for p in default_estimation_strategy(normal)}
        phases_novel = {p.phase: p for p in default_estimation_strategy(novel)}
        assert phases_novel[RecoveryPhase.DIAGNOSIS].expected_minutes > \
               phases_normal[RecoveryPhase.DIAGNOSIS].expected_minutes

    @pytest.mark.parametrize("team_size,expected_faster", [
        (1, False),
        (4, True),
    ])
    def test_team_size_affects_diagnosis(self, team_size: int, expected_faster: bool) -> None:
        single = IncidentProfile("a", Severity.SEV2, [], team_size=1)
        multi = IncidentProfile("b", Severity.SEV2, [], team_size=team_size)
        single_diag = next(
            p for p in default_estimation_strategy(single)
            if p.phase == RecoveryPhase.DIAGNOSIS
        )
        multi_diag = next(
            p for p in default_estimation_strategy(multi)
            if p.phase == RecoveryPhase.DIAGNOSIS
        )
        if expected_faster:
            assert multi_diag.expected_minutes < single_diag.expected_minutes
        else:
            assert multi_diag.expected_minutes == single_diag.expected_minutes


# --- Monte Carlo simulation --------------------------------------------

class TestSimulation:
    def test_simulation_produces_expected_count(self, estimator: RecoveryTimeEstimator,
                                                  sev1_profile: IncidentProfile) -> None:
        result = estimator.estimate(sev1_profile)
        assert len(result.simulated_totals) == 200

    def test_p90_greater_than_p50(self, estimator: RecoveryTimeEstimator,
                                    sev1_profile: IncidentProfile) -> None:
        result = estimator.estimate(sev1_profile)
        assert result.p90 >= result.p50

    def test_deterministic_with_seed(self, sev1_profile: IncidentProfile) -> None:
        e1 = RecoveryTimeEstimator(seed=99, simulation_runs=50)
        e2 = RecoveryTimeEstimator(seed=99, simulation_runs=50)
        r1 = e1.estimate(sev1_profile)
        r2 = e2.estimate(sev1_profile)
        assert r1.p50 == pytest.approx(r2.p50)


# --- Scenario comparison ------------------------------------------------

class TestComparison:
    def test_runbook_improves_recovery(self, estimator: RecoveryTimeEstimator) -> None:
        base = IncidentProfile("a", Severity.SEV2, ["api"], has_runbook=False)
        improved = IncidentProfile("b", Severity.SEV2, ["api"], has_runbook=True)
        result = estimator.compare_scenarios(base, improved)
        assert result["improvement_pct"] > 0

    def test_comparison_keys(self, estimator: RecoveryTimeEstimator) -> None:
        p = IncidentProfile("a", Severity.SEV3, [])
        result = estimator.compare_scenarios(p, p)
        assert "base_p50" in result
        assert "improved_p50" in result
        assert "improvement_pct" in result


# --- Serialization ------------------------------------------------------

class TestSerialization:
    def test_to_dict_structure(self, estimator: RecoveryTimeEstimator,
                                sev1_profile: IncidentProfile) -> None:
        d = estimator.estimate(sev1_profile).to_dict()
        assert "incident_id" in d
        assert "p50_minutes" in d
        assert "p90_minutes" in d
        assert len(d["phases"]) == 5
