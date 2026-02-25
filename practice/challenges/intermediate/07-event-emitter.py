"""
Challenge: Event Emitter
Difficulty: Intermediate
Concepts: classes, callbacks, pub/sub pattern, dictionaries of lists
Time: 35 minutes

Implement a pub/sub event emitter with the following methods:
- `on(event, callback)` -- register a callback for an event
- `off(event, callback)` -- remove a specific callback for an event
- `emit(event, *args, **kwargs)` -- call all callbacks registered for the event
- `once(event, callback)` -- register a callback that fires only once

Examples:
    emitter = EventEmitter()
    results = []
    emitter.on("greet", lambda name: results.append(f"Hello {name}"))
    emitter.emit("greet", "Alice")  # results == ["Hello Alice"]
"""


class EventEmitter:
    """Pub/sub event emitter. Implement this class."""

    def __init__(self):
        # Hint: Use a dict mapping event names to lists of callbacks.
        pass

    def on(self, event: str, callback) -> None:
        """Register a callback for an event."""
        pass

    def off(self, event: str, callback) -> None:
        """Remove a specific callback for an event."""
        pass

    def emit(self, event: str, *args, **kwargs) -> None:
        """Emit an event, calling all registered callbacks with the given arguments."""
        pass

    def once(self, event: str, callback) -> None:
        """Register a callback that is automatically removed after its first invocation."""
        # Hint: Create a wrapper that calls the callback and then calls self.off.
        pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Basic on and emit
    emitter = EventEmitter()
    results = []
    emitter.on("test", lambda x: results.append(x))
    emitter.emit("test", 42)
    assert results == [42], "Basic on/emit failed"

    # Test 2: Multiple listeners
    results.clear()
    emitter.on("test", lambda x: results.append(x * 2))
    emitter.emit("test", 5)
    assert results == [5, 10], "Multiple listeners failed"

    # Test 3: off removes listener
    emitter2 = EventEmitter()
    results2 = []

    def handler(x):
        results2.append(x)

    emitter2.on("ev", handler)
    emitter2.emit("ev", 1)
    emitter2.off("ev", handler)
    emitter2.emit("ev", 2)
    assert results2 == [1], "off did not remove listener"

    # Test 4: once fires only once
    emitter3 = EventEmitter()
    results3 = []
    emitter3.once("ping", lambda: results3.append("pong"))
    emitter3.emit("ping")
    emitter3.emit("ping")
    assert results3 == ["pong"], "once should fire only once"

    # Test 5: Emit with no listeners does nothing
    emitter4 = EventEmitter()
    emitter4.emit("nonexistent", "data")  # should not raise

    # Test 6: Multiple events are independent
    emitter5 = EventEmitter()
    a_results = []
    b_results = []
    emitter5.on("a", lambda: a_results.append(1))
    emitter5.on("b", lambda: b_results.append(2))
    emitter5.emit("a")
    assert a_results == [1] and b_results == [], "Events should be independent"

    print("All tests passed!")
