"""
Challenge: CLI Argument Parser
Difficulty: Intermediate
Concepts: string parsing, argument handling, dictionaries, error handling
Time: 40 minutes

Build a simple command-line argument parser from scratch (no argparse).

The parser should:
1. Parse positional arguments in order.
2. Parse flags like `--verbose` (boolean, True if present).
3. Parse named arguments like `--name=value` or `--name value`.
4. Return a dict with all parsed arguments.

Implement the `CLIParser` class with:
- `add_positional(name)` -- add an expected positional argument
- `add_flag(name)` -- add a boolean flag (e.g., --verbose)
- `add_option(name, default=None)` -- add a named option (e.g., --output=file.txt)
- `parse(args)` -- parse a list of argument strings and return a dict

Examples:
    parser = CLIParser()
    parser.add_positional("filename")
    parser.add_flag("verbose")
    parser.add_option("output", default="out.txt")
    result = parser.parse(["input.txt", "--verbose", "--output=result.txt"])
    # {"filename": "input.txt", "verbose": True, "output": "result.txt"}
"""


class CLIParser:
    """Simple CLI argument parser. Implement this class."""

    def __init__(self):
        # Hint: Store lists of positional names, flag names, and option names with defaults.
        pass

    def add_positional(self, name: str) -> None:
        """Register an expected positional argument."""
        pass

    def add_flag(self, name: str) -> None:
        """Register a boolean flag (e.g., --verbose)."""
        pass

    def add_option(self, name: str, default=None) -> None:
        """Register a named option with a default value (e.g., --output=file.txt)."""
        pass

    def parse(self, args: list[str]) -> dict:
        """Parse the argument list and return a dict of parsed values. Implement this method."""
        # Hint: Iterate through args. If it starts with --, it's a flag or option. Otherwise, positional.
        pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Positional arguments
    p1 = CLIParser()
    p1.add_positional("input")
    p1.add_positional("output")
    result = p1.parse(["file.txt", "out.txt"])
    assert result == {"input": "file.txt", "output": "out.txt"}, "Positional args failed"

    # Test 2: Flags
    p2 = CLIParser()
    p2.add_flag("verbose")
    p2.add_flag("debug")
    result = p2.parse(["--verbose"])
    assert result == {"verbose": True, "debug": False}, "Flags failed"

    # Test 3: Options with = syntax
    p3 = CLIParser()
    p3.add_option("output", default="out.txt")
    result = p3.parse(["--output=result.txt"])
    assert result == {"output": "result.txt"}, "Option with = failed"

    # Test 4: Options with space syntax
    p4 = CLIParser()
    p4.add_option("name", default="world")
    result = p4.parse(["--name", "Alice"])
    assert result == {"name": "Alice"}, "Option with space failed"

    # Test 5: Default values
    p5 = CLIParser()
    p5.add_option("output", default="out.txt")
    p5.add_flag("verbose")
    result = p5.parse([])
    assert result == {"output": "out.txt", "verbose": False}, "Defaults failed"

    # Test 6: Mixed arguments
    p6 = CLIParser()
    p6.add_positional("filename")
    p6.add_flag("verbose")
    p6.add_option("output", default="out.txt")
    result = p6.parse(["input.txt", "--verbose", "--output=result.txt"])
    assert result == {"filename": "input.txt", "verbose": True, "output": "result.txt"}, "Mixed args failed"

    print("All tests passed!")
