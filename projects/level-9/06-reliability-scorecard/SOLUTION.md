# Solution: Level 9 / Project 06 - Reliability Scorecard

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first -- it guides
> your thinking without giving away the answer.
>
> [Back to project README](./README.md)

---

## Complete solution

```python
"""Reliability Scorecard — score system reliability across multiple dimensions."""

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


# WHY per-dimension normalizer functions? -- Each dimension has a completely
# different scale: availability is 99.0-100.0%, MTTR is 0-120 minutes,
# deployment frequency is 0-14/week. Normalization maps each to 0-1 so
# they can be weighted and summed. Without normalization, a raw 99.9
# availability would dominate a raw 5 deploys/week.

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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Per-dimension normalizer functions (Strategy pattern) | Each dimension has a different scale and direction (higher-is-better vs lower-is-better); separate functions make the mapping explicit | Single normalizer with direction flag -- loses the domain-specific scaling logic (availability 99.0-100 vs MTTR 0-120) |
| Weighted scoring with normalized inputs | Different dimensions matter differently; availability (weight 2.0) affects the score more than test coverage (weight 1.0) | Equal weights -- treats all dimensions as equally important, which contradicts DORA findings |
| Lambda-based recommendation functions | Lightweight; each recommendation is a one-liner that checks the threshold | Class hierarchy for recommendations -- excessive structure for simple threshold checks |
| Clamped normalization with `max(0, min(1, ...))` | Prevents scores outside 0-1 range even with extreme input values | Unclamped scores -- a 101% availability would produce a score >1.0, breaking grade thresholds |
| Letter grades derived from normalized scores | Familiar academic grading provides instant intuition ("B is good, F is failing") | Numeric-only scoring -- harder for non-technical stakeholders to interpret |

## Alternative approaches

### Approach B: Trend-aware scoring with period-over-period comparison

```python
class TrendScorer:
    """Score reliability across multiple periods and detect trends.
    A service improving from D to B is in a better position than
    one stable at B but trending down."""
    def __init__(self):
        self._history: list[Scorecard] = []

    def add_period(self, scorecard: Scorecard) -> None:
        self._history.append(scorecard)

    def trend_report(self) -> dict:
        if len(self._history) < 2:
            return {"trend": "insufficient_data"}
        recent = self._history[-1].overall_score
        previous = self._history[-2].overall_score
        delta = recent - previous
        return {
            "current": round(recent, 2),
            "previous": round(previous, 2),
            "delta": round(delta, 2),
            "trend": "improving" if delta > 0.05 else "declining" if delta < -0.05 else "stable",
        }
```

**Trade-off:** Trend analysis adds temporal context: a B-grade service that was an F last quarter is on a positive trajectory, while a B-grade service that was an A is degrading. This context changes prioritization decisions. The tradeoff is needing historical data storage and more complex analysis. Use point-in-time scoring for initial assessments; trend analysis when you have multiple periods of data.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| All weights set to zero | `total_weight` is 0, causing division by zero in weight normalization | Guard with `if total_weight == 0: return Scorecard(0.0, Grade.F, [], period)` |
| Availability value below 99.0 | Normalizer returns 0.0 (or negative before clamping); the 99-100 range is intentionally narrow | This is correct behavior: sub-99% availability is indeed an F grade for most production systems |
| Missing dimension in NORMALIZERS dict | Falls back to identity function `lambda v: v`, but raw values may not be in 0-1 range | Register all dimensions in NORMALIZERS, or validate inputs before scoring |
