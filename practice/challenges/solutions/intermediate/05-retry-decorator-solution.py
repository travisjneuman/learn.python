"""
Solution: Retry Decorator with Exponential Backoff

Approach: retry() is a decorator factory that returns a decorator. The
decorator wraps the function in a loop that catches specified exceptions.
On each failure, it sleeps for an exponentially increasing delay (base * 2^i).
If all retries are exhausted, it re-raises the last exception.
"""

import time
import functools


def retry(max_retries: int = 3, base_delay: float = 0.1, exceptions: tuple = (Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):  # +1 because first call is not a "retry"
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        # Exponential backoff: base_delay * 2^attempt
                        delay = base_delay * (2 ** attempt)
                        time.sleep(delay)
                    else:
                        raise
            raise last_exception  # Should not reach here, but just in case
        return wrapper
    return decorator


if __name__ == "__main__":
    call_count = 0

    @retry(max_retries=3, base_delay=0.001)
    def always_works():
        nonlocal call_count
        call_count += 1
        return "ok"

    assert always_works() == "ok"
    assert call_count == 1

    attempt = 0

    @retry(max_retries=5, base_delay=0.001)
    def works_third_try():
        nonlocal attempt
        attempt += 1
        if attempt < 3:
            raise ValueError("not yet")
        return "finally"

    assert works_third_try() == "finally"
    assert attempt == 3

    @retry(max_retries=2, base_delay=0.001)
    def always_fails():
        raise RuntimeError("permanent failure")

    try:
        always_fails()
        assert False
    except RuntimeError as e:
        assert "permanent failure" in str(e)

    @retry(max_retries=3, base_delay=0.001, exceptions=(ValueError,))
    def wrong_exception():
        raise TypeError("not caught")

    try:
        wrong_exception()
        assert False
    except TypeError:
        pass

    @retry(max_retries=3, base_delay=0.001)
    def documented():
        """A documented function."""
        return True

    assert documented.__name__ == "documented"
    assert documented.__doc__ == "A documented function."

    print("All tests passed!")
