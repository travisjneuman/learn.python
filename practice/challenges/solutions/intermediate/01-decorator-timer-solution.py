"""
Solution: Decorator Timer

Approach: The timer decorator wraps the original function. It records the
time before and after the function call, prints the elapsed time, and
returns the original result. functools.wraps preserves the original
function's metadata (name, docstring).
"""

import time
import functools


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.2f}s")
        return result
    return wrapper


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

    assert add(2, 3) == 5
    assert add.__name__ == "add"
    assert add.__doc__ == "Add two numbers."

    captured = io.StringIO()
    sys.stdout = captured
    slow()
    sys.stdout = sys.__stdout__
    output = captured.getvalue()
    assert "slow" in output
    assert "took" in output or "s" in output

    print("All tests passed!")
