"""Tests for Query Cache Layer.

Covers: LRU eviction, TTL expiration, statistics, decorator, and edge cases.
"""

from __future__ import annotations

import time
from typing import Any

import pytest

from project import CacheStats, LRUCache, cached


# --- Fixtures -----------------------------------------------------------

@pytest.fixture
def small_cache() -> LRUCache:
    """A cache with capacity 3 for easy eviction testing."""
    return LRUCache(capacity=3, default_ttl=60.0)


# --- CacheStats ---------------------------------------------------------

class TestCacheStats:
    def test_hit_rate_with_no_requests(self) -> None:
        stats = CacheStats()
        assert stats.hit_rate == 0.0

    @pytest.mark.parametrize("hits,misses,expected_rate", [
        (1, 0, 100.0),
        (3, 1, 75.0),
        (0, 5, 0.0),
        (1, 1, 50.0),
    ])
    def test_hit_rate_calculation(self, hits: int, misses: int, expected_rate: float) -> None:
        stats = CacheStats(hits=hits, misses=misses)
        assert stats.hit_rate == expected_rate


# --- LRU eviction -------------------------------------------------------

class TestLRUEviction:
    def test_evicts_oldest_when_full(self, small_cache: LRUCache) -> None:
        small_cache.put("a", 1)
        small_cache.put("b", 2)
        small_cache.put("c", 3)
        small_cache.put("d", 4)  # should evict "a"
        assert small_cache.get("a") is None
        assert small_cache.get("d") == 4
        assert small_cache.stats.evictions == 1

    def test_access_refreshes_lru_order(self, small_cache: LRUCache) -> None:
        small_cache.put("a", 1)
        small_cache.put("b", 2)
        small_cache.put("c", 3)
        small_cache.get("a")  # refresh "a" — now "b" is oldest
        small_cache.put("d", 4)  # should evict "b"
        assert small_cache.get("b") is None
        assert small_cache.get("a") == 1

    def test_capacity_validation(self) -> None:
        with pytest.raises(ValueError, match="at least 1"):
            LRUCache(capacity=0)


# --- TTL expiration -----------------------------------------------------

class TestTTLExpiration:
    def test_expired_entry_returns_none(self) -> None:
        cache = LRUCache(capacity=10, default_ttl=0.05)
        cache.put("key", "value")
        assert cache.get("key") == "value"
        time.sleep(0.06)
        assert cache.get("key") is None
        assert cache.stats.expirations == 1

    def test_custom_ttl_per_entry(self) -> None:
        cache = LRUCache(capacity=10, default_ttl=60.0)
        cache.put("short", "val", ttl=0.05)
        cache.put("long", "val", ttl=60.0)
        time.sleep(0.06)
        assert cache.get("short") is None
        assert cache.get("long") == "val"


# --- Invalidation and clear ---------------------------------------------

class TestInvalidation:
    def test_invalidate_existing_key(self, small_cache: LRUCache) -> None:
        small_cache.put("x", 10)
        assert small_cache.invalidate("x") is True
        assert small_cache.get("x") is None

    def test_invalidate_missing_key(self, small_cache: LRUCache) -> None:
        assert small_cache.invalidate("nope") is False

    def test_clear_empties_cache(self, small_cache: LRUCache) -> None:
        small_cache.put("a", 1)
        small_cache.put("b", 2)
        small_cache.clear()
        assert small_cache.size == 0


# --- Decorator ----------------------------------------------------------

class TestCachedDecorator:
    def test_decorator_caches_results(self) -> None:
        cache = LRUCache(capacity=10, default_ttl=60.0)
        call_count = 0

        @cached(cache)
        def expensive(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        assert expensive(5) == 10
        assert expensive(5) == 10  # should hit cache
        assert call_count == 1
        assert cache.stats.hits == 1


# --- Eviction callback --------------------------------------------------

class TestEvictionCallback:
    def test_on_evict_called(self) -> None:
        evicted: list[tuple[str, Any]] = []
        cache = LRUCache(
            capacity=2, default_ttl=60.0,
            on_evict=lambda k, v: evicted.append((k, v)),
        )
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)  # evicts "a"
        assert len(evicted) == 1
        assert evicted[0] == ("a", 1)
