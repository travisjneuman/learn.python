"""Query Cache Layer — LRU cache with TTL expiration for expensive computations.

Design rationale:
    Caching is fundamental to performance-sensitive systems. This project
    implements a from-scratch LRU cache with time-to-live expiration,
    hit/miss statistics, and eviction callbacks — teaching how caches work
    beneath abstractions like functools.lru_cache or Redis.

Concepts practised:
    - OrderedDict for LRU ordering
    - time-based expiration (TTL)
    - dataclasses for cache entries and statistics
    - decorator pattern for transparent caching
    - cache invalidation strategies
"""

from __future__ import annotations

import argparse
import json
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Callable


# --- Domain types -------------------------------------------------------

# WHY build an LRU cache from scratch? -- functools.lru_cache doesn't support
# TTL expiration or eviction callbacks. Understanding OrderedDict-based LRU
# internals prepares you for tuning production caches (Redis, Memcached)
# where eviction policy, TTL, and hit-rate monitoring all matter.
@dataclass
class CacheEntry:
    """A single cached value with metadata."""
    key: str
    value: Any
    created_at: float
    ttl_seconds: float
    access_count: int = 0

    @property
    def is_expired(self) -> bool:
        """Check if entry has exceeded its TTL."""
        # WHY monotonic() instead of time()? -- time.time() can jump backwards
        # (NTP adjustments, daylight saving). monotonic() only moves forward,
        # preventing false expirations.
        return (time.monotonic() - self.created_at) > self.ttl_seconds


@dataclass
class CacheStats:
    """Accumulated cache performance statistics."""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0

    @property
    def total_requests(self) -> int:
        return self.hits + self.misses

    @property
    def hit_rate(self) -> float:
        """Return hit rate as a percentage, 0.0 if no requests yet."""
        if self.total_requests == 0:
            return 0.0
        return round(self.hits / self.total_requests * 100, 2)

    def to_dict(self) -> dict[str, Any]:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "expirations": self.expirations,
            "total_requests": self.total_requests,
            "hit_rate_pct": self.hit_rate,
        }


# --- LRU Cache implementation -------------------------------------------

class LRUCache:
    """Least-Recently-Used cache with TTL expiration.

    When capacity is reached, the least-recently-accessed entry is evicted.
    Entries that exceed their TTL are lazily expired on access.
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
        """Retrieve a value by key, returning None on miss or expiration."""
        if key not in self._store:
            self._stats.misses += 1
            return None

        entry = self._store[key]

        # Lazy expiration: check TTL on access
        if entry.is_expired:
            self._remove(key)
            self._stats.expirations += 1
            self._stats.misses += 1
            return None

        # Move to end (most recently used)
        self._store.move_to_end(key)
        entry.access_count += 1
        self._stats.hits += 1
        return entry.value

    def put(self, key: str, value: Any, ttl: float | None = None) -> None:
        """Insert or update a cache entry."""
        effective_ttl = ttl if ttl is not None else self._default_ttl

        # Update existing key — move to end
        if key in self._store:
            self._store[key] = CacheEntry(
                key=key, value=value,
                created_at=time.monotonic(), ttl_seconds=effective_ttl,
            )
            self._store.move_to_end(key)
            return

        # Evict LRU if at capacity
        if len(self._store) >= self._capacity:
            self._evict_lru()

        self._store[key] = CacheEntry(
            key=key, value=value,
            created_at=time.monotonic(), ttl_seconds=effective_ttl,
        )

    def invalidate(self, key: str) -> bool:
        """Remove a specific key. Returns True if key existed."""
        if key in self._store:
            self._remove(key)
            return True
        return False

    def clear(self) -> None:
        """Remove all entries from the cache."""
        self._store.clear()

    def keys(self) -> list[str]:
        """Return all non-expired keys in LRU order (oldest first)."""
        expired = [k for k, v in self._store.items() if v.is_expired]
        for k in expired:
            self._remove(k)
            self._stats.expirations += 1
        return list(self._store.keys())

    def _evict_lru(self) -> None:
        """Remove the least-recently-used entry."""
        if not self._store:
            return
        key, entry = self._store.popitem(last=False)
        self._stats.evictions += 1
        if self._on_evict:
            self._on_evict(key, entry.value)

    def _remove(self, key: str) -> None:
        """Remove an entry by key."""
        entry = self._store.pop(key, None)
        if entry and self._on_evict:
            self._on_evict(key, entry.value)


# --- Decorator for transparent caching ----------------------------------

def cached(cache: LRUCache, ttl: float | None = None) -> Callable:
    """Decorator that transparently caches function results.

    The cache key is built from the function name and its arguments.
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key_parts = [func.__name__] + [repr(a) for a in args]
            key_parts += [f"{k}={repr(v)}" for k, v in sorted(kwargs.items())]
            cache_key = "|".join(key_parts)

            result = cache.get(cache_key)
            if result is not None:
                return result

            result = func(*args, **kwargs)
            cache.put(cache_key, result, ttl=ttl)
            return result
        wrapper.__wrapped__ = func  # type: ignore[attr-defined]
        return wrapper
    return decorator


# --- Demo: simulate expensive queries -----------------------------------

def simulate_expensive_query(query_id: str, delay: float = 0.01) -> dict[str, Any]:
    """Simulate a slow database or API query."""
    time.sleep(delay)
    return {"query_id": query_id, "result": f"data_for_{query_id}", "rows": 42}


def run_demo(cache_size: int = 5, ttl: float = 10.0, queries: list[str] | None = None) -> dict[str, Any]:
    """Run a demonstration of the cache with repeated queries."""
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


# --- CLI ----------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LRU cache with TTL expiration demo")
    parser.add_argument("--capacity", type=int, default=5, help="Max cache entries")
    parser.add_argument("--ttl", type=float, default=10.0, help="Default TTL in seconds")
    parser.add_argument("--queries", nargs="*", default=None, help="Query IDs to run")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    output = run_demo(cache_size=args.capacity, ttl=args.ttl, queries=args.queries)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
