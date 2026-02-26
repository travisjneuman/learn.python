"""Level 0 project: Duplicate Line Finder.

Enter lines of text and find which ones appear more than once.
Report duplicates and their counts.

Concepts: dictionaries for counting, sets for uniqueness, text input.
"""


def count_line_occurrences(lines: list) -> dict:
    """Count how many times each line appears.

    WHY a dict? -- A dictionary maps each unique line (the key) to its
    count (the value).  This is the fundamental pattern for counting
    things in Python.
    """
    counts = {}
    for line in lines:
        if line in counts:
            counts[line] += 1
        else:
            counts[line] = 1
    return counts


def find_duplicates(lines: list) -> list:
    """Find lines that appear more than once and report details.

    Returns a list of dicts, each containing the duplicated text,
    the count, and the line numbers where it appears.
    """
    counts = count_line_occurrences(lines)

    duplicates = []
    for text, count in counts.items():
        if count > 1:
            # Find all line numbers (1-based) where this text appears.
            positions = []
            for i, line in enumerate(lines):
                if line == text:
                    positions.append(i + 1)

            duplicates.append({
                "text": text,
                "count": count,
                "line_numbers": positions,
            })

    return duplicates


def build_report(lines: list) -> dict:
    """Build a full report about duplicates in the input."""
    non_empty = [line for line in lines if line]
    duplicates = find_duplicates(non_empty)

    return {
        "total_lines": len(non_empty),
        "unique_lines": len(set(non_empty)),
        "duplicate_count": len(duplicates),
        "duplicates": duplicates,
    }


# This guard means the code below only runs when you execute the file
# directly (python project.py), NOT when another file imports it.
if __name__ == "__main__":
    print("=== Duplicate Line Finder ===")
    print("Enter lines of text. Enter a blank line when done.\n")

    lines = []
    line_num = 1
    while True:
        line = input(f"  Line {line_num}: ")
        if line == "":
            break
        lines.append(line.strip())
        line_num += 1

    if not lines:
        print("No lines entered.")
    else:
        report = build_report(lines)

        print(f"\n=== Duplicate Line Report ===")
        print(f"  Total lines: {report['total_lines']}")
        print(f"  Unique lines: {report['unique_lines']}")
        print(f"  Duplicated lines: {report['duplicate_count']}")

        if report["duplicates"]:
            print("\n  Duplicates found:")
            for dup in report["duplicates"]:
                positions = ", ".join(str(n) for n in dup["line_numbers"])
                print(f"    '{dup['text']}' appears {dup['count']} times (lines {positions})")
        else:
            print("\n  No duplicates found.")
