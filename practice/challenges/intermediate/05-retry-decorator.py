"""
Challenge: Retry Decorator with Exponential Backoff
Difficulty: Intermediate
Concepts: decorators, exceptions, time.sleep, exponential backoff
Time: 35 minutes

Write a decorator `retry` that retries a function call on exception.
Parameters:
- max_retries (int): maximum number of retry attempts (default 3)
- base_delay (float): initial delay in seconds (default 0.1)
- exceptions (tuple): exception types to catch (default (Exception,))

The delay doubles each retry (exponential backoff): base_delay, base_delay*2, base_delay*4, ...

If all retries are exhausted, raise the last exception.

Examples:
    @retry(max_retries=3, base_delay=0.01)
    def flaky():
        if random.random() < 0.7:
            raise ConnectionError("failed")
        return "success"
"""

import time
import functools


def retry(max_retries: int = 3, base_delay: float = 0.1, exceptions: tuple = (Exception,)):
    """Decorator factory for retrying functions with exponential backoff. Implement this."""
    # Hint: Return a decorator that wraps the function in a loop with try/except.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Succeeds on first try
    call_count = 0

    @retry(max_retries=3, base_delay=0.001)
    def always_works():
        global call_count
        call_count += 1
        return "ok"

    assert always_works() == "ok", "Immediate success failed"
    assert call_count == 1, "Should only call once on success"

    # Test 2: Succeeds after retries
    attempt = 0

    @retry(max_retries=5, base_delay=0.001)
    def works_third_try():
        global attempt
        attempt += 1
        if attempt < 3:
            raise ValueError("not yet")
        return "finally"

    assert works_third_try() == "finally", "Retry success failed"
    assert attempt == 3, "Should have taken 3 attempts"

    # Test 3: Exhausts retries and raises
    @retry(max_retries=2, base_delay=0.001)
    def always_fails():
        raise RuntimeError("permanent failure")

    try:
        always_fails()
        assert False, "Should have raised RuntimeError"
    except RuntimeError as e:
        assert "permanent failure" in str(e), "Wrong exception message"

    # Test 4: Only catches specified exceptions
    @retry(max_retries=3, base_delay=0.001, exceptions=(ValueError,))
    def wrong_exception():
        raise TypeError("not caught")

    try:
        wrong_exception()
        assert False, "Should have raised TypeError immediately"
    except TypeError:
        pass

    # Test 5: Preserves function metadata
    @retry(max_retries=3, base_delay=0.001)
    def documented():
        """A documented function."""
        return True

    assert documented.__name__ == "documented", "Name not preserved"
    assert documented.__doc__ == "A documented function.", "Docstring not preserved"

    print("All tests passed!")
