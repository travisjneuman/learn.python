# Solution: Elite Track / Algorithms and Complexity Lab

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
> [Walkthrough](./WALKTHROUGH.md) for guided hints.

---

## Complete solution

```python
"""Algorithms and Complexity Lab.

This project is part of the elite extension track.
It intentionally emphasizes explicit, testable engineering decisions.
"""

# WHY deterministic execution? -- Algorithms labs must produce repeatable results
# so learners can compare Big-O predictions against actual run behavior. Any
# randomness would make performance analysis impossible to reproduce.

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse CLI inputs for deterministic project execution."""
    parser = argparse.ArgumentParser(description="Algorithms and Complexity Lab")
    # WHY required --input/--output? -- Explicit file paths make every run
    # reproducible. No hidden defaults means the learner controls exactly
    # where data comes from and where results go.
    parser.add_argument("--input", required=True, help="Path to input text data")
    parser.add_argument("--output", required=True, help="Path to output JSON summary")
    # WHY optional run-id? -- Traceability across repeated benchmark sessions.
    # When comparing algorithm variants, the run-id distinguishes results.
    parser.add_argument("--run-id", default="manual-run", help="Optional run identifier")
    return parser.parse_args()


def load_lines(input_path: Path) -> list[str]:
    """Load normalized input lines and reject empty datasets safely."""
    if not input_path.exists():
        raise FileNotFoundError(f"input file not found: {input_path}")
    # WHY strip whitespace? -- Cross-platform consistency. Windows editors
    # add \r\n, macOS uses \n. Stripping normalizes both to the same output
    # so test assertions are stable across platforms.
    lines = [line.strip() for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise ValueError("input file contains no usable lines")
    return lines


def classify_line(line: str) -> dict[str, Any]:
    """Transform one CSV-like line into structured fields with validation."""
    parts = [piece.strip() for piece in line.split(",")]
    # WHY exactly 3 fields? -- Strict schema validation catches corrupt data
    # at parse time rather than producing mysterious downstream errors.
    if len(parts) != 3:
        raise ValueError(f"invalid line format (expected 3 comma fields): {line}")

    name, score_raw, severity = parts
    score = int(score_raw)
    return {
        "name": name,
        "score": score,
        "severity": severity,
        # WHY is_high_risk boolean? -- Creates a consistent risk lens for
        # downstream summaries. Centralizing the definition of "high risk"
        # here means the summary logic does not need to re-derive it.
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
    # WHY mkdir(parents=True)? -- First-time runners may not have the data/
    # directory yet. Creating it automatically prevents a confusing
    # FileNotFoundError on the very first run.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    """Execute end-to-end project run."""
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    lines = load_lines(input_path)
    records = [classify_line(line) for line in lines]

    payload = build_summary(records, "Algorithms and Complexity Lab", args.run_id)
    write_summary(output_path, payload)

    print(f"output_summary.json written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Deterministic CLI pipeline (input -> transform -> output) | Reproducible runs enable comparing algorithm variants by diffing output files | Interactive REPL -- non-reproducible, cannot be automated in CI |
| Fail-fast validation (FileNotFoundError, ValueError) | Corrupt data caught immediately at the source rather than producing silent wrong results downstream | Lenient parsing with defaults -- hides data quality issues |
| Pure transformation functions | Each function takes input and returns output with no side effects; easy to test, easy to benchmark | Stateful class with mutable state -- harder to isolate for performance measurement |
| JSON output with embedded records | Full traceability: summary stats plus raw data for debugging; diffable across runs | Summary-only output -- loses the ability to inspect individual records |

## Alternative approaches

### Approach B: Timing-instrumented benchmark runner

```python
import time
from typing import Callable

def benchmark(fn: Callable, *args, iterations: int = 100) -> dict[str, float]:
    """Measure function execution time across multiple iterations."""
    times = []
    for _ in range(iterations):
        start = time.perf_counter_ns()
        fn(*args)
        elapsed = time.perf_counter_ns() - start
        times.append(elapsed / 1_000_000)  # convert to ms

    return {
        "min_ms": round(min(times), 3),
        "max_ms": round(max(times), 3),
        "avg_ms": round(sum(times) / len(times), 3),
        "iterations": iterations,
    }
```

**Trade-off:** Adding timing instrumentation lets learners compare theoretical Big-O complexity against measured wall-clock time. However, the current scaffold focuses on data pipeline correctness first. Timing can be layered on top once the pipeline is solid, following the principle of "make it correct, then make it fast."

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Input file has trailing blank lines | `load_lines` strips them via the `if line.strip()` filter, so they are silently ignored | The filter is the prevention; no action needed |
| Score field contains non-integer text | `int(score_raw)` raises `ValueError` with a clear message | Add a try/except around the int conversion with a descriptive error |
| Output directory does not exist | `mkdir(parents=True, exist_ok=True)` creates it automatically | Already handled by the write_summary function |
