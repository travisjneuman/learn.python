# Algorithms and Complexity Lab — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. This project teaches systematic analysis of input data with deterministic processing and structured output. Spend at least 30 minutes attempting it independently.

## Thinking Process

This project looks simple on the surface: read a CSV-like input file, classify each line, compute a summary, and write JSON output. But the engineering decisions embedded in it are what separate production-grade code from scripts. Every function is deterministic (same input always produces same output). Every boundary is validated (missing file, empty file, malformed line). Every output is structured for downstream consumers (JSON with stable keys).

The mental model is a **data pipeline**: `load -> validate -> transform -> summarize -> persist`. Each stage is a pure function (except I/O at the edges). This separation means you can test the transform and summarize logic without touching the filesystem, and you can swap the input format (CSV, JSON, database) without changing the core logic.

The key engineering constraint is **reproducibility**. The `run_id` parameter creates traceability: you can tell which invocation produced which output. The deterministic functions mean two runs with the same input produce the same output (except for the timestamp). This is essential for benchmarking, where you need to compare runs before and after an optimization.

## Step 1: Parse CLI Arguments

**What to do:** Write `parse_args()` using `argparse` with three arguments: `--input` (required path to input data), `--output` (required path to output JSON), and `--run-id` (optional identifier, defaults to "manual-run").

**Why:** CLI arguments make the script composable. Instead of hardcoding paths, you can run `python project.py --input data/sample_input.txt --output data/output_summary.json --run-id smoke-check` and get deterministic, traceable results. The `run-id` supports automation: a CI pipeline can pass a build number, a benchmark suite can pass a version tag.

```python
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Algorithms and Complexity Lab")
    parser.add_argument("--input", required=True, help="Path to input text data")
    parser.add_argument("--output", required=True, help="Path to output JSON summary")
    parser.add_argument("--run-id", default="manual-run", help="Optional run identifier")
    return parser.parse_args()
```

Both `--input` and `--output` are `required=True`. This is intentional -- the script should fail immediately if the caller forgets to specify where to read from or write to, rather than silently using a default that might not exist.

**Predict:** What happens if you run `python project.py` with no arguments? What error does `argparse` produce?

## Step 2: Load and Validate Input Lines

**What to do:** Write `load_lines()` that reads a file, strips whitespace, filters empty lines, and rejects empty datasets.

**Why:** Input validation is the first line of defense. A missing file should produce a clear `FileNotFoundError`, not a cryptic traceback from a downstream function. An empty file should produce a clear `ValueError`, not a division-by-zero error when computing averages. Fail fast, fail clearly.

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

Three details matter:

- **`encoding="utf-8"` is explicit.** On Windows, the default encoding is often `cp1252`, which can silently corrupt non-ASCII characters. Always specify UTF-8 for cross-platform consistency.
- **`line.strip()` is applied twice** -- once in the filter condition (`if line.strip()`) and once in the output list. This ensures both filtering and normalization happen, removing trailing whitespace and `\r\n` line endings.
- **Empty lines are silently dropped**, but an entirely empty file raises an error. This is the right balance: a stray blank line is normal; a completely empty input is probably a mistake.

**Predict:** If the input file contains `"alpha,10,ok\n\n\nbeta,7,warn\n"`, how many lines does `load_lines()` return?

## Step 3: Transform Each Line into Structured Data

**What to do:** Write `classify_line()` that splits a CSV-like line into three fields (name, score, severity) and adds a computed `is_high_risk` boolean.

**Why:** Raw text lines are not useful for analysis. Transforming each line into a structured dictionary with typed fields (integer score, boolean risk flag) enables downstream aggregation. The validation (exactly 3 comma-separated fields) catches malformed input before it causes confusing errors later.

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

The `is_high_risk` flag combines two conditions with `or`: either the severity is elevated ("warn" or "critical"), or the score is below 5. This creates a consistent risk lens that the summary can count without re-evaluating the raw data.

**Predict:** For the line `"gamma,2,critical"`, what does `classify_line()` return? Is it high risk, and for how many reasons?

## Step 4: Build the Summary Payload

**What to do:** Write `build_summary()` that takes the classified records, a project title, and a run ID, and produces a deterministic JSON-ready summary with counts and averages.

**Why:** The summary is the deliverable. It contains everything a downstream consumer needs: how many records were processed, how many are high risk, the average score, and the raw records for debugging. The `run_id` and `project_title` provide traceability -- you can match any output file back to the exact invocation that produced it.

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

Three details to notice:

- **`round(..., 2)` ensures consistent decimal places.** Without rounding, floating-point arithmetic might produce `6.333333333333333` instead of `6.33`.
- **`datetime.now(timezone.utc)` uses timezone-aware UTC.** This avoids ambiguity about which timezone the timestamp is in -- essential for distributed systems.
- **The records are included in the output.** This seems redundant, but it is invaluable for debugging: you can see exactly what was processed without re-running the pipeline.

**Predict:** Given records `[{"score": 10, "is_high_risk": False}, {"score": 3, "is_high_risk": True}]`, what is the `average_score`? What is `high_risk_count`?

## Step 5: Write Output and Orchestrate the Pipeline

**What to do:** Write `write_summary()` for file persistence and `main()` to orchestrate the full pipeline: parse args, load, transform, summarize, write.

**Why:** `write_summary()` handles directory creation (`parents=True`) so the script works even on first run when the output directory does not exist. The `main()` function is the orchestrator that connects all the pure functions into an end-to-end pipeline.

```python
def write_summary(output_path: Path, payload: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    lines = load_lines(input_path)
    records = [classify_line(line) for line in lines]

    payload = build_summary(records, "Algorithms and Complexity Lab", args.run_id)
    write_summary(output_path, payload)

    print(f"output_summary.json written to {output_path}")
    return 0
```

The `main()` function returns an integer exit code (0 for success). The `if __name__ == "__main__": raise SystemExit(main())` pattern converts this into a proper process exit code, which CI systems and shell scripts use to detect success or failure.

**Predict:** If `load_lines()` raises `FileNotFoundError`, does `main()` return 0? What happens to the process exit code?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Forgetting `encoding="utf-8"` | Relying on platform default encoding | Always specify encoding explicitly for cross-platform safety |
| `int(score_raw)` crashes on non-numeric input | No validation before conversion | Wrap in try/except or validate format before converting |
| Division by zero in `avg_score` | Empty records list | `load_lines()` prevents this, but add a guard in `build_summary()` for safety |
| Output directory does not exist | First run in a clean environment | `output_path.parent.mkdir(parents=True, exist_ok=True)` |
| Timestamp varies between runs | Using `datetime.now()` without timezone | This is expected -- `generated_utc` is the only non-deterministic field |

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

Then inspect `data/output_summary.json`. It should contain 3 records (alpha, beta, gamma), with `high_risk_count: 2` (beta is "warn" and gamma is "critical" with score < 5), and `average_score: 6.33`.

## What You Learned

- **Deterministic pipelines** produce the same output for the same input. This enables benchmarking (compare before and after optimization), reproducibility (anyone can re-run and verify), and debugging (replay a failing run with the exact same data).
- **Fail-fast validation** at input boundaries prevents confusing errors downstream. A clear "input file not found" message at the top of the pipeline is worth far more than a cryptic `KeyError` buried in a transform function.
- **Structured output with traceability** (run ID, project title, UTC timestamp) turns a script into a tool. You can match any output file back to the invocation that produced it, which is essential for audit trails and production debugging.
