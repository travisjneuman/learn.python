"""
Solution: CLI Argument Parser

Approach: Track positional arg names, flag names, and option names with defaults.
During parsing, iterate through args. If an arg starts with --, determine if
it is a flag (no value) or an option (with = or followed by a value). Otherwise,
assign it to the next positional slot. Build the result dict from defaults first,
then overwrite with parsed values.
"""


class CLIParser:
    def __init__(self):
        self._positionals: list[str] = []
        self._flags: list[str] = []
        self._options: dict[str, object] = {}  # name -> default

    def add_positional(self, name: str) -> None:
        self._positionals.append(name)

    def add_flag(self, name: str) -> None:
        self._flags.append(name)

    def add_option(self, name: str, default=None) -> None:
        self._options[name] = default

    def parse(self, args: list[str]) -> dict:
        result = {}

        # Initialize defaults for flags (False) and options (their defaults)
        for flag in self._flags:
            result[flag] = False
        for name, default in self._options.items():
            result[name] = default

        positional_index = 0
        i = 0

        while i < len(args):
            arg = args[i]

            if arg.startswith("--"):
                # Could be a flag or an option
                if "=" in arg:
                    # --name=value syntax
                    name, value = arg[2:].split("=", 1)
                    result[name] = value
                elif arg[2:] in self._flags:
                    # Boolean flag
                    result[arg[2:]] = True
                else:
                    # --name value syntax (option with space separator)
                    name = arg[2:]
                    if i + 1 < len(args):
                        i += 1
                        result[name] = args[i]
            else:
                # Positional argument
                if positional_index < len(self._positionals):
                    result[self._positionals[positional_index]] = arg
                    positional_index += 1

            i += 1

        return result


if __name__ == "__main__":
    p1 = CLIParser()
    p1.add_positional("input")
    p1.add_positional("output")
    result = p1.parse(["file.txt", "out.txt"])
    assert result == {"input": "file.txt", "output": "out.txt"}

    p2 = CLIParser()
    p2.add_flag("verbose")
    p2.add_flag("debug")
    result = p2.parse(["--verbose"])
    assert result == {"verbose": True, "debug": False}

    p3 = CLIParser()
    p3.add_option("output", default="out.txt")
    result = p3.parse(["--output=result.txt"])
    assert result == {"output": "result.txt"}

    p4 = CLIParser()
    p4.add_option("name", default="world")
    result = p4.parse(["--name", "Alice"])
    assert result == {"name": "Alice"}

    p5 = CLIParser()
    p5.add_option("output", default="out.txt")
    p5.add_flag("verbose")
    result = p5.parse([])
    assert result == {"output": "out.txt", "verbose": False}

    p6 = CLIParser()
    p6.add_positional("filename")
    p6.add_flag("verbose")
    p6.add_option("output", default="out.txt")
    result = p6.parse(["input.txt", "--verbose", "--output=result.txt"])
    assert result == {"filename": "input.txt", "verbose": True, "output": "result.txt"}

    print("All tests passed!")
