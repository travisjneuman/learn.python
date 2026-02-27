"""Level 0 project: Mini Toolkit.

Combine three small utilities from earlier projects into one
command-line tool: word count, line duplicates, and string cleaning.

Concepts: combining functions, argparse subcommands, code reuse.
"""


import argparse
import json
from pathlib import Path


# --- Tool 1: Word Counter ---

def count_words(text: str) -> dict[str, int]:
    """Count words, lines, and characters in text.

    WHY return a dict? -- Bundling results in a dict makes the
    function useful for both printing and saving to JSON.
    """
    words = text.split()
    lines = text.splitlines()
    return {
        "words": len(words),
        "lines": len(lines),
        "characters": len(text),
    }


# --- Tool 2: Duplicate Finder ---

def find_duplicates(lines: list[str]) -> list[dict[str, str | int]]:
    """Find lines that appear more than once.

    WHY track counts with a dict? -- A dictionary lets us count
    occurrences in a single pass through the list.
    """
    counts = {}
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped in counts:
            counts[stripped] += 1
        else:
            counts[stripped] = 1

    return [
        {"text": text, "count": count}
        for text, count in counts.items()
        if count > 1
    ]


# --- Tool 3: String Cleaner ---

def clean_string(text: str) -> str:
    """Strip, lowercase, and remove non-alphanumeric characters.

    WHY chain operations? -- Each step does one thing.  Chaining
    them creates a clear pipeline.
    """
    result = text.strip().lower()
    cleaned = []
    for char in result:
        if char.isalnum() or char == " ":
            cleaned.append(char)
    output = "".join(cleaned)
    # Collapse multiple spaces.
    while "  " in output:
        output = output.replace("  ", " ")
    return output


# --- Toolkit dispatcher ---

def run_tool(tool_name: str, text: str) -> dict[str, object]:
    """Run one of the three tools and return results.

    WHY a dispatcher? -- A single function that routes to the right
    tool based on a name string.  This is a simple version of the
    command pattern used in real applications.
    """
    if tool_name == "wordcount":
        return {"tool": "wordcount", "result": count_words(text)}

    elif tool_name == "duplicates":
        lines = text.splitlines()
        dupes = find_duplicates(lines)
        return {"tool": "duplicates", "result": dupes}

    elif tool_name == "clean":
        lines = text.splitlines()
        cleaned = [clean_string(line) for line in lines if line.strip()]
        return {"tool": "clean", "result": cleaned}

    else:
        return {"tool": tool_name, "error": f"Unknown tool: {tool_name}"}


def run_all_tools(text: str) -> dict[str, object]:
    """Run all three tools on the same text and collect results.

    WHY run all? -- The default mode gives a complete analysis,
    showing the learner how multiple utilities work together.
    """
    return {
        "wordcount": count_words(text),
        "duplicates": find_duplicates(text.splitlines()),
        "clean_preview": [clean_string(line) for line in text.splitlines()[:3] if line.strip()],
    }


def parse_args() -> argparse.Namespace:
    """Define command-line options."""
    parser = argparse.ArgumentParser(description="Level 0 Mini Toolkit")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    parser.add_argument("--tool", choices=["wordcount", "duplicates", "clean", "all"],
                        default="all", help="Which tool to run")
    return parser.parse_args()


def main() -> None:
    """Program entry point."""
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
