"""Module 02 / Project 04 -- File Processor CLI.

A practical CLI that processes text files in a directory:
  - counts words per file
  - finds the longest line
  - calculates average line length
  - shows a progress bar using rich.progress

Run it with:
    python project.py --directory data
    python project.py --directory data --output report.txt
"""

from pathlib import Path

import click
# rich.progress provides track(), a drop-in wrapper for any iterable
# that displays a progress bar in the terminal.
from rich.progress import track


def analyze_file(filepath):
    """Analyze a single text file and return a stats dictionary.

    Reads the file, splits into lines and words, then computes:
      - word count
      - longest line length (in characters)
      - average line length (in characters)
    """
    # Read the file content as a string.
    content = filepath.read_text(encoding="utf-8")

    # Split into lines for per-line analysis.
    lines = content.splitlines()

    # Split the full content on whitespace to get all words.
    words = content.split()

    # Find the longest line by character count.
    # If the file is empty, longest is 0.
    longest = max((len(line) for line in lines), default=0)

    # Calculate average line length.
    # Guard against division by zero for empty files.
    if lines:
        avg_length = sum(len(line) for line in lines) / len(lines)
    else:
        avg_length = 0.0

    return {
        "filename": filepath.name,
        "word_count": len(words),
        "longest_line": longest,
        "avg_line_length": round(avg_length, 1),
    }


def format_report(results):
    """Build a human-readable report string from a list of result dicts."""
    # Start with a divider line.
    lines = ["Results:", "-" * 40]

    for result in results:
        # File name as a header.
        lines.append(result["filename"])

        # Stats indented under the filename.
        lines.append(
            f"  Words: {result['word_count']}   "
            f"Longest line: {result['longest_line']} chars   "
            f"Avg line length: {result['avg_line_length']} chars"
        )
        lines.append("")  # blank line between files

    # Summary at the bottom.
    total_words = sum(r["word_count"] for r in results)
    lines.append("-" * 40)
    lines.append(f"Total files: {len(results)}")
    lines.append(f"Total words: {total_words}")

    return "\n".join(lines)


@click.command()
@click.option(
    "--directory", "-d",
    required=True,
    type=click.Path(exists=True, file_okay=False),
    help="Directory containing text files to process.",
)
@click.option(
    "--output", "-o",
    default=None,
    type=click.Path(),
    help="Optional file path to save the report.",
)
@click.option(
    "--pattern", "-p",
    default="*.txt",
    show_default=True,
    help="Glob pattern for files to include.",
)
def process(directory, output, pattern):
    """Process text files in a directory and display statistics."""

    # Convert the directory string to a Path object.
    dir_path = Path(directory)

    # glob() returns a generator of Path objects matching the pattern.
    # sorted() makes the output order predictable (alphabetical).
    files = sorted(dir_path.glob(pattern))

    # Tell the user if no files matched.
    if not files:
        click.echo(f"No files matching '{pattern}' found in {directory}")
        return

    click.echo("Processing files...")

    results = []

    # track() wraps any iterable and shows a progress bar.
    # It figures out the total from len(files) and updates
    # the bar each time the loop body finishes one iteration.
    for filepath in track(files, description="  "):
        stats = analyze_file(filepath)
        results.append(stats)

    # Build and display the report.
    report = format_report(results)
    click.echo("")
    click.echo(report)

    # If the user asked for an output file, write the report there too.
    if output:
        output_path = Path(output)
        output_path.write_text(report, encoding="utf-8")
        click.echo(f"\nReport saved to {output_path}")


# Entry-point guard.
if __name__ == "__main__":
    process()
