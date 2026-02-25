"""Module 02 / Project 01 -- Click Basics.

This script builds a simple greeting CLI to demonstrate the three
core Click decorators: @click.command(), @click.option(), and
@click.argument().

Run it with:
    python project.py World
    python project.py World --shout
    python project.py --help
"""

# click is a third-party library for building command-line interfaces.
# Install it with: pip install click
import click


# @click.command() turns this function into a CLI entry point.
# Click reads the docstring and uses it as the help description.
@click.command()
# @click.argument() defines a required positional value.
# "name" becomes the first thing the user types after the script name.
@click.argument("name")
# @click.option() defines an optional flag.
# --greeting has a default value so the user can skip it.
@click.option(
    "--greeting",
    default="Hello",
    help="Word to use for the greeting.",
    show_default=True,
)
# is_flag=True means --shout is a boolean toggle: present = True, absent = False.
@click.option(
    "--shout",
    is_flag=True,
    help="Uppercase the entire output.",
)
def greet(name, greeting, shout):
    """Greet someone by name. A small first step into Click."""

    # Build the message from the greeting word and the name argument.
    message = f"{greeting}, {name}!"

    # If the user passed --shout, convert everything to uppercase.
    if shout:
        message = message.upper()

    # click.echo() is Click's version of print().
    # It handles encoding issues on Windows and plays nicely with pipes.
    click.echo(message)


# Standard Python entry-point guard.
# When you run "python project.py", Python sets __name__ to "__main__".
# Without this guard, importing the file would execute the CLI immediately.
if __name__ == "__main__":
    # Call the decorated function. Click takes over argument parsing here.
    greet()
