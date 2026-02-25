"""Tests for Release Readiness Evaluator.

Covers: criteria scoring, readiness levels, required failures, and report structure.
"""

from __future__ import annotations

import pytest

from project import (
    CriterionResult,
    EvaluatorConfig,
    ReadinessLevel,
    ReleaseReadinessEvaluator,
    changelog_criterion,
    lint_clean_criterion,
    performance_criterion,
    security_scan_criterion,
    coverage_criterion,
)


# --- Criterion factories ------------------------------------------------

class TestCriterionFactories:
    @pytest.mark.parametrize("coverage,required,expected_pass", [
        (90.0, 80.0, True),
        (80.0, 80.0, True),
        (79.0, 80.0, False),
    ])
    def test_coverage_criterion(
        self, coverage: float, required: float, expected_pass: bool,
    ) -> None:
        c = coverage_criterion(coverage, required)
        result = c.evaluate_fn()
        assert result.passed == expected_pass

    @pytest.mark.parametrize("issues,expected_pass", [
        (0, True),
        (1, False),
        (5, False),
    ])
    def test_lint_criterion(self, issues: int, expected_pass: bool) -> None:
        c = lint_clean_criterion(issues)
        result = c.evaluate_fn()
        assert result.passed == expected_pass

    def test_security_critical_vuln_fails(self) -> None:
        c = security_scan_criterion(vulnerabilities=3, critical=1)
        result = c.evaluate_fn()
        assert result.passed is False

    def test_security_no_critical_passes(self) -> None:
        c = security_scan_criterion(vulnerabilities=2, critical=0)
        result = c.evaluate_fn()
        assert result.passed is True

    @pytest.mark.parametrize("p99,threshold,expected_pass", [
        (200, 500, True),
        (500, 500, True),
        (600, 500, False),
    ])
    def test_performance_criterion(
        self, p99: float, threshold: float, expected_pass: bool,
    ) -> None:
        c = performance_criterion(p99, threshold)
        result = c.evaluate_fn()
        assert result.passed == expected_pass


# --- Evaluator ----------------------------------------------------------

class TestEvaluator:
    def test_all_passing_gives_go(self) -> None:
        evaluator = ReleaseReadinessEvaluator()
        evaluator.add_criterion(coverage_criterion(95.0))
        evaluator.add_criterion(security_scan_criterion(0, 0))
        evaluator.add_criterion(changelog_criterion(True))
        report = evaluator.evaluate("v1.0")
        assert report.readiness == ReadinessLevel.GO
        assert report.overall_score > 0.8

    def test_required_failure_gives_no_go(self) -> None:
        evaluator = ReleaseReadinessEvaluator()
        evaluator.add_criterion(coverage_criterion(50.0, 80.0))  # fails, required
        evaluator.add_criterion(changelog_criterion(True))
        report = evaluator.evaluate("v1.0")
        assert report.readiness == ReadinessLevel.NO_GO
        assert "test_coverage" in report.required_failures

    def test_low_score_gives_no_go(self) -> None:
        evaluator = ReleaseReadinessEvaluator()
        evaluator.add_criterion(lint_clean_criterion(15))
        evaluator.add_criterion(performance_criterion(900.0, 500.0))
        report = evaluator.evaluate("v1.0")
        assert report.readiness == ReadinessLevel.NO_GO

    def test_no_criteria_gives_no_go(self) -> None:
        evaluator = ReleaseReadinessEvaluator()
        report = evaluator.evaluate("v1.0")
        assert report.readiness == ReadinessLevel.NO_GO

    def test_conditional_score_range(self) -> None:
        evaluator = ReleaseReadinessEvaluator(
            EvaluatorConfig(go_threshold=0.9, conditional_threshold=0.6)
        )
        # Use non-required criteria to avoid automatic NO_GO from required failures
        evaluator.add_criterion(lint_clean_criterion(10))      # score: 0.5
        evaluator.add_criterion(changelog_criterion(True))     # score: 1.0
        evaluator.add_criterion(performance_criterion(600, 500))  # score: 0.83
        report = evaluator.evaluate("v1.0")
        # Weighted average ~0.78, between 0.6 and 0.9 => CONDITIONAL
        assert report.readiness == ReadinessLevel.CONDITIONAL


# --- Report structure ---------------------------------------------------

class TestReport:
    def test_report_to_dict(self) -> None:
        evaluator = ReleaseReadinessEvaluator()
        evaluator.add_criterion(changelog_criterion(True))
        report = evaluator.evaluate("v1.0")
        d = report.to_dict()
        assert "release_name" in d
        assert "overall_score" in d
        assert "criteria" in d
        assert d["passed"] + d["failed"] == len(d["criteria"])
