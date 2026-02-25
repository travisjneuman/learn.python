"""
Challenge 13: Event System
Difficulty: Level 8
Topic: Pub/sub event system with weak references

Build a publish-subscribe event system where listeners are stored as weak
references. This means listeners are automatically unregistered when they
are garbage collected, preventing memory leaks.

Concepts: weakref, WeakMethod, callbacks, pub/sub pattern.
Review: concepts/classes-and-objects.md

Instructions:
    1. Implement `EventBus.subscribe` — register a callback for an event.
    2. Implement `EventBus.emit` — call all live listeners for an event.
    3. Implement `EventBus.unsubscribe` — remove a specific listener.
    4. Dead weak references should be cleaned up automatically on emit.
"""

import weakref
from collections.abc import Callable
from typing import Any


class EventBus:
    """A pub/sub event bus with weak-reference listeners.

    Listeners are stored as weak references so that if the object owning
    the callback is garbage collected, the listener is automatically cleaned up.

    For simplicity, this implementation stores plain function references
    (not bound methods). Use weakref.ref for each callback.
    """

    def __init__(self) -> None:
        # event_name -> list of weakref.ref to callables
        self._listeners: dict[str, list[weakref.ref]] = {}

    def subscribe(self, event: str, callback: Callable[..., Any]) -> None:
        """Register *callback* as a listener for *event*.

        Store a weakref.ref to the callback.
        """
        # YOUR CODE HERE
        ...

    def unsubscribe(self, event: str, callback: Callable[..., Any]) -> None:
        """Remove *callback* from listeners of *event*.

        If the callback is not found, do nothing (no error).
        """
        # YOUR CODE HERE
        ...

    def emit(self, event: str, *args: Any, **kwargs: Any) -> int:
        """Emit *event*, calling all live listeners with the given arguments.

        Clean up any dead weak references encountered during iteration.
        Return the number of listeners that were actually called.
        """
        # YOUR CODE HERE
        ...

    def listener_count(self, event: str) -> int:
        """Return the count of live listeners for *event*."""
        # YOUR CODE HERE
        ...


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    bus = EventBus()
    results: list[str] = []

    def on_click(x: int, y: int) -> None:
        results.append(f"click:{x},{y}")

    def on_click2(x: int, y: int) -> None:
        results.append(f"click2:{x},{y}")

    def on_hover(target: str) -> None:
        results.append(f"hover:{target}")

    # --- Subscribe and emit ---
    bus.subscribe("click", on_click)
    bus.subscribe("click", on_click2)
    bus.subscribe("hover", on_hover)

    count = bus.emit("click", 10, 20)
    assert count == 2
    assert "click:10,20" in results
    assert "click2:10,20" in results

    results.clear()
    count = bus.emit("hover", target="button")
    assert count == 1
    assert results == ["hover:button"]

    # Emit unknown event
    assert bus.emit("unknown") == 0

    # --- Unsubscribe ---
    bus.unsubscribe("click", on_click2)
    results.clear()
    count = bus.emit("click", 5, 5)
    assert count == 1
    assert results == ["click:5,5"]

    # Unsubscribe non-existent (no error)
    bus.unsubscribe("click", on_click2)

    # --- Listener count ---
    assert bus.listener_count("click") == 1
    assert bus.listener_count("hover") == 1
    assert bus.listener_count("unknown") == 0

    # --- Weak reference cleanup ---
    collected_results: list[str] = []

    def make_handler(tag: str) -> Callable:
        def handler(data: str) -> None:
            collected_results.append(f"{tag}:{data}")
        return handler

    h1 = make_handler("h1")
    h2 = make_handler("h2")
    bus.subscribe("data", h1)
    bus.subscribe("data", h2)
    assert bus.listener_count("data") == 2

    bus.emit("data", "test")
    assert len(collected_results) == 2

    # Delete h2 — its weak ref should become dead
    del h2
    import gc
    gc.collect()

    collected_results.clear()
    count = bus.emit("data", "after_gc")
    assert count == 1, f"Expected 1 live listener after GC, got {count}"
    assert collected_results == ["h1:after_gc"]

    # Dead ref should be cleaned up
    assert bus.listener_count("data") == 1

    print("All tests passed.")
