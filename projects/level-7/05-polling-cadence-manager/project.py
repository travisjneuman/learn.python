"""Level 7 / Project 05 — Polling Cadence Manager.

Implements adaptive polling intervals that speed up when data changes
frequently and slow down during quiet periods.

Key concepts:
- Adaptive polling: adjust interval based on change rate
- Exponential backoff for idle periods
- Minimum/maximum interval bounds
- Change detection via hash comparison
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
# and misses changes during busy ones. Adaptive intervals use backoff (slow
# down when idle) and speedup (accelerate when changes detected), bounded by
# min/max to prevent both runaway polling and excessive staleness.
@dataclass
class PollConfig:
    min_interval: float = 1.0
    max_interval: float = 60.0
    backoff_factor: float = 1.5    # multiply interval when no change (slow down)
    speedup_factor: float = 0.5    # multiply interval when change found (speed up)


@dataclass
class PollState:
    current_interval: float = 5.0
    last_hash: str = ""
    polls_done: int = 0
    changes_detected: int = 0
    history: list[dict] = field(default_factory=list)


def compute_hash(data: str) -> str:
    return hashlib.md5(data.encode("utf-8")).hexdigest()


def poll_once(state: PollState, data: str, config: PollConfig) -> bool:
    """Simulate a single poll. Returns True if data changed."""
    new_hash = compute_hash(data)
    changed = new_hash != state.last_hash and state.last_hash != ""

    if changed:
        state.changes_detected += 1
        state.current_interval = max(
            config.min_interval,
            state.current_interval * config.speedup_factor,
        )
        logging.info("change detected, interval=%.1f", state.current_interval)
    else:
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
