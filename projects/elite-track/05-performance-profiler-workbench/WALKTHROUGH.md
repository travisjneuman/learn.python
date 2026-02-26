# Performance Profiler Workbench — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. This project builds a profiling pipeline that processes performance data, identifies bottlenecks, and reports optimization impact. Spend at least 30 minutes attempting it independently.

## Thinking Process

Optimization without measurement is guesswork. A developer might "optimize" a function by adding caching, only to discover that the function was already fast and the real bottleneck was a database query. This project teaches the systematic approach: instrument, measure, classify, and report. By processing structured input data through a deterministic pipeline, you produce comparable results across runs -- essential for answering "did my optimization actually help?"

The architecture follows the same pipeline pattern as other elite track projects: `parse CLI -> load input -> validate -> transform -> summarize -> persist`. What makes this project distinct is the _domain_: the input represents performance metrics (component names, scores, severity levels), and the transform classifies each record as high-risk or normal based on both severity and score thresholds. The summary aggregates these classifications into a report that highlights what needs attention.

The engineering discipline here is **reproducibility as a feature**. The `run-id` parameter lets you tag runs ("before-optimization", "after-caching-added") and compare their outputs side by side. The deterministic processing ensures that differences in output reflect actual changes in input data, not randomness in the pipeline.

## Step 1: Set Up CLI Argument Parsing

**What to do:** Write `parse_args()` with three arguments: `--input` (path to performance data), `--output` (path for JSON results), and `--run-id` (identifier for this profiling run).

**Why:** Profiling is iterative. You run the profiler, make a change, and run it again. CLI arguments let you point at different input files and tag outputs with meaningful identifiers. A CI system can automate this: run the profiler against each commit, compare results, and flag performance regressions.

```python
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Performance Profiler Workbench")
    parser.add_argument("--input", required=True, help="Path to input text data")
    parser.add_argument("--output", required=True, help="Path to output JSON summary")
    parser.add_argument("--run-id", default="manual-run", help="Optional run identifier")
    return parser.parse_args()
```

Both `--input` and `--output` are required because a profiler without input data or output destination is useless. The `--run-id` defaults to `"manual-run"` for ad-hoc use, but you should always provide a meaningful ID when comparing runs.

**Predict:** If you run the profiler twice with `--run-id v1` and `--run-id v2`, how would you compare the two outputs? What fields would differ?

## Step 2: Load and Validate Performance Data

**What to do:** Write `load_lines()` to read the input file, strip whitespace, and reject missing or empty files.

**Why:** Performance data might come from logs, monitoring systems, or test harnesses. The input validation ensures the pipeline fails clearly on bad data rather than producing misleading results. An empty input file should raise an error, not produce a report claiming "0 high-risk components" (which would look like everything is fine).

```python
def load_lines(input_path: Path) -> list[str]:
    if not input_path.exists():
        raise FileNotFoundError(f"input file not found: {input_path}")

    lines = [
        line.strip()
        for line in input_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not lines:
        raise ValueError("input file contains no usable lines")
    return lines
```

The list comprehension does two things at once: filters out empty lines (`if line.strip()`) and normalizes remaining lines (`.strip()` in the expression). This handles common input quirks like trailing newlines, carriage returns from Windows, and blank lines between records.

**Predict:** What does `load_lines()` return for a file containing `"api-server,15,ok\n\ndb-query,2,critical\n"`? How many lines?

## Step 3: Classify Performance Records

**What to do:** Write `classify_line()` that parses each CSV-like line into a structured record with name, score, severity, and a computed `is_high_risk` flag.

**Why:** Raw text is not analyzable. Transforming each line into a typed dictionary enables aggregation (average scores, risk counts) and filtering (show only high-risk components). The `is_high_risk` flag combines severity and score into a single boolean that downstream code can count without re-parsing the raw data.

```python
def classify_line(line: str) -> dict[str, Any]:
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
```

The risk classification uses two independent criteria: elevated severity ("warn" or "critical") OR a score below 5. A component can be high-risk for either reason or both. In a profiling context, a low score might indicate poor performance even if the severity label says "ok" -- the numeric data overrides the categorical label.

