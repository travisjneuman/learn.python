"""
Challenge 15: Functional Pipeline
Difficulty: Level 7
Topic: Compose pure functions with reduce and partial

Build a functional programming toolkit that lets you compose functions into
pipelines, curry them, and chain transformations — all without mutating state.

Concepts: functools.reduce, functools.partial, closures, higher-order functions.
Review: concepts/functions-explained.md

Instructions:
    1. Implement `pipe` — compose functions left-to-right.
    2. Implement `compose` — compose functions right-to-left.
    3. Implement `curry` — convert a multi-arg function to a chain of single-arg calls.
    4. Implement `map_pipeline` — apply a list of transforms to a list of items.
"""

import functools
from collections.abc import Callable
from typing import Any, TypeVar

A = TypeVar("A")
B = TypeVar("B")


def pipe(*funcs: Callable) -> Callable:
    """Compose functions left-to-right.

    pipe(f, g, h)(x) == h(g(f(x)))

    If no functions are given, return the identity function.
    If one function is given, return it as-is.
    """
    # YOUR CODE HERE
    ...


def compose(*funcs: Callable) -> Callable:
    """Compose functions right-to-left.

    compose(f, g, h)(x) == f(g(h(x)))

    If no functions are given, return the identity function.
    """
    # YOUR CODE HERE
    ...


def curry(func: Callable) -> Callable:
    """Convert a function of N arguments into a chain of single-argument calls.

    curry(f)(a)(b)(c) == f(a, b, c)

    Uses inspect to determine the number of required parameters.
    When all required arguments have been collected, call the function.
    """
    # YOUR CODE HERE
    ...


def map_pipeline(transforms: list[Callable[[A], A]], items: list[A]) -> list[A]:
    """Apply each transform in order to every item in *items*.

    Equivalent to:
        for transform in transforms:
            items = [transform(item) for item in items]
        return items

    But implement it using pipe() or reduce().
    """
    # YOUR CODE HERE
    ...


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- pipe ---
    double = lambda x: x * 2
    add_one = lambda x: x + 1
    square = lambda x: x ** 2

    f = pipe(double, add_one)
    assert f(3) == 7  # double(3)=6, add_one(6)=7

    g = pipe(add_one, double, square)
    assert g(2) == 36  # add_one(2)=3, double(3)=6, square(6)=36

    identity = pipe()
    assert identity(42) == 42

    single = pipe(double)
    assert single(5) == 10

    # --- compose ---
    h = compose(square, double)  # square(double(x))
    assert h(3) == 36  # double(3)=6, square(6)=36

    h2 = compose(add_one, square, double)  # add_one(square(double(x)))
    assert h2(2) == 17  # double(2)=4, square(4)=16, add_one(16)=17

    # --- curry ---
    def add3(a: int, b: int, c: int) -> int:
        return a + b + c

    curried = curry(add3)
    assert curried(1)(2)(3) == 6

    # Partial application
    add_to_5 = curried(2)(3)
    assert add_to_5(10) == 15

    def greet(name: str, greeting: str) -> str:
        return f"{greeting}, {name}!"

    curried_greet = curry(greet)
    assert curried_greet("Alice")("Hello") == "Hello, Alice!"

    # Single-arg function should just work
    curried_double = curry(double)
    assert curried_double(5) == 10

    # --- map_pipeline ---
    nums = [1, 2, 3, 4]
    result = map_pipeline([double, add_one], nums)
    assert result == [3, 5, 7, 9]  # double each, then add one

    # Empty transforms = identity
    assert map_pipeline([], [1, 2, 3]) == [1, 2, 3]

    # String transforms
    words = ["hello", "world"]
    result2 = map_pipeline([str.upper, lambda s: s + "!"], words)
    assert result2 == ["HELLO!", "WORLD!"]

    print("All tests passed.")
