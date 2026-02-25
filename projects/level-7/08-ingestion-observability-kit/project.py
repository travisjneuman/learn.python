"""Level 7 / Project 08 — Ingestion Observability Kit.

Structured logging and metrics for data-ingestion pipelines.
Every record gets a correlation ID so operators can trace failures
back to specific input rows across pipeline stages.

Key concepts:
- Correlation IDs for distributed tracing
- Structured log records (JSON-formatted)
- Metric counters (rows_in, rows_out, errors, duration)
- Stage-level aggregation
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
