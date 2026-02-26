# Checkpoint Recovery Tool — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Level 4 / Project 12 — Checkpoint Recovery Tool.

Processes items in a list, saving checkpoints after each batch.
If the process crashes and restarts, it resumes from the last
checkpoint instead of reprocessing everything from scratch.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

# ---------- logging ----------

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

# ---------- checkpoint management ----------


def load_checkpoint(checkpoint_path: Path) -> dict:
    """Load the last saved checkpoint.

    Returns a dict with:
    - last_processed_index: int (0-based, -1 if no checkpoint)
    - results: list of previously processed results
    """
    if not checkpoint_path.exists():
        return {"last_processed_index": -1, "results": []}

    try:
        data = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        return {
            "last_processed_index": data.get("last_processed_index", -1),
            "results": data.get("results", []),
        }
    except (json.JSONDecodeError, KeyError):
        # WHY: A corrupt checkpoint file should not crash the entire run.
        # Starting fresh is safer than trying to parse broken JSON — you
        # lose some progress but the run will complete correctly.
        logging.warning("Corrupt checkpoint file — starting fresh")
        return {"last_processed_index": -1, "results": []}


def save_checkpoint(checkpoint_path: Path, index: int, results: list[dict]) -> None:
    """Persist current progress to a checkpoint file.

    WHY write-then-rename (atomic write pattern)? If the process crashes
    mid-write, a partially written checkpoint would corrupt recovery.
    Writing to a .tmp file first and then atomically replacing the real
    checkpoint ensures we always have a complete, valid checkpoint.
    """
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = checkpoint_path.with_suffix(".tmp")
    temp_path.write_text(
        json.dumps({"last_processed_index": index, "results": results}, indent=2),
        encoding="utf-8",
    )
    # WHY: Path.replace() is atomic on most filesystems — the old file is
    # swapped for the new one in a single operation. This prevents the
    # window where no valid checkpoint exists.
    temp_path.replace(checkpoint_path)


def clear_checkpoint(checkpoint_path: Path) -> None:
    """Remove the checkpoint file after successful completion."""
    # WHY: Leaving a stale checkpoint would cause the next run to think
    # it is resuming a crashed run and skip items that need reprocessing.
    if checkpoint_path.exists():
        checkpoint_path.unlink()

# ---------- processing logic ----------


def process_item(item: str) -> dict:
    """Process a single item. This is the 'work' function.

    In a real pipeline this might call an API, run a calculation, etc.
    Here we do simple text analysis as a placeholder.
    """
    return {
        "original": item,
        "length": len(item),
        "word_count": len(item.split()),
        "uppercase": item.upper(),
    }


def process_with_checkpoints(
    items: list[str],
    checkpoint_path: Path,
    batch_size: int = 5,
) -> list[dict]:
    """Process items with periodic checkpointing.

    If a checkpoint exists, resume from where we left off.
    Saves a checkpoint every `batch_size` items.
    """
    state = load_checkpoint(checkpoint_path)
    # WHY: +1 because last_processed_index is the index of the last
    # COMPLETED item. We want to start at the next one.
    start_index = state["last_processed_index"] + 1
    results = state["results"]

    if start_index > 0:
        logging.info("Resuming from checkpoint at index %d", start_index)

    for i in range(start_index, len(items)):
        result = process_item(items[i])
        result["index"] = i
        results.append(result)

        # WHY: Checkpoint every batch_size items to limit re-work on crash.
        # Too frequent = I/O overhead. Too infrequent = lots of lost progress
        # on crash. batch_size is the tuning knob.
        if (i + 1) % batch_size == 0:
            save_checkpoint(checkpoint_path, i, results)
            logging.info("Checkpoint saved at index %d", i)

    # WHY: Save a final checkpoint so the last partial batch is not lost.
    if items:
        save_checkpoint(checkpoint_path, len(items) - 1, results)

    return results

# ---------- runner ----------


def run(
    input_path: Path,
    output_path: Path,
    checkpoint_path: Path,
    batch_size: int = 5,
) -> dict:
    """Full processing run with checkpoint recovery."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    items = [
        line.strip()
        for line in input_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    results = process_with_checkpoints(items, checkpoint_path, batch_size)

    # Write final output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    # WHY: Clear the checkpoint on success so the next run starts fresh
    # instead of incorrectly resuming from a completed run.
    clear_checkpoint(checkpoint_path)

    summary = {
        "total_items": len(items),
        "processed": len(results),
        "checkpoint_cleared": True,
    }
    logging.info("Processing complete: %d items", len(results))
    return summary

# ---------- CLI ----------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process items with checkpoint recovery")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/processed_output.json")
    parser.add_argument("--checkpoint", default="data/.checkpoint.json")
    parser.add_argument("--batch-size", type=int, default=5, help="Checkpoint every N items")
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    summary = run(
        Path(args.input), Path(args.output),
        Path(args.checkpoint), args.batch_size,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Write-then-rename (atomic write) for checkpoints | If the process crashes mid-write, a partially written file would corrupt recovery. Atomic replacement ensures the checkpoint is always either the old valid version or the new valid version — never a broken intermediate state. |
| Clear checkpoint on successful completion | A stale checkpoint from a completed run would cause the next run to skip all items, producing empty output. Clearing it signals "this run finished normally." |
| Recover gracefully from corrupt checkpoint files | A corrupt checkpoint (invalid JSON) should not permanently block the pipeline. Starting fresh loses some progress but guarantees eventual completion. |
| `batch_size` as a tuning parameter | Frequent checkpoints (batch_size=1) minimize re-work on crash but add I/O overhead. Infrequent checkpoints (batch_size=1000) are faster but risk more lost progress. The parameter lets users tune this tradeoff. |

## Alternative Approaches

### Using a database (SQLite) instead of a JSON checkpoint file

```python
import sqlite3

def save_checkpoint_db(db_path: str, index: int, result: dict):
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT OR REPLACE INTO checkpoints (item_index, result_json) VALUES (?, ?)",
        (index, json.dumps(result))
    )
    conn.commit()
    conn.close()
```

**Trade-off:** SQLite gives you ACID transactions (crash-safe by default), efficient querying, and per-item granularity. However, it adds complexity and a dependency. The JSON file approach is simpler to understand and debug — you can open the checkpoint in any text editor to inspect its contents.

### Using `signal` handlers for graceful shutdown

```python
import signal

def handle_sigint(signum, frame):
    save_checkpoint(checkpoint_path, current_index, results)
    logging.info("Interrupted — checkpoint saved at index %d", current_index)
    raise SystemExit(1)

signal.signal(signal.SIGINT, handle_sigint)
```

**Trade-off:** Signal handlers let you save a checkpoint when the user presses Ctrl+C, preserving progress that would otherwise be lost. However, signal handlers interact poorly with some libraries and can mask bugs. The batch-checkpoint approach in the main solution provides reasonable crash recovery without signal handling complexity.

## Common Pitfalls

1. **Forgetting the final checkpoint** — If you only checkpoint every N items, the last partial batch (items after the last checkpoint) is lost on crash. The solution saves a final checkpoint after the loop completes.
2. **Setting `batch_size` to 0** — This causes a `ZeroDivisionError` in `(i + 1) % batch_size`. Always validate that batch_size is positive before processing begins.
3. **Not using atomic writes** — Writing directly to the checkpoint file means a crash during the write leaves a half-written file. On the next run, `json.loads()` fails on the corrupt data and the checkpoint is lost. The write-then-rename pattern prevents this.
