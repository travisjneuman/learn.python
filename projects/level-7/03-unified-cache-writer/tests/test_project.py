"""Tests for Unified Cache Writer."""

from __future__ import annotations

import json

import pytest

from project import FileCache, MemoryCache, SqliteCache, run, write_to_caches


class TestMemoryCache:
    def test_set_and_get(self) -> None:
        c = MemoryCache()
        c.set("k1", "v1")
        assert c.get("k1") == "v1"

    def test_miss_returns_none(self) -> None:
        c = MemoryCache()
        assert c.get("nope") is None

    def test_delete(self) -> None:
        c = MemoryCache()
        c.set("k", "v")
        assert c.delete("k") is True
        assert c.get("k") is None

    def test_stats(self) -> None:
        c = MemoryCache()
        c.set("a", "1")
        c.get("a")
        c.get("b")
        stats = c.stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 1


class TestFileCache:
    def test_persistence(self, tmp_path) -> None:
        path = tmp_path / "cache.json"
        c1 = FileCache(path)
        c1.set("k", "v")
        c2 = FileCache(path)
        assert c2.get("k") == "v"


class TestSqliteCache:
    def test_set_get_delete(self) -> None:
        c = SqliteCache()
        c.set("k", "v")
        assert c.get("k") == "v"
        c.delete("k")
        assert c.get("k") is None
        c.close()

    @pytest.mark.parametrize("n", [0, 1, 10])
    def test_stats_count(self, n: int) -> None:
        c = SqliteCache()
        for i in range(n):
            c.set(f"k{i}", f"v{i}")
        assert c.stats()["size"] == n
        c.close()


class TestWriteToCaches:
    def test_writes_to_memory(self) -> None:
        records = [{"key": "a", "val": 1}, {"key": "b", "val": 2}]
        result = write_to_caches(records, ["memory"])
        assert result.written == 2


@pytest.mark.integration
def test_run_end_to_end(tmp_path) -> None:
    config = {
        "records": [{"key": "x", "data": "hello"}],
        "backends": ["memory"],
    }
    inp = tmp_path / "config.json"
    inp.write_text(json.dumps(config), encoding="utf-8")
    out = tmp_path / "out.json"

    summary = run(inp, out)
    assert summary["records_written"] == 1
