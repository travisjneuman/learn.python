"""Tests for Cache Backfill Runner."""

from __future__ import annotations

import json

import pytest

from project import CacheStats, CacheWithBackfill, run


class TestCacheStats:
    def test_miss_rate_empty(self) -> None:
        s = CacheStats()
        assert s.miss_rate == 0.0

    @pytest.mark.parametrize("hits,misses,expected_miss", [
        (8, 2, 0.2),
        (5, 5, 0.5),
        (0, 10, 1.0),
    ])
    def test_miss_rate(self, hits: int, misses: int, expected_miss: float) -> None:
        s = CacheStats(hits=hits, misses=misses)
        assert s.miss_rate == expected_miss


class TestCacheWithBackfill:
    def test_cache_hit(self) -> None:
        cache = CacheWithBackfill({"a": "1"})
        cache.put("a", "1")
        assert cache.get("a") == "1"
        assert cache.stats.hits == 1

    def test_cache_miss_fetches_from_source(self) -> None:
        cache = CacheWithBackfill({"a": "1"})
        val = cache.get("a")
        assert val == "1"
        assert cache.stats.misses == 1

    def test_missing_key_returns_none(self) -> None:
        cache = CacheWithBackfill({})
        assert cache.get("nope") is None

    def test_auto_backfill_on_high_miss_rate(self) -> None:
        source = {f"k{i}": f"v{i}" for i in range(20)}
        cache = CacheWithBackfill(source, miss_threshold=0.5, backfill_batch=5)
        # All misses → should trigger backfill after 3rd lookup
        for i in range(5):
            cache.get(f"k{i}")
        assert cache.stats.backfills >= 1
        assert cache.cache_size > 5  # backfill loaded extra keys

    def test_force_backfill(self) -> None:
        source = {"a": "1", "b": "2", "c": "3"}
        cache = CacheWithBackfill(source)
        loaded = cache.force_backfill()
        assert loaded == 3
        assert cache.cache_size == 3

    def test_summary(self) -> None:
        cache = CacheWithBackfill({"a": "1"})
        cache.get("a")
        s = cache.summary()
        assert s["misses"] == 1
        assert "cache_size" in s

    def test_audit_log(self) -> None:
        source = {f"k{i}": f"v{i}" for i in range(10)}
        cache = CacheWithBackfill(source, miss_threshold=0.3, backfill_batch=5)
        for i in range(5):
            cache.get(f"k{i}")
        assert len(cache.audit_log) >= 1


@pytest.mark.integration
def test_run_end_to_end(tmp_path) -> None:
    config = {
        "source": {"user_1": "Alice", "user_2": "Bob", "user_3": "Carol"},
        "lookups": ["user_1", "user_99", "user_2", "user_1"],
        "miss_threshold": 0.5,
        "backfill_batch": 5,
    }
    inp = tmp_path / "config.json"
    inp.write_text(json.dumps(config), encoding="utf-8")
    out = tmp_path / "out.json"
    summary = run(inp, out)
    assert summary["hits"] >= 1  # user_1 should hit after first miss
    assert len(summary["lookup_results"]) == 4
