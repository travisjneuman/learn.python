# Solution: Level 0 / Project 11 - Simple Menu Loop

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 0 project: Simple Menu Loop.

Present a numbered menu to the user, execute their choice,
and loop until they choose to quit.  Reads commands from a
file for batch/test mode, or from stdin for interactive mode.

Concepts: while loops, if/elif/else, break, functions as menu actions.
"""


import argparse
import json
from pathlib import Path


# --- Menu action functions ---
# WHY separate functions: Each action is isolated and testable.
# assert "Hello" in action_greet() works without running the full menu.
# Adding a new action means writing one function and one elif branch.

def action_greet() -> str:
    """Return a greeting message."""
    return "Hello! Welcome to the Simple Menu."


def action_time_table(n: int = 5) -> str:
    """Return a multiplication table for n.

    WHY default to 5? -- Gives a useful example when the user
    does not provide a number.
    """
    # WHY list comprehension: It builds all 10 lines in one expression.
    # Each line computes n * i for i from 1 to 10.
    lines = [f"  {n} x {i} = {n * i}" for i in range(1, 11)]
    return f"Multiplication table for {n}:\n" + "\n".join(lines)


def action_count_letters(text: str) -> str:
    """Count the letters (non-space characters) in a string."""
    # WHY sum with generator: sum(1 for c in text if c != " ") counts
    # characters that are not spaces.  This is a compact counting pattern.
    count = sum(1 for c in text if c != " ")
    return f"'{text}' has {count} letters (excluding spaces)."


def action_reverse(text: str) -> str:
    """Reverse a string.

    WHY [::-1]? -- Slicing with step -1 walks through the string
    backwards, creating a reversed copy.  It is a Python idiom.
    """
    return f"Reversed: '{text[::-1]}'"


# --- Menu system ---

# WHY a dict for menu options: The menu text and option numbers are
# defined in one place.  If you add option "6", you update one dict
# and add one elif branch — nothing else changes.
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

    # WHY if/elif chain: At Level 0, an explicit chain makes the
    # control flow visible.  Each branch calls one action function.
    # In a later project you could refactor this into a dict dispatch.
    if choice == "1":
        return action_greet()
    elif choice == "2":
        # WHY try/except: The argument might not be a valid number.
        # Falling back to 5 keeps the program running instead of crashing.
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
        # WHY return an error message instead of raising: Keeps the menu
        # loop running.  The user can try again without restarting.
        return f"Unknown option: '{choice}'. Please choose 1-5."


def run_batch(commands: list[str]) -> list[dict]:
    """Process a list of commands in batch mode (for testing).

    Each command is a string like '1' or '3 hello'.
    """
    results = []
    for cmd in commands:
        # WHY split(maxsplit=1): This splits into at most 2 parts.
        # "3 hello world" becomes ["3", "hello world"] — the argument
        # can contain spaces without being split further.
        parts = cmd.strip().split(maxsplit=1)
        if not parts:
            continue

        choice = parts[0]
        argument = parts[1] if len(parts) > 1 else "Python"

        # WHY break on "5": Quit should stop processing remaining commands.
        # Commands after "5" in the batch file are intentionally ignored.
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
    """Program entry point.

    WHY a main() function? -- It groups the top-level logic in one place.
    The if __name__ == "__main__" block just calls main().  This pattern
    makes the program importable without side effects.
    """
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Each action is a separate function | `action_greet()`, `action_reverse()`, etc. are independently testable. Adding a new action is one function + one elif | Inline all logic in `execute_choice()` — makes the function long and hard to test individual actions |
| `execute_choice()` takes an `argument` parameter | Makes the function testable without `input()`. Tests pass `execute_choice("4", "hello")` directly | Use `input()` inside each action — requires mocking stdin for tests, which is complex at Level 0 |
| `run_batch()` processes a list of command strings | Enables file-based testing and repeatable runs. The same commands produce the same results every time | Interactive-only mode — harder to test, cannot reproduce results |
| `MENU_OPTIONS` is a module-level dict | Defines the menu structure in one place. Both `format_menu()` and documentation use the same source of truth | Hard-code the menu text in `format_menu()` — duplicates the option list |

## Alternative approaches

### Approach B: Dict dispatch instead of if/elif

```python
def execute_choice(choice: str, argument: str = "Python") -> str:
    # Map choice strings directly to functions.
    actions = {
        "1": lambda arg: action_greet(),
        "2": lambda arg: action_time_table(int(arg) if arg.isdigit() else 5),
        "3": lambda arg: action_count_letters(arg),
        "4": lambda arg: action_reverse(arg),
        "5": lambda arg: "Goodbye!",
    }

    choice = choice.strip()
    if choice in actions:
        return actions[choice](argument)
    return f"Unknown option: '{choice}'. Please choose 1-5."
```

**Trade-off:** Dict dispatch eliminates the if/elif chain entirely. Adding a new action is one dict entry instead of a new branch. However, the `lambda` wrappers add complexity — some actions ignore the argument, others need type conversion. At Level 0, the if/elif chain makes the control flow explicit and easy to follow. Dict dispatch is the natural next step once you are comfortable with functions-as-values.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| User enters choice `99` | `execute_choice("99")` returns `"Unknown option: '99'. Please choose 1-5."` | Already handled by the else branch |
| Batch file has `5` (quit) in the middle | `run_batch()` processes commands up to and including `5`, then stops. Later commands are ignored | Already handled by the `break` statement |
| Action `2` receives a non-numeric argument | `int(argument)` raises `ValueError`, caught by try/except. Falls back to `n = 5` | Already handled |
| Batch file is empty | `commands` is an empty list. `run_batch([])` returns `[]`. No crash | Already handled — the for loop simply does not execute |
| Command has no argument (e.g. just `"3"`) | `parts` has length 1. `argument` defaults to `"Python"`. `action_count_letters("Python")` works fine | Already handled by the default argument |

## Key takeaways

1. **Menu-driven programs follow the loop-dispatch-execute pattern.** Show options, get a choice, run the matching action, repeat. This is the architecture behind every CLI tool, game menu, and interactive console. Understanding it here prepares you for building real tools.
2. **`split(maxsplit=1)` is essential for command parsing.** It splits on the first space only, keeping the rest of the string intact. `"3 hello world".split(maxsplit=1)` gives `["3", "hello world"]`. Without `maxsplit`, multi-word arguments would be split apart.
3. **Batch mode makes programs testable.** Reading commands from a file instead of `input()` means you can run the same test scenario repeatedly. This is the foundation of automated testing — predictable inputs produce predictable outputs.
4. **Functions as building blocks compose into programs.** `action_greet()`, `action_reverse()`, `execute_choice()`, `run_batch()`, and `main()` are layers. Each layer calls the one below it. This layered structure is how professional software is built.
