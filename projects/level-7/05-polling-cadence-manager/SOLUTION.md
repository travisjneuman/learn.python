# Solution: Level 7 / Project 05 - Polling Cadence Manager

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
"""Level 7 / Project 05 — Polling Cadence Manager.

Implements adaptive polling intervals that speed up when data changes
frequently and slow down during quiet periods.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path


# WHY adaptive polling? -- Fixed polling wastes resources during quiet periods
# and misses changes during busy ones.  Adaptive intervals use backoff (slow
# down when idle) and speedup (accelerate when changes detected), bounded by
# min/max to prevent both runaway polling and excessive staleness.
@dataclass
class PollConfig:
    min_interval: float = 1.0
    max_interval: float = 60.0
    backoff_factor: float = 1.5    # multiply interval when no change
    speedup_factor: float = 0.5    # multiply interval when change found


@dataclass
class PollState:
    current_interval: float = 5.0
    last_hash: str = ""
    polls_done: int = 0
    changes_detected: int = 0
    history: list[dict] = field(default_factory=list)


# WHY MD5 for change detection? -- We only need to detect whether data
# changed, not secure it.  MD5 is fast and sufficient for comparing
# snapshots.  Any collision would just mean a missed change, not a
# security vulnerability.
def compute_hash(data: str) -> str:
    return hashlib.md5(data.encode("utf-8")).hexdigest()


def poll_once(state: PollState, data: str, config: PollConfig) -> bool:
    """Simulate a single poll.  Returns True if data changed."""
    new_hash = compute_hash(data)
    # WHY check last_hash != ""? -- On the very first poll there is no
    # previous hash to compare against.  Treating the first poll as
    # "no change" avoids a false positive that would immediately speed up.
    changed = new_hash != state.last_hash and state.last_hash != ""

    if changed:
        state.changes_detected += 1
        # WHY max(min_interval, ...)? -- Speedup multiplies the interval
        # down, but we must never go below min_interval to avoid hammering
        # the data source with sub-second polls.
        state.current_interval = max(
            config.min_interval,
            state.current_interval * config.speedup_factor,
        )
        logging.info("change detected, interval=%.1f", state.current_interval)
    else:
        # WHY min(max_interval, ...)? -- Backoff multiplies the interval
        # up, but capping at max_interval prevents the poll from becoming
        # so infrequent that stale data goes undetected.
        state.current_interval = min(
            config.max_interval,
            state.current_interval * config.backoff_factor,
        )

    state.last_hash = new_hash
    state.polls_done += 1
    state.history.append({
        "poll": state.polls_done,
        "changed": changed,
        "interval": round(state.current_interval, 2),
        "hash": new_hash[:8],
    })
    return changed


def simulate_polling(data_snapshots: list[str], config: PollConfig | None = None) -> PollState:
    """Run through a list of data snapshots, adjusting cadence."""
    config = config or PollConfig()
    state = PollState(current_interval=config.min_interval * 2)

    for snapshot in data_snapshots:
        poll_once(state, snapshot, config)

    return state


def run(input_path: Path, output_path: Path) -> dict:
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")
    config_data = json.loads(input_path.read_text(encoding="utf-8"))
    snapshots = config_data.get("snapshots", [])
    # WHY **config_data.get(...)? -- Unpacking the config dict into PollConfig
    # keyword args lets the JSON file override any default without code changes.
    poll_cfg = PollConfig(**config_data.get("config", {}))

    state = simulate_polling(snapshots, poll_cfg)

    summary = {
        "polls": state.polls_done,
        "changes": state.changes_detected,
        "final_interval": round(state.current_interval, 2),
        "history": state.history,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Polling Cadence Manager")
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
| Hash-based change detection | Comparing hashes is O(1) regardless of data size; works for any serializable data | Field-by-field diff -- more granular but requires knowing the schema |
| Multiplicative backoff/speedup | Exponential curves are the standard for adaptive intervals (used in TCP, HTTP retries, etc.) | Additive step (add/subtract fixed seconds) -- slower to adapt to sustained quiet or busy periods |
| `min_interval` / `max_interval` bounds | Prevents runaway polling (too fast) or excessive staleness (too slow) | Unbounded -- dangerous; a backoff_factor > 1 with no cap grows forever |
| History list in `PollState` | Makes the simulation inspectable and testable; useful for visualizing cadence over time | Only track final state -- simpler but loses observability into how cadence evolved |

## Alternative approaches

### Approach B: Moving-average change rate

```python
def adaptive_interval(change_rate: float, base: float = 5.0) -> float:
    """Interval inversely proportional to recent change rate."""
    if change_rate > 0.8:
        return max(1.0, base * 0.25)    # very active
    elif change_rate > 0.3:
        return base                       # moderate
    else:
        return min(60.0, base * 3.0)     # quiet
```

**Trade-off:** A moving-average approach smooths out spiky change patterns, preventing the interval from oscillating between extremes. But it requires a window of recent polls to compute the average, making it slower to react to sudden bursts.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| `backoff_factor` set to 0 or negative | Interval collapses to 0 or goes negative, causing infinite/impossible polling | Validate `backoff_factor > 1.0` in the constructor |
| `min_interval > max_interval` | Bounds contradict each other; `max()` and `min()` clamp to nonsensical values | Raise `ValueError` if `min_interval >= max_interval` during config parsing |
| All snapshots are identical | Interval keeps backing off to max; no changes ever detected | Expected behavior, but log a notice if zero changes are detected across all polls |
