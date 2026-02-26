# Solution: Elite Track / Distributed Cache Simulator

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
> [Walkthrough](./WALKTHROUGH.md) for guided hints.

---

## Complete solution

```python
"""Distributed Cache Simulator.

This project is part of the elite extension track.
It intentionally emphasizes explicit, testable engineering decisions.
"""

# WHY simulate distributed caching? -- Real distributed caches (Redis, Memcached)
# introduce network latency and consistency challenges. Simulating cache behavior
# deterministically lets learners study eviction policies, hit rates, and consistency
# models without infrastructure setup.

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse CLI inputs for deterministic project execution."""
    parser = argparse.ArgumentParser(description="Distributed Cache Simulator")
    parser.add_argument("--input", required=True, help="Path to input text data")
    parser.add_argument("--output", required=True, help="Path to output JSON summary")
    parser.add_argument("--run-id", default="manual-run", help="Optional run identifier")
    return parser.parse_args()


def load_lines(input_path: Path) -> list[str]:
    """Load normalized input lines and reject empty datasets safely."""
    if not input_path.exists():
        raise FileNotFoundError(f"input file not found: {input_path}")
    lines = [line.strip() for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise ValueError("input file contains no usable lines")
    return lines


def classify_line(line: str) -> dict[str, Any]:
    """Transform one CSV-like line into structured fields with validation."""
    parts = [piece.strip() for piece in line.split(",")]
    if len(parts) != 3:
        raise ValueError(f"invalid line format (expected 3 comma fields): {line}")

    name, score_raw, severity = parts
    score = int(score_raw)
    return {
        "name": name,
        "score": score,
        "severity": severity,
        "is_high_risk": severity in {"warn", "critical"} or score < 5,
    }


def build_summary(records: list[dict[str, Any]], project_title: str, run_id: str) -> dict[str, Any]:
    """Build deterministic summary payload for testing and teach-back review."""
    high_risk_count = sum(1 for record in records if record["is_high_risk"])
    avg_score = round(sum(record["score"] for record in records) / len(records), 2)

    return {
        "project_title": project_title,
        "run_id": run_id,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "record_count": len(records),
        "high_risk_count": high_risk_count,
        "average_score": avg_score,
        "records": records,
    }


def write_summary(output_path: Path, payload: dict[str, Any]) -> None:
    """Write JSON output with parent directory creation for first-time runs."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    """Execute end-to-end project run."""
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    lines = load_lines(input_path)
    records = [classify_line(line) for line in lines]

    payload = build_summary(records, "Distributed Cache Simulator", args.run_id)
    write_summary(output_path, payload)

    print(f"output_summary.json written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Deterministic simulation over real Redis/Memcached | No infrastructure required; learners study eviction and consistency patterns in pure Python | Real cache integration -- realistic but requires Docker setup and network configuration |
| CSV input as cache access log | Each line represents a cache operation (key, score/latency, severity); simple to generate and modify | Binary protocol simulation -- closer to real caches but harder to inspect and edit |
| Fail-fast on missing files | Cache simulators must load access patterns from files; missing data should halt immediately | Return empty results -- hides configuration errors |
| JSON output for analysis | Cache hit rates and latency distributions are easily computed from the structured output | Console-only output -- not diffable, not suitable for automated analysis |

## Alternative approaches

### Approach B: LRU cache with hit/miss tracking

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._store: OrderedDict[str, Any] = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Any | None:
        if key in self._store:
            self._store.move_to_end(key)
            self.hits += 1
            return self._store[key]
        self.misses += 1
        return None

    def put(self, key: str, value: Any) -> None:
        if key in self._store:
            self._store.move_to_end(key)
        self._store[key] = value
        if len(self._store) > self._capacity:
            self._store.popitem(last=False)  # Evict LRU entry

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
```

**Trade-off:** A full LRU implementation lets learners experiment with cache sizing, eviction policies (LRU vs LFU vs FIFO), and TTL expiration. However, the current scaffold focuses on the data pipeline pattern first. The LRU cache can be added as the "Alter it" enhancement, building on the solid pipeline foundation.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Cache capacity set to zero | Every access is a miss; hit rate is always 0% | Validate capacity > 0 at construction time |
| Same key accessed repeatedly | LRU keeps it at the front; 100% hit rate after the first miss | This is correct behavior; use it to demonstrate cache warming patterns |
| Input file with duplicate entries | Each line is processed independently; duplicates inflate record_count | Add deduplication in build_summary if unique-key semantics are needed |
