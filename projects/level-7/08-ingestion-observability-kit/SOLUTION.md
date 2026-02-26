# Solution: Level 7 / Project 08 - Ingestion Observability Kit

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
"""Level 7 / Project 08 — Ingestion Observability Kit.

Structured logging and metrics for data-ingestion pipelines.
Every record gets a correlation ID so operators can trace failures
back to specific input rows across pipeline stages.
"""

from __future__ import annotations

import argparse
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path


# -- Data model ----------------------------------------------------------

# WHY structured log entries with correlation IDs? -- In a multi-stage
# pipeline, a single input row passes through extract -> validate -> load.
# When something fails, the correlation_id lets you trace that specific
# row's journey across all stages -- essential for debugging production issues.
@dataclass
class LogEntry:
    """One structured log line."""
    timestamp: float
    correlation_id: str
    stage: str
    level: str          # INFO | WARN | ERROR
    message: str
    extra: dict = field(default_factory=dict)


@dataclass
class StageMetrics:
    """Counters for a single pipeline stage."""
    stage: str
    rows_in: int = 0
    rows_out: int = 0
    errors: int = 0
    start_time: float = 0.0
    end_time: float = 0.0

    @property
    def duration(self) -> float:
        return round(self.end_time - self.start_time, 4)

    @property
    def error_rate(self) -> float:
        # WHY guard against zero? -- Division by zero when rows_in is 0
        # (empty input) would crash.  Returning 0.0 is semantically correct:
        # no rows processed means no errors.
        return round(self.errors / self.rows_in, 4) if self.rows_in else 0.0


# -- Core logic ----------------------------------------------------------

class ObservabilityKit:
    """Collect logs and metrics across pipeline stages."""

    def __init__(self) -> None:
        self.logs: list[LogEntry] = []
        self.metrics: dict[str, StageMetrics] = {}

    def start_stage(self, stage: str, rows_in: int) -> StageMetrics:
        m = StageMetrics(stage=stage, rows_in=rows_in, start_time=time.time())
        self.metrics[stage] = m
        self._log(stage, "INFO", f"stage started with {rows_in} rows")
        return m

    def end_stage(self, stage: str, rows_out: int, errors: int = 0) -> None:
        # WHY direct dict access (not .get)? -- If the stage was never
        # started, this KeyError is intentional: ending an unstarted stage
        # is a programming bug that should fail loudly.
        m = self.metrics[stage]
        m.rows_out = rows_out
        m.errors = errors
        m.end_time = time.time()
        self._log(stage, "INFO", f"stage completed: {rows_out} out, {errors} errors")

    def log_error(self, stage: str, correlation_id: str, message: str) -> None:
        self._log(stage, "ERROR", message, correlation_id=correlation_id)

    def log_warn(self, stage: str, correlation_id: str, message: str) -> None:
        self._log(stage, "WARN", message, correlation_id=correlation_id)

    def _log(self, stage: str, level: str, message: str,
             correlation_id: str = "") -> None:
        entry = LogEntry(
            timestamp=time.time(),
            # WHY generate a UUID if no correlation_id? -- System-level logs
            # (stage start/end) do not belong to a specific row but still
            # need a unique ID for log aggregation tools.
            correlation_id=correlation_id or str(uuid.uuid4())[:8],
            stage=stage,
            level=level,
            message=message,
        )
        self.logs.append(entry)
        logging.log(
            {"INFO": logging.INFO, "WARN": logging.WARNING, "ERROR": logging.ERROR}[level],
            "[%s] %s — %s", entry.correlation_id, stage, message,
        )

    def summary(self) -> dict:
        stages = {}
        for name, m in self.metrics.items():
            stages[name] = {
                "rows_in": m.rows_in,
                "rows_out": m.rows_out,
                "errors": m.errors,
                "duration": m.duration,
                "error_rate": m.error_rate,
            }
        return {
            "stages": stages,
            "total_logs": len(self.logs),
            "total_errors": sum(1 for e in self.logs if e.level == "ERROR"),
        }


# -- Simulated pipeline -------------------------------------------------

def ingest_stage(records: list[dict], kit: ObservabilityKit) -> list[dict]:
    """Parse raw records, flag bad ones."""
    kit.start_stage("ingest", len(records))
    good, errs = [], 0
    for rec in records:
        cid = rec.get("id", str(uuid.uuid4())[:8])
        # WHY check for "value" field? -- This simulates contract validation
        # at the ingestion boundary.  Records without a value field are
        # malformed and should be logged as errors, not passed downstream.
        if "value" not in rec:
            kit.log_error("ingest", cid, "missing 'value' field")
            errs += 1
            continue
        good.append(rec)
    kit.end_stage("ingest", len(good), errs)
    return good


def transform_stage(records: list[dict], kit: ObservabilityKit) -> list[dict]:
    """Normalise values to uppercase."""
    kit.start_stage("transform", len(records))
    out = []
    for rec in records:
        rec["value"] = str(rec["value"]).upper()
        out.append(rec)
    kit.end_stage("transform", len(out))
    return out


def run_pipeline(records: list[dict]) -> tuple[list[dict], dict]:
    kit = ObservabilityKit()
    data = ingest_stage(records, kit)
    data = transform_stage(data, kit)
    return data, kit.summary()


# -- Entry points --------------------------------------------------------

def run(input_path: Path, output_path: Path) -> dict:
    config = json.loads(input_path.read_text(encoding="utf-8")) if input_path.exists() else {}
    records = config.get("records", [])
    _, summary = run_pipeline(records)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingestion Observability Kit")
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
| Correlation IDs on every log entry | Enables tracing a single record's journey across all pipeline stages | Stage-level logging only -- cannot pinpoint which specific record failed |
| `ObservabilityKit` passed into each stage | Centralizes all logs and metrics in one object; stages do not need to know about logging infrastructure | Global logger -- works but makes testing harder and couples stages to a specific logging backend |
| `StageMetrics` as a dataclass with computed properties | `duration` and `error_rate` always reflect current state; no risk of stale pre-computed values | Store computed values at `end_stage` time -- faster access but requires careful update sequencing |
| `_log` maps level strings to logging constants | Structured logs use string levels ("ERROR") for readability; the mapping bridges to Python's logging module | Use `logging.ERROR` constants directly -- less readable in structured log output |

## Alternative approaches

### Approach B: Decorator-based stage instrumentation

```python
def instrumented(stage_name: str, kit: ObservabilityKit):
    def decorator(fn):
        def wrapper(records, *args, **kwargs):
            kit.start_stage(stage_name, len(records))
            try:
                result = fn(records, *args, **kwargs)
                kit.end_stage(stage_name, len(result))
                return result
            except Exception as e:
                kit.log_error(stage_name, "system", str(e))
                raise
        return wrapper
    return decorator
```

**Trade-off:** Decorators reduce boilerplate (no manual start/end calls) and guarantee `end_stage` is called even on exceptions. But they hide the observability logic, making it harder for learners to see what metrics are being collected.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| `end_stage()` called for a stage never started | `KeyError` on `self.metrics[stage]` | Check if stage exists first, or document that `start_stage` must precede `end_stage` |
| Empty records list passed to pipeline | `rows_in = 0`, `error_rate` property returns 0.0 (guarded) | The zero-division guard handles this; no crash |
| Two stages with the same name | Second `start_stage` overwrites the first in `self.metrics` | Use unique stage names, or append a counter to detect duplicates |
