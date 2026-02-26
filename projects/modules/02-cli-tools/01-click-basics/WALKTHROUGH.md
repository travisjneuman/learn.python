# Click Basics — Step-by-Step Walkthrough

[<- Back to Project README](./README.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 15 minutes attempting it independently. You need to build a simple CLI that greets someone by name, with options for shouting and changing the greeting word. If you can get `python project.py World` to print "Hello, World!" you are off to a good start.

## Thinking Process

A command-line interface (CLI) takes input from the terminal and produces output. You have already written scripts that use `input()` to ask questions. Click replaces that approach with something more professional: named options (`--shout`), positional arguments (`World`), and automatic help text (`--help`). Instead of a conversation ("What is your name?"), the user provides everything up front in one command.

Click works through decorators — those `@` symbols you stack on top of a function. Each decorator adds a piece of CLI behavior. `@click.command()` turns the function into a CLI entry point. `@click.argument("name")` says "the first positional value on the command line becomes the `name` parameter." `@click.option("--shout")` says "if the user passes `--shout`, set this parameter to True." Click reads these decorators and does all the parsing for you.

The mental model is a layer cake. Your function is the cake. Each decorator is a layer on top. When the user runs the script, Click peels off the layers from top to bottom, parsing the command line, and then calls your function with the parsed values.

## Step 1: Import Click and Create a Command

**What to do:** Import the `click` library and decorate a function with `@click.command()`.

**Why:** `@click.command()` transforms a regular Python function into a CLI program. Without it, your function is just a function — nobody can call it from the terminal with arguments. This decorator is the foundation that everything else builds on.

```python
import click

@click.command()
def greet():
    """Greet someone by name. A small first step into Click."""
    click.echo("Hello!")
```

Notice `click.echo()` instead of `print()`. They do the same thing most of the time, but `click.echo()` handles encoding issues on Windows and works correctly when output is piped to a file.

**Predict:** If you run this script now with `python project.py --help`, what will Click display? Where does it get the description text from?

## Step 2: Add a Required Argument

**What to do:** Add `@click.argument("name")` and accept `name` as a function parameter.

**Why:** A Click argument is a required positional value — the user must provide it. The decorator name `"name"` must match the function parameter name. When the user types `python project.py World`, Click assigns `"World"` to the `name` parameter.

```python
@click.command()
@click.argument("name")
def greet(name):
    """Greet someone by name."""
    click.echo(f"Hello, {name}!")
```

**Predict:** What happens if the user runs `python project.py` without providing a name? Try it.

## Step 3: Add an Option with a Default Value

**What to do:** Add a `--greeting` option that defaults to `"Hello"`.

**Why:** Options are optional (the clue is in the name). They have a `--` prefix and can appear anywhere on the command line. By giving `--greeting` a default value, the user can skip it and still get a working greeting, or override it with `--greeting Howdy`.

```python
@click.command()
@click.argument("name")
@click.option(
    "--greeting",
    default="Hello",
    help="Word to use for the greeting.",
    show_default=True,
)
def greet(name, greeting):
    """Greet someone by name."""
    message = f"{greeting}, {name}!"
    click.echo(message)
```

Two details to notice:

- **`show_default=True`** tells Click to display the default value in the `--help` text. Without it, the user has to guess what the default is.
- **The parameter name** in the function (`greeting`) is derived from the option name (`--greeting`). Click strips the dashes and converts hyphens to underscores.

**Predict:** If you run `python project.py World --greeting Howdy`, what will the output be? What about `python project.py --greeting Howdy World` — does the order matter for options?

## Step 4: Add a Boolean Flag

**What to do:** Add a `--shout` option that is a boolean flag (present = True, absent = False).

**Why:** A flag is an on/off switch. The user either passes `--shout` or does not. There is no value after it — its mere presence means True. This is different from `--greeting`, which expects a value after it. The `is_flag=True` parameter tells Click this distinction.

```python
@click.option(
    "--shout",
    is_flag=True,
    help="Uppercase the entire output.",
)
def greet(name, greeting, shout):
    """Greet someone by name."""
    message = f"{greeting}, {name}!"
    if shout:
        message = message.upper()
    click.echo(message)
```

**Predict:** What is the value of `shout` when the user does NOT pass `--shout`? What about when they do?

## Step 5: Add the Entry Point Guard

**What to do:** Add the `if __name__ == "__main__"` block and call the decorated function.

**Why:** When you run `python project.py World`, Python sets `__name__` to `"__main__"`. The guard ensures the CLI only starts when the file is executed directly. If another file imports this module, the CLI will not run automatically. Inside the guard, you call `greet()` with no arguments — Click handles argument parsing internally.

```python
if __name__ == "__main__":
    greet()
```

Notice that you call `greet()` with no arguments even though the function signature has `name`, `greeting`, and `shout`. Click intercepts the call and fills in the parameters from the command line.

**Predict:** What happens if you call `greet("World", "Hi", False)` directly instead of letting Click handle it? Try it and see.

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| `TypeError: greet() missing argument 'name'` | Calling the function directly instead of through Click | Call `greet()` with no args — Click parses the CLI |
| Decorator order confusion | Decorators execute bottom-to-top | `@click.command()` goes on top, arguments and options below |
| `--shout` expects a value | Forgot `is_flag=True` | Add `is_flag=True` to make it a boolean toggle |
| Function parameter does not match option name | Click derives param names from option names | `--greeting` becomes `greeting`; `--my-flag` becomes `my_flag` |

## Testing Your Solution

Run the script with different combinations:

```bash
python project.py World
python project.py World --shout
python project.py World --greeting Howdy
python project.py --help
```

Expected output:
```text
Hello, World!
HELLO, WORLD!
Howdy, World!
Usage: project.py [OPTIONS] NAME
...
```

## What You Learned

- **`@click.command()`** turns a plain function into a CLI program that parses command-line arguments automatically.
- **`@click.argument()`** defines required positional values, while **`@click.option()`** defines optional named flags and values with defaults.
- **`is_flag=True`** creates a boolean toggle that is True when present and False when absent — no value needed after it.
- **`click.echo()`** is a safer alternative to `print()` that handles encoding differences across platforms.
