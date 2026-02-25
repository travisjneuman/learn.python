"""Level 0 project: Daily Checklist Writer.

Read a list of tasks from a file (or accept them as arguments),
format them as a numbered checklist, and write the result to a file.

Concepts: writing files, string formatting, lists, loops, Path.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_tasks(path: Path) -> list[str]:
    """Load task descriptions from a file (one per line).

    WHY strip and filter? -- The file might have blank lines or
    trailing whitespace.  We only want actual task descriptions.
    """
    if not path.exists():
        raise FileNotFoundError(f"Tasks file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip()]


def format_checklist(title: str, tasks: list[str]) -> str:
    """Format tasks into a printable checklist with checkboxes.

    WHY number the tasks? -- Numbering makes it easy to refer to
    a specific task ('have you done item 3?') and gives the learner
    a sense of progress as they work through the list.
    """
    if not tasks:
        return f"{title}\n(no tasks)"

    lines = [title, "=" * len(title), ""]

    for i, task in enumerate(tasks, start=1):
        # [ ] is an unchecked checkbox -- a common plain-text convention.
        lines.append(f"  {i}. [ ] {task}")

    lines.append("")
    lines.append(f"Total tasks: {len(tasks)}")
    return "\n".join(lines)


def write_checklist(path: Path, content: str) -> None:
    """Write the checklist string to a file.

    WHY a separate function? -- Isolating file-writing makes it
    easy to test the formatting logic without touching the filesystem.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def checklist_summary(tasks: list[str]) -> dict:
    """Build a JSON-friendly summary of the checklist."""
    return {
        "total_tasks": len(tasks),
        "tasks": tasks,
        "completed": 0,
        "remaining": len(tasks),
    }


def parse_args() -> argparse.Namespace:
    """Define command-line options."""
    parser = argparse.ArgumentParser(description="Daily Checklist Writer")
    parser.add_argument("--input", default="data/sample_input.txt",
                        help="File with task descriptions (one per line)")
    parser.add_argument("--output", default="data/checklist.txt",
                        help="Output file for the formatted checklist")
    parser.add_argument("--title", default="Daily Checklist",
                        help="Title for the checklist")
    return parser.parse_args()


def main() -> None:
    """Program entry point."""
    args = parse_args()

    tasks = load_tasks(Path(args.input))
    checklist = format_checklist(args.title, tasks)

    # Print the checklist to the terminal.
    print(checklist)

    # Write the checklist to a text file.
    output_path = Path(args.output)
    write_checklist(output_path, checklist)
    print(f"\nChecklist written to {output_path}")

    # Also write a JSON summary for programmatic use.
    summary = checklist_summary(tasks)
    json_path = output_path.with_suffix(".json")
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
