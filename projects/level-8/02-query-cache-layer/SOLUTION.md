# Solution: Level 8 / Project 02 - Query Cache Layer

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first -- it guides
> your thinking without giving away the answer.
>
> [Back to project README](./README.md)

---

## Complete solution

```python
"""Query Cache Layer -- LRU cache with TTL expiration for expensive computations."""

from __future__ import annotations

import argparse
import json
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Callable


# --- Domain types -------------------------------------------------------

# WHY build from scratch instead of functools.lru_cache? -- lru_cache doesn't
# support TTL expiration, eviction callbacks, or hit-rate metrics. Building
# from OrderedDict teaches the mechanics that production caches (Redis,
# Memcached) use underneath.
@dataclass
class CacheEntry:
    key: str
    value: Any
    created_at: float
    ttl_seconds: float
    access_count: int = 0

    @property
    def is_expired(self) -> bool:
        # WHY time.monotonic()? -- time.time() can jump backwards during NTP
        # corrections or leap seconds. monotonic() only moves forward,
        # preventing false expirations from clock adjustments.
        return (time.monotonic() - self.created_at) > self.ttl_seconds


@dataclass
class CacheStats:
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0

    @property
    def total_requests(self) -> int:
        return self.hits + self.misses

    @property
    def hit_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return round(self.hits / self.total_requests * 100, 2)

    def to_dict(self) -> dict[str, Any]:
        return {
            "hits": self.hits, "misses": self.misses,
            "evictions": self.evictions, "expirations": self.expirations,
            "total_requests": self.total_requests,
            "hit_rate_pct": self.hit_rate,
        }


# --- LRU Cache implementation -------------------------------------------

class LRUCache:
    """Least-Recently-Used cache with TTL expiration.

    WHY OrderedDict? -- It maintains insertion order AND provides O(1)
    move_to_end(), which is exactly what LRU needs: on every access,
    move the entry to the end (most recent), and evict from the front
    (least recent) when full.
    """

    def __init__(
        self,
        capacity: int = 128,
        default_ttl: float = 60.0,
        on_evict: Callable[[str, Any], None] | None = None,
    ) -> None:
        if capacity < 1:
            raise ValueError("Cache capacity must be at least 1")
        self._capacity = capacity
        self._default_ttl = default_ttl
        self._store: OrderedDict[str, CacheEntry] = OrderedDict()
        self._stats = CacheStats()
        self._on_evict = on_evict

    @property
    def stats(self) -> CacheStats:
        return self._stats

    @property
    def size(self) -> int:
        return len(self._store)

    def get(self, key: str) -> Any | None:
        if key not in self._store:
            self._stats.misses += 1
            return None

        entry = self._store[key]

        # WHY lazy expiration? -- Checking TTL on access (lazy) avoids
        # background timer threads. The tradeoff: expired entries linger
        # in memory until accessed. For most caches this is acceptable
        # because memory pressure is managed by the capacity limit.
        if entry.is_expired:
            self._remove(key)
            self._stats.expirations += 1
            self._stats.misses += 1
            return None

        # WHY move_to_end? -- This is the "recently used" part of LRU.
        # Every access refreshes the entry's position, so frequently
        # accessed entries stay in the cache while stale ones drift
        # to the front and get evicted first.
        self._store.move_to_end(key)
        entry.access_count += 1
        self._stats.hits += 1
        return entry.value

    def put(self, key: str, value: Any, ttl: float | None = None) -> None:
        effective_ttl = ttl if ttl is not None else self._default_ttl

        # WHY update in place for existing keys? -- Updating an existing
        # key should refresh its TTL and move it to the end, not evict
        # another entry to make room.
        if key in self._store:
            self._store[key] = CacheEntry(
                key=key, value=value,
                created_at=time.monotonic(), ttl_seconds=effective_ttl,
            )
            self._store.move_to_end(key)
            return

        if len(self._store) >= self._capacity:
            self._evict_lru()

        self._store[key] = CacheEntry(
            key=key, value=value,
            created_at=time.monotonic(), ttl_seconds=effective_ttl,
        )

    def invalidate(self, key: str) -> bool:
        if key in self._store:
            self._remove(key)
            return True
        return False

    def clear(self) -> None:
        self._store.clear()

    def keys(self) -> list[str]:
        # WHY prune expired keys here? -- keys() is often called for
        # debugging or warm-up. Cleaning expired entries prevents
        # reporting stale keys that would miss on actual get().
        expired = [k for k, v in self._store.items() if v.is_expired]
        for k in expired:
            self._remove(k)
            self._stats.expirations += 1
        return list(self._store.keys())

    def _evict_lru(self) -> None:
        if not self._store:
            return
        # WHY popitem(last=False)? -- OrderedDict.popitem(last=False)
        # removes the FIRST item, which is the least recently used.
        key, entry = self._store.popitem(last=False)
        self._stats.evictions += 1
        if self._on_evict:
            self._on_evict(key, entry.value)

    def _remove(self, key: str) -> None:
        entry = self._store.pop(key, None)
        if entry and self._on_evict:
            self._on_evict(key, entry.value)


# --- Decorator for transparent caching ----------------------------------

def cached(cache: LRUCache, ttl: float | None = None) -> Callable:
    """WHY a decorator? -- Transparent caching means the caller doesn't
    know or care that results are cached. The decorator intercepts calls,
    builds a cache key from function name + args, and returns cached
    results when available. This is the Proxy pattern."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # WHY repr() for key parts? -- repr() produces unambiguous
            # string representations. str() on a list gives the same
            # output as str() on a tuple, but repr() distinguishes them.
            key_parts = [func.__name__] + [repr(a) for a in args]
            key_parts += [f"{k}={repr(v)}" for k, v in sorted(kwargs.items())]
            cache_key = "|".join(key_parts)

            result = cache.get(cache_key)
            if result is not None:
                return result

            result = func(*args, **kwargs)
            cache.put(cache_key, result, ttl=ttl)
            return result
        wrapper.__wrapped__ = func
        return wrapper
    return decorator


# --- Demo ---------------------------------------------------------------

def simulate_expensive_query(query_id: str, delay: float = 0.01) -> dict[str, Any]:
    time.sleep(delay)
    return {"query_id": query_id, "result": f"data_for_{query_id}", "rows": 42}


def run_demo(cache_size: int = 5, ttl: float = 10.0, queries: list[str] | None = None) -> dict[str, Any]:
    cache = LRUCache(capacity=cache_size, default_ttl=ttl)
    if queries is None:
        queries = ["users", "orders", "users", "products", "users", "orders",
                    "inventory", "reports", "users", "analytics"]
    results: list[dict[str, Any]] = []
    for q in queries:
        cached_result = cache.get(q)
        if cached_result is not None:
            results.append({"query": q, "source": "cache", "data": cached_result})
        else:
            data = simulate_expensive_query(q, delay=0.001)
            cache.put(q, data)
            results.append({"query": q, "source": "computed", "data": data})
    return {
        "queries_executed": len(queries),
        "cache_stats": cache.stats.to_dict(),
        "cache_keys": cache.keys(),
        "results_preview": results[:5],
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="LRU cache with TTL expiration demo")
    parser.add_argument("--capacity", type=int, default=5)
    parser.add_argument("--ttl", type=float, default=10.0)
    parser.add_argument("--queries", nargs="*", default=None)
    args = parser.parse_args(argv)
    output = run_demo(cache_size=args.capacity, ttl=args.ttl, queries=args.queries)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| OrderedDict for LRU ordering | O(1) move_to_end and O(1) popitem give optimal LRU performance | Plain dict + timestamp sorting -- O(n log n) on every eviction |
| Lazy TTL expiration on access | No background threads, no timer complexity | Eager expiration with a background thread -- more accurate but adds threading complexity |
| Eviction callback (`on_evict`) | Allows callers to log, persist, or cascade invalidations when entries are removed | No callback -- simpler but loses observability into cache churn |
| `repr()` for cache key building | Unambiguous string representation prevents key collisions between different types | `str()` -- simpler but `str([1])` and `str((1,))` can collide |

## Alternative approaches

### Approach B: dict with timestamp-based LRU

```python
class SimpleCache:
    def __init__(self, capacity: int):
        self._store: dict[str, tuple[Any, float]] = {}
        self._capacity = capacity

    def get(self, key: str) -> Any | None:
        if key in self._store:
            value, _ = self._store[key]
            self._store[key] = (value, time.monotonic())  # refresh timestamp
            return value
        return None

    def put(self, key: str, value: Any) -> None:
        if len(self._store) >= self._capacity and key not in self._store:
            oldest = min(self._store, key=lambda k: self._store[k][1])
            del self._store[oldest]
        self._store[key] = (value, time.monotonic())
```

**Trade-off:** This approach uses a plain dict and finds the LRU entry by scanning timestamps. It is simpler to understand but eviction is O(n) instead of O(1). Acceptable for small caches (< 100 entries) but becomes a bottleneck at scale.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Cache returns `None` for a legitimately cached `None` value | `get()` returns `None` for both "not found" and "cached None", creating a false miss | Use a sentinel object (`_MISSING = object()`) instead of `None` for cache misses |
| Clock jumps backward (NTP correction) | `time.time()` goes backward, causing entries to appear un-expired | Use `time.monotonic()` which is guaranteed to never go backward |
| Mutable values cached by reference | Caller modifies the returned dict, corrupting the cached copy | Return `copy.deepcopy(entry.value)` from `get()` or document that callers must not mutate |
