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
        logging.warning("Corrupt checkpoint file — starting fresh")
        return {"last_processed_index": -1, "results": []}


def save_checkpoint(checkpoint_path: Path, index: int, results: list[dict]) -> None:
    """Persist current progress to a checkpoint file.

    We write to a temp file first, then rename — this ensures the checkpoint
    is never partially written (atomic write pattern).
    """
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = checkpoint_path.with_suffix(".tmp")
    temp_path.write_text(
        json.dumps({"last_processed_index": index, "results": results}, indent=2),
        encoding="utf-8",
    )
    temp_path.replace(checkpoint_path)


def clear_checkpoint(checkpoint_path: Path) -> None:
    """Remove the checkpoint file after successful completion."""
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
    start_index = state["last_processed_index"] + 1
    results = state["results"]

    if start_index > 0:
        logging.info("Resuming from checkpoint at index %d", start_index)

    for i in range(start_index, len(items)):
        result = process_item(items[i])
        result["index"] = i
        results.append(result)

        # Save checkpoint every batch_size items
        if (i + 1) % batch_size == 0:
            save_checkpoint(checkpoint_path, i, results)
            logging.info("Checkpoint saved at index %d", i)

    # Final checkpoint
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

    # Clean up checkpoint on success
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
