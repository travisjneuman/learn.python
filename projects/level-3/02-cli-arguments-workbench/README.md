# Level 3 / Project 02 - CLI Arguments Workbench
Home: [README](../../../README.md)

> **Try in Browser:** [Practice similar concepts online](../../browser/level-2.html?ex=2) — browser exercises cover Level 2 topics

## Before You Start

Recall these prerequisites before diving in:
- Can you use `argparse` to create a basic command-line interface with required and optional arguments?
- Can you write a class with an `__init__` method?

**Estimated time:** 30 minutes

## Focus
- robust argparse patterns

## Why this project exists
This project gives you level-appropriate practice in a realistic operations context.
Goal: run the baseline, alter behavior, break one assumption, recover safely, and explain the fix.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-3/02-cli-arguments-workbench
python project.py temp --c-to-f 100
python project.py --json dist --km-to-mi 42.195
python project.py -v weight --kg-to-lbs 70
pytest -q
```

## Expected terminal output
```text
100 C = 212.0 F
{"input_value": 42.195, ...}
70 kg = 154.3234 lbs
Formula: lbs = kg * 2.20462
14 passed
```

## Expected artifacts
- Conversion results on stdout
- Passing tests
- Updated `notes.md`

## Worked Example

Here is a similar (but different) problem, solved step by step.

**Problem:** Write a CLI tool that converts between file size units (bytes, KB, MB, GB).

**Step 1: Set up argparse with a subcommand.**

```python
import argparse

def build_parser():
    parser = argparse.ArgumentParser(description="File size converter")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    size_cmd = sub.add_parser("convert", help="Convert file sizes")
    size_cmd.add_argument("value", type=float)
    size_cmd.add_argument("--from-unit", choices=["B", "KB", "MB", "GB"], required=True)
    size_cmd.add_argument("--to-unit", choices=["B", "KB", "MB", "GB"], required=True)
    return parser
```

**Step 2: Write the conversion through a common unit (bytes).**

```python
MULTIPLIERS = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3}

def convert_size(value, from_unit, to_unit):
    bytes_value = value * MULTIPLIERS[from_unit]
    return bytes_value / MULTIPLIERS[to_unit]
```

**Step 3: Wire it together.** `python tool.py convert 1 --from-unit GB --to-unit MB` outputs `1024.0`.

**The thought process:** Argparse handles parsing and validation. The hub-and-spoke pattern (through bytes) handles conversion. Subcommands make the CLI extensible. This is the same approach the CLI workbench uses.

## Design First
Before writing code, sketch your approach in `notes.md`:
- What functions or classes do you need?
- What data structures will you use?
- What's the flow from input to output?
- What could go wrong?

---

**Checkpoint:** Baseline code runs and all tests pass. Commit your work before continuing.

## Alter it (required) — Extension
1. Add a new conversion category — pick a domain that interests you.
2. What output formatting options would make this tool more useful?
3. Can you make the conversion direction configurable instead of hardcoded?

## Break it (required) — Core
1. Try feeding the tool unexpected input types — what happens?
2. Can you find an edge case where validation fails silently?
3. What happens when batch input is malformed?

## Fix it (required) — Core
1. Improve the error experience for the most confusing failure you found.
2. Handle a data format edge case the tool currently misses.
3. Add domain-appropriate input validation.

---

**Checkpoint:** All modifications done, tests still pass. Good time to review your changes.

## Explain it (teach-back)
1. What does `add_mutually_exclusive_group` do and why use it?
2. How does a custom argparse type function (like `positive_float`) work?
3. What is a `@dataclass` and why is it better than a plain dict for `ConversionResult`?
4. How do argparse subcommands differ from positional arguments?

## Mastery check
You can move on when you can:
- build a CLI with subcommands and mutually exclusive groups,
- write custom argparse type validators,
- use `@dataclass` for structured return values,
- process batch operations from a JSON file.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Files and Paths](../../../concepts/files-and-paths.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts:

- "I am working on CLI Arguments Workbench. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to add subcommands to argparse. Can you show me a minimal example with two subcommands, using a topic different from unit conversion?"
- "Can you explain what `add_mutually_exclusive_group` does in argparse with a simple example?"

---

| [← Prev](../01-package-layout-starter/README.md) | [Home](../../../README.md) | [Next →](../03-logging-baseline-tool/README.md) |
|:---|:---:|---:|
