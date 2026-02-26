# Staff Engineer Capstone — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. This capstone integrates architecture, reliability, security, and communication evidence into one system -- the kind of system-level thinking that defines staff+ engineering. Spend at least 45 minutes attempting it independently.

## Thinking Process

Staff engineering is not about writing more code. It is about making decisions that affect multiple teams, balancing technical debt against feature velocity, and building platforms that scale organizational output. This capstone asks you to build a system that processes heterogeneous input (components with different names, scores, and severity levels), classifies risk, and produces a structured report that a leadership team can act on.

The pipeline is the same pattern used throughout the elite track: `load -> validate -> transform -> summarize -> persist`. What makes this a capstone is the _integration mindset_. You are not just classifying lines of text -- you are building an evidence system. Each record represents a component that was evaluated. The summary tells you: across all evaluated components, how many are at risk? What is the average health score? Where should the team focus next?

Think of this as the reporting layer for a staff engineer's system review. Before proposing an architecture change to leadership, you need evidence: "We evaluated 12 subsystems. 4 are high-risk (33%). The average health score is 6.2, which is below our target of 8.0. Here are the specific components that need investment." This project builds the tool that generates that evidence.

## Step 1: Parse CLI Arguments for Traceable Execution

**What to do:** Write `parse_args()` with `--input`, `--output`, and `--run-id` arguments.

**Why:** Staff-level work demands traceability. When you present findings to leadership, they will ask: "When was this data collected? Can we reproduce this?" The `run-id` answers both questions. The explicit input/output paths make the tool composable with other systems (CI pipelines, monitoring dashboards, review processes).

```python
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Staff Engineer Capstone")
    parser.add_argument("--input", required=True, help="Path to input text data")
    parser.add_argument("--output", required=True, help="Path to output JSON summary")
    parser.add_argument("--run-id", default="manual-run", help="Optional run identifier")
    return parser.parse_args()
```

In a real staff engineer context, you would extend this with arguments like `--format` (JSON/CSV/HTML), `--threshold` (configurable risk threshold), and `--team` (filter by team ownership). The current interface is the minimal viable version that establishes the pattern.

**Predict:** A staff engineer runs this weekly with `--run-id "week-12-2026"`. How would they track trends over time using these run IDs?

## Step 2: Load Input Data with Boundary Validation

**What to do:** Write `load_lines()` to read, strip, filter, and validate the input file.

**Why:** The boundary between external data and your system is where most bugs live. A missing file, an empty file, a file with unexpected encoding -- these are the realities of production data. Validating at the boundary means the rest of your pipeline can trust its input.

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

Staff engineering context: in a real system, the input might come from multiple sources -- monitoring tools, code analysis, security scanners, team surveys. Each source has different reliability. The `load_lines()` function is the trust boundary: everything that passes through it meets your minimum quality bar (exists, non-empty, properly encoded).

**Predict:** If a monitoring tool produces an output file with only blank lines (e.g., a bug in the exporter), what does `load_lines()` do? Is this the right behavior?

## Step 3: Classify Each Component

**What to do:** Write `classify_line()` to parse CSV-like input into structured records with risk classification.

**Why:** Classification is the analytical core. Raw data ("auth-service,3,critical") becomes structured evidence ("auth-service has score 3, severity critical, is high-risk"). The `is_high_risk` flag combines quantitative (score < 5) and qualitative (severity is "warn" or "critical") signals into a single actionable indicator.

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

The dual-criteria risk classification reflects a staff engineer's judgment. A component with severity "critical" is obviously risky. But a component with score 2 and severity "ok" is also risky -- it might be "ok" today but trending toward failure. Both signals matter, and `or` captures both.

**Predict:** In the sample data, `alpha` has `score=10, severity=ok`. `beta` has `score=7, severity=warn`. `gamma` has `score=2, severity=critical`. Which are high-risk and why?

## Step 4: Build the Evidence Summary

**What to do:** Write `build_summary()` that computes aggregate statistics and packages them with traceability metadata.

**Why:** The summary is the evidence artifact. When a staff engineer says "33% of our subsystems are at risk," the summary is the backing data. It includes the raw records so anyone can verify the claim, the average score for trend tracking, and the run metadata for auditability.

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

The summary fields map directly to leadership questions:

- `record_count` answers: "How comprehensive is this review?"
- `high_risk_count` answers: "How many things need immediate attention?"
- `average_score` answers: "What is our overall system health?"
- `records` answers: "Show me the specifics."

**Predict:** With sample data (scores 10, 7, 2), the average is 6.33. If you added a fourth component with score 1 and severity "critical", what would the new average be? How would high_risk_count change?

## Step 5: Persist and Orchestrate

**What to do:** Write `write_summary()` and `main()` to complete the pipeline.

**Why:** The final step connects the analytical pipeline to the filesystem. The output JSON becomes an artifact that can be committed to a repository, attached to a review document, or ingested by a dashboard. The `main()` function is the composition root -- it wires all the pure functions together.

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

    payload = build_summary(records, "Staff Engineer Capstone", args.run_id)
    write_summary(output_path, payload)

    print(f"output_summary.json written to {output_path}")
    return 0
```

The `return 0` exit code is a contract with the operating system: 0 means success, non-zero means failure. CI systems, shell scripts, and monitoring tools rely on this convention. If `main()` raises an uncaught exception, `SystemExit(main())` propagates it, and the OS sees a non-zero exit code.

**Predict:** If you wanted to add a `--verbose` flag that prints each record as it is classified, where in `main()` would you add that logic? How would you keep the function under 20 lines?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Treating the tool as a one-time script | Running once and drawing conclusions | Run against multiple input sets; track trends across runs |
| Ignoring components with low score but "ok" severity | Only looking at the severity label | The `is_high_risk` flag captures low-score components regardless of severity label |
| Not including raw records in the summary | Trying to keep the output small | Records are essential for verification; stakeholders will ask "which components?" |
| Hardcoding the project title | Making it a constant | Pass it as a parameter for reuse across different evaluation contexts |
| No error handling for `int()` conversion | Assuming scores are always integers | Add try/except around `int(score_raw)` with a clear error message |

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

Inspect the output. With the default sample input, expect `record_count: 3`, `high_risk_count: 2` (beta and gamma), and `average_score: 6.33`.

## What You Learned

- **Staff engineering is about evidence, not opinion.** This pipeline turns raw data into structured evidence that supports architectural decisions. "We should invest in auth-service" is an opinion. "Auth-service has a risk score of 2/10 and severity critical" is evidence.
- **System-level thinking means integration.** Each function in this pipeline is simple. The value is in how they compose: CLI for traceability, validation for trust, classification for analysis, summarization for communication, persistence for auditability. The whole is greater than the sum of its parts.
- **Reproducibility enables accountability.** When you produce a report with a run ID and UTC timestamp, anyone can re-run it with the same input and verify your conclusions. This is the standard of engineering rigor expected at the staff+ level.
