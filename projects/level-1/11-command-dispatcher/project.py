"""Level 1 project: Command Dispatcher.

Map command strings to handler functions and execute them with arguments.
A simple implementation of the command pattern.

Concepts: functions as values, dictionaries mapping strings to functions, *args.
"""


import argparse
import json
from pathlib import Path


# --- Command handler functions ---

def cmd_upper(text: str) -> str:
    """Convert text to uppercase."""
    return text.upper()


def cmd_lower(text: str) -> str:
    """Convert text to lowercase."""
    return text.lower()


def cmd_reverse(text: str) -> str:
    """Reverse the text."""
    return text[::-1]


def cmd_count_words(text: str) -> str:
    """Count words in the text."""
    count = len(text.split())
    return f"{count} words"


def cmd_title(text: str) -> str:
    """Convert text to title case."""
    return text.title()


# --- Dispatcher ---

# WHY a dict of functions? -- This is the command pattern: we map
# string names to callable functions.  Adding a new command only
# requires adding one entry to this dict.
COMMANDS = {
    "upper": cmd_upper,
    "lower": cmd_lower,
    "reverse": cmd_reverse,
    "count": cmd_count_words,
    "title": cmd_title,
}


def dispatch(command: str, argument: str) -> dict[str, str]:
    """Look up a command by name and execute it.

    Returns a dict with the command, argument, and result (or error).
    """
    command = command.strip().lower()
    argument = argument.strip()

    if command not in COMMANDS:
        return {
            "command": command,
            "argument": argument,
            "error": f"Unknown command: {command}. Available: {', '.join(COMMANDS.keys())}",
        }

    handler = COMMANDS[command]
    result = handler(argument)

    return {
        "command": command,
        "argument": argument,
        "result": result,
    }


def list_commands() -> list[str]:
    """Return a list of available command names."""
    return list(COMMANDS.keys())


def process_file(path: Path) -> list[dict[str, str]]:
    """Read command lines from a file and execute each.

    Expected format: COMMAND argument text here
    Example: upper hello world
    """
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    results = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        parts = stripped.split(maxsplit=1)
        command = parts[0]
        argument = parts[1] if len(parts) > 1 else ""

        results.append(dispatch(command, argument))

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Command Dispatcher")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = process_file(Path(args.input))

    print("=== Command Dispatcher ===\n")
    print(f"  Available commands: {', '.join(list_commands())}\n")

    for r in results:
        if "error" in r:
            print(f"  ERROR: {r['error']}")
        else:
            print(f"  {r['command']}({r['argument']!r}) => {r['result']!r}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
