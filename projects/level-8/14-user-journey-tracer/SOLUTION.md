# Solution: Level 8 / Project 14 - User Journey Tracer

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first -- it guides
> your thinking without giving away the answer.
>
> [Back to project README](./README.md)

---

## Complete solution

```python
"""User Journey Tracer -- trace user journeys through system events."""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class EventType(Enum):
    PAGE_VIEW = "page_view"
    CLICK = "click"
    FORM_SUBMIT = "form_submit"
    PURCHASE = "purchase"
    ERROR = "error"
    SESSION_START = "session_start"
    SESSION_END = "session_end"

# WHY flat events instead of pre-structured journeys? -- Raw event streams
# are how analytics data actually arrives: one event at a time, out of order,
# from multiple users. Reconstructing journeys from flat events teaches the
# groupby-then-sort pattern that Amplitude and Mixpanel use internally.
@dataclass
class UserEvent:
    user_id: str
    event_type: EventType
    page: str
    timestamp: float
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class Journey:
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
        # WHY preserve first-visit order? -- Funnel analysis needs to know
        # the order pages were first seen, not every page view. Deduplication
        # with insertion order gives the true journey path.
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
        return {"user_id": self.user_id, "event_count": self.event_count,
                "pages_visited": self.pages_visited,
                "duration_seconds": round(self.duration_seconds, 1),
                "had_error": self.had_error, "converted": self.converted}

@dataclass
class FunnelStage:
    name: str
    count: int = 0
    drop_off_count: int = 0
    conversion_rate: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {"stage": self.name, "count": self.count,
                "drop_off": self.drop_off_count,
                "conversion_rate_pct": round(self.conversion_rate * 100, 1)}

# WHY session_gap_seconds for session splitting? -- Analytics platforms
# define a "session" as a sequence of events with no gap longer than N
# minutes (typically 30). A user who returns after 2 hours is a new session.
def reconstruct_journeys(events: list[UserEvent],
                         session_gap_seconds: float = 1800) -> list[Journey]:
    by_user: dict[str, list[UserEvent]] = defaultdict(list)
    for event in events:
        by_user[event.user_id].append(event)

    journeys: list[Journey] = []
    for user_id, user_events in by_user.items():
        sorted_events = sorted(user_events, key=lambda e: e.timestamp)
        current_session: list[UserEvent] = [sorted_events[0]]
        for event in sorted_events[1:]:
            gap = event.timestamp - current_session[-1].timestamp
            if gap > session_gap_seconds:
                journeys.append(_build_journey(user_id, current_session))
                current_session = [event]
            else:
                current_session.append(event)
        if current_session:
            journeys.append(_build_journey(user_id, current_session))

    return sorted(journeys, key=lambda j: j.start_time)

def _build_journey(user_id: str, events: list[UserEvent]) -> Journey:
    return Journey(user_id=user_id, events=events,
                   start_time=events[0].timestamp, end_time=events[-1].timestamp)

def analyze_funnel(journeys: list[Journey], stages: list[str]) -> list[FunnelStage]:
    """WHY funnel analysis? -- Funnels show where users drop off in a
    multi-step process (home -> search -> product -> cart -> checkout).
    The biggest drop-off stage is where to focus optimization efforts."""
    stage_results: list[FunnelStage] = []
    previous_count = len(journeys)
    for stage_name in stages:
        matching = sum(1 for j in journeys if stage_name in j.pages_visited)
        drop_off = previous_count - matching
        rate = matching / len(journeys) if journeys else 0.0
        stage_results.append(FunnelStage(name=stage_name, count=matching,
                                          drop_off_count=max(0, drop_off),
                                          conversion_rate=rate))
        previous_count = matching
    return stage_results

def journey_stats(journeys: list[Journey]) -> dict[str, Any]:
    if not journeys:
        return {"total_journeys": 0}
    durations = [j.duration_seconds for j in journeys]
    page_counts = [j.page_count for j in journeys]
    return {
        "total_journeys": len(journeys),
        "unique_users": len(set(j.user_id for j in journeys)),
        "avg_duration_seconds": round(sum(durations) / len(durations), 1),
        "avg_pages_per_journey": round(sum(page_counts) / len(page_counts), 1),
        "error_rate_pct": round(sum(1 for j in journeys if j.had_error) / len(journeys) * 100, 1),
        "conversion_rate_pct": round(sum(1 for j in journeys if j.converted) / len(journeys) * 100, 1),
    }

def run_demo() -> dict[str, Any]:
    rng = random.Random(42)
    pages = ["home", "search", "product", "cart", "checkout", "confirmation"]
    base_time = 1700000000.0
    events: list[UserEvent] = []
    for user_num in range(50):
        user_id = f"user-{user_num:04d}"
        t = base_time + rng.uniform(0, 3600)
        for i, page in enumerate(pages):
            events.append(UserEvent(user_id=user_id, event_type=EventType.PAGE_VIEW,
                                    page=page, timestamp=t + i * rng.uniform(30, 300)))
            if rng.random() < 0.05:
                events.append(UserEvent(user_id=user_id, event_type=EventType.ERROR,
                                        page=page, timestamp=t + i * rng.uniform(30, 300) + 1))
            if page == "confirmation":
                events.append(UserEvent(user_id=user_id, event_type=EventType.PURCHASE,
                                        page=page, timestamp=t + i * rng.uniform(30, 300) + 2))
            if rng.random() < 0.15 * (i + 1):
                break
    journeys = reconstruct_journeys(events, session_gap_seconds=1800)
    funnel = analyze_funnel(journeys, pages)
    return {"stats": journey_stats(journeys), "funnel": [s.to_dict() for s in funnel],
            "sample_journeys": [j.to_dict() for j in journeys[:5]]}

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="User journey tracer")
    parser.add_argument("--demo", action="store_true", default=True)
    parser.parse_args(argv)
    print(json.dumps(run_demo(), indent=2))

if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Session gap-based splitting (30 min) | Industry standard; matches how Google Analytics and Amplitude define sessions | Fixed session IDs -- requires client-side session tracking, unavailable in server logs |
| Groupby user then sort by time | Efficient O(n log n) approach; handles out-of-order events naturally | Pre-sorted event stream -- assumes data arrives in order, which is rarely true |
| First-visit deduplication for pages_visited | Gives the true journey path without revisit noise | All visits -- inflates page count and obscures the actual funnel path |
| Funnel compares against total journeys | Shows absolute conversion rate at each stage | Stage-to-stage comparison -- shows relative drop-off but hides absolute performance |

## Alternative approaches

### Approach B: Streaming journey reconstruction

```python
class StreamingJourneyBuilder:
    """Build journeys incrementally as events arrive, without buffering
    all events in memory. Suitable for real-time analytics pipelines."""
    def __init__(self, gap_seconds: float = 1800):
        self._active: dict[str, Journey] = {}
        self._completed: list[Journey] = []
        self._gap = gap_seconds

    def process_event(self, event: UserEvent) -> Journey | None:
        journey = self._active.get(event.user_id)
        if journey and (event.timestamp - journey.end_time) > self._gap:
            self._completed.append(journey)
            journey = None
        if journey is None:
            journey = Journey(user_id=event.user_id, start_time=event.timestamp)
            self._active[event.user_id] = journey
        journey.events.append(event)
        journey.end_time = event.timestamp
        return None  # journeys complete on timeout
```

**Trade-off:** Streaming reconstruction processes events one at a time with bounded memory. Essential for real-time pipelines processing millions of events per second. The batch approach (sort all events, then group) is simpler and produces identical results, but requires all events to fit in memory.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Events arriving out of timestamp order | Sorting per-user events fixes this, but cross-user ordering may be wrong | Sort the final journey list by start_time |
| Session gap too short (e.g. 60s) | A user pausing to read a page for 2 minutes starts a new session | Use industry standard of 1800s (30 min) or tune based on your product |
| Empty funnel stages list | `analyze_funnel()` returns empty list; division by zero if journeys is empty | Guard with `if journeys else 0.0` in conversion rate calculation |
