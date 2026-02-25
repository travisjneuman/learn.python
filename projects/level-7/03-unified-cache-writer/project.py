"""Level 7 / Project 03 — Unified Cache Writer.

Writes data to multiple cache backends through a common interface:
in-memory dict, JSON file, and SQLite.

Key concepts:
- Strategy pattern: swap backends without changing calling code
- Protocol / duck typing for cache interface
- Cache operations: get, set, delete, clear, stats
- Backend comparison: speed vs persistence vs capacity
"""

from __future__ import annotations

import argparse
import json
import logging
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Cache backends
# ---------------------------------------------------------------------------


class MemoryCache:
    """Fast in-memory cache using a plain dict."""

    def __init__(self) -> None:
        self._store: dict[str, str] = {}
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> str | None:
        val = self._store.get(key)
        if val is not None:
            self._hits += 1
        else:
            self._misses += 1
        return val

    def set(self, key: str, value: str) -> None:
        self._store[key] = value

    def delete(self, key: str) -> bool:
        return self._store.pop(key, None) is not None

    def clear(self) -> None:
        self._store.clear()

    def stats(self) -> dict:
        return {"backend": "memory", "size": len(self._store),
                "hits": self._hits, "misses": self._misses}


class FileCache:
    """JSON-file-backed cache. Persistent but slower."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._hits = 0
        self._misses = 0
        self._store = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            return json.loads(self.path.read_text(encoding="utf-8"))
        return {}

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._store), encoding="utf-8")

    def get(self, key: str) -> str | None:
        val = self._store.get(key)
        if val is not None:
            self._hits += 1
        else:
            self._misses += 1
        return val

    def set(self, key: str, value: str) -> None:
        self._store[key] = value
        self._save()

    def delete(self, key: str) -> bool:
        removed = self._store.pop(key, None) is not None
        if removed:
            self._save()
        return removed

    def clear(self) -> None:
        self._store.clear()
        self._save()

    def stats(self) -> dict:
        return {"backend": "file", "size": len(self._store),
                "hits": self._hits, "misses": self._misses}


class SqliteCache:
    """SQLite-backed cache. Persistent and queryable."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(db_path)
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS cache "
            "(key TEXT PRIMARY KEY, value TEXT NOT NULL)"
        )
        self._conn.commit()
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> str | None:
        row = self._conn.execute(
            "SELECT value FROM cache WHERE key = ?", (key,)
        ).fetchone()
        if row:
            self._hits += 1
            return row[0]
        self._misses += 1
        return None

    def set(self, key: str, value: str) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO cache (key, value) VALUES (?, ?)",
            (key, value),
        )
        self._conn.commit()

    def delete(self, key: str) -> bool:
        cur = self._conn.execute("DELETE FROM cache WHERE key = ?", (key,))
        self._conn.commit()
        return cur.rowcount > 0

    def clear(self) -> None:
        self._conn.execute("DELETE FROM cache")
        self._conn.commit()

    def stats(self) -> dict:
        count = self._conn.execute("SELECT COUNT(*) FROM cache").fetchone()[0]
        return {"backend": "sqlite", "size": count,
                "hits": self._hits, "misses": self._misses}

    def close(self) -> None:
        self._conn.close()


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------


def create_cache(backend: str, path: Path | None = None):
    if backend == "memory":
        return MemoryCache()
    elif backend == "file":
        return FileCache(path or Path("data/cache.json"))
    elif backend == "sqlite":
        return SqliteCache(str(path) if path else ":memory:")
    raise ValueError(f"Unknown backend: {backend}")


# ---------------------------------------------------------------------------
# Writer
# ---------------------------------------------------------------------------


@dataclass
class WriteResult:
    written: int = 0
    backends_used: list[str] = field(default_factory=list)


def write_to_caches(
    records: list[dict],
    backends: list[str],
    base_path: Path | None = None,
) -> WriteResult:
    """Write all records to each specified backend."""
    result = WriteResult()
    caches = []

    for b in backends:
        bp = (base_path / f"cache_{b}.json") if base_path and b == "file" else None
        caches.append((b, create_cache(b, bp)))
        result.backends_used.append(b)

    for rec in records:
        key = rec.get("key", "")
        value = json.dumps(rec)
        for _, cache in caches:
            cache.set(key, value)
        result.written += 1

    for _, cache in caches:
        if hasattr(cache, "close"):
            cache.close()

    return result


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run(input_path: Path, output_path: Path) -> dict:
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    config = json.loads(input_path.read_text(encoding="utf-8"))
    records = config.get("records", [])
    backends = config.get("backends", ["memory"])

    result = write_to_caches(records, backends, output_path.parent)

    summary = {
        "records_written": result.written,
        "backends_used": result.backends_used,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info("wrote %d records to %d backends", result.written, len(result.backends_used))
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Unified Cache Writer — multi-backend caching")
    parser.add_argument("--input", default="data/sample_input.json")
    parser.add_argument("--output", default="data/output_summary.json")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    args = parse_args()
    summary = run(Path(args.input), Path(args.output))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
