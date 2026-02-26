# Solution: Level 7 / Project 14 - Cache Backfill Runner

> **STOP — Try it yourself first!**
>
> You learn by building, not by reading answers. Spend at least 30 minutes
> attempting this project before looking here.
>
> - Re-read the [README](./README.md) for requirements
> 
---

## Complete solution

```python
"""Level 7 / Project 14 — Cache Backfill Runner.

When cache miss rates exceed a threshold, triggers a backfill from
the authoritative data source.  Tracks hit/miss counters and decides
when to backfill automatically.
"""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path


# -- Data model ----------------------------------------------------------

@dataclass
class CacheStats:
    hits: int = 0
    misses: int = 0
    backfills: int = 0

    @property
    def total(self) -> int:
        return self.hits + self.misses

    @property
    def miss_rate(self) -> float:
        # WHY guard against zero total? -- On first access, total is 0.
        # Dividing by zero would crash; returning 0.0 is semantically
        # correct (no requests = no misses).
        return round(self.misses / self.total, 4) if self.total else 0.0

    @property
    def hit_rate(self) -> float:
        return round(self.hits / self.total, 4) if self.total else 0.0


# -- Core logic ----------------------------------------------------------

# WHY automatic backfill? -- When cache miss rate exceeds a threshold, it
# means most requests are hitting the slow source anyway.  Proactively
# loading a batch of source data into cache reduces future misses.  The
# threshold prevents premature backfills during cold-start (when misses
# are expected).
class CacheWithBackfill:
    """Simple cache that auto-backfills from a source when miss rate is high."""

    def __init__(
        self,
        source: dict[str, str],
        miss_threshold: float = 0.5,
        backfill_batch: int = 10,
    ) -> None:
        self._cache: dict[str, str] = {}
        self._source = source
        self.miss_threshold = miss_threshold
        self.backfill_batch = backfill_batch
        self.stats = CacheStats()
        self._audit: list[dict] = []

    def get(self, key: str) -> str | None:
        """Look up a key.  Records hit/miss and may trigger backfill."""
        if key in self._cache:
            self.stats.hits += 1
            return self._cache[key]

        self.stats.misses += 1
        logging.info("cache miss key=%s miss_rate=%.2f", key, self.stats.miss_rate)

        # WHY require total >= 3 before checking miss_rate? -- During
        # cold-start, the first few requests are always misses (100% miss
        # rate).  Waiting for at least 3 lookups prevents premature backfills
        # when the cache is just warming up.
        if self.stats.total >= 3 and self.stats.miss_rate >= self.miss_threshold:
            self._backfill()

        # WHY try source directly for the missed key? -- Even if a batch
        # backfill did not include this specific key (e.g. batch was full),
        # we should still return the correct value to the caller.
        if key in self._source:
            val = self._source[key]
            self._cache[key] = val
            return val
        return None

    def put(self, key: str, value: str) -> None:
        self._cache[key] = value

    def _backfill(self) -> None:
        """Load a batch of keys from source into cache."""
        loaded = 0
        for k, v in self._source.items():
            if k not in self._cache:
                self._cache[k] = v
                loaded += 1
                # WHY cap at backfill_batch? -- Loading the entire source
                # at once could be expensive (large dataset, slow source).
                # Batch limiting spreads the cost across multiple backfills.
                if loaded >= self.backfill_batch:
                    break
        self.stats.backfills += 1
        self._audit.append({"action": "backfill", "loaded": loaded})
        logging.info("backfill completed: loaded %d keys", loaded)

    def force_backfill(self) -> int:
        """Manually trigger a full backfill (loads everything)."""
        loaded = 0
        for k, v in self._source.items():
            if k not in self._cache:
                self._cache[k] = v
                loaded += 1
        self.stats.backfills += 1
        self._audit.append({"action": "force_backfill", "loaded": loaded})
        return loaded

    @property
    def cache_size(self) -> int:
        return len(self._cache)

    @property
    def audit_log(self) -> list[dict]:
        return list(self._audit)

    def summary(self) -> dict:
        return {
            "cache_size": self.cache_size,
            "hits": self.stats.hits,
            "misses": self.stats.misses,
            "hit_rate": self.stats.hit_rate,
            "miss_rate": self.stats.miss_rate,
            "backfills": self.stats.backfills,
        }


# -- Entry points --------------------------------------------------------

def run(input_path: Path, output_path: Path) -> dict:
    config = json.loads(input_path.read_text(encoding="utf-8")) if input_path.exists() else {}

    source = config.get("source", {})
    lookups = config.get("lookups", [])
    threshold = config.get("miss_threshold", 0.5)
    batch = config.get("backfill_batch", 10)

    cache = CacheWithBackfill(source, miss_threshold=threshold, backfill_batch=batch)

    results: list[dict] = []
    for key in lookups:
        val = cache.get(key)
        results.append({"key": key, "value": val, "found": val is not None})

    summary = cache.summary()
    summary["lookup_results"] = results

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cache Backfill Runner")
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
| Threshold-based automatic backfill | Balances between hammering the source (too eager) and serving stale/missing data (too lazy) | Time-based backfill (every N seconds) -- does not respond to actual miss patterns; wastes resources during quiet periods |
| Minimum 3 lookups before evaluating miss rate | Prevents premature backfills during cold-start when miss rate is naturally 100% | No minimum -- first miss at 100% rate triggers immediate backfill before cache has a chance to warm |
| Batch-limited backfill | Spreads cost across multiple trigger events; avoids loading entire source in one expensive operation | Full backfill on every trigger -- simpler but could block the caller for a long time with large sources |
| Direct source lookup after backfill miss | Ensures the caller always gets the correct value even if batch did not include their key | Return None and let caller retry -- worse UX; caller has to handle retry logic |

## Alternative approaches

### Approach B: LRU eviction with backfill on capacity

```python
from collections import OrderedDict

class LRUCacheWithBackfill:
    def __init__(self, source, capacity=100):
        self._cache = OrderedDict()
        self._source = source
        self._capacity = capacity

    def get(self, key):
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        val = self._source.get(key)
        if val:
            if len(self._cache) >= self._capacity:
                self._cache.popitem(last=False)  # evict LRU
            self._cache[key] = val
        return val
```

**Trade-off:** LRU eviction keeps the cache bounded in size, which is critical for memory-constrained environments. But it does not proactively backfill -- it only caches on demand. Combining LRU eviction with threshold-based backfill gives the best of both worlds.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| `miss_threshold` set to 0.0 | Every single miss triggers a backfill (cache thrashing) | Validate that `miss_threshold` is between 0.01 and 1.0 |
| Source dict is empty | Backfills load zero keys; miss rate stays high; repeated fruitless backfills | Skip backfill when `len(self._source) == 0` |
| Lookups request keys not in the source | `get` returns None; miss counter increments; may trigger unnecessary backfills | Track "source misses" separately from "cache misses" to distinguish the two |
