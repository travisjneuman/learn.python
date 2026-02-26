# Solution: Level 7 / Project 03 - Unified Cache Writer

> **STOP — Try it yourself first!**
>
> You learn by building, not by reading answers. Spend at least 30 minutes
> attempting this project before looking here.
>
> - Re-read the [README](./README.md) for requirements
> - Try the [WALKTHROUGH](./WALKTHROUGH.md) for guided hints without spoilers

---

## Complete solution

```python
"""Level 7 / Project 03 — Unified Cache Writer.

Writes data to multiple cache backends through a common interface:
in-memory dict, JSON file, and SQLite.
"""

from __future__ import annotations

import argparse
import json
import logging
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Cache backends — three implementations, one interface
# ---------------------------------------------------------------------------

# WHY three separate backends behind one interface? -- This is the Strategy
# pattern.  Each backend has different trade-offs (speed vs persistence vs
# capacity), but callers use the same get/set/delete API.  Swapping backends
# requires zero changes to calling code.

class MemoryCache:
    """Fast in-memory cache using a plain dict."""

    def __init__(self) -> None:
        self._store: dict[str, str] = {}
        # WHY track hits/misses? -- Cache hit rate is the primary metric for
        # deciding whether the cache is effective or needs tuning.
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
        # WHY return bool? -- Tells the caller whether the key existed,
        # useful for idempotency checks.
        return self._store.pop(key, None) is not None

    def clear(self) -> None:
        self._store.clear()

    def stats(self) -> dict:
        return {"backend": "memory", "size": len(self._store),
                "hits": self._hits, "misses": self._misses}


class FileCache:
    """JSON-file-backed cache.  Persistent but slower."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._hits = 0
        self._misses = 0
        self._store = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            return json.loads(self.path.read_text(encoding="utf-8"))
        return {}

    # WHY save after every write? -- File cache trades speed for durability.
    # Every set/delete flushes to disk so data survives process crashes.
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
    """SQLite-backed cache.  Persistent and queryable."""

    def __init__(self, db_path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(db_path)
        # WHY CREATE TABLE IF NOT EXISTS? -- Makes the cache safe to
        # initialize multiple times without crashing on an existing table.
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS cache "
            "(key TEXT PRIMARY KEY, value TEXT NOT NULL)"
        )
        self._conn.commit()
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> str | None:
        # WHY parameterized query (?)? -- Prevents SQL injection even
        # though this is a local cache.  Good habit for any SQL code.
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

# WHY a factory function? -- Callers specify a backend name ("memory",
# "file", "sqlite") and get back the right implementation.  The factory
# hides construction details (file paths, DB connections) from callers.
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

    # WHY close only if the method exists? -- MemoryCache and FileCache do
    # not need explicit cleanup, but SqliteCache holds a DB connection that
    # should be closed to release the file lock.
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Strategy pattern (three classes, one interface) | Swap backends without changing calling code; easy to add Redis, Memcached later | Single class with `if backend == ...` branches -- violates open/closed principle |
| Factory function `create_cache()` | Hides construction details (paths, connections) from callers | Direct instantiation -- forces callers to know about each backend's constructor |
| `FileCache` flushes on every write | Trades speed for durability; data survives crashes | Batch flush -- faster but risks data loss on unexpected exit |
| `hasattr(cache, "close")` instead of Protocol | Pragmatic duck typing; avoids requiring all backends to implement a no-op close | Abstract base class with `close()` on all backends -- cleaner but adds boilerplate |

## Alternative approaches

### Approach B: Abstract base class with Protocol

```python
from typing import Protocol

class CacheBackend(Protocol):
    def get(self, key: str) -> str | None: ...
    def set(self, key: str, value: str) -> None: ...
    def delete(self, key: str) -> bool: ...
    def clear(self) -> None: ...
    def stats(self) -> dict: ...
```

**Trade-off:** A Protocol provides static type checking -- mypy will catch missing methods at lint time. The current duck-typing approach is simpler but relies on runtime checks. Use Protocol when the codebase has strict type checking enabled.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| FileCache path does not exist and parent directory is missing | `FileNotFoundError` when writing | `_save()` creates parent dirs with `mkdir(parents=True)` |
| Two processes write to the same SQLite file simultaneously | `sqlite3.OperationalError: database is locked` | Use WAL mode (`PRAGMA journal_mode=WAL`) or switch to a server-based DB |
| Records lack a `"key"` field | All records map to empty string key, overwriting each other | Validate or generate keys before writing (e.g. hash the record content) |
