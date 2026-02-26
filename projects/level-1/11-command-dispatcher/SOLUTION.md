# Solution: Level 1 / Project 11 - Command Dispatcher

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 1 project: Command Dispatcher.

Map command strings to handler functions and execute them with arguments.
A simple implementation of the command pattern.

Concepts: functions as values, dictionaries mapping strings to functions, *args.
"""


import argparse
import json
from pathlib import Path


# --- Command handler functions ---

# WHY separate handler functions: Each command does one small thing.
# Having them as standalone functions means they are individually
# testable and can be composed or reused elsewhere.

# WHY cmd_upper: Demonstrates the simplest possible command — call
# a single built-in method and return the result.
def cmd_upper(text: str) -> str:
    """Convert text to uppercase."""
    return text.upper()


# WHY cmd_lower: Paired with cmd_upper to show that multiple commands
# can share the same interface (take a string, return a string).
def cmd_lower(text: str) -> str:
    """Convert text to lowercase."""
    return text.lower()


# WHY cmd_reverse: String reversal with [::-1] is a classic Python
# idiom.  It introduces slice notation with a step value.
def cmd_reverse(text: str) -> str:
    """Reverse the text."""
    # WHY [::-1]: This is a slice with step -1, which starts at the
    # end and walks backwards.  "abc"[::-1] produces "cba".
    return text[::-1]


# WHY cmd_count_words: Shows that a command can return a different
# format (a descriptive string) rather than just a transformation
# of the input.
def cmd_count_words(text: str) -> str:
    """Count words in the text."""
    # WHY split() with no args: Splitting on whitespace handles
    # multiple spaces, tabs, and newlines correctly.
    count = len(text.split())
    return f"{count} words"


# WHY cmd_title: Title case is useful for formatting names and
# headings.  It capitalises the first letter of every word.
def cmd_title(text: str) -> str:
    """Convert text to title case."""
    return text.title()


# --- Dispatcher ---

# WHY a dict of functions: This is the command pattern — we map
# string names to callable functions.  Adding a new command only
# requires adding one entry to this dict.  No if/elif needed.
COMMANDS = {
    "upper": cmd_upper,
    "lower": cmd_lower,
    "reverse": cmd_reverse,
    "count": cmd_count_words,
    "title": cmd_title,
}


# WHY dispatch: This is the heart of the project.  It looks up a
# command name in the COMMANDS dict, gets the corresponding function,
# and calls it.  This demonstrates that functions are first-class
# objects in Python — they can be stored in dicts and called later.
def dispatch(command: str, argument: str) -> dict:
    """Look up a command by name and execute it.

    Returns a dict with the command, argument, and result (or error).
    """
    command = command.strip().lower()
    argument = argument.strip()

    if command not in COMMANDS:
        # WHY list available commands: Telling the user what commands
        # exist helps them fix the typo without reading documentation.
        return {
            "command": command,
            "argument": argument,
            "error": f"Unknown command: {command}. Available: {', '.join(COMMANDS.keys())}",
        }

    # WHY handler = COMMANDS[command]: This retrieves the function
    # object (not its result).  cmd_upper is a function; COMMANDS["upper"]
    # gives us that same function.  Then handler(argument) calls it.
    handler = COMMANDS[command]
    result = handler(argument)

    return {
        "command": command,
        "argument": argument,
        "result": result,
    }


# WHY list_commands: Provides an API for discovering available
# commands.  Useful for help text and --list flags.
def list_commands() -> list[str]:
    """Return a list of available command names."""
    return list(COMMANDS.keys())


# WHY process_file: Reads command lines from a file, splits each
# into command + argument, and dispatches.
def process_file(path: Path) -> list[dict]:
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

        # WHY split(maxsplit=1): The first word is the command name;
        # everything after it is the argument.  maxsplit=1 ensures
        # "upper hello world" splits into ["upper", "hello world"],
        # not ["upper", "hello", "world"].
        parts = stripped.split(maxsplit=1)
        command = parts[0]
        # WHY default to "": A command with no argument (just "upper")
        # should not crash.  An empty string is a safe default.
        argument = parts[1] if len(parts) > 1 else ""

        results.append(dispatch(command, argument))

    return results


# WHY parse_args: Standard argparse for flexible input/output paths.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Command Dispatcher")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


# WHY main: Orchestrates reading, dispatching, displaying, and saving.
def main() -> None:
    args = parse_args()
    results = process_file(Path(args.input))

    print("=== Command Dispatcher ===\n")
    print(f"  Available commands: {', '.join(list_commands())}\n")

    for r in results:
        if "error" in r:
            print(f"  ERROR: {r['error']}")
        else:
            # WHY !r: The !r format flag shows the repr() of the value,
            # adding quotes around strings.  This makes whitespace
            # and empty strings visible in the output.
            print(f"  {r['command']}({r['argument']!r}) => {r['result']!r}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Dict mapping command names to functions | Adding a command is one dict entry; the dispatch logic never changes | If/elif chain — requires modifying the dispatch function for every new command |
| Functions as first-class values in the dict | Demonstrates Python's ability to treat functions as data; the same pattern powers web frameworks and plugin systems | Lambda functions in the dict — works but harder to test and document individually |
| Return error dict for unknown commands | Lets the caller decide how to handle errors (display, log, retry) without crashing the program | Raise KeyError — would require try/except in every caller |
| All handlers share the same signature (`str -> str`) | Uniform interface means the dispatcher does not need special-case logic per command | Mixed signatures — requires the dispatcher to inspect and adapt arguments per command |

## Alternative approaches

### Approach B: If/elif dispatcher

```python
def dispatch_if_elif(command: str, argument: str) -> dict:
    """Dispatch using if/elif instead of a dict."""
    command = command.strip().lower()
    argument = argument.strip()

    # WHY this approach exists: It is the most intuitive for beginners.
    # You check each command name and call the right function.
    if command == "upper":
        result = argument.upper()
    elif command == "lower":
        result = argument.lower()
    elif command == "reverse":
        result = argument[::-1]
    elif command == "count":
        result = f"{len(argument.split())} words"
    elif command == "title":
        result = argument.title()
    else:
        return {"command": command, "argument": argument,
                "error": f"Unknown command: {command}"}

    return {"command": command, "argument": argument, "result": result}
```

**Trade-off:** The if/elif approach is simpler to understand — each branch is explicit. But it does not scale: adding 20 commands means 20 elif branches. The dict approach scales better because adding a command is one line (`"newcmd": cmd_newcmd`), and the dispatch logic stays the same. The dict approach also makes it easy to list available commands, which the if/elif approach cannot do without duplicating the command names.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Unknown command like `"fly to the moon"` | `dispatch()` returns an error dict listing available commands | The `if command not in COMMANDS` check handles this |
| Command with no argument (just `"upper"`) | `parts[1] if len(parts) > 1 else ""` provides an empty string; `cmd_upper("")` returns `""` | The default argument is already in place |
| Empty line in input file | `if not stripped: continue` skips it | The blank-line guard is already in place |
| Case mismatch (`"UPPER"` instead of `"upper"`) | `command.strip().lower()` normalises to lowercase before lookup | The case normalisation is built into `dispatch()` |

## Key takeaways

1. **Functions are first-class objects in Python.** You can store them in variables, put them in dicts, pass them to other functions, and call them later. `COMMANDS["upper"]` retrieves the function `cmd_upper`; `COMMANDS["upper"]("hello")` calls it. This is one of the most powerful features of Python.
2. **The command pattern (dict dispatch) is everywhere.** Web frameworks map URL paths to handler functions. CLI frameworks map subcommands to functions. Plugin systems map names to loaded modules. The pattern you learned here is the foundation of all of them.
3. **Uniform function signatures enable generic dispatch.** Because all handlers take `str` and return `str`, the dispatcher does not need to know anything about what each command does. This "program to an interface" principle is central to good software design and becomes even more important with classes and protocols in later levels.
