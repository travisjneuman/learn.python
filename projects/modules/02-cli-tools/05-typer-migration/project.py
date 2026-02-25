"""Module 02 / Project 05 -- Typer Migration.

Rebuilds the file utility from Project 02 using Typer instead of Click.
Same three subcommands (info, count, head), same behavior, different API.

KEY DIFFERENCE: Typer uses Python type annotations to define the CLI.
Click uses stacked decorators. Compare this file to 02-multi-command-cli/project.py
to see the two approaches side by side.

Run it with:
    python project.py info project.py
    python project.py count project.py
    python project.py head project.py --lines 10
"""

import os
from datetime import datetime
from pathlib import Path

# Typer is built on top of Click. When you import typer, Click is
# available under the hood. Typer adds a layer that reads type
# annotations instead of requiring decorators for every option.
import typer

# In Click you wrote: cli = click.Group()
# In Typer you write: app = typer.Typer()
# The concept is the same -- a container for subcommands.
app = typer.Typer(help="A small file utility with info, count, and head subcommands.")


# --------------------------------------------------------------------------- #
# Subcommand: info
# --------------------------------------------------------------------------- #

# In Click:  @cli.command() + @click.argument("filepath", type=click.Path(exists=True))
# In Typer:  @app.command() + a type-annotated parameter
#
# Typer sees "filepath: Path" and knows it is a required argument.
# The type annotation (Path) tells Typer to treat it as a filesystem path.
@app.command()
def info(filepath: Path):
    """Show file size and last-modified date."""

    # Typer does not have Click's built-in exists=True check on Path,
    # so we handle it ourselves.
    if not filepath.exists():
        typer.echo(f"Error: file not found: {filepath}")
        raise typer.Exit(code=1)

    size = os.path.getsize(filepath)
    mtime = os.path.getmtime(filepath)
    modified = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")

    # typer.echo() works exactly like click.echo() because Typer
    # delegates to Click internally.
    typer.echo(f"File:     {filepath}")
    typer.echo(f"Size:     {size:,} bytes")
    typer.echo(f"Modified: {modified}")


# --------------------------------------------------------------------------- #
# Subcommand: count
# --------------------------------------------------------------------------- #

# In Click:  @cli.command() + @click.argument(...) + separate decorators
# In Typer:  @app.command() + type-annotated function signature
@app.command()
def count(filepath: Path):
    """Count lines, words, and characters in a file."""

    if not filepath.exists():
        typer.echo(f"Error: file not found: {filepath}")
        raise typer.Exit(code=1)

    content = filepath.read_text(encoding="utf-8")
    lines = content.splitlines()
    words = content.split()
    chars = len(content)

    typer.echo(f"Lines: {len(lines):,}")
    typer.echo(f"Words: {len(words):,}")
    typer.echo(f"Chars: {chars:,}")


# --------------------------------------------------------------------------- #
# Subcommand: head
# --------------------------------------------------------------------------- #

# In Click:  @click.option("--lines", "-n", default=5, ...)
# In Typer:  lines: int = typer.Option(5, "--lines", "-n", help="...")
#
# Typer distinguishes arguments from options by how you annotate them:
#   - Plain type annotation (filepath: Path)  -->  argument
#   - typer.Option(...)                         -->  option with a default
@app.command()
def head(
    filepath: Path,
    lines: int = typer.Option(
        5,
        "--lines", "-n",
        help="Number of lines to display from the top.",
    ),
):
    """Show the first N lines of a file."""

    if not filepath.exists():
        typer.echo(f"Error: file not found: {filepath}")
        raise typer.Exit(code=1)

    content = filepath.read_text(encoding="utf-8")
    all_lines = content.splitlines()

    # Slice to get the first N lines, just like the Click version.
    selected = all_lines[:lines]

    for line in selected:
        typer.echo(line)


# Entry-point guard.
# In Click:  cli()
# In Typer:  app()
# Both hand off to Click's argument parser under the hood.
if __name__ == "__main__":
    app()
