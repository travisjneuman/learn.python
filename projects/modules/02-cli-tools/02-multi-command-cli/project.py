"""Module 02 / Project 02 -- Multi-Command CLI.

A file utility with three subcommands:
  info  -- show file size and last-modified date
  count -- count lines, words, and characters
  head  -- print the first N lines

Demonstrates click.group() for organizing related commands.

Run it with:
    python project.py info project.py
    python project.py count project.py
    python project.py head project.py --lines 10
"""

import os
from datetime import datetime

import click


# @click.group() turns this function into a command group.
# Instead of doing work itself, it acts as a dispatcher for subcommands.
@click.group()
def cli():
    """A small file utility with info, count, and head subcommands."""
    # The group function body usually stays empty.
    # Click calls the appropriate subcommand after this runs.
    pass


# --------------------------------------------------------------------------- #
# Subcommand: info
# --------------------------------------------------------------------------- #

# @cli.command() registers "info" as a subcommand of the cli group.
@cli.command()
# click.Path(exists=True) tells Click to verify the file exists
# before the function even runs. If the file is missing, Click
# prints a clear error and exits -- no try/except needed.
@click.argument("filepath", type=click.Path(exists=True))
def info(filepath):
    """Show file size and last-modified date."""

    # os.path.getsize returns the file size in bytes.
    size = os.path.getsize(filepath)

    # os.path.getmtime returns the modification time as a Unix timestamp.
    # We convert it to a human-readable string.
    mtime = os.path.getmtime(filepath)
    modified = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")

    # Print a tidy summary. The comma formatting (:,) adds thousand separators.
    click.echo(f"File:     {filepath}")
    click.echo(f"Size:     {size:,} bytes")
    click.echo(f"Modified: {modified}")


# --------------------------------------------------------------------------- #
# Subcommand: count
# --------------------------------------------------------------------------- #

@cli.command()
@click.argument("filepath", type=click.Path(exists=True))
def count(filepath):
    """Count lines, words, and characters in a file."""

    # Read the entire file into memory.
    # For very large files you would stream line by line, but for a
    # learning project reading everything at once is clearer.
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # splitlines() breaks the text on any newline character.
    lines = content.splitlines()

    # split() with no arguments splits on any whitespace and
    # ignores leading/trailing whitespace -- exactly what wc does.
    words = content.split()

    # len() on a string gives the character count (including newlines).
    chars = len(content)

    click.echo(f"Lines: {len(lines):,}")
    click.echo(f"Words: {len(words):,}")
    click.echo(f"Chars: {chars:,}")


# --------------------------------------------------------------------------- #
# Subcommand: head
# --------------------------------------------------------------------------- #

@cli.command()
@click.argument("filepath", type=click.Path(exists=True))
# --lines defaults to 5. The user can override it.
@click.option(
    "--lines", "-n",
    default=5,
    show_default=True,
    help="Number of lines to display from the top.",
)
def head(filepath, lines):
    """Show the first N lines of a file."""

    with open(filepath, "r", encoding="utf-8") as f:
        # Read all lines, then slice. For huge files you could use
        # itertools.islice, but clarity wins here.
        all_lines = f.readlines()

    # Slice the list to get only the first N lines.
    selected = all_lines[:lines]

    # Print each line. rstrip() removes the trailing newline so
    # click.echo does not double-space the output.
    for line in selected:
        click.echo(line.rstrip())


# Entry-point guard.
if __name__ == "__main__":
    # Calling cli() hands control to Click's group dispatcher.
    # Click inspects sys.argv, finds the subcommand name, and
    # calls the matching function.
    cli()
