"""
Solution: Event Emitter

Approach: Store a dictionary mapping event names to lists of callback functions.
For `once`, create a wrapper that calls the original callback then removes
itself. Copy the listener list before iterating in emit to avoid issues
if a listener modifies the list (e.g., once removing itself).
"""


class EventEmitter:
    def __init__(self):
        self._listeners: dict[str, list] = {}

    def on(self, event: str, callback) -> None:
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)

    def off(self, event: str, callback) -> None:
        if event in self._listeners:
            self._listeners[event] = [
                cb for cb in self._listeners[event] if cb is not callback
            ]

    def emit(self, event: str, *args, **kwargs) -> None:
        if event not in self._listeners:
            return
        # Copy the list to avoid mutation during iteration (e.g., once listeners)
        for callback in list(self._listeners.get(event, [])):
            callback(*args, **kwargs)

    def once(self, event: str, callback) -> None:
        def wrapper(*args, **kwargs):
            callback(*args, **kwargs)
            self.off(event, wrapper)

        self.on(event, wrapper)


if __name__ == "__main__":
    emitter = EventEmitter()
    results = []
    emitter.on("test", lambda x: results.append(x))
    emitter.emit("test", 42)
    assert results == [42]

    results.clear()
    emitter.on("test", lambda x: results.append(x * 2))
    emitter.emit("test", 5)
    assert results == [5, 10]

    emitter2 = EventEmitter()
    results2 = []

    def handler(x):
        results2.append(x)

    emitter2.on("ev", handler)
    emitter2.emit("ev", 1)
    emitter2.off("ev", handler)
    emitter2.emit("ev", 2)
    assert results2 == [1]

    emitter3 = EventEmitter()
    results3 = []
    emitter3.once("ping", lambda: results3.append("pong"))
    emitter3.emit("ping")
    emitter3.emit("ping")
    assert results3 == ["pong"]

    emitter4 = EventEmitter()
    emitter4.emit("nonexistent", "data")

    emitter5 = EventEmitter()
    a_results = []
    b_results = []
    emitter5.on("a", lambda: a_results.append(1))
    emitter5.on("b", lambda: b_results.append(2))
    emitter5.emit("a")
    assert a_results == [1] and b_results == []

    print("All tests passed!")
