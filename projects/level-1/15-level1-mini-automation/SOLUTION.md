# Solution: Level 1 / Project 15 - Level 1 Mini Automation

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 1 project: Level 1 Mini Automation.

A multi-step automation pipeline that reads a configuration of tasks,
executes each step in sequence, and produces a summary report.
Combines file operations, string processing, and data aggregation
from earlier projects into one workflow.

Concepts: pipeline pattern, step sequencing, combining learned skills.
"""


import argparse
import csv
import json
from datetime import datetime
from pathlib import Path


# WHY step_read_lines: This is Step 1 of the pipeline.  Automation
# pipelines break work into discrete steps, where each step does one
# thing and passes its result to the next.  Reading and cleaning lines
# is the "Extract" phase of ETL (Extract-Transform-Load).
def step_read_lines(path: Path) -> list[str]:
    """Step 1: Read and clean lines from a text file."""
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    raw = path.read_text(encoding="utf-8").splitlines()
    # WHY strip and filter: Raw files often have trailing whitespace
    # and blank lines.  Cleaning at the source prevents downstream
    # steps from processing empty data.
    return [line.strip() for line in raw if line.strip()]


# WHY step_parse_records: Step 2 converts raw text lines into
# structured data (dicts).  This is the same text-to-dict pattern
# used in the Log Line Parser and CSV Reader projects.
def step_parse_records(lines: list[str]) -> list[dict[str, str]]:
    """Step 2: Parse pipe-delimited lines into records.

    WHY pipe-delimited? -- Using '|' as delimiter is common in log
    files and data feeds where commas appear in the data itself.
    """
    records = []
    for line in lines:
        # WHY split on "|": Pipe-delimited data is an alternative to
        # CSV when the data contains commas.  Each part becomes a
        # field after stripping whitespace.
        parts = [p.strip() for p in line.split("|")]
        # WHY skip short lines: A line with fewer than 3 parts is
        # malformed.  Skipping it is safer than crashing or guessing
        # what the missing fields should be.
        if len(parts) < 3:
            continue
        records.append({
            "name": parts[0],
            # WHY .lower(): Normalising the status field ensures
            # "Active", "ACTIVE", and "active" all match the same
            # filter criteria in the next step.
            "status": parts[1].lower(),
            "value": parts[2],
        })
    return records


# WHY step_filter_active: Step 3 removes records that should not be
# processed.  In real automation, you often skip failed, disabled,
# or irrelevant entries before doing expensive transformations.
def step_filter_active(records: list[dict[str, str]]) -> list[dict[str, str]]:
    """Step 3: Keep only records with status 'active' or 'ok'."""
    # WHY a set: Set lookup is O(1), making the filter efficient.
    # It also makes it easy to add new valid statuses later.
    active_statuses = {"active", "ok", "pass", "success"}
    return [r for r in records if r["status"] in active_statuses]


# WHY step_transform: Step 4 normalises and converts data into the
# format needed by downstream consumers.  Raw data rarely matches
# what the summary step needs — names may have inconsistent casing,
# values may be strings instead of numbers.
def step_transform(records: list[dict[str, str]]) -> list[dict[str, object]]:
    """Step 4: Transform records -- normalise names and parse values."""
    transformed = []
    for r in records:
        # WHY .title(): Capitalises the first letter of each word.
        # "alice smith" becomes "Alice Smith" — clean, consistent.
        name = r["name"].strip().title()
        try:
            value = float(r["value"])
        except ValueError:
            # WHY default to 0.0: A non-numeric value like "N/A"
            # should not crash the pipeline.  Defaulting to 0 lets
            # the record pass through with a safe fallback.
            value = 0.0
        transformed.append({"name": name, "status": r["status"], "value": value})
    return transformed


# WHY step_summarise: Step 5 aggregates transformed records into a
# summary — the final output.  This is the "Load" phase of ETL:
# producing the deliverable (a report, a dashboard, a database insert).
def step_summarise(records: list[dict[str, object]]) -> dict[str, object]:
    """Step 5: Aggregate transformed records into a summary."""
    # WHY guard against empty: If all records were filtered out in
    # Step 3, we have nothing to summarise.  Returning zero values
    # is cleaner than crashing on division by zero.
    if not records:
        return {"count": 0, "total_value": 0.0, "average_value": 0.0, "names": []}

    values = [r["value"] for r in records]
    total = round(sum(values), 2)
    return {
        "count": len(records),
        "total_value": total,
        "average_value": round(total / len(records), 2),
        # WHY collect names: Including the list of processed names
        # in the summary makes the report self-documenting — you can
        # see exactly which records contributed to the totals.
        "names": [r["name"] for r in records],
    }


# WHY run_pipeline: This is the orchestrator — it calls each step in
# sequence and tracks how many records survive each stage.  Having
# one function that runs the whole pipeline makes it easy to test
# end-to-end with a single function call.
def run_pipeline(input_path: Path) -> dict[str, object]:
    """Execute all pipeline steps in sequence and return results."""
    # WHY track counts at each step: Pipeline debugging requires
    # knowing where data was lost.  "3 parsed, 2 active, 2 summarised"
    # tells you exactly 1 record was filtered out in Step 3.
    lines = step_read_lines(input_path)
    records = step_parse_records(lines)
    active = step_filter_active(records)
    transformed = step_transform(active)
    summary = step_summarise(transformed)

    return {
        "input_file": str(input_path),
        "total_lines": len(lines),
        "parsed_records": len(records),
        "active_records": len(active),
        "summary": summary,
    }


# WHY format_report: Displays the pipeline results as a readable
# report showing the funnel of data through each step.
def format_report(result: dict[str, object]) -> str:
    """Format pipeline results as a human-readable report."""
    lines = [
        "=== Automation Pipeline Report ===",
        "",
        f"  Input:           {result['input_file']}",
        f"  Lines read:      {result['total_lines']}",
        f"  Records parsed:  {result['parsed_records']}",
        f"  Active records:  {result['active_records']}",
        "",
    ]

    summary = result["summary"]
    lines.append(f"  Processed:       {summary['count']}")
    lines.append(f"  Total value:     {summary['total_value']}")
    lines.append(f"  Average value:   {summary['average_value']}")

    if summary["names"]:
        lines.append("")
        lines.append("  Names:")
        for name in summary["names"]:
            lines.append(f"    - {name}")

    return "\n".join(lines)


# WHY parse_args: Standard argparse for flexible input/output paths.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Level 1 Mini Automation")
    parser.add_argument("--input", default="data/sample_input.txt",
                        help="Pipe-delimited data file")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


# WHY main: Top-level orchestration — run pipeline, display, save.
def main() -> None:
    args = parse_args()

    result = run_pipeline(Path(args.input))
    print(format_report(result))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Five separate `step_*` functions | Each step has a single responsibility and is independently testable; the pipeline is composable and extensible | One large function — would mix parsing, filtering, transforming, and summarising, making debugging difficult |
| `run_pipeline()` as single orchestrator | One entry point for the whole pipeline makes end-to-end testing trivial (`run_pipeline(path)` returns everything) | Call steps individually from `main()` — works but scatters the pipeline logic |
| Track record counts at each stage | Pipeline debugging requires knowing where data dropped off; the funnel report (3 parsed, 2 active, 2 summarised) pinpoints filter losses | Only report final counts — hides where data was filtered, making debugging harder |
| Default to 0.0 for non-numeric values | Keeps the pipeline running even with dirty data; the record is not lost, just given a safe default value | Raise ValueError — would stop the pipeline at the first bad value |

## Alternative approaches

### Approach B: Generator-based pipeline (lazy evaluation)

```python
from typing import Generator

def step_parse_lazy(lines: list[str]) -> Generator[dict, None, None]:
    """Parse records lazily using a generator."""
    # WHY generators: Instead of building a complete list at each step,
    # generators yield one record at a time.  For large datasets, this
    # uses much less memory because only one record is in memory at a time.
    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            continue
        yield {"name": parts[0], "status": parts[1].lower(), "value": parts[2]}

def step_filter_lazy(records: Generator) -> Generator[dict, None, None]:
    """Filter lazily — only passes matching records through."""
    active_statuses = {"active", "ok", "pass", "success"}
    for r in records:
        if r["status"] in active_statuses:
            yield r

# Usage: pipe steps together
# records = step_filter_lazy(step_parse_lazy(lines))
```

**Trade-off:** Generators are more memory-efficient for large datasets because they process one record at a time instead of building intermediate lists. However, generators can only be iterated once, and you cannot easily count records at each stage without consuming the generator. The list-based approach in the primary solution is better for learning, debugging, and producing the funnel report. Use generators when processing files too large to fit in memory.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Line with only 2 pipe-separated values | `step_parse_records()` skips it because `len(parts) < 3` | The length check is already in place |
| Non-numeric value field like `"N/A"` | `step_transform()` catches ValueError from `float()` and defaults to 0.0 | The try/except with a 0.0 fallback handles this |
| All records have status `"failed"` | `step_filter_active()` returns `[]`, `step_summarise([])` returns zero counts | The empty-list guard in `step_summarise()` prevents ZeroDivisionError |
| Input file does not exist | `step_read_lines()` raises `FileNotFoundError` with the path in the message | The explicit existence check catches this before attempting to read |

## Key takeaways

1. **The pipeline pattern (step functions chained in sequence) is the foundation of data engineering.** ETL (Extract-Transform-Load) pipelines, CI/CD workflows, and Unix command pipelines (`cat file | grep | sort | uniq`) all use this same structure: each step takes input, produces output, and passes it to the next step.
2. **Tracking counts at each stage is essential for pipeline debugging.** When your summary says "0 records processed" but you started with 100 lines, the stage counts tell you exactly where the data was lost (parsing? filtering? transformation?). This observability pattern is used in every production data pipeline.
3. **This capstone project combines everything from Level 1.** File reading (Projects 1, 4, 5), string parsing (Projects 1, 4), filtering (Projects 4, 10), transformation (Projects 3, 6, 13), aggregation (Projects 5, 6, 14), and structured output (all projects). You are now ready for Level 2, where you will work with classes, modules, and more complex architectures.