**Predict:** A component has `score=3` and `severity="ok"`. Is it high-risk? Why might a low score with "ok" severity still warrant attention?

## Step 4: Build the Profiling Summary

**What to do:** Write `build_summary()` that computes `record_count`, `high_risk_count`, `average_score`, and includes the full records list.

**Why:** The summary is the profiler's report. It answers: "How many components were profiled? How many need attention? What is the overall performance level?" Including the raw records enables drill-down: after seeing "3 high-risk components," the operator can look at the records to find exactly which ones.

```python
def build_summary(
    records: list[dict[str, Any]],
    project_title: str,
    run_id: str,
) -> dict[str, Any]:
    high_risk_count = sum(1 for record in records if record["is_high_risk"])
    avg_score = round(
        sum(record["score"] for record in records) / len(records), 2
    )

    return {
        "project_title": project_title,
        "run_id": run_id,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "record_count": len(records),
        "high_risk_count": high_risk_count,
        "average_score": avg_score,
        "records": records,
    }
```

The `average_score` is a single number that summarizes overall performance. If the average drops between runs, something got worse. If it improves, the optimization worked. Combined with `high_risk_count`, you get both a broad view (average) and a targeted view (how many components are in trouble).

**Predict:** If you profile 10 components and 3 are high-risk, what percentage of your system needs attention? Is 30% acceptable for a production system?

## Step 5: Persist Results and Run the Full Pipeline

**What to do:** Write `write_summary()` for JSON persistence and `main()` to orchestrate the end-to-end pipeline.

**Why:** The pipeline orchestrator connects all pure functions into a complete workflow. The JSON output is the artifact that enables comparison: diff two output files from different runs to see what changed. The `parents=True` flag in `mkdir` ensures the output directory chain is created on first run.

```python
def write_summary(output_path: Path, payload: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    # Pipeline: load -> transform -> summarize -> persist
    lines = load_lines(input_path)
    records = [classify_line(line) for line in lines]
    payload = build_summary(records, "Performance Profiler Workbench", args.run_id)
    write_summary(output_path, payload)

    print(f"output_summary.json written to {output_path}")
    return 0
```

The list comprehension `[classify_line(line) for line in lines]` will fail on the first malformed line. This is fail-fast behavior: you want to know about bad data immediately, not discover it after processing half the file. For a more resilient pipeline, you could catch `ValueError` per line and collect errors separately.

**Predict:** If line 5 of 10 is malformed, do lines 1-4 still get processed? Does the output file get written?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Comparing outputs without the same run-id | Using default "manual-run" for all runs | Always provide a meaningful `--run-id` when benchmarking |
| `int()` crashes on decimal scores | Input has "3.5" instead of "3" | Use `float()` then `int()`, or decide if decimals should be allowed |
| Ignoring the `generated_utc` when diffing | Timestamp changes every run | Exclude `generated_utc` when comparing outputs, or use a fixed timestamp in tests |
| Pipeline produces empty output on error | Exception raised but no output written | Let the exception propagate; do not write partial output |
| Running profiler once and concluding | Single data point cannot show trends | Profile before and after changes; track scores over time |

## Testing Your Solution

```bash
pytest -q
```

Expected output:
```text
2 passed
```

Test from the command line:

```bash
python project.py --input data/sample_input.txt --output data/output_summary.json --run-id smoke-check
```

Inspect the output file. With the default sample input (`alpha,10,ok` / `beta,7,warn` / `gamma,2,critical`), expect: `record_count: 3`, `high_risk_count: 2`, `average_score: 6.33`.

## What You Learned

- **Profiling is a discipline, not a tool.** The tool (this pipeline) processes data, but the discipline is systematic: measure first, hypothesize, change one thing, measure again. Without before-and-after comparison, you cannot prove an optimization worked.
- **Risk classification combines multiple signals.** A component can be high-risk due to severity, score, or both. Real profilers combine latency percentiles, error rates, and resource utilization into composite risk scores -- the same principle as the `is_high_risk` flag here.
- **Reproducible output enables comparison.** Deterministic processing, stable JSON keys, and run IDs let you diff two output files and see exactly what changed. This is the foundation for automated performance regression detection in CI pipelines.
