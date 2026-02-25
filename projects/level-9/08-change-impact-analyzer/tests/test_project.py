"""Tests for Change Impact Analyzer.

Covers: service graph, impact traversal, risk scoring, and recommendations.
"""

from __future__ import annotations

import pytest

from project import (
    Change,
    ChangeImpactAnalyzer,
    ChangeType,
    RiskLevel,
    Service,
    ServiceGraph,
)


# --- Fixtures -----------------------------------------------------------

@pytest.fixture
def graph() -> ServiceGraph:
    g = ServiceGraph()
    g.add_service(Service("A", "team-1", tier=1, slos=["avail-99.9"]))
    g.add_service(Service("B", "team-1", tier=2))
    g.add_service(Service("C", "team-2", tier=2))
    g.add_service(Service("D", "team-3", tier=3))
    g.add_dependency("B", "A")  # B depends on A
    g.add_dependency("C", "A")  # C depends on A
    g.add_dependency("D", "B")  # D depends on B
    return g


# --- ServiceGraph -------------------------------------------------------

class TestServiceGraph:
    def test_direct_dependents(self, graph: ServiceGraph) -> None:
        deps = graph.direct_dependents("A")
        assert deps == {"B", "C"}

    def test_transitive_dependents(self, graph: ServiceGraph) -> None:
        transitive, depth = graph.transitive_dependents("A")
        assert "D" in transitive  # D -> B -> A
        assert depth == 2

    def test_no_dependents(self, graph: ServiceGraph) -> None:
        deps = graph.direct_dependents("D")
        assert len(deps) == 0


# --- Impact analysis ----------------------------------------------------

class TestImpactAnalysis:
    def test_change_to_core_service(self, graph: ServiceGraph) -> None:
        analyzer = ChangeImpactAnalyzer(graph)
        change = Change("c1", "A", ChangeType.CODE, "Update logic")
        result = analyzer.analyze(change)
        assert "B" in result.directly_affected
        assert "C" in result.directly_affected
        assert len(result.affected_teams) >= 2

    def test_change_to_leaf_service(self, graph: ServiceGraph) -> None:
        analyzer = ChangeImpactAnalyzer(graph)
        change = Change("c2", "D", ChangeType.CODE, "Fix bug")
        result = analyzer.analyze(change)
        assert len(result.directly_affected) == 0

    @pytest.mark.parametrize("change_type,min_expected_score", [
        (ChangeType.SCHEMA, 40),
        (ChangeType.CODE, 20),
        (ChangeType.CONFIG, 25),
    ])
    def test_risk_varies_by_type(
        self, graph: ServiceGraph, change_type: ChangeType,
        min_expected_score: float,
    ) -> None:
        analyzer = ChangeImpactAnalyzer(graph)
        change = Change("c", "A", change_type, "Change")
        result = analyzer.analyze(change)
        assert result.risk_score >= min_expected_score

    def test_schema_change_gets_migration_recommendation(self, graph: ServiceGraph) -> None:
        analyzer = ChangeImpactAnalyzer(graph)
        change = Change("c", "A", ChangeType.SCHEMA, "Add column")
        result = analyzer.analyze(change)
        assert any("schema" in r.lower() for r in result.recommendations)


# --- Serialization ------------------------------------------------------

class TestSerialization:
    def test_result_to_dict(self, graph: ServiceGraph) -> None:
        analyzer = ChangeImpactAnalyzer(graph)
        change = Change("c1", "A", ChangeType.CODE, "Test")
        d = analyzer.analyze(change).to_dict()
        assert "risk_level" in d
        assert "affected_teams" in d
        assert "recommendations" in d
