# Solution: Level 9 / Project 03 - Event Driven Pipeline Lab

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
"""Event-Driven Pipeline Lab — event sourcing with event store and projections."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


# --- Domain types -------------------------------------------------------

class EventCategory(Enum):
    USER = "user"
    ORDER = "order"
    INVENTORY = "inventory"
    PAYMENT = "payment"


# WHY frozen=True for events? -- Event sourcing's core invariant is that
# events are immutable once stored. Frozen dataclasses enforce this at the
# language level — any attempt to mutate an event raises AttributeError.
# The version field supports schema evolution: when the event shape changes,
# bump the version so projections can handle both old and new formats.
@dataclass(frozen=True)
class Event:
    """An immutable domain event."""
    event_id: int
    category: EventCategory
    event_type: str
    aggregate_id: str
    data: dict[str, Any]
    timestamp: float
    version: int = 1


@dataclass
class Projection:
    """A materialized view built from events."""
    name: str
    state: dict[str, Any] = field(default_factory=dict)
    events_processed: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "events_processed": self.events_processed,
            "state": self.state,
        }


# --- Event store --------------------------------------------------------

EventHandler = Callable[[Event], None]


class EventStore:
    """Append-only event store with subscriber support.

    Events are immutable once stored. Subscribers receive events
    in real-time as they are appended. Projections can replay
    the full event history to rebuild state.
    """

    def __init__(self) -> None:
        self._events: list[Event] = []
        self._next_id = 1
        # WHY a subscriber list rather than direct projection coupling? --
        # The event store should not know about projection types. Any callable
        # can subscribe, enabling logging, metrics, and projections to all
        # receive events without modifying the store.
        self._subscribers: list[EventHandler] = []

    @property
    def count(self) -> int:
        return len(self._events)

    def append(self, category: EventCategory, event_type: str,
               aggregate_id: str, data: dict[str, Any],
               timestamp: float = 0.0) -> Event:
        """Append an event to the store and notify subscribers."""
        event = Event(
            event_id=self._next_id,
            category=category,
            event_type=event_type,
            aggregate_id=aggregate_id,
            data=data,
            timestamp=timestamp or float(self._next_id),
        )
        self._events.append(event)
        self._next_id += 1

        for subscriber in self._subscribers:
            subscriber(event)

        return event

    def subscribe(self, handler: EventHandler) -> None:
        """Register a subscriber for new events."""
        self._subscribers.append(handler)

    def get_events(self, aggregate_id: str | None = None,
                   category: EventCategory | None = None,
                   after_id: int = 0) -> list[Event]:
        """Query events with optional filters."""
        result = self._events
        if aggregate_id:
            result = [e for e in result if e.aggregate_id == aggregate_id]
        if category:
            result = [e for e in result if e.category == category]
        if after_id > 0:
            result = [e for e in result if e.event_id > after_id]
        return result

    # WHY a reducer function for temporal queries? -- Each aggregate type
    # has its own state shape. A reducer function lets the caller define
    # how to fold events into state, keeping the event store generic.
    # This is the same pattern as Redux reducers and Kafka Streams aggregations.
    def get_state_at(self, aggregate_id: str, timestamp: float,
                     reducer: Callable[[dict[str, Any], Event], dict[str, Any]]) -> dict[str, Any]:
        """Replay events up to a timestamp to reconstruct state."""
        state: dict[str, Any] = {}
        for event in self._events:
            if event.aggregate_id == aggregate_id and event.timestamp <= timestamp:
                state = reducer(state, event)
        return state

    def all_events(self) -> list[Event]:
        return list(self._events)


# --- Projection builders -----------------------------------------------

class OrderCountProjection:
    """Projects a count of orders by status."""

    def __init__(self) -> None:
        self.projection = Projection(name="order_counts")

    def handle(self, event: Event) -> None:
        if event.category != EventCategory.ORDER:
            return
        self.projection.events_processed += 1
        status = event.data.get("status", "unknown")
        counts = self.projection.state.setdefault("by_status", {})
        counts[status] = counts.get(status, 0) + 1


class UserActivityProjection:
    """Projects user activity summaries."""

    def __init__(self) -> None:
        self.projection = Projection(name="user_activity")

    def handle(self, event: Event) -> None:
        if event.category != EventCategory.USER:
            return
        self.projection.events_processed += 1
        user_id = event.aggregate_id
        users = self.projection.state.setdefault("users", {})
        user = users.setdefault(user_id, {"event_count": 0, "last_event": ""})
        user["event_count"] += 1
        user["last_event"] = event.event_type


class InventoryProjection:
    """Projects inventory levels from stock events."""

    def __init__(self) -> None:
        self.projection = Projection(name="inventory_levels")

    def handle(self, event: Event) -> None:
        if event.category != EventCategory.INVENTORY:
            return
        self.projection.events_processed += 1
        product = event.aggregate_id
        levels = self.projection.state.setdefault("products", {})
        current = levels.get(product, 0)
        quantity = event.data.get("quantity", 0)

        if event.event_type == "stock_added":
            levels[product] = current + quantity
        elif event.event_type == "stock_removed":
            levels[product] = max(0, current - quantity)


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    store = EventStore()

    orders = OrderCountProjection()
    users = UserActivityProjection()
    inventory = InventoryProjection()

    store.subscribe(orders.handle)
    store.subscribe(users.handle)
    store.subscribe(inventory.handle)

    # Simulate event stream
    store.append(EventCategory.USER, "registered", "user-001", {"name": "Alice"}, 1.0)
    store.append(EventCategory.USER, "logged_in", "user-001", {}, 2.0)
    store.append(EventCategory.INVENTORY, "stock_added", "widget-A", {"quantity": 100}, 3.0)
    store.append(EventCategory.ORDER, "created", "order-001", {"user": "user-001", "status": "pending"}, 4.0)
    store.append(EventCategory.ORDER, "confirmed", "order-001", {"status": "confirmed"}, 5.0)
    store.append(EventCategory.INVENTORY, "stock_removed", "widget-A", {"quantity": 3}, 6.0)
    store.append(EventCategory.ORDER, "created", "order-002", {"user": "user-001", "status": "pending"}, 7.0)
    store.append(EventCategory.PAYMENT, "processed", "pay-001", {"amount": 49.99, "order": "order-001"}, 8.0)

    # Temporal query: what was inventory at timestamp 5?
    def inventory_reducer(state: dict, event: Event) -> dict:
        qty = state.get("quantity", 0)
        if event.event_type == "stock_added":
            qty += event.data.get("quantity", 0)
        elif event.event_type == "stock_removed":
            qty -= event.data.get("quantity", 0)
        return {"quantity": qty}

    inventory_at_5 = store.get_state_at("widget-A", 5.0, inventory_reducer)

    return {
        "total_events": store.count,
        "projections": {
            "orders": orders.projection.to_dict(),
            "users": users.projection.to_dict(),
            "inventory": inventory.projection.to_dict(),
        },
        "temporal_query": {"widget-A_at_t5": inventory_at_5},
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Event-driven pipeline lab")
    parser.add_argument("--demo", action="store_true", default=True)
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
| Frozen dataclass for Event | Enforces immutability at language level; prevents accidental mutation of stored events | Regular dataclass with convention -- relies on discipline rather than enforcement |
| Append-only store with subscriber pattern | Mirrors real event stores (Kafka, EventStore DB); subscribers decouple producers from consumers | Direct projection updates inside `append` -- couples the store to specific projection types |
| Reducer function for temporal queries | Each aggregate defines its own fold logic; keeps the store generic and reusable | Storing snapshots at each event -- faster reads but doubles storage and complicates the append path |
| Category-based event filtering in projections | Each projection ignores irrelevant categories early, avoiding unnecessary processing | Global filter on the store -- prevents subscribers from seeing events they might need later |
| Auto-incrementing event IDs | Provides total ordering of events; `after_id` filtering enables incremental catch-up | Timestamps for ordering -- timestamps can be identical for events appended in the same call |

## Alternative approaches

### Approach B: Snapshot-based projection recovery

```python
class SnapshottedProjection:
    """Save periodic snapshots to avoid replaying the full event history.
    After a crash, rebuild from the latest snapshot + events since."""
    def __init__(self, name: str, snapshot_interval: int = 100):
        self.name = name
        self.state: dict = {}
        self._processed = 0
        self._snapshot_interval = snapshot_interval
        self._snapshots: list[tuple[int, dict]] = []

    def handle(self, event) -> None:
        # ... process event ...
        self._processed += 1
        if self._processed % self._snapshot_interval == 0:
            self._snapshots.append((self._processed, dict(self.state)))

    def recover(self, events: list) -> None:
        """Recover from latest snapshot instead of full replay."""
        if self._snapshots:
            last_count, snapshot = self._snapshots[-1]
            self.state = dict(snapshot)
            events = events[last_count:]
        for e in events:
            self.handle(e)
```

**Trade-off:** Snapshots bound recovery time: instead of replaying 10 million events, you load the latest snapshot and replay only events since then. Essential for production systems with large event histories. The tradeoff is snapshot management complexity (storage, consistency, cleanup). Use full replay for learning and small systems; snapshots when replay time exceeds acceptable recovery targets.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Subscriber registered after events already appended | Subscriber misses historical events; projection state is incomplete | Provide a `replay` method that feeds all existing events to a new subscriber |
| Projection state mutation leaks across projections | If two projections share a mutable `data` dict from the same event, one mutation affects both | Events are frozen, but `data` dict values could be mutable; use deep copy in projections if needed |
| Temporal query with timestamp before any event | Reducer never processes any events; returns empty dict | Document that empty dict means "no state at this time" or return a sentinel value |
