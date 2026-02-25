"""
Challenge 06: Decorator Stack
Difficulty: Level 6
Topic: Build composable decorators with functools.wraps

Create three decorators that can be stacked in any order on any function.
Each decorator adds a specific behaviour. Understanding decorator composition
is essential for working with Flask, FastAPI, pytest, and more.

Concepts: closures, functools.wraps, *args/**kwargs, decorator stacking.
Review: concepts/decorators-explained.md

Instructions:
    1. `log_calls` — records each call to a shared list.
    2. `retry` — retries the function up to *times* on exception.
    3. `cache_result` — caches results by arguments (simple memoization).
"""

import functools
from collections.abc import Callable
from typing import Any


def log_calls(log: list[str]) -> Callable:
    """Decorator factory that appends "<func_name>(<args>)" to *log* on each call.

    Format: "func_name(arg1, arg2, key=val)" — use repr() for each argument.
    The decorator must preserve the original function's name and docstring.
    """
    # YOUR CODE HERE
    ...


def retry(times: int = 3) -> Callable:
    """Decorator factory that retries the wrapped function up to *times* attempts.

    - On each failure, catch the exception and try again.
    - If all attempts fail, re-raise the LAST exception.
    - Must preserve the original function's name and docstring.
    """
    # YOUR CODE HERE
    ...


def cache_result(func: Callable) -> Callable:
    """Decorator that caches return values based on positional arguments.

    - Use a dict stored on the wrapper as `wrapper._cache`.
    - Key: tuple of positional args (ignore kwargs for simplicity).
    - Must preserve the original function's name and docstring.
    """
    # YOUR CODE HERE
    ...


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- log_calls ---
    call_log: list[str] = []

    @log_calls(call_log)
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    assert add(1, 2) == 3
    assert add(3, b=4) == 7
    assert call_log[0] == "add(1, 2)"
    assert call_log[1] == "add(3, b=4)"
    assert add.__name__ == "add"
    assert add.__doc__ == "Add two numbers."

    # --- retry ---
    _attempt = {"count": 0}

    @retry(times=3)
    def flaky() -> str:
        """Sometimes fails."""
        _attempt["count"] += 1
        if _attempt["count"] < 3:
            raise ConnectionError("fail")
        return "ok"

    assert flaky() == "ok"
    assert _attempt["count"] == 3
    assert flaky.__name__ == "flaky"

    # All attempts fail
    @retry(times=2)
    def always_fails() -> None:
        raise ValueError("nope")

    try:
        always_fails()
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert str(e) == "nope"

    # --- cache_result ---
    _calls = {"count": 0}

    @cache_result
    def expensive(n: int) -> int:
        _calls["count"] += 1
        return n * n

    assert expensive(4) == 16
    assert expensive(4) == 16  # cached
    assert _calls["count"] == 1, "Should have only computed once"
    assert expensive(5) == 25
    assert _calls["count"] == 2
    assert (4,) in expensive._cache
    assert expensive.__name__ == "expensive"

    # --- Stacked decorators ---
    stack_log: list[str] = []

    @log_calls(stack_log)
    @cache_result
    def square(x: int) -> int:
        return x * x

    assert square(3) == 9
    assert square(3) == 9
    assert len(stack_log) == 2  # logged twice even though cached

    print("All tests passed.")
