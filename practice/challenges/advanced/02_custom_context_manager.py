"""
Challenge 02: Custom Context Manager
Difficulty: Level 6
Topic: Build a context manager for managed resources

Create a context manager class that tracks resource acquisition and release,
logging every open/close event. Then build a second version using
@contextmanager from contextlib.

Concepts: __enter__, __exit__, contextlib.contextmanager, resource safety.
Review: concepts/files-and-paths.md (context managers section)

Instructions:
    1. Implement the `ManagedResource` class as a context manager.
    2. Implement the `managed_resource` generator-based context manager.
    3. Both must append events to the provided `log` list.
"""

from collections.abc import Generator
from contextlib import contextmanager


class ManagedResource:
    """A context manager that logs open/close events.

    On enter: append "open:<name>" to *log* and return self.
    On exit: append "close:<name>" to *log*.
    If an exception occurred inside the block, also append
    "error:<name>:<exception_class_name>" BEFORE the close entry.
    The exception should NOT be suppressed (let it propagate).
    """

    def __init__(self, name: str, log: list[str]) -> None:
        self.name = name
        self.log = log

    def __enter__(self) -> "ManagedResource":
        # YOUR CODE HERE
        ...

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:  # noqa: ANN001
        # YOUR CODE HERE
        ...


@contextmanager
def managed_resource(name: str, log: list[str]) -> Generator[str, None, None]:
    """Generator-based context manager with the same logging behaviour.

    Yields the *name* string.  Logs "open:<name>" before yield and
    "close:<name>" after.  On exception, logs "error:<name>:<class_name>"
    before close, then re-raises.
    """
    # YOUR CODE HERE
    ...


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- Class-based tests ---
    log: list[str] = []
    with ManagedResource("db", log) as res:
        assert isinstance(res, ManagedResource)
    assert log == ["open:db", "close:db"], f"Basic usage failed: {log}"

    # With exception
    log.clear()
    try:
        with ManagedResource("db", log):
            raise ValueError("boom")
    except ValueError:
        pass
    assert log == [
        "open:db",
        "error:db:ValueError",
        "close:db",
    ], f"Exception logging failed: {log}"

    # --- Generator-based tests ---
    log.clear()
    with managed_resource("file", log) as name:
        assert name == "file"
    assert log == ["open:file", "close:file"], f"Generator basic failed: {log}"

    log.clear()
    try:
        with managed_resource("file", log):
            raise RuntimeError("oops")
    except RuntimeError:
        pass
    assert log == [
        "open:file",
        "error:file:RuntimeError",
        "close:file",
    ], f"Generator exception failed: {log}"

    print("All tests passed.")
