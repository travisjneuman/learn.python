# Solution: Level 0 / Project 15 - Level 0 Mini Toolkit

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 0 project: Mini Toolkit.

Combine three small utilities from earlier projects into one
command-line tool: word count, line duplicates, and string cleaning.

Concepts: combining functions, argparse subcommands, code reuse.
"""


import argparse
import json
from pathlib import Path


# --- Tool 1: Word Counter ---

def count_words(text: str) -> dict:
    """Count words, lines, and characters in text.

    WHY return a dict? -- Bundling results in a dict makes the
    function useful for both printing and saving to JSON.  The caller
    does not need to know which metric to request — they get all three.
    """
    words = text.split()
    lines = text.splitlines()
    return {
        "words": len(words),
        "lines": len(lines),
        "characters": len(text),
    }


# --- Tool 2: Duplicate Finder ---

def find_duplicates(lines: list[str]) -> list[dict]:
    """Find lines that appear more than once.

    WHY track counts with a dict? -- A dictionary lets us count
    occurrences in a single pass through the list.  This is the
    same counting pattern from Project 10.
    """
    counts = {}
    for line in lines:
        stripped = line.strip()
        # WHY skip empty lines: Blank lines appearing multiple times is
        # noise, not meaningful duplication.
        if not stripped:
            continue
        if stripped in counts:
            counts[stripped] += 1
        else:
            counts[stripped] = 1

    # WHY list comprehension with filter: We only want items where count > 1.
    # The comprehension builds the result list in one expression.
    return [
        {"text": text, "count": count}
        for text, count in counts.items()
        if count > 1
    ]


# --- Tool 3: String Cleaner ---

def clean_string(text: str) -> str:
    """Strip, lowercase, and remove non-alphanumeric characters.

    WHY chain operations? -- Each step does one thing.  Chaining
    them creates a clear pipeline.  This is the same pattern
    from Project 08, condensed into one function.
    """
    # WHY strip().lower() first: Remove outer whitespace and normalise
    # case before filtering characters.
    result = text.strip().lower()
    cleaned = []
    for char in result:
        # WHY isalnum() or space: Keep letters, digits, and spaces.
        # Everything else (punctuation, symbols) is removed.
        if char.isalnum() or char == " ":
            cleaned.append(char)
    output = "".join(cleaned)
    # WHY collapse spaces: Removing special characters can leave gaps.
    # "hello...world" becomes "helloworld" (no gap), but
    # "hello - world" becomes "hello  world" (double space).
    # Collapsing fixes the latter case.
    while "  " in output:
        output = output.replace("  ", " ")
    return output


# --- Toolkit dispatcher ---

def run_tool(tool_name: str, text: str) -> dict:
    """Run one of the three tools and return results.

    WHY a dispatcher? -- A single function that routes to the right
    tool based on a name string.  This is a simple version of the
    command pattern used in real applications like git (git add,
    git commit, git push are all subcommands dispatched by name).
    """
    if tool_name == "wordcount":
        return {"tool": "wordcount", "result": count_words(text)}

    elif tool_name == "duplicates":
        lines = text.splitlines()
        dupes = find_duplicates(lines)
        return {"tool": "duplicates", "result": dupes}

    elif tool_name == "clean":
        lines = text.splitlines()
        # WHY list comprehension with filter: Skip empty lines before
        # cleaning to avoid producing empty strings in the output.
        cleaned = [clean_string(line) for line in lines if line.strip()]
        return {"tool": "clean", "result": cleaned}

    else:
        # WHY return error dict: Unknown tool names produce a clear error
        # message instead of a crash.  The caller can check for "error".
        return {"tool": tool_name, "error": f"Unknown tool: {tool_name}"}


def run_all_tools(text: str) -> dict:
    """Run all three tools on the same text and collect results.

    WHY run all? -- The default mode gives a complete analysis,
    showing the learner how multiple utilities work together.
    This is like running `wc`, `sort -u`, and `tr` in a Unix pipeline.
    """
    return {
        "wordcount": count_words(text),
        "duplicates": find_duplicates(text.splitlines()),
        # WHY only first 3 lines for clean_preview: The full cleaning
        # output could be very long.  A preview shows the tool works
        # without flooding the terminal.
        "clean_preview": [clean_string(line) for line in text.splitlines()[:3] if line.strip()],
    }


def parse_args() -> argparse.Namespace:
    """Define command-line options.

    WHY argparse choices: The choices=["wordcount", "duplicates", "clean", "all"]
    parameter makes argparse reject invalid tool names automatically.
    The user gets a helpful error message for free.
    """
    parser = argparse.ArgumentParser(description="Level 0 Mini Toolkit")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    parser.add_argument("--tool", choices=["wordcount", "duplicates", "clean", "all"],
                        default="all", help="Which tool to run")
    return parser.parse_args()


def main() -> None:
    """Program entry point.

    WHY main() orchestrates everything: It reads the file, runs the
    requested tool, displays results, and saves output.  Each step
    calls a focused function.  main() is the conductor; the functions
    are the musicians.
    """
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    text = input_path.read_text(encoding="utf-8")

    if args.tool == "all":
        results = run_all_tools(text)
        print("=== Mini Toolkit: All Tools ===\n")
        wc = results["wordcount"]
        print(f"  Word Count: {wc['words']} words, {wc['lines']} lines, {wc['characters']} chars")
        dupes = results["duplicates"]
        print(f"  Duplicates: {len(dupes)} found")
        for d in dupes:
            print(f"    '{d['text']}' x{d['count']}")
        print(f"  Clean preview: {results['clean_preview'][:3]}")
    else:
        results = run_tool(args.tool, text)
        print(f"=== Tool: {args.tool} ===")
        print(json.dumps(results, indent=2))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nOutput written to {output_path}")


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Three independent tool functions | Each tool can be tested in isolation: `assert count_words("hi there")["words"] == 2`. No coupling between tools | One monolithic function that does everything — impossible to test individual tools |
| `run_tool()` dispatcher function | Routes tool name to implementation. Adding a 4th tool means adding one elif branch and one function | Direct if/elif in `main()` — mixes routing logic with I/O, harder to test |
| `run_all_tools()` for the default mode | Gives a complete overview with one command. Shows how small utilities compose into a dashboard | Require the user to run each tool separately — more commands, less convenient |
| `argparse` with `choices` parameter | Rejects invalid tool names at the argument-parsing level with a helpful auto-generated error message | Manual validation in `run_tool()` — works but requires writing custom error messages |
| Functions reused from earlier projects (06, 08, 10) | Demonstrates code reuse. The same counting, cleaning, and duplicate-finding patterns appear again, reinforcing learning | Write new implementations — misses the pedagogical point of combining what you already know |

## Alternative approaches

### Approach B: Dict dispatch with tool registry

```python
# Register tools in a dict mapping names to (function, description) pairs.
TOOLS = {
    "wordcount": {
        "fn": lambda text: {"tool": "wordcount", "result": count_words(text)},
        "description": "Count words, lines, and characters",
    },
    "duplicates": {
        "fn": lambda text: {"tool": "duplicates", "result": find_duplicates(text.splitlines())},
        "description": "Find duplicate lines",
    },
    "clean": {
        "fn": lambda text: {"tool": "clean", "result": [clean_string(l) for l in text.splitlines() if l.strip()]},
        "description": "Clean and normalize text",
    },
}

def run_tool(tool_name: str, text: str) -> dict:
    if tool_name not in TOOLS:
        return {"tool": tool_name, "error": f"Unknown tool: {tool_name}. Available: {list(TOOLS.keys())}"}
    return TOOLS[tool_name]["fn"](text)

def format_menu() -> str:
    lines = ["Available tools:"]
    for name, info in TOOLS.items():
        lines.append(f"  {name}: {info['description']}")
    return "\n".join(lines)
```

**Trade-off:** A tool registry makes adding new tools purely declarative — add one dict entry and the tool appears in the menu, help text, and validation automatically. This is the "plugin architecture" pattern used by real CLI tools like `git`, `docker`, and `kubectl`. However, it requires understanding lambdas, nested dicts, and functions-as-values, which may be too much at Level 0. The if/elif approach makes the routing explicit and easy to follow.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Unknown tool name via `run_tool()` | Returns `{"tool": "nope", "error": "Unknown tool: nope"}`. No crash | Already handled by the else branch. Additionally, `argparse choices` prevents this from the command line |
| Empty file as input | `count_words("")` returns `{"words": 0, "lines": 0, "characters": 0}`. `find_duplicates([])` returns `[]`. `clean_string("")` returns `""`. No crash | Already handled — all tools produce sensible empty results |
| `--tool` flag omitted | `argparse` uses `default="all"`, running all tools. This is intentional and documented in the help text | Already handled by the default parameter |
| Very large file | All tools process the full text in memory. For a gigabyte file, this could exhaust RAM | For Level 0 this is acceptable. Production code would process line-by-line or use streaming |
| File with mixed line endings (\\r\\n and \\n) | `splitlines()` handles all line-ending styles correctly. No issue | Already handled by using `splitlines()` instead of `split("\\n")` |

## Key takeaways

1. **Small functions compose into powerful programs.** `count_words()`, `find_duplicates()`, and `clean_string()` are simple individually. Combined in `run_all_tools()`, they create a multi-function text analysis suite. This is the core lesson of Level 0: build small, test small, combine into big.
2. **The dispatcher pattern routes commands to handlers.** `run_tool("wordcount", text)` calls `count_words()`. This is the same pattern behind `git add`, `docker run`, and every CLI tool with subcommands. Understanding it here prepares you for building real tools.
3. **`argparse` with `choices` gives you input validation for free.** Instead of writing `if tool not in ["wordcount", "duplicates", "clean"]: raise ValueError(...)`, `argparse` does it automatically and generates a helpful error message. Leverage library features instead of reimplementing them.
4. **This project is a capstone — everything from Level 0 comes together.** Word counting from Project 06, duplicate detection from Project 10, string cleaning from Project 08, menu dispatch from Project 11, file I/O from Project 07, and argparse from Project 13. If you understand this project, you have mastered the fundamentals. Level 1 builds on everything you learned here.
