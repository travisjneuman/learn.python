"""Level 0 project: Terminal Hello Lab.

Practice printing to the terminal, using variables, and
understanding how Python sends text to your screen.

Concepts: print(), variables, string concatenation, f-strings, escape characters.
"""

from __future__ import annotations

# argparse lets us accept command-line flags like --name.
import argparse
# json for writing structured output.
import json
# Path is a safer way to work with file paths than raw strings.
from pathlib import Path


def greet(name: str) -> str:
    """Build a personalised greeting string.

    WHY a function? -- Putting logic in a function makes it testable.
    We can call greet("Ada") in a test without running the whole script.
    """
    return f"Hello, {name}! Welcome to Python."


def build_banner(title: str, width: int = 40) -> str:
    """Create a decorative banner around a title.

    WHY width defaults to 40? -- Default arguments let callers skip
    the parameter when the common case is fine.
    """
    # The * character repeated `width` times makes a horizontal line.
    border = "*" * width

    # .center() pads the title with spaces so it sits in the middle.
    centered_title = title.center(width)

    # We join three lines with newline characters.
    return f"{border}\n{centered_title}\n{border}"


def build_info_card(name: str, language: str, day: int) -> dict:
    """Collect key facts into a dictionary.

    WHY a dict? -- Dictionaries let you label each piece of data
    with a key, making the output self-documenting.
    """
    return {
        "name": name,
        "language": language,
        "learning_day": day,
        "greeting": greet(name),
    }


def run_hello_lab(name: str, day: int) -> dict:
    """Execute the full hello-lab workflow and return results.

    Steps:
    1. Print a banner to the terminal.
    2. Print a personalised greeting.
    3. Print learning-day info.
    4. Return a summary dict for file output.
    """
    # --- Terminal output (side effects) ---
    banner = build_banner("TERMINAL HELLO LAB")
    print(banner)
    print()  # blank line for readability

    greeting = greet(name)
    print(greeting)

    # \t is a tab character -- it indents the text.
    print(f"\tDay {day} of your Python journey.")
    print()

    # Escape characters demo: \n inside a string creates a new line.
    print("Fun fact: Python is named after Monty Python,\nnot the snake!")

    # --- Build summary for file output ---
    summary = build_info_card(name, "Python", day)
    return summary


def parse_args() -> argparse.Namespace:
    """Define command-line options."""
    parser = argparse.ArgumentParser(description="Terminal Hello Lab")
    parser.add_argument("--name", default="Learner", help="Your name")
    parser.add_argument("--day", type=int, default=1, help="Learning day number")
    parser.add_argument("--output", default="data/output.json", help="Output file path")
    return parser.parse_args()


def main() -> None:
    """Program entry point."""
    args = parse_args()
    summary = run_hello_lab(args.name, args.day)

    # Write the summary to a JSON file so we can inspect it later.
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nSummary written to {output_path}")


# This guard means the code below only runs when you execute the file
# directly (python project.py), NOT when another file imports it.
if __name__ == "__main__":
    main()
