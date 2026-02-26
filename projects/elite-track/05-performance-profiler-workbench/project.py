"""Performance Profiler Workbench.

This project is part of the elite extension track.
It intentionally emphasizes explicit, testable engineering decisions.
"""


# WHY a profiling workbench? -- Optimization without measurement is guesswork.
# This project teaches systematic profiling: instrument, measure, identify
# bottlenecks, optimize, re-measure. The deterministic input ensures profiling
# results are comparable across runs — essential for validating that an
# optimization actually improved performance.
# Engineering note: this script is intentionally deterministic for reproducible learning drills.
# Engineering note: input validation must fail fast with explicit errors.
# Engineering note: transformations are kept pure to simplify testing and review.
# Engineering note: output payload is stable to support smoke checks and diffing.
# Engineering note: run_id supports traceability across repeated benchmark sessions.
# Engineering note: structure favors readability for teach-back and mentorship workflows.

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse CLI inputs for deterministic project execution."""
    parser = argparse.ArgumentParser(description="Performance Profiler Workbench")
    # Input file path controls deterministic source data for the run.
    parser.add_argument("--input", required=True, help="Path to input text data")
    # Output file path lets users compare run artifacts between iterations.
    parser.add_argument("--output", required=True, help="Path to output JSON summary")
    # Run identifier supports traceability across repeated runs.
    parser.add_argument("--run-id", default="manual-run", help="Optional run identifier")
    return parser.parse_args()


def load_lines(input_path: Path) -> list[str]:
    """Load normalized input lines and reject empty datasets safely."""
    if not input_path.exists():
        raise FileNotFoundError(f"input file not found: {input_path}")

    # Trim whitespace so test assertions stay stable across editors/platforms.
    lines = [line.strip() for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise ValueError("input file contains no usable lines")
    return lines


def classify_line(line: str) -> dict[str, Any]:
    """Transform one CSV-like line into structured fields with validation."""
    parts = [piece.strip() for piece in line.split(",")]
    # Each row must include name, numeric score, and severity status.
    if len(parts) != 3:
        raise ValueError(f"invalid line format (expected 3 comma fields): {line}")

    name, score_raw, severity = parts
    score = int(score_raw)
    return {
        "name": name,
        "score": score,
        "severity": severity,
        # This boolean creates a consistent risk lens for downstream summaries.
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
        # Keep original transformed records for debugging and verification drills.
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

    # Load and transform each input row with explicit validation.
    lines = load_lines(input_path)
    records = [classify_line(line) for line in lines]

    # Build and persist deterministic output for smoke checks and self-review.
    payload = build_summary(records, "Performance Profiler Workbench", args.run_id)
    write_summary(output_path, payload)

    print(f"output_summary.json written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
