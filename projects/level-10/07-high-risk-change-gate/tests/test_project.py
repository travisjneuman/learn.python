"""Tests for High-Risk Change Gate.

Covers individual risk factors, aggregate scoring, gate decisions,
policy enforcement, and edge cases.
"""
from __future__ import annotations

import pytest

from project import (
    AuthChangeFactor,
    BlastRadiusFactor,
    ChangeGate,
    ChangeRequest,
    ChangeSizeFactor,
    DeployWindowFactor,
    GateDecision,
    RiskLevel,
    RollbackFactor,
    SchemaChangeFactor,
    build_default_gate,
)


@pytest.fixture
def low_risk_change() -> ChangeRequest:
    return ChangeRequest("CHG-001", "Fix typo", "alice", ["docs"], lines_changed=3, deploy_window="off_peak")


@pytest.fixture
def high_risk_change() -> ChangeRequest:
    return ChangeRequest(
        "CHG-002", "Migrate billing schema", "bob",
        ["billing", "payment", "reporting"],
        changes_schema=True, changes_auth=True, lines_changed=600,
    )


@pytest.fixture
def gate() -> ChangeGate:
    return build_default_gate()


class TestBlastRadiusFactor:
    @pytest.mark.parametrize("services,expected_score", [
        ([], 0.0),
        (["a"], 10.0),
        (["a", "b", "c"], 30.0),
        (["a", "b", "c", "d"], 30.0),
    ])
    def test_score_scales_with_services(self, services: list[str], expected_score: float) -> None:
        change = ChangeRequest("c", "t", "a", services)
        assert BlastRadiusFactor().assess(change).score == expected_score


class TestSchemaChangeFactor:
    def test_schema_change_scores_high(self) -> None:
        change = ChangeRequest("c", "t", "a", changes_schema=True)
        assert SchemaChangeFactor().assess(change).score == 25.0

    def test_no_schema_scores_zero(self) -> None:
        change = ChangeRequest("c", "t", "a", changes_schema=False)
        assert SchemaChangeFactor().assess(change).score == 0.0


class TestRollbackFactor:
    def test_rollback_reduces_score(self) -> None:
        change = ChangeRequest("c", "t", "a", is_rollback=True)
        assert RollbackFactor().assess(change).score == -15.0


class TestChangeSizeFactor:
    @pytest.mark.parametrize("lines,expected_score", [
        (10, 5.0), (100, 10.0), (300, 15.0), (1000, 20.0),
    ])
    def test_size_buckets(self, lines: int, expected_score: float) -> None:
        change = ChangeRequest("c", "t", "a", lines_changed=lines)
        assert ChangeSizeFactor().assess(change).score == expected_score


class TestChangeGate:
    def test_low_risk_auto_approved(self, gate: ChangeGate, low_risk_change: ChangeRequest) -> None:
        result = gate.evaluate(low_risk_change)
        assert result.risk_level == RiskLevel.LOW
        assert result.decision == GateDecision.APPROVED

    def test_high_risk_needs_review(self, gate: ChangeGate, high_risk_change: ChangeRequest) -> None:
        result = gate.evaluate(high_risk_change)
        assert result.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL)
        assert result.required_approvers >= 2

    def test_rollback_lowers_risk(self, gate: ChangeGate) -> None:
        normal = ChangeRequest("c1", "t", "a", ["s1", "s2"], lines_changed=100)
        rollback = ChangeRequest("c2", "t", "a", ["s1", "s2"], lines_changed=100, is_rollback=True)
        assert gate.evaluate(rollback).total_score < gate.evaluate(normal).total_score


class TestRiskLevel:
    @pytest.mark.parametrize("score,expected", [
        (0.0, RiskLevel.LOW), (24.9, RiskLevel.LOW),
        (25.0, RiskLevel.MEDIUM), (50.0, RiskLevel.HIGH),
        (75.0, RiskLevel.CRITICAL),
    ])
    def test_score_to_level(self, score: float, expected: RiskLevel) -> None:
        assert RiskLevel.from_score(score) == expected


class TestGateResult:
    def test_summary_structure(self, gate: ChangeGate, low_risk_change: ChangeRequest) -> None:
        summary = gate.evaluate(low_risk_change).summary()
        assert "change_id" in summary
        assert "factors" in summary
        assert len(summary["factors"]) == gate.factor_count
