"""
Solution: Rate Limiter (Token Bucket)

Approach: Track the current number of tokens and the last refill time.
Before each consume attempt, calculate how much time has passed and add
tokens proportionally (capped at max). consume() checks if enough tokens
are available. wait_and_consume() calculates how long to sleep before
enough tokens will be available, then consumes.
"""

import time


class RateLimiter:
    def __init__(self, max_tokens: int, refill_rate: float):
        self.max_tokens = max_tokens
        self.refill_rate = refill_rate
        self.tokens = float(max_tokens)
        self.last_refill = time.time()

    def _refill(self) -> None:
        now = time.time()
        elapsed = now - self.last_refill
        # Add tokens proportional to elapsed time
        self.tokens = min(self.max_tokens, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def consume(self, tokens: int = 1) -> bool:
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def wait_and_consume(self, tokens: int = 1) -> None:
        self._refill()
        if self.tokens < tokens:
            # Calculate how long until enough tokens are available
            deficit = tokens - self.tokens
            if self.refill_rate > 0:
                wait_time = deficit / self.refill_rate
                time.sleep(wait_time)
        # After waiting, refill and consume
        self._refill()
        self.tokens -= tokens


if __name__ == "__main__":
    limiter = RateLimiter(max_tokens=5, refill_rate=10.0)
    assert limiter.consume(3) is True
    assert limiter.consume(3) is False

    limiter2 = RateLimiter(max_tokens=5, refill_rate=100.0)
    limiter2.consume(5)
    time.sleep(0.05)
    assert limiter2.consume(3) is True

    limiter3 = RateLimiter(max_tokens=3, refill_rate=100.0)
    time.sleep(0.1)
    assert limiter3.consume(3) is True
    assert limiter3.consume(1) is False

    limiter4 = RateLimiter(max_tokens=5, refill_rate=100.0)
    limiter4.consume(5)
    start = time.time()
    limiter4.wait_and_consume(1)
    elapsed = time.time() - start
    assert elapsed < 0.5

    limiter5 = RateLimiter(max_tokens=3, refill_rate=0.0)
    assert limiter5.consume(3) is True
    assert limiter5.consume(1) is False

    print("All tests passed!")
