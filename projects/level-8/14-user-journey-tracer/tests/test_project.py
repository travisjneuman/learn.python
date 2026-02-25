"""Tests for User Journey Tracer.

Covers: journey reconstruction, funnel analysis, statistics, and edge cases.
"""

from __future__ import annotations

import pytest

from project import (
    EventType,
    Journey,
    UserEvent,
    analyze_funnel,
    journey_stats,
    reconstruct_journeys,
)


# --- Fixtures -----------------------------------------------------------

@pytest.fixture
def sample_events() -> list[UserEvent]:
    """Events for 2 users with different journey patterns."""
    base = 1000.0
    return [
        UserEvent("u1", EventType.PAGE_VIEW, "home", base),
        UserEvent("u1", EventType.PAGE_VIEW, "search", base + 60),
        UserEvent("u1", EventType.PAGE_VIEW, "product", base + 120),
        UserEvent("u1", EventType.PURCHASE, "product", base + 180),
        UserEvent("u2", EventType.PAGE_VIEW, "home", base + 10),
        UserEvent("u2", EventType.PAGE_VIEW, "search", base + 70),
        UserEvent("u2", EventType.ERROR, "search", base + 75),
    ]


# --- Journey reconstruction --------------------------------------------

class TestReconstruction:
    def test_groups_by_user(self, sample_events: list[UserEvent]) -> None:
        journeys = reconstruct_journeys(sample_events)
        user_ids = {j.user_id for j in journeys}
        assert user_ids == {"u1", "u2"}

    def test_session_splitting(self) -> None:
        """Events with a large time gap should create separate sessions."""
        events = [
            UserEvent("u1", EventType.PAGE_VIEW, "home", 1000),
            UserEvent("u1", EventType.PAGE_VIEW, "search", 1060),
            UserEvent("u1", EventType.PAGE_VIEW, "home", 5000),  # 4000s gap
        ]
        journeys = reconstruct_journeys(events, session_gap_seconds=1800)
        u1_journeys = [j for j in journeys if j.user_id == "u1"]
        assert len(u1_journeys) == 2

    def test_journey_properties(self, sample_events: list[UserEvent]) -> None:
        journeys = reconstruct_journeys(sample_events)
        u1 = next(j for j in journeys if j.user_id == "u1")
        assert u1.converted is True
        assert u1.had_error is False
        assert u1.page_count == 3

        u2 = next(j for j in journeys if j.user_id == "u2")
        assert u2.converted is False
        assert u2.had_error is True


# --- Journey dataclass --------------------------------------------------

class TestJourney:
    def test_pages_visited_deduplicates(self) -> None:
        events = [
            UserEvent("u", EventType.PAGE_VIEW, "home", 1),
            UserEvent("u", EventType.PAGE_VIEW, "search", 2),
            UserEvent("u", EventType.PAGE_VIEW, "home", 3),  # revisit
        ]
        j = Journey(user_id="u", events=events, start_time=1, end_time=3)
        assert j.pages_visited == ["home", "search"]

    def test_empty_journey(self) -> None:
        j = Journey(user_id="u")
        assert j.duration_seconds == 0.0
        assert j.event_count == 0


# --- Funnel analysis ----------------------------------------------------

class TestFunnelAnalysis:
    def test_funnel_counts(self, sample_events: list[UserEvent]) -> None:
        journeys = reconstruct_journeys(sample_events)
        funnel = analyze_funnel(journeys, ["home", "search", "product"])
        assert funnel[0].count == 2  # both users hit home
        assert funnel[1].count == 2  # both users hit search
        assert funnel[2].count == 1  # only u1 hit product

    @pytest.mark.parametrize("stages,expected_first_count", [
        (["home"], 2),
        (["nonexistent"], 0),
    ])
    def test_funnel_edge_cases(
        self, sample_events: list[UserEvent],
        stages: list[str], expected_first_count: int,
    ) -> None:
        journeys = reconstruct_journeys(sample_events)
        funnel = analyze_funnel(journeys, stages)
        assert funnel[0].count == expected_first_count

    def test_empty_journeys_funnel(self) -> None:
        funnel = analyze_funnel([], ["home", "search"])
        assert all(s.count == 0 for s in funnel)


# --- Statistics ---------------------------------------------------------

class TestJourneyStats:
    def test_basic_stats(self, sample_events: list[UserEvent]) -> None:
        journeys = reconstruct_journeys(sample_events)
        stats = journey_stats(journeys)
        assert stats["total_journeys"] == 2
        assert stats["unique_users"] == 2
        assert stats["conversion_rate_pct"] == 50.0

    def test_empty_stats(self) -> None:
        stats = journey_stats([])
        assert stats["total_journeys"] == 0
