"""Level 0 project: Simple Menu Loop.

Present a numbered menu to the user, execute their choice,
and loop until they choose to quit.  Reads commands from a
file for batch/test mode, or from stdin for interactive mode.

Concepts: while loops, if/elif/else, break, functions as menu actions.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


# --- Menu action functions ---
# Each function performs one menu action and returns a message string.
# WHY separate functions? -- Each action is isolated, testable, and
# the menu dispatcher stays clean.

def action_greet() -> str:
    """Return a greeting message."""
    return "Hello! Welcome to the Simple Menu."


def action_time_table(n: int = 5) -> str:
    """Return a multiplication table for n.

    WHY default to 5? -- Gives a useful example when the user
    does not provide a number.
    """
    lines = [f"  {n} x {i} = {n * i}" for i in range(1, 11)]
    return f"Multiplication table for {n}:\n" + "\n".join(lines)


def action_count_letters(text: str) -> str:
    """Count the letters (non-space characters) in a string."""
    count = sum(1 for c in text if c != " ")
    return f"'{text}' has {count} letters (excluding spaces)."


def action_reverse(text: str) -> str:
    """Reverse a string.

    WHY [::-1]? -- Slicing with step -1 walks through the string
    backwards, creating a reversed copy.
    """
    return f"Reversed: '{text[::-1]}'"


# --- Menu system ---

MENU_OPTIONS = {
    "1": "Greet",
    "2": "Multiplication table",
    "3": "Count letters in a word",
    "4": "Reverse a word",
    "5": "Quit",
}


def format_menu() -> str:
    """Build the menu text that the user sees."""
    lines = ["\n=== Simple Menu ==="]
    for key, label in MENU_OPTIONS.items():
        lines.append(f"  {key}. {label}")
    lines.append("")
    return "\n".join(lines)


def execute_choice(choice: str, argument: str = "Python") -> str:
    """Run the action for a given menu choice.

    WHY an argument parameter? -- Some actions need input (a word to
    reverse, a number for the table).  Passing it in makes the
    function testable without needing interactive input.
    """
    choice = choice.strip()

    if choice == "1":
        return action_greet()
    elif choice == "2":
        try:
            n = int(argument)
        except ValueError:
            n = 5
        return action_time_table(n)
    elif choice == "3":
        return action_count_letters(argument)
    elif choice == "4":
        return action_reverse(argument)
    elif choice == "5":
        return "Goodbye!"
    else:
        return f"Unknown option: '{choice}'. Please choose 1-5."


def run_batch(commands: list[str]) -> list[dict]:
    """Process a list of commands in batch mode (for testing).

    Each command is a string like '1' or '3 hello'.
    """
    results = []
    for cmd in commands:
        parts = cmd.strip().split(maxsplit=1)
        if not parts:
            continue

        choice = parts[0]
        argument = parts[1] if len(parts) > 1 else "Python"

        if choice == "5":
            results.append({"command": cmd.strip(), "output": "Goodbye!"})
            break

        output = execute_choice(choice, argument)
        results.append({"command": cmd.strip(), "output": output})

    return results


def parse_args() -> argparse.Namespace:
    """Define command-line options."""
    parser = argparse.ArgumentParser(description="Simple Menu Loop")
    parser.add_argument("--input", default="data/sample_input.txt",
                        help="File with commands (batch mode)")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    """Program entry point."""
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    commands = [line.strip() for line in
                input_path.read_text(encoding="utf-8").splitlines()
                if line.strip()]

    print(format_menu())
    results = run_batch(commands)

    for r in results:
        print(f"  [{r['command']}] => {r['output']}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\n{len(results)} commands processed. Output: {output_path}")


if __name__ == "__main__":
    main()
