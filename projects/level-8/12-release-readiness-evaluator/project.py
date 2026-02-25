"""Release Readiness Evaluator — score release readiness based on configurable criteria.

Design rationale:
    Shipping software requires checking many gates: test coverage, linting,
    security scans, documentation, and changelog entries. This project builds
    a configurable readiness evaluator that scores a release candidate against
    weighted criteria — the same pattern used in CI/CD release gates.

Concepts practised:
    - weighted scoring with configurable criteria
    - dataclasses for criteria and evaluation results
    - strategy pattern for pluggable evaluators
    - threshold-based go/no-go decisions
    - structured reporting
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


# --- Domain types -------------------------------------------------------

class ReadinessLevel(Enum):
    GO = "go"
    CONDITIONAL = "conditional"
    NO_GO = "no_go"


class CriterionCategory(Enum):
    TESTING = "testing"
    SECURITY = "security"
    DOCUMENTATION = "documentation"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"
    INFRASTRUCTURE = "infrastructure"


@dataclass
class Criterion:
    """A single readiness criterion to evaluate."""
    name: str
    category: CriterionCategory
    weight: float  # 0.0 - 1.0, importance
    evaluate_fn: Callable[[], CriterionResult]
    required: bool = False  # If True, failure = automatic NO_GO


@dataclass
class CriterionResult:
    """Result of evaluating a single criterion."""
    name: str
    passed: bool
    score: float  # 0.0 - 1.0
    message: str = ""
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "score": round(self.score, 2),
            "message": self.message,
        }


@dataclass
class ReadinessReport:
    """Complete readiness evaluation report."""
    release_name: str
    overall_score: float
    readiness: ReadinessLevel
    criteria_results: list[CriterionResult]
    required_failures: list[str]
    go_threshold: float
    conditional_threshold: float

    @property
    def passed_count(self) -> int:
        return sum(1 for r in self.criteria_results if r.passed)

    @property
    def failed_count(self) -> int:
        return sum(1 for r in self.criteria_results if not r.passed)

    def to_dict(self) -> dict[str, Any]:
        return {
            "release_name": self.release_name,
            "overall_score": round(self.overall_score, 2),
            "readiness": self.readiness.value,
            "passed": self.passed_count,
            "failed": self.failed_count,
            "required_failures": self.required_failures,
            "criteria": [r.to_dict() for r in self.criteria_results],
        }


# --- Evaluator engine ---------------------------------------------------

@dataclass
class EvaluatorConfig:
    """Configuration for the readiness evaluator."""
    go_threshold: float = 0.8       # Score >= this = GO
    conditional_threshold: float = 0.6  # Score >= this = CONDITIONAL, below = NO_GO


class ReleaseReadinessEvaluator:
    """Evaluates release readiness against weighted criteria."""

    def __init__(self, config: EvaluatorConfig | None = None) -> None:
        self._config = config or EvaluatorConfig()
        self._criteria: list[Criterion] = []

    def add_criterion(self, criterion: Criterion) -> None:
        self._criteria.append(criterion)

    def evaluate(self, release_name: str) -> ReadinessReport:
        """Run all criteria and compute weighted readiness score."""
        results: list[CriterionResult] = []
        required_failures: list[str] = []
        total_weight = sum(c.weight for c in self._criteria)

        if total_weight == 0:
            return ReadinessReport(
                release_name=release_name,
                overall_score=0.0,
                readiness=ReadinessLevel.NO_GO,
                criteria_results=[],
                required_failures=[],
                go_threshold=self._config.go_threshold,
                conditional_threshold=self._config.conditional_threshold,
            )

        weighted_score = 0.0
        for criterion in self._criteria:
            result = criterion.evaluate_fn()
            results.append(result)
            weighted_score += result.score * (criterion.weight / total_weight)

            if criterion.required and not result.passed:
                required_failures.append(criterion.name)

        # Determine readiness level
        if required_failures:
            readiness = ReadinessLevel.NO_GO
        elif weighted_score >= self._config.go_threshold:
            readiness = ReadinessLevel.GO
        elif weighted_score >= self._config.conditional_threshold:
            readiness = ReadinessLevel.CONDITIONAL
        else:
            readiness = ReadinessLevel.NO_GO

        return ReadinessReport(
            release_name=release_name,
            overall_score=weighted_score,
            readiness=readiness,
            criteria_results=results,
            required_failures=required_failures,
            go_threshold=self._config.go_threshold,
            conditional_threshold=self._config.conditional_threshold,
        )


# --- Criterion factories ------------------------------------------------

def coverage_criterion(
    coverage_pct: float,
    required_pct: float = 80.0,
) -> Criterion:
    """Check that test coverage meets the minimum threshold."""
    def evaluate() -> CriterionResult:
        score = min(coverage_pct / required_pct, 1.0)
        return CriterionResult(
            name="test_coverage",
            passed=coverage_pct >= required_pct,
            score=score,
            message=f"Coverage {coverage_pct}% (required {required_pct}%)",
        )
    return Criterion(
        name="test_coverage", category=CriterionCategory.TESTING,
        weight=0.25, evaluate_fn=evaluate, required=True,
    )


def lint_clean_criterion(issues_count: int) -> Criterion:
    """Check that linting has no issues."""
    def evaluate() -> CriterionResult:
        return CriterionResult(
            name="lint_clean",
            passed=issues_count == 0,
            score=1.0 if issues_count == 0 else max(0, 1 - issues_count / 20),
            message=f"{issues_count} lint issues",
        )
    return Criterion(
        name="lint_clean", category=CriterionCategory.TESTING,
        weight=0.15, evaluate_fn=evaluate,
    )


def security_scan_criterion(
    vulnerabilities: int,
    critical: int = 0,
) -> Criterion:
    """Check security scan results."""
    def evaluate() -> CriterionResult:
        passed = critical == 0
        score = 1.0 if vulnerabilities == 0 else max(0, 1 - vulnerabilities / 10)
        return CriterionResult(
            name="security_scan",
            passed=passed,
            score=score,
            message=f"{vulnerabilities} vulns ({critical} critical)",
        )
    return Criterion(
        name="security_scan", category=CriterionCategory.SECURITY,
        weight=0.25, evaluate_fn=evaluate, required=True,
    )


def changelog_criterion(has_entry: bool) -> Criterion:
    """Check that changelog has been updated."""
    def evaluate() -> CriterionResult:
        return CriterionResult(
            name="changelog_updated",
            passed=has_entry,
            score=1.0 if has_entry else 0.0,
            message="Changelog updated" if has_entry else "No changelog entry",
        )
    return Criterion(
        name="changelog_updated", category=CriterionCategory.DOCUMENTATION,
        weight=0.10, evaluate_fn=evaluate,
    )


def performance_criterion(
    p99_ms: float,
    threshold_ms: float = 500.0,
) -> Criterion:
    """Check that p99 latency meets the threshold."""
    def evaluate() -> CriterionResult:
        score = min(threshold_ms / max(p99_ms, 0.1), 1.0)
        return CriterionResult(
            name="performance_p99",
            passed=p99_ms <= threshold_ms,
            score=score,
            message=f"p99={p99_ms}ms (threshold={threshold_ms}ms)",
        )
    return Criterion(
        name="performance_p99", category=CriterionCategory.PERFORMANCE,
        weight=0.25, evaluate_fn=evaluate,
    )


# --- CLI ----------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    """Demonstrate release readiness evaluation."""
    evaluator = ReleaseReadinessEvaluator()

    evaluator.add_criterion(coverage_criterion(85.0))
    evaluator.add_criterion(lint_clean_criterion(2))
    evaluator.add_criterion(security_scan_criterion(1, critical=0))
    evaluator.add_criterion(changelog_criterion(True))
    evaluator.add_criterion(performance_criterion(320.0))

    report = evaluator.evaluate("v2.1.0-rc1")
    return report.to_dict()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Release readiness evaluator")
    parser.add_argument("--release", default="v2.1.0-rc1", help="Release name")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    output = run_demo()
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
