# Solution: Elite Track / Performance Profiler Workbench

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
> [Walkthrough](./WALKTHROUGH.md) for guided hints.

---

## Complete solution

```python
"""Performance Profiler Workbench.

This project is part of the elite extension track.
It intentionally emphasizes explicit, testable engineering decisions.
"""

# WHY a profiling workbench? -- Optimization without measurement is guesswork.
# This project teaches systematic profiling: instrument, measure, identify
# bottlenecks, optimize, re-measure. The deterministic input ensures profiling
# results are comparable across runs -- essential for validating that an
# optimization actually improved performance.

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse CLI inputs for deterministic project execution."""
    parser = argparse.ArgumentParser(description="Performance Profiler Workbench")
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
        # WHY is_high_risk for profiling? -- In a performance context, "warn"
        # and "critical" map to slow code paths. Low scores indicate poor
        # throughput. Flagging these as high-risk identifies optimization targets.
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

    payload = build_summary(records, "Performance Profiler Workbench", args.run_id)
    write_summary(output_path, payload)

    print(f"output_summary.json written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Deterministic profiling data | Comparing optimization runs requires identical input; non-deterministic data makes before/after comparisons meaningless | Random workload generation -- more realistic but diffs are unstable |
| Score-based risk classification | Scores below 5 indicate code paths that need optimization; creates a clear "fix these first" list | Percentile-based ranking -- more statistically sound but harder to explain |
| JSON output for profile results | Structured data enables automated regression detection (compare current vs baseline JSON) | Flamegraph output -- visually rich but requires tooling to generate |
| Pure functions for transformations | Profiling functions should not have side effects; makes it easy to measure their execution time in isolation | Stateful profiler class -- harder to benchmark individual stages |

## Alternative approaches

### Approach B: Decorator-based function profiling

```python
import functools
import time
from typing import Callable

_profiles: dict[str, list[float]] = {}

def profile(fn: Callable) -> Callable:
    """Decorator that records execution time for each function call."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        result = fn(*args, **kwargs)
        elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
        _profiles.setdefault(fn.__name__, []).append(elapsed_ms)
        return result
    return wrapper

def profile_report() -> dict[str, dict[str, float]]:
    """Generate a summary of all profiled function calls."""
    return {
        name: {
            "calls": len(times),
            "total_ms": round(sum(times), 3),
            "avg_ms": round(sum(times) / len(times), 3),
            "max_ms": round(max(times), 3),
        }
        for name, times in _profiles.items()
    }
```

**Trade-off:** A decorator-based profiler instruments functions with zero code changes (just add `@profile`). It captures real timing data and identifies hot paths. However, it adds overhead to every call and produces non-deterministic output (timing varies by machine). The deterministic scaffold produces stable output for learning; the decorator profiler is a natural "Alter it" enhancement.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Profiling in production with high overhead | Instrumentation slows the application; timing measurements distort results | Use sampling profilers (cProfile, py-spy) that have minimal overhead |
| Micro-benchmarking a single function | Results are dominated by JIT warmup, cache effects, and OS scheduling | Run hundreds of iterations and report percentiles (p50, p95, p99) |
| Optimizing the wrong function | 90% of time is spent in 10% of code; optimizing a fast function wastes effort | Profile first, identify the hottest path, then optimize only that path |
