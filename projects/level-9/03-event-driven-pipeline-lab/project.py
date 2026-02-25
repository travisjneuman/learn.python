"""Event-Driven Pipeline Lab — event sourcing with event store and projections.

Design rationale:
    Event sourcing stores state as a sequence of immutable events rather than
    mutable records. This project builds an event store with projections that
    materialize views from events — the foundational pattern for CQRS, audit
    trails, and temporal queries.

Concepts practised:
    - event sourcing: append-only event store
    - projections: materializing views from event streams
    - observer pattern for event subscribers
    - dataclasses for typed events
    - temporal queries (state at a point in time)
"""

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
