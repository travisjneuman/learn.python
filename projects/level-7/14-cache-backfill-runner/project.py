"""Level 7 / Project 14 — Cache Backfill Runner.

When cache miss rates exceed a threshold, triggers a backfill from
the authoritative data source.  Tracks hit/miss counters and decides
when to backfill automatically.

Key concepts:
- Cache hit/miss ratio tracking
- Threshold-triggered backfill
- Batch loading from source into cache
- Backfill audit and statistics
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
        return round(self.misses / self.total, 4) if self.total else 0.0

    @property
    def hit_rate(self) -> float:
        return round(self.hits / self.total, 4) if self.total else 0.0


# -- Core logic ----------------------------------------------------------

# WHY automatic backfill? -- When cache miss rate exceeds a threshold, it
# means most requests are hitting the slow source anyway. Proactively loading
# a batch of source data into cache reduces future misses. The threshold
# prevents premature backfills during cold-start (when misses are expected).
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

        # Check if backfill needed
        if self.stats.total >= 3 and self.stats.miss_rate >= self.miss_threshold:
            self._backfill()

        # Try source directly for the requested key
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
                if loaded >= self.backfill_batch:
                    break
        self.stats.backfills += 1
        self._audit.append({"action": "backfill", "loaded": loaded})
        logging.info("backfill completed: loaded %d keys", loaded)

    def force_backfill(self) -> int:
        """Manually trigger a full backfill."""
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
