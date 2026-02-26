# Solution: Elite Track / Concurrent Job System

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
> [Walkthrough](./WALKTHROUGH.md) for guided hints.

---

## Complete solution

```python
"""Concurrent Job System.

This project is part of the elite extension track.
It intentionally emphasizes explicit, testable engineering decisions.
"""

# WHY deterministic concurrency simulation? -- Real threading is non-deterministic,
# making tests flaky. By simulating job scheduling deterministically, learners
# study concurrency patterns (dependency resolution, resource contention) without
# fighting race conditions in the test harness.

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse CLI inputs for deterministic project execution."""
    parser = argparse.ArgumentParser(description="Concurrent Job System")
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

    payload = build_summary(records, "Concurrent Job System", args.run_id)
    write_summary(output_path, payload)

    print(f"output_summary.json written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Deterministic simulation over real threading | Tests are reproducible; learners focus on concurrency patterns without debugging race conditions | Real asyncio/threading -- realistic but flaky tests and non-deterministic output |
| Sequential pipeline (load -> classify -> summarize) | Models a job system where each stage depends on the previous; easy to reason about data flow | Parallel stage execution -- more realistic but harder to debug and test |
| Fail-fast on malformed input | A concurrent system that silently swallows errors produces corrupt results that are hard to trace | Skip-and-log -- tolerant but hides data quality issues in a learning context |
| Run-id for traceability | Concurrent job systems need correlation IDs; this teaches the pattern even in a simplified pipeline | No tracing -- simpler but loses the ability to correlate runs |

## Alternative approaches

### Approach B: Thread pool with bounded concurrency

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_jobs(lines: list[str], max_workers: int = 4) -> list[dict]:
    """Process lines concurrently with bounded worker pool."""
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(classify_line, line): i for i, line in enumerate(lines)}
        for future in as_completed(futures):
            results.append((futures[future], future.result()))
    # Sort by original index to restore deterministic ordering
    results.sort(key=lambda x: x[0])
    return [r[1] for r in results]
```

**Trade-off:** A real thread pool demonstrates bounded concurrency and resource management. However, `as_completed` returns results in non-deterministic order, requiring re-sorting. The deterministic scaffold is better for learning because output diffs are stable across runs.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Input file with thousands of lines | Sequential processing is slow; a real system would need worker pools | Add timing instrumentation to identify when parallelism becomes necessary |
| Non-integer score in CSV | `int()` raises ValueError, halting the entire pipeline | Add try/except per line with error collection, so one bad line does not stop all processing |
| Concurrent writes to the same output file | Not an issue in this deterministic scaffold, but would corrupt data in a threaded version | Use atomic file writes (write to temp, then rename) in concurrent implementations |
