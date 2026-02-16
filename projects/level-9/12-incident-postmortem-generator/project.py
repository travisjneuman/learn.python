"""Level 9 project: Incident Postmortem Generator.

Heavily commented advanced template:
- run context object,
- timing metrics,
- structured output payload,
- operational logging with run identifiers.
"""

from __future__ import annotations

# argparse parses command-line flags.
import argparse
# json serializes output artifacts.
import json
# logging captures operational events.
import logging
# time is used to compute runtime duration.
import time
# dataclass simplifies context container definitions.
from dataclasses import dataclass
# Path enables robust path management.
from pathlib import Path

PROJECT_LEVEL = 9
PROJECT_TITLE = "Incident Postmortem Generator"
PROJECT_FOCUS = "post-incident template automation"


@dataclass
class RunContext:
    """Container for run-time configuration and identifiers."""

    input_path: Path
    output_path: Path
    run_id: str


def configure_logging() -> None:
    """Set logging format suitable for operational troubleshooting."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def load_items(path: Path) -> list[str]:
    """Load and normalize non-empty text lines from input."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    raw_lines = path.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in raw_lines if line.strip()]


def build_records(items: list[str]) -> list[dict]:
    """Transform input items into richer structured records."""
    records: list[dict] = []
    for idx, item in enumerate(items, start=1):
        records.append(
            {
                "row_num": idx,
                "raw_value": item,
                "normalized": item.lower().replace(" ", "_"),
                "length": len(item),
            }
        )
    return records


def build_summary(records: list[dict], elapsed_ms: int = 0) -> dict:
    """Build high-level metrics for run output and diagnostics."""
    lengths = [r["length"] for r in records]

    return {
        "project_title": PROJECT_TITLE,
        "project_level": PROJECT_LEVEL,
        "project_focus": PROJECT_FOCUS,
        "record_count": len(records),
        "max_length": max(lengths) if lengths else 0,
        "min_length": min(lengths) if lengths else 0,
        "elapsed_ms": elapsed_ms,
    }


def run(ctx: RunContext) -> dict:
    """Execute full workflow using provided run context.

    Steps:
    1) load items,
    2) build records,
    3) compute metrics,
    4) persist structured payload.
    """
    start_time = time.time()

    items = load_items(ctx.input_path)
    records = build_records(items)

    elapsed_ms = int((time.time() - start_time) * 1000)
    summary = build_summary(records, elapsed_ms=elapsed_ms)

    payload = {
        "run_id": ctx.run_id,
        "project": PROJECT_TITLE,
        "summary": summary,
        "records_preview": records[:5],
    }

    ctx.output_path.parent.mkdir(parents=True, exist_ok=True)
    ctx.output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    logging.info("run_id=%s project=%s output=%s", ctx.run_id, PROJECT_TITLE, ctx.output_path)
    return summary


def parse_args() -> argparse.Namespace:
    """Define CLI interface for advanced project execution."""
    parser = argparse.ArgumentParser(description="Advanced learning project runner")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output_summary.json")
    parser.add_argument("--run-id", default="manual-run")
    return parser.parse_args()


def main() -> None:
    """Entrypoint that wires configuration, context, run, and output."""
    configure_logging()
    args = parse_args()

    ctx = RunContext(
        input_path=Path(args.input),
        output_path=Path(args.output),
        run_id=args.run_id,
    )

    summary = run(ctx)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
