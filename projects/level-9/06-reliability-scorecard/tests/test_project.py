"""Tests for Reliability Scorecard.

Covers: normalization, grading, weighted scoring, and recommendations.
"""

from __future__ import annotations

import pytest

from project import (
    Dimension,
    DimensionInput,
    Grade,
    ReliabilityScorer,
    normalize_availability,
    normalize_change_failure_rate,
    normalize_mttr,
    score_to_grade,
)


# --- Grading ------------------------------------------------------------

class TestGrading:
    @pytest.mark.parametrize("score,expected_grade", [
        (0.95, Grade.A),
        (0.85, Grade.B),
        (0.75, Grade.C),
        (0.65, Grade.D),
        (0.4, Grade.F),
    ])
    def test_score_to_grade(self, score: float, expected_grade: Grade) -> None:
        assert score_to_grade(score) == expected_grade


# --- Normalizers --------------------------------------------------------

class TestNormalizers:
    @pytest.mark.parametrize("availability,expected", [
        (100.0, 1.0),
        (99.5, 0.5),
        (99.0, 0.0),
        (98.0, 0.0),  # clamped
    ])
    def test_availability(self, availability: float, expected: float) -> None:
        assert normalize_availability(availability) == pytest.approx(expected)

    @pytest.mark.parametrize("mttr,expected", [
        (0, 1.0),
        (60, 0.5),
        (120, 0.0),
        (200, 0.0),
    ])
    def test_mttr(self, mttr: float, expected: float) -> None:
        assert normalize_mttr(mttr) == pytest.approx(expected)

    @pytest.mark.parametrize("cfr,expected", [
        (0, 1.0),
        (25, 0.5),
        (50, 0.0),
    ])
    def test_change_failure_rate(self, cfr: float, expected: float) -> None:
        assert normalize_change_failure_rate(cfr) == pytest.approx(expected)


# --- ReliabilityScorer --------------------------------------------------

class TestScorer:
    def test_perfect_scores(self) -> None:
        scorer = ReliabilityScorer()
        inputs = [
            DimensionInput(Dimension.AVAILABILITY, 100.0),
            DimensionInput(Dimension.MTTR, 0),
            DimensionInput(Dimension.TEST_COVERAGE, 100),
        ]
        scorecard = scorer.score(inputs)
        assert scorecard.overall_grade == Grade.A
        assert scorecard.overall_score == pytest.approx(1.0)

    def test_poor_scores(self) -> None:
        scorer = ReliabilityScorer()
        inputs = [
            DimensionInput(Dimension.AVAILABILITY, 98.0),
            DimensionInput(Dimension.MTTR, 200),
        ]
        scorecard = scorer.score(inputs)
        assert scorecard.overall_grade == Grade.F

    def test_weighted_scoring(self) -> None:
        scorer = ReliabilityScorer()
        inputs = [
            DimensionInput(Dimension.AVAILABILITY, 100.0, weight=10.0),
            DimensionInput(Dimension.MTTR, 200, weight=1.0),  # terrible but low weight
        ]
        scorecard = scorer.score(inputs)
        assert scorecard.overall_score > 0.8  # heavily weighted toward availability

    def test_empty_inputs(self) -> None:
        scorer = ReliabilityScorer()
        scorecard = scorer.score([])
        assert scorecard.overall_grade == Grade.F

    def test_recommendations_for_low_scores(self) -> None:
        scorer = ReliabilityScorer()
        inputs = [DimensionInput(Dimension.MTTR, 100)]  # poor MTTR
        scorecard = scorer.score(inputs)
        rec = scorecard.dimensions[0].recommendation
        assert len(rec) > 0

    def test_serialization(self) -> None:
        scorer = ReliabilityScorer()
        inputs = [DimensionInput(Dimension.AVAILABILITY, 99.9)]
        d = scorer.score(inputs, period="Q1").to_dict()
        assert "overall_score" in d
        assert "dimensions" in d
        assert d["period"] == "Q1"
