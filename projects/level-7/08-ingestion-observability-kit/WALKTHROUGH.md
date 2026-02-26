# Ingestion Observability Kit — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) | [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. The goal is to build a structured logging and metrics system that tracks what happens inside a data pipeline: how many records went in, how many came out, how many had errors, and how long each stage took. If you can create a class that collects log entries and counters, you are on the right track.

## Thinking Process

Consider what happens when a data pipeline fails at 3 AM. The on-call engineer gets paged and needs to answer three questions fast: What failed? Which records were affected? How long had it been failing? Without structured observability, the answer is "grep through a mess of print statements and hope for the best."

Observability is about instrumenting your code so that when things go wrong (and they will), you have the information you need to diagnose the problem quickly. This project builds three key instruments. First, structured log entries that include a correlation ID, a stage name, a severity level, and a message — not just free-form text strings. Second, per-stage metrics that count rows in, rows out, errors, and duration. Third, a summary function that aggregates everything into a report.

The correlation ID is the most important concept here. Imagine a pipeline processing 10,000 records. Record #7,432 fails during the transform stage. Without a correlation ID, you know "something failed somewhere." With a correlation ID, you know "record `abc-123` failed at the transform stage with error: missing value field." That specificity is the difference between a 5-minute fix and a 2-hour investigation.

## Step 1: Define the Data Models

**What to do:** Create two dataclasses: `LogEntry` for individual log lines and `StageMetrics` for per-stage counters. `LogEntry` should have a timestamp, correlation ID, stage name, severity level, and message. `StageMetrics` should track rows in, rows out, errors, start time, and end time.

**Why:** Typed data models enforce consistency. Every log entry has the same shape, making it possible to filter, search, and aggregate later. The `StageMetrics` class uses `@property` for computed values like `duration` and `error_rate`, which keeps the raw counters simple while providing derived metrics on demand.

```python
@dataclass
class LogEntry:
    timestamp: float
    correlation_id: str
    stage: str
    level: str          # INFO | WARN | ERROR
    message: str
    extra: dict = field(default_factory=dict)

@dataclass
class StageMetrics:
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
```

**Predict:** Why does `error_rate` check `if self.rows_in` before dividing? What would happen mathematically if `rows_in` were 0?

## Step 2: Build the ObservabilityKit Class

**What to do:** Create the `ObservabilityKit` class with a list of `LogEntry` objects and a dictionary of `StageMetrics` keyed by stage name. Add `start_stage()` and `end_stage()` methods to bracket each pipeline stage.

**Why:** The kit acts as a collector: pipeline stages call into it to report what is happening, and the kit stores everything for later analysis. Using a dictionary for metrics (keyed by stage name) means you can have any number of stages without modifying the kit.

```python
class ObservabilityKit:
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
```

**Predict:** What happens if you call `end_stage("transform")` but never called `start_stage("transform")` first? What exception would `self.metrics[stage]` raise?

## Step 3: Add Logging Methods with Correlation IDs

**What to do:** Add `log_error()`, `log_warn()`, and a private `_log()` method. Each creates a `LogEntry` with a timestamp, the record's correlation ID, and the message. The correlation ID should be the record's own ID when available, or a short UUID when not.

**Why:** Correlation IDs are the thread that connects a record's journey across stages. When the ingest stage logs an error about record "B-003", and later the transform stage processes record "B-003", the correlation ID lets you trace the full history of that specific record.

```python
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
```

**Predict:** Why generate a short UUID (`str(uuid.uuid4())[:8]`) when no correlation ID is provided? Why not just use an empty string?

## Step 4: Build the Pipeline Stages

**What to do:** Write two pipeline functions: `ingest_stage()` that parses records and flags bad ones, and `transform_stage()` that normalizes values. Both functions accept the `ObservabilityKit` and call `start_stage()`/`end_stage()` to bracket their work.

**Why:** This demonstrates the pattern: each stage tells the kit when it starts (and how many records it received), does its work (logging errors for individual records along the way), and then tells the kit when it finishes (and how many records survived). The kit collects everything passively.

```python
def ingest_stage(records: list[dict], kit: ObservabilityKit) -> list[dict]:
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
    kit.start_stage("transform", len(records))
    out = []
    for rec in records:
        rec["value"] = str(rec["value"]).upper()
        out.append(rec)
    kit.end_stage("transform", len(out))
    return out
```

**Predict:** If 5 records go into the ingest stage and 2 are missing the "value" field, what will `rows_in`, `rows_out`, and `errors` be for the ingest stage metrics?

## Step 5: Generate the Summary Report

**What to do:** Add a `summary()` method to the kit that aggregates all stage metrics and log counts into a single dictionary.

**Why:** The summary is what gets written to the output file and what operators look at first. It provides a quick overview: how many stages ran, how many errors total, and the detailed breakdown per stage. This is the dashboard view of your pipeline health.

```python
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
```

**Predict:** Why count `total_errors` from the log entries rather than summing `errors` from all stage metrics? Could these numbers ever differ?

## Step 6: Wire Up the Pipeline Runner

**What to do:** Write `run_pipeline()` that creates a kit, runs both stages in sequence (passing records from one to the next), and returns the processed data plus the summary.

**Why:** This is where you see the full flow: raw records enter, pass through ingest (where bad records are filtered out), then through transform (where values are normalized), and out the other end. The kit captures everything that happened along the way.

```python
def run_pipeline(records: list[dict]) -> tuple[list[dict], dict]:
    kit = ObservabilityKit()
    data = ingest_stage(records, kit)
    data = transform_stage(data, kit)
    return data, kit.summary()
```

**Predict:** If you added a third stage called `"load"` after transform, what would you need to change in `run_pipeline()`? What about the `ObservabilityKit` class itself?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Calling `end_stage()` for a stage that was never started | Typo in stage name, or skipping a stage conditionally | Check `if stage in self.metrics` before accessing it, or raise a clear `KeyError` message |
| Using `print()` instead of structured log entries | Old habits from debugging simple scripts | Always use `kit.log_error()` or `kit.log_warn()` so the data is captured in the summary |
| Forgetting to count errors separately from rows_out | It is tempting to just subtract, but filtered rows and errored rows are different | Track `errs` explicitly and pass it to `end_stage()` |
| Passing the wrong `rows_in` count to `start_stage()` | Using the original full list length instead of the filtered list from the previous stage | Always use `len(records)` where `records` is the input to THIS stage, not the original input |

## Testing Your Solution

```bash
pytest -q
```

You should see 2+ tests pass. The tests verify that the pipeline processes records correctly, that errors are counted accurately, and that the summary output has the expected structure.

## What You Learned

- **Structured logging** (with typed fields like stage, level, and correlation_id) is fundamentally different from `print()` debugging. Structured logs can be searched, filtered, and aggregated by machines, while print statements are only useful to humans staring at a terminal.
- **Correlation IDs** connect a record's journey across pipeline stages. When you see an error for correlation_id "abc-123", you can filter all logs for that ID and see every step that record went through. This is the foundation of distributed tracing systems like Jaeger and Zipkin.
- **Per-stage metrics** (rows_in, rows_out, errors, duration) give you the "vital signs" of your pipeline. A healthy pipeline has low error rates and consistent durations. A spike in errors or a sudden increase in duration tells you something changed, even before users notice.
