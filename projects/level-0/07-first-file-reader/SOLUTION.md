# Solution: Level 0 / Project 07 - First File Reader

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 0 project: First File Reader.

Read a text file and display its contents with line numbers,
plus a summary of line count, word count, and file size.

Concepts: file I/O, open(), encoding, error handling.
"""


def read_file_lines(filepath: str) -> list:
    """Read a file and return all lines (preserving blank lines).

    WHY not strip blank lines? -- In a file reader we want to show
    the file exactly as it is, including empty lines.
    """
    # WHY "with open(...)": The with statement automatically closes the
    # file when the block ends, even if an error occurs.  Without it,
    # you risk leaving files open, which can cause data corruption or
    # "file in use" errors on Windows.
    #
    # WHY encoding="utf-8": Files can be stored in different encodings.
    # Specifying UTF-8 explicitly ensures we read text correctly on all
    # operating systems.  Without it, Windows might default to a different
    # encoding and mangle special characters.
    with open(filepath, encoding="utf-8") as f:
        # WHY .read().splitlines() instead of .readlines(): readlines()
        # keeps the \n at the end of each line.  splitlines() strips it,
        # giving us clean lines without trailing newline characters.
        return f.read().splitlines()


def format_with_line_numbers(lines: list) -> str:
    """Add line numbers to each line for display.

    WHY right-justify the number? -- When files have more than 9 lines,
    lining up the numbers makes the output much easier to read.
    The width is calculated from the total number of lines.
    """
    if not lines:
        return "(empty file)"

    # WHY len(str(len(lines))): If a file has 100 lines, the widest
    # number is "100" which has 3 digits.  str(len(lines)) gives "100",
    # len("100") gives 3.  We use this to right-align all numbers.
    width = len(str(len(lines)))

    numbered = []
    # WHY enumerate with start=1: Humans count lines from 1, not 0.
    for i, line in enumerate(lines, start=1):
        # WHY f-string with >{width}: The format spec >{width} right-
        # justifies the number in a field of `width` characters.
        # For a 100-line file: "  1 | ...", " 10 | ...", "100 | ...".
        numbered.append(f"  {i:>{width}} | {line}")

    return "\n".join(numbered)


def file_summary(filepath: str, lines: list) -> dict:
    """Build a summary dict with stats about the file.

    Includes the file name, line count, word count, and character count.
    """
    # WHY join lines with \n: We reconstruct the full text to count
    # words and characters consistently.
    text = "\n".join(lines)
    word_count = len(text.split())

    # WHY split on both / and \: File paths use / on Mac/Linux and
    # \ on Windows.  Normalising to / first means the split works on
    # any operating system.
    name = filepath.replace("\\", "/").split("/")[-1]

    return {
        "file_name": name,
        "lines": len(lines),
        "words": word_count,
        "characters": len(text),
        # WHY non_empty_lines: Knowing how many lines have actual content
        # vs. how many are blank gives a better picture of file density.
        # sum() with a generator counts lines where strip() is truthy.
        "non_empty_lines": sum(1 for line in lines if line.strip()),
    }


if __name__ == "__main__":
    print("=== File Reader ===")
    filepath = input("Enter a file path to read (e.g. data/sample_input.txt): ")

    # WHY try/except FileNotFoundError: The most common error when reading
    # files is that the path is wrong.  Catching this specific error lets
    # us show a helpful message instead of a scary traceback.
    try:
        lines = read_file_lines(filepath)
    except FileNotFoundError:
        print(f"  File not found: {filepath}")
        print("  Make sure the file exists and the path is correct.")
    else:
        # WHY else on try: The else block runs only if no exception
        # occurred.  This keeps the "success path" clearly separated
        # from the "error path".
        name = filepath.replace("\\", "/").split("/")[-1]
        print(f"\n=== Contents of {name} ===\n")
        print(format_with_line_numbers(lines))

        summary = file_summary(filepath, lines)
        print(f"\n=== Summary ===")
        print(f"  Lines:      {summary['lines']} ({summary['non_empty_lines']} non-empty)")
        print(f"  Words:      {summary['words']}")
        print(f"  Characters: {summary['characters']}")
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `read_file_lines()` uses `open()` with `encoding="utf-8"` | Explicit encoding prevents platform-dependent behaviour. On Windows, the default encoding might not be UTF-8 | Omit encoding — works on many files but silently mangles special characters on some systems |
| `format_with_line_numbers()` dynamically calculates number width | A 10-line file uses 2-digit numbers, a 1000-line file uses 4-digit numbers. Numbers always align cleanly | Hard-code width to 4 — wastes space for small files and breaks for files over 9999 lines |
| `file_summary()` takes `lines` as a parameter instead of reading the file itself | Avoids reading the file twice. `read_file_lines()` handles I/O; `file_summary()` handles analysis | Read the file inside `file_summary()` — duplicates I/O logic and reads the file a second time |
| Returns `"(empty file)"` for empty input | A clear message is better than blank output, which might make the user think something is broken | Return an empty string — technically correct but confusing for beginners |

## Alternative approaches

### Approach B: Using `pathlib.Path` instead of `open()`

```python
from pathlib import Path

def read_file_lines(filepath: str) -> list:
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    return path.read_text(encoding="utf-8").splitlines()

def file_summary(filepath: str, lines: list) -> dict:
    path = Path(filepath)
    text = "\n".join(lines)
    return {
        "file_name": path.name,           # Path handles OS differences
        "lines": len(lines),
        "words": len(text.split()),
        "characters": len(text),
        "non_empty_lines": sum(1 for line in lines if line.strip()),
        "file_size_bytes": path.stat().st_size,  # Bonus: actual file size
    }
```

**Trade-off:** `pathlib.Path` is the modern Python way to work with files. `path.name` extracts the filename automatically (no manual string splitting). `path.read_text()` is a one-liner. However, at Level 0, understanding `open()` and `with` teaches the fundamental file I/O pattern that exists in every programming language. `pathlib` is syntactic sugar you can adopt once you understand the basics.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| File does not exist | `open()` raises `FileNotFoundError`, caught by the try/except in `__main__` — shows a helpful message | Already handled |
| File is empty (0 bytes) | `read_file_lines()` returns `[]`. `format_with_line_numbers([])` returns `"(empty file)"`. `file_summary()` shows 0 lines, 0 words | Already handled |
| File has a different encoding (e.g. Latin-1) | `open(..., encoding="utf-8")` raises `UnicodeDecodeError` for bytes that are not valid UTF-8 | Add a try/except for `UnicodeDecodeError` and suggest trying a different encoding |
| File path has spaces (e.g. "My Documents/file.txt") | Python handles spaces in paths fine. No issue | No fix needed |
| Very large file (gigabytes) | `f.read()` loads the entire file into memory, which could crash | For Level 0 this is fine. Production code would read line-by-line with `for line in f:` |

## Key takeaways

1. **Always use `with open(...)` to read files.** The `with` statement guarantees the file is closed even if an error occurs. Forgetting to close files leads to data corruption and resource leaks. This is non-negotiable in Python.
2. **Specify `encoding="utf-8"` explicitly.** Python's default encoding varies by operating system. Being explicit prevents bugs that only appear on certain machines — a common source of "works on my computer" problems.
3. **Separate I/O from logic.** `read_file_lines()` handles file access; `format_with_line_numbers()` and `file_summary()` handle processing. This separation makes the processing functions testable with fake data — no real files needed.
4. **`enumerate()` gives you both the index and the value in a loop.** Instead of manually tracking `i = 0; i += 1`, `enumerate(lines, start=1)` gives you `(1, "first line"), (2, "second line"), ...` automatically. This is the standard Python way to loop with an index.
