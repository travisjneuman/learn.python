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


def step_read_lines(path: Path) -> list[str]:
    """Step 1: Read and clean lines from a text file.

    WHY a dedicated step? -- Automation pipelines break work into
    discrete steps.  Each step does one thing and passes results
    to the next step.
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    raw = path.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in raw if line.strip()]


def step_parse_records(lines: list[str]) -> list[dict[str, str]]:
    """Step 2: Parse pipe-delimited lines into records.

    WHY pipe-delimited? -- Using '|' as delimiter is common in log
    files and data feeds where commas appear in the data itself.
    """
    records = []
    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            continue
        records.append({
            "name": parts[0],
            "status": parts[1].lower(),
            "value": parts[2],
        })
    return records


def step_filter_active(records: list[dict[str, str]]) -> list[dict[str, str]]:
    """Step 3: Keep only records with status 'active' or 'ok'.

    WHY filter? -- Real automation often needs to skip failed,
    disabled, or irrelevant entries before processing.
    """
    active_statuses = {"active", "ok", "pass", "success"}
    return [r for r in records if r["status"] in active_statuses]


def step_transform(records: list[dict[str, str]]) -> list[dict[str, object]]:
    """Step 4: Transform records — normalise names and parse values.

    WHY transform? -- Raw data rarely matches the format downstream
    systems need.  Cleaning and normalising is a standard pipeline step.
    """
    transformed = []
    for r in records:
        name = r["name"].strip().title()
        try:
            value = float(r["value"])
        except ValueError:
            value = 0.0
        transformed.append({"name": name, "status": r["status"], "value": value})
    return transformed


def step_summarise(records: list[dict[str, object]]) -> dict[str, object]:
    """Step 5: Aggregate transformed records into a summary.

    WHY summarise? -- The final step of most pipelines is to produce
    a report or summary that humans or downstream systems consume.
    """
    if not records:
        return {"count": 0, "total_value": 0.0, "average_value": 0.0, "names": []}

    values = [r["value"] for r in records]
    total = round(sum(values), 2)
    return {
        "count": len(records),
        "total_value": total,
        "average_value": round(total / len(records), 2),
        "names": [r["name"] for r in records],
    }


def run_pipeline(input_path: Path) -> dict[str, object]:
    """Execute all pipeline steps in sequence and return results.

    WHY a single orchestrator? -- Having one function that calls
    each step in order makes the pipeline easy to test, debug,
    and extend with new steps.
    """
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Level 1 Mini Automation")
    parser.add_argument("--input", default="data/sample_input.txt",
                        help="Pipe-delimited data file")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    result = run_pipeline(Path(args.input))
    print(format_report(result))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
