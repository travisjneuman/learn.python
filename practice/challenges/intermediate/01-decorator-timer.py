"""
Challenge: Decorator Timer
Difficulty: Intermediate
Concepts: decorators, functools.wraps, time module, closures
Time: 30 minutes

Write a decorator called `timer` that measures how long a function takes to
execute. The decorator should:
- Print the function name and elapsed time in seconds.
- Return the original function's result unchanged.
- Preserve the original function's name and docstring (use functools.wraps).

You may use the `time` module.

Examples:
    @timer
    def slow_add(a, b):
        time.sleep(0.1)
        return a + b

    result = slow_add(1, 2)  # prints: slow_add took 0.10s
    # result == 3
"""

import time
import functools


def timer(func):
    """Decorator that prints the execution time of the wrapped function. Implement this."""
    # Hint: Use time.time() before and after calling the function, then print the difference.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    import io
    import sys

    @timer
    def add(a, b):
        """Add two numbers."""
        return a + b

    @timer
    def slow():
        time.sleep(0.05)
        return "done"

    # Test 1: Return value preserved
    assert add(2, 3) == 5, "Return value not preserved"

    # Test 2: Function name preserved
    assert add.__name__ == "add", "Function name not preserved"

    # Test 3: Docstring preserved
    assert add.__doc__ == "Add two numbers.", "Docstring not preserved"

    # Test 4: Timer output printed
    captured = io.StringIO()
    sys.stdout = captured
    slow()
    sys.stdout = sys.__stdout__
    output = captured.getvalue()
    assert "slow" in output, "Function name not in timer output"
    assert "took" in output or "s" in output, "Time not in timer output"

    print("All tests passed!")
