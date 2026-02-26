"""Reliability Scorecard — score system reliability across multiple dimensions.

Design rationale:
    Reliability is multi-dimensional: uptime, MTTR, change failure rate,
    deployment frequency, and incident response all contribute. This project
    builds a weighted scorecard that evaluates reliability across these
    dimensions and generates improvement recommendations.

Concepts practised:
    - weighted multi-criteria scoring
    - dataclasses for scorecard dimensions
    - normalization and grading
    - trend analysis across scoring periods
    - strategy pattern for scoring functions
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


# --- Domain types -------------------------------------------------------

class Grade(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"


# WHY these specific dimensions? -- These align with the DORA metrics
# (Deployment Frequency, Change Failure Rate, MTTR, Lead Time) plus
# operational dimensions. DORA research shows these four metrics
# statistically predict software delivery performance. Adding availability,
# incident response, and test coverage rounds out the reliability picture.
class Dimension(Enum):
    AVAILABILITY = "availability"
    MTTR = "mean_time_to_recovery"
    CHANGE_FAILURE_RATE = "change_failure_rate"
    DEPLOYMENT_FREQUENCY = "deployment_frequency"
    INCIDENT_RESPONSE = "incident_response"
    TEST_COVERAGE = "test_coverage"


@dataclass
class DimensionScore:
    """Score for a single reliability dimension."""
    dimension: Dimension
    raw_value: float
    normalized_score: float  # 0.0 - 1.0
    weight: float
    grade: Grade
    unit: str = ""
    recommendation: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "dimension": self.dimension.value,
            "raw_value": round(self.raw_value, 2),
            "score": round(self.normalized_score, 2),
            "weight": self.weight,
            "grade": self.grade.value,
            "unit": self.unit,
            "recommendation": self.recommendation,
        }


@dataclass
class Scorecard:
    """Complete reliability scorecard."""
    overall_score: float
    overall_grade: Grade
    dimensions: list[DimensionScore]
    period: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "overall_score": round(self.overall_score, 2),
            "overall_grade": self.overall_grade.value,
            "period": self.period,
            "dimensions": [d.to_dict() for d in self.dimensions],
        }


# --- Scoring functions (Strategy pattern) -------------------------------

def score_to_grade(score: float) -> Grade:
    """Convert a 0-1 score to a letter grade."""
    if score >= 0.9:
        return Grade.A
    if score >= 0.8:
        return Grade.B
    if score >= 0.7:
        return Grade.C
    if score >= 0.6:
        return Grade.D
    return Grade.F


def normalize_availability(value: float) -> float:
    """Normalize availability (99.0-100.0) to 0-1 scale."""
    return max(0, min(1, (value - 99.0) / 1.0))


def normalize_mttr(value_minutes: float) -> float:
    """Normalize MTTR (lower is better). 0 min = 1.0, 120+ min = 0.0."""
    return max(0, min(1, 1 - (value_minutes / 120)))


def normalize_change_failure_rate(value_pct: float) -> float:
    """Normalize CFR (lower is better). 0% = 1.0, 50%+ = 0.0."""
    return max(0, min(1, 1 - (value_pct / 50)))


def normalize_deployment_freq(deploys_per_week: float) -> float:
    """Normalize deployment frequency (higher is better)."""
    return max(0, min(1, deploys_per_week / 14))  # 2x daily = 1.0


def normalize_incident_response(minutes: float) -> float:
    """Normalize incident response time (lower is better)."""
    return max(0, min(1, 1 - (minutes / 60)))


def normalize_test_coverage(pct: float) -> float:
    """Normalize test coverage (higher is better)."""
    return max(0, min(1, pct / 100))


NORMALIZERS: dict[Dimension, Callable[[float], float]] = {
    Dimension.AVAILABILITY: normalize_availability,
    Dimension.MTTR: normalize_mttr,
    Dimension.CHANGE_FAILURE_RATE: normalize_change_failure_rate,
    Dimension.DEPLOYMENT_FREQUENCY: normalize_deployment_freq,
    Dimension.INCIDENT_RESPONSE: normalize_incident_response,
    Dimension.TEST_COVERAGE: normalize_test_coverage,
}

UNITS: dict[Dimension, str] = {
    Dimension.AVAILABILITY: "%",
    Dimension.MTTR: "minutes",
    Dimension.CHANGE_FAILURE_RATE: "%",
    Dimension.DEPLOYMENT_FREQUENCY: "deploys/week",
    Dimension.INCIDENT_RESPONSE: "minutes",
    Dimension.TEST_COVERAGE: "%",
}

RECOMMENDATIONS: dict[Dimension, Callable[[float], str]] = {
    Dimension.AVAILABILITY: lambda s: "" if s >= 0.8 else "Improve uptime monitoring and redundancy",
    Dimension.MTTR: lambda s: "" if s >= 0.8 else "Automate incident response runbooks",
    Dimension.CHANGE_FAILURE_RATE: lambda s: "" if s >= 0.8 else "Add canary deployments and feature flags",
    Dimension.DEPLOYMENT_FREQUENCY: lambda s: "" if s >= 0.8 else "Invest in CI/CD pipeline improvements",
    Dimension.INCIDENT_RESPONSE: lambda s: "" if s >= 0.8 else "Establish on-call rotation and alerting",
    Dimension.TEST_COVERAGE: lambda s: "" if s >= 0.8 else "Increase test coverage, especially integration tests",
}


# --- Scorecard builder --------------------------------------------------

@dataclass
class DimensionInput:
    """Raw input for a single dimension."""
    dimension: Dimension
    value: float
    weight: float = 1.0


class ReliabilityScorer:
    """Builds reliability scorecards from raw metrics."""

    def score(self, inputs: list[DimensionInput], period: str = "") -> Scorecard:
        total_weight = sum(i.weight for i in inputs)
        if total_weight == 0:
            return Scorecard(0.0, Grade.F, [], period)

        dimensions: list[DimensionScore] = []
        weighted_sum = 0.0

        for inp in inputs:
            normalizer = NORMALIZERS.get(inp.dimension, lambda v: v)
            normalized = normalizer(inp.value)
            grade = score_to_grade(normalized)
            rec_fn = RECOMMENDATIONS.get(inp.dimension, lambda s: "")
            recommendation = rec_fn(normalized)

            dim_score = DimensionScore(
                dimension=inp.dimension,
                raw_value=inp.value,
                normalized_score=normalized,
                weight=inp.weight,
                grade=grade,
                unit=UNITS.get(inp.dimension, ""),
                recommendation=recommendation,
            )
            dimensions.append(dim_score)
            weighted_sum += normalized * (inp.weight / total_weight)

        overall_grade = score_to_grade(weighted_sum)
        return Scorecard(weighted_sum, overall_grade, dimensions, period)


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    scorer = ReliabilityScorer()
    inputs = [
        DimensionInput(Dimension.AVAILABILITY, 99.85, weight=2.0),
        DimensionInput(Dimension.MTTR, 25, weight=1.5),
        DimensionInput(Dimension.CHANGE_FAILURE_RATE, 8, weight=1.0),
        DimensionInput(Dimension.DEPLOYMENT_FREQUENCY, 10, weight=1.0),
        DimensionInput(Dimension.INCIDENT_RESPONSE, 12, weight=1.5),
        DimensionInput(Dimension.TEST_COVERAGE, 78, weight=1.0),
    ]
    scorecard = scorer.score(inputs, period="2025-Q1")
    return scorecard.to_dict()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reliability scorecard generator")
    parser.add_argument("--period", default="2025-Q1")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    print(json.dumps(run_demo(), indent=2))


if __name__ == "__main__":
    main()
