"""Tests for Event-Driven Pipeline Lab.

Covers: event store, projections, subscribers, temporal queries, and filtering.
"""

from __future__ import annotations

import pytest

from project import (
    EventCategory,
    EventStore,
    InventoryProjection,
    OrderCountProjection,
    UserActivityProjection,
)


# --- Fixtures -----------------------------------------------------------

@pytest.fixture
def store() -> EventStore:
    return EventStore()


# --- Event store --------------------------------------------------------

class TestEventStore:
    def test_append_and_count(self, store: EventStore) -> None:
        store.append(EventCategory.USER, "registered", "u1", {"name": "A"})
        store.append(EventCategory.USER, "logged_in", "u1", {})
        assert store.count == 2

    def test_auto_incrementing_ids(self, store: EventStore) -> None:
        e1 = store.append(EventCategory.USER, "a", "u1", {})
        e2 = store.append(EventCategory.USER, "b", "u2", {})
        assert e2.event_id == e1.event_id + 1

    def test_events_are_immutable(self, store: EventStore) -> None:
        event = store.append(EventCategory.USER, "test", "u1", {"key": "val"})
        with pytest.raises(AttributeError):
            event.event_type = "modified"  # type: ignore[misc]


# --- Querying -----------------------------------------------------------

class TestQuerying:
    def test_filter_by_aggregate(self, store: EventStore) -> None:
        store.append(EventCategory.ORDER, "created", "o1", {})
        store.append(EventCategory.ORDER, "created", "o2", {})
        results = store.get_events(aggregate_id="o1")
        assert len(results) == 1

    def test_filter_by_category(self, store: EventStore) -> None:
        store.append(EventCategory.USER, "registered", "u1", {})
        store.append(EventCategory.ORDER, "created", "o1", {})
        results = store.get_events(category=EventCategory.USER)
        assert len(results) == 1

    def test_filter_after_id(self, store: EventStore) -> None:
        store.append(EventCategory.USER, "a", "u1", {})
        store.append(EventCategory.USER, "b", "u1", {})
        store.append(EventCategory.USER, "c", "u1", {})
        results = store.get_events(after_id=2)
        assert len(results) == 1
        assert results[0].event_type == "c"


# --- Subscribers --------------------------------------------------------

class TestSubscribers:
    def test_subscriber_receives_events(self, store: EventStore) -> None:
        received: list[str] = []
        store.subscribe(lambda e: received.append(e.event_type))
        store.append(EventCategory.USER, "registered", "u1", {})
        assert received == ["registered"]


# --- Projections --------------------------------------------------------

class TestOrderCountProjection:
    def test_counts_by_status(self, store: EventStore) -> None:
        proj = OrderCountProjection()
        store.subscribe(proj.handle)
        store.append(EventCategory.ORDER, "created", "o1", {"status": "pending"})
        store.append(EventCategory.ORDER, "confirmed", "o2", {"status": "confirmed"})
        store.append(EventCategory.ORDER, "created", "o3", {"status": "pending"})
        assert proj.projection.state["by_status"]["pending"] == 2
        assert proj.projection.state["by_status"]["confirmed"] == 1

    def test_ignores_non_order_events(self, store: EventStore) -> None:
        proj = OrderCountProjection()
        store.subscribe(proj.handle)
        store.append(EventCategory.USER, "registered", "u1", {})
        assert proj.projection.events_processed == 0


class TestInventoryProjection:
    def test_stock_tracking(self, store: EventStore) -> None:
        proj = InventoryProjection()
        store.subscribe(proj.handle)
        store.append(EventCategory.INVENTORY, "stock_added", "widget", {"quantity": 100})
        store.append(EventCategory.INVENTORY, "stock_removed", "widget", {"quantity": 30})
        assert proj.projection.state["products"]["widget"] == 70

    def test_stock_never_negative(self, store: EventStore) -> None:
        proj = InventoryProjection()
        store.subscribe(proj.handle)
        store.append(EventCategory.INVENTORY, "stock_added", "item", {"quantity": 5})
        store.append(EventCategory.INVENTORY, "stock_removed", "item", {"quantity": 10})
        assert proj.projection.state["products"]["item"] == 0


# --- Temporal queries ---------------------------------------------------

class TestTemporalQueries:
    def test_state_at_timestamp(self, store: EventStore) -> None:
        store.append(EventCategory.INVENTORY, "stock_added", "w", {"quantity": 50}, 1.0)
        store.append(EventCategory.INVENTORY, "stock_added", "w", {"quantity": 30}, 2.0)
        store.append(EventCategory.INVENTORY, "stock_removed", "w", {"quantity": 10}, 3.0)

        def reducer(state, event):
            qty = state.get("quantity", 0)
            if event.event_type == "stock_added":
                qty += event.data.get("quantity", 0)
            elif event.event_type == "stock_removed":
                qty -= event.data.get("quantity", 0)
            return {"quantity": qty}

        state = store.get_state_at("w", 2.0, reducer)
        assert state["quantity"] == 80  # 50 + 30
