"""Level 0 project: First File Reader.

Read a text file and display its contents with line numbers,
plus a summary of line count, word count, and file size.

Concepts: file I/O, open(), encoding, error handling.
"""


def read_file_lines(filepath: str) -> list[str]:
    """Read a file and return all lines (preserving blank lines).

    WHY not strip blank lines? -- In a file reader we want to show
    the file exactly as it is, including empty lines.
    """
    with open(filepath, encoding="utf-8") as f:
        return f.read().splitlines()


def format_with_line_numbers(lines: list[str]) -> str:
    """Add line numbers to each line for display.

    WHY right-justify the number? -- When files have more than 9 lines,
    lining up the numbers makes the output much easier to read.
    The width is calculated from the total number of lines.
    """
    if not lines:
        return "(empty file)"

    # Figure out how wide the line numbers need to be.
    width = len(str(len(lines)))

    numbered = []
    for i, line in enumerate(lines, start=1):
        # f-string with >{width} right-justifies the number.
        numbered.append(f"  {i:>{width}} | {line}")

    return "\n".join(numbered)


def file_summary(filepath: str, lines: list[str]) -> dict[str, str | int]:
    """Build a summary dict with stats about the file.

    Includes the file name, line count, word count, and character count.
    """
    text = "\n".join(lines)
    word_count = len(text.split())

    # Extract just the file name from the path.
    # We split on both / and \ to handle any operating system.
    name = filepath.replace("\\", "/").split("/")[-1]

    return {
        "file_name": name,
        "lines": len(lines),
        "words": word_count,
        "characters": len(text),
        "non_empty_lines": sum(1 for line in lines if line.strip()),
    }


# This guard means the code below only runs when you execute the file
# directly (python project.py), NOT when another file imports it.
if __name__ == "__main__":
    print("=== File Reader ===")
    filepath = input("Enter a file path to read (e.g. data/sample_input.txt): ")

    try:
        lines = read_file_lines(filepath)
    except FileNotFoundError:
        print(f"  File not found: {filepath}")
        print("  Make sure the file exists and the path is correct.")
    else:
        # Display file contents with line numbers.
        name = filepath.replace("\\", "/").split("/")[-1]
        print(f"\n=== Contents of {name} ===\n")
        print(format_with_line_numbers(lines))

        # Display the summary.
        summary = file_summary(filepath, lines)
        print(f"\n=== Summary ===")
        print(f"  Lines:      {summary['lines']} ({summary['non_empty_lines']} non-empty)")
        print(f"  Words:      {summary['words']}")
        print(f"  Characters: {summary['characters']}")
