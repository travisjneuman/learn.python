"""Level 9 learning project: Sql Query Runner.

Advanced template with run context, timing, structured payload output,
and detailed comments to support self-study at higher levels.
"""

from __future__ import annotations

# argparse parses CLI options.
import argparse
# json serializes run artifacts.
import json
# logging records operational events.
import logging
# time is used to measure runtime duration.
import time
# dataclass provides a clear typed container for run configuration.
from dataclasses import dataclass
# Path is used for robust filesystem handling.
from pathlib import Path

PROJECT_LEVEL = 9
PROJECT_NAME = "Sql Query Runner"


@dataclass
class RunContext:
    """Context object containing run-time inputs.

    Keeping these in one object simplifies extension and testing.
    """

    input_path: Path
    output_path: Path
    run_id: str


def configure_logging() -> None:
    """Initialize logger for consistent run diagnostics."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def load_lines(path: Path) -> list[str]:
    """Read non-empty lines from the input file."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    raw_lines = path.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in raw_lines if line.strip()]


def transform(lines: list[str]) -> list[dict]:
    """Transform text lines into richer records.

    Added fields for advanced exercises:
    - normalized key style,
    - computed string length.
    """
    records: list[dict] = []
    for idx, line in enumerate(lines, start=1):
        records.append(
            {
                "row_num": idx,
                "value": line,
                "normalized": line.lower().replace(" ", "_"),
                "length": len(line),
            }
        )
    return records


def summarize(records: list[dict], elapsed_ms: int) -> dict:
    """Create a run summary, including timing diagnostics."""
    lengths = [r["length"] for r in records]

    return {
        "project_name": PROJECT_NAME,
        "project_level": PROJECT_LEVEL,
        "record_count": len(records),
        "max_length": max(lengths) if lengths else 0,
        "min_length": min(lengths) if lengths else 0,
        "elapsed_ms": elapsed_ms,
    }


def run(ctx: RunContext) -> dict:
    """Execute full data flow using the run context.

    Steps:
    1) read input,
    2) transform,
    3) summarize,
    4) persist payload with run metadata.
    """
    start = time.time()

    lines = load_lines(ctx.input_path)
    records = transform(lines)

    elapsed_ms = int((time.time() - start) * 1000)
    summary = summarize(records, elapsed_ms)

    payload = {
        "run_id": ctx.run_id,
        "summary": summary,
        "records_preview": records[:5],
    }

    ctx.output_path.parent.mkdir(parents=True, exist_ok=True)
    ctx.output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    logging.info("run_id=%s output=%s", ctx.run_id, ctx.output_path)
    return summary


def parse_args() -> argparse.Namespace:
    """Define CLI for advanced project runner."""
    parser = argparse.ArgumentParser(description="Advanced learning project runner")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output_summary.json")
    parser.add_argument("--run-id", default="manual-run")
    return parser.parse_args()


def main() -> None:
    """Program entrypoint for advanced project template."""
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
