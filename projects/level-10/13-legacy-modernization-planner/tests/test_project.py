"""Tests for Legacy Modernization Planner.

Covers scoring engine, strategy selection, roadmap generation,
and plan composition.
"""
from __future__ import annotations

import pytest

from project import (
    LegacyComponent,
    ModernizationStrategy,
    Phase,
    compute_effort,
    compute_risk,
    compute_urgency,
    create_plan,
    generate_roadmap,
    recommend_strategy,
    score_component,
)


@pytest.fixture
def old_monolith() -> LegacyComponent:
    return LegacyComponent("monolith", "Java", 15, 100000, 30, 20, 5.0, 9, False)


@pytest.fixture
def modern_service() -> LegacyComponent:
    return LegacyComponent("api-svc", "Python", 2, 3000, 4, 90, 0.1, 6, True)


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

class TestScoring:
    def test_old_component_high_urgency(self, old_monolith: LegacyComponent) -> None:
        assert compute_urgency(old_monolith) > 50

    def test_modern_service_low_urgency(self, modern_service: LegacyComponent) -> None:
        assert compute_urgency(modern_service) < 20

    def test_large_codebase_high_effort(self, old_monolith: LegacyComponent) -> None:
        assert compute_effort(old_monolith) > 30

    def test_documented_service_lower_effort(self, modern_service: LegacyComponent) -> None:
        effort_with_docs = compute_effort(modern_service)
        undoc = LegacyComponent("x", "Py", 2, 3000, 4, 90, 0.1, 6, False)
        effort_without = compute_effort(undoc)
        assert effort_with_docs < effort_without

    def test_critical_component_high_risk(self, old_monolith: LegacyComponent) -> None:
        assert compute_risk(old_monolith) > 30


# ---------------------------------------------------------------------------
# Strategy selection
# ---------------------------------------------------------------------------

class TestStrategy:
    def test_low_effort_low_risk_refactor(self) -> None:
        assert recommend_strategy(20, 10, 15) == ModernizationStrategy.REFACTOR

    def test_high_risk_wraps(self) -> None:
        assert recommend_strategy(50, 30, 40) == ModernizationStrategy.WRAP

    @pytest.mark.parametrize("urgency,effort,risk,expected", [
        (10, 10, 10, ModernizationStrategy.REFACTOR),
        (60, 20, 20, ModernizationStrategy.REWRITE),
        (30, 50, 20, ModernizationStrategy.REPLACE),
    ])
    def test_strategy_variants(self, urgency: float, effort: float,
                                risk: float, expected: ModernizationStrategy) -> None:
        assert recommend_strategy(urgency, effort, risk) == expected


# ---------------------------------------------------------------------------
# Scoring full component
# ---------------------------------------------------------------------------

class TestScoreComponent:
    def test_priority_considers_business_criticality(self) -> None:
        critical = LegacyComponent("x", "Py", 10, 5000, 5, 30, 3.0, 10, False)
        minor = LegacyComponent("y", "Py", 10, 5000, 5, 30, 3.0, 2, False)
        assert score_component(critical).priority > score_component(minor).priority

    def test_invalid_criticality_raises(self) -> None:
        with pytest.raises(ValueError):
            LegacyComponent("x", "Py", 1, 1000, 1, 50, 0, 0)


# ---------------------------------------------------------------------------
# Roadmap and plan
# ---------------------------------------------------------------------------

class TestRoadmap:
    def test_roadmap_has_five_phases_per_component(self, old_monolith: LegacyComponent) -> None:
        scores = [score_component(old_monolith)]
        roadmap = generate_roadmap(scores)
        assert len(roadmap) == 5
        phases = [s.phase for s in roadmap]
        assert phases == [Phase.ASSESS, Phase.WRAP, Phase.MIGRATE, Phase.VALIDATE, Phase.DECOMMISSION]


class TestCreatePlan:
    def test_plan_summary(self, old_monolith: LegacyComponent, modern_service: LegacyComponent) -> None:
        plan = create_plan([old_monolith, modern_service])
        summary = plan.summary()
        assert summary["components_analyzed"] == 2
        assert summary["total_estimated_weeks"] > 0
        assert len(summary["priorities"]) == 2
