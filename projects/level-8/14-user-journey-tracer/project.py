"""User Journey Tracer — trace user journeys through system events.

Design rationale:
    Understanding how users flow through a system is essential for
    debugging, optimization, and product analytics. This project builds
    a journey tracer that reconstructs user sessions from event streams,
    identifies drop-off points, and computes conversion funnels — the
    same pattern used by Amplitude, Mixpanel, and custom analytics.

Concepts practised:
    - event stream processing
    - session reconstruction from timestamps
    - funnel analysis with stage transitions
    - dataclasses for events and journeys
    - groupby-style aggregation
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# --- Domain types -------------------------------------------------------

class EventType(Enum):
    PAGE_VIEW = "page_view"
    CLICK = "click"
    FORM_SUBMIT = "form_submit"
    PURCHASE = "purchase"
    ERROR = "error"
    SESSION_START = "session_start"
    SESSION_END = "session_end"


@dataclass
class UserEvent:
    """A single user interaction event."""
    user_id: str
    event_type: EventType
    page: str
    timestamp: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Journey:
    """A reconstructed user journey (session)."""
    user_id: str
    events: list[UserEvent] = field(default_factory=list)
    start_time: float = 0.0
    end_time: float = 0.0

    @property
    def duration_seconds(self) -> float:
        return self.end_time - self.start_time if self.events else 0.0

    @property
    def page_count(self) -> int:
        return len(set(e.page for e in self.events))

    @property
    def event_count(self) -> int:
        return len(self.events)

    @property
    def pages_visited(self) -> list[str]:
        """Return pages in visit order, deduplicated to first visit."""
        seen: set[str] = set()
        ordered: list[str] = []
        for e in self.events:
            if e.page not in seen:
                seen.add(e.page)
                ordered.append(e.page)
        return ordered

    @property
    def had_error(self) -> bool:
        return any(e.event_type == EventType.ERROR for e in self.events)

    @property
    def converted(self) -> bool:
        return any(e.event_type == EventType.PURCHASE for e in self.events)

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "event_count": self.event_count,
            "pages_visited": self.pages_visited,
            "duration_seconds": round(self.duration_seconds, 1),
            "had_error": self.had_error,
            "converted": self.converted,
        }


@dataclass
class FunnelStage:
    """A single stage in a conversion funnel."""
    name: str
    count: int = 0
    drop_off_count: int = 0
    conversion_rate: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.name,
            "count": self.count,
            "drop_off": self.drop_off_count,
            "conversion_rate_pct": round(self.conversion_rate * 100, 1),
        }


# --- Journey reconstruction --------------------------------------------

def reconstruct_journeys(
    events: list[UserEvent],
    session_gap_seconds: float = 1800,  # 30 min default
) -> list[Journey]:
    """Group events into user journeys based on time gaps.

    Events from the same user that occur within session_gap_seconds
    of each other are grouped into the same journey.
    """
    # Group by user
    by_user: dict[str, list[UserEvent]] = defaultdict(list)
    for event in events:
        by_user[event.user_id].append(event)

    journeys: list[Journey] = []
    for user_id, user_events in by_user.items():
        sorted_events = sorted(user_events, key=lambda e: e.timestamp)

        # Split into sessions based on time gaps
        current_session: list[UserEvent] = [sorted_events[0]]
        for event in sorted_events[1:]:
            gap = event.timestamp - current_session[-1].timestamp
            if gap > session_gap_seconds:
                # New session
                journeys.append(_build_journey(user_id, current_session))
                current_session = [event]
            else:
                current_session.append(event)

        if current_session:
            journeys.append(_build_journey(user_id, current_session))

    return sorted(journeys, key=lambda j: j.start_time)


def _build_journey(user_id: str, events: list[UserEvent]) -> Journey:
    return Journey(
        user_id=user_id,
        events=events,
        start_time=events[0].timestamp,
        end_time=events[-1].timestamp,
    )


# --- Funnel analysis ----------------------------------------------------

def analyze_funnel(
    journeys: list[Journey],
    stages: list[str],
) -> list[FunnelStage]:
    """Compute conversion funnel across ordered page stages.

    For each stage, count how many journeys reached that page.
    Drop-off is the difference from the previous stage.
    """
    stage_results: list[FunnelStage] = []
    previous_count = len(journeys)

    for stage_name in stages:
        matching = sum(
            1 for j in journeys if stage_name in j.pages_visited
        )
        drop_off = previous_count - matching
        rate = matching / len(journeys) if journeys else 0.0

        stage_results.append(FunnelStage(
            name=stage_name,
            count=matching,
            drop_off_count=max(0, drop_off),
            conversion_rate=rate,
        ))
        previous_count = matching

    return stage_results


# --- Analytics helpers --------------------------------------------------

def journey_stats(journeys: list[Journey]) -> dict[str, Any]:
    """Compute aggregate statistics across all journeys."""
    if not journeys:
        return {"total_journeys": 0}

    durations = [j.duration_seconds for j in journeys]
    page_counts = [j.page_count for j in journeys]

    return {
        "total_journeys": len(journeys),
        "unique_users": len(set(j.user_id for j in journeys)),
        "avg_duration_seconds": round(sum(durations) / len(durations), 1),
        "avg_pages_per_journey": round(sum(page_counts) / len(page_counts), 1),
        "error_rate_pct": round(
            sum(1 for j in journeys if j.had_error) / len(journeys) * 100, 1
        ),
        "conversion_rate_pct": round(
            sum(1 for j in journeys if j.converted) / len(journeys) * 100, 1
        ),
    }


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    """Simulate user journeys through an e-commerce funnel."""
    import random
    rng = random.Random(42)

    pages = ["home", "search", "product", "cart", "checkout", "confirmation"]
    base_time = 1700000000.0
    events: list[UserEvent] = []

    for user_num in range(50):
        user_id = f"user-{user_num:04d}"
        t = base_time + rng.uniform(0, 3600)

        # Each user progresses through pages with drop-off probability
        for i, page in enumerate(pages):
            events.append(UserEvent(
                user_id=user_id,
                event_type=EventType.PAGE_VIEW,
                page=page,
                timestamp=t + i * rng.uniform(30, 300),
            ))
            # Add error events randomly
            if rng.random() < 0.05:
                events.append(UserEvent(
                    user_id=user_id,
                    event_type=EventType.ERROR,
                    page=page,
                    timestamp=t + i * rng.uniform(30, 300) + 1,
                ))
            # Purchase on confirmation page
            if page == "confirmation":
                events.append(UserEvent(
                    user_id=user_id,
                    event_type=EventType.PURCHASE,
                    page=page,
                    timestamp=t + i * rng.uniform(30, 300) + 2,
                ))
            # Drop off with increasing probability
            if rng.random() < 0.15 * (i + 1):
                break

    journeys = reconstruct_journeys(events, session_gap_seconds=1800)
    funnel = analyze_funnel(journeys, pages)
    stats = journey_stats(journeys)

    return {
        "stats": stats,
        "funnel": [s.to_dict() for s in funnel],
        "sample_journeys": [j.to_dict() for j in journeys[:5]],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="User journey tracer and funnel analyzer")
    parser.add_argument("--demo", action="store_true", default=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    print(json.dumps(run_demo(), indent=2))


if __name__ == "__main__":
    main()
