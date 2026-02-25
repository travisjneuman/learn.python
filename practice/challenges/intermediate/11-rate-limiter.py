"""
Challenge: Rate Limiter (Token Bucket)
Difficulty: Intermediate
Concepts: token bucket algorithm, time module, classes, state management
Time: 40 minutes

Implement a token bucket rate limiter.
- The bucket has a maximum capacity of `max_tokens`.
- Tokens are added at a rate of `refill_rate` tokens per second.
- `consume(tokens)` attempts to consume the given number of tokens.
  Returns True if there are enough tokens, False otherwise.
- `wait_and_consume(tokens)` blocks until enough tokens are available, then consumes.

You may use the `time` module.

Examples:
    limiter = RateLimiter(max_tokens=5, refill_rate=1.0)
    limiter.consume(3)   # True -- 2 tokens left
    limiter.consume(3)   # False -- only 2 available
    time.sleep(1)        # 1 token refilled -- now 3 available
    limiter.consume(3)   # True
"""

import time


class RateLimiter:
    """Token bucket rate limiter. Implement this class."""

    def __init__(self, max_tokens: int, refill_rate: float):
        """
        Initialize the rate limiter.
        - max_tokens: maximum number of tokens the bucket can hold
        - refill_rate: tokens added per second
        """
        # Hint: Store max_tokens, refill_rate, current tokens, and last refill time.
        pass

    def _refill(self) -> None:
        """Refill tokens based on elapsed time since last refill."""
        # Hint: Calculate elapsed time, add (elapsed * refill_rate) tokens, cap at max_tokens.
        pass

    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens. Return True if successful, False if not enough tokens."""
        pass

    def wait_and_consume(self, tokens: int = 1) -> None:
        """Block until enough tokens are available, then consume them."""
        # Hint: Calculate how long until enough tokens are available, sleep, then consume.
        pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Initial tokens available
    limiter = RateLimiter(max_tokens=5, refill_rate=10.0)
    assert limiter.consume(3) is True, "Initial consume failed"

    # Test 2: Not enough tokens
    assert limiter.consume(3) is False, "Should fail when not enough tokens"

    # Test 3: Refill over time
    limiter2 = RateLimiter(max_tokens=5, refill_rate=100.0)
    limiter2.consume(5)  # drain all tokens
    time.sleep(0.05)  # ~5 tokens refilled at 100/sec
    assert limiter2.consume(3) is True, "Refill over time failed"

    # Test 4: Tokens don't exceed max
    limiter3 = RateLimiter(max_tokens=3, refill_rate=100.0)
    time.sleep(0.1)  # way more than enough to fill
    assert limiter3.consume(3) is True, "Max tokens consume failed"
    assert limiter3.consume(1) is False, "Should not exceed max_tokens"

    # Test 5: wait_and_consume blocks until ready
    limiter4 = RateLimiter(max_tokens=5, refill_rate=100.0)
    limiter4.consume(5)  # drain all
    start = time.time()
    limiter4.wait_and_consume(1)
    elapsed = time.time() - start
    assert elapsed < 0.5, "wait_and_consume took too long"

    # Test 6: Consume exactly available
    limiter5 = RateLimiter(max_tokens=3, refill_rate=0.0)
    assert limiter5.consume(3) is True, "Exact consume failed"
    assert limiter5.consume(1) is False, "Should be empty after exact consume"

    print("All tests passed!")
