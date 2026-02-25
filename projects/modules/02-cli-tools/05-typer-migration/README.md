# Module 02 / Project 05 -- Typer Migration

Home: [README](../../../../README.md)

## Focus

- Typer as a modern alternative to Click
- Comparing Click decorators to Typer's type-annotation approach
- Rebuilding familiar functionality with a different API
- Understanding when to choose Click vs Typer

## Why this project exists

Typer is built on top of Click but takes a different approach: instead of stacking decorators, you declare your CLI using Python type hints. The result is less boilerplate and tighter integration with modern Python. This project rebuilds the file utility from Project 02 using Typer so you can see the same tool expressed two ways and decide which style you prefer.

## Run

```bash
cd projects/modules/02-cli-tools/05-typer-migration

# Show top-level help
python project.py --help

# Show file info
python project.py info project.py

# Count lines, words, and characters
python project.py count project.py

# Show the first 5 lines (default)
python project.py head project.py

# Show the first 10 lines
python project.py head project.py --lines 10
```

## Expected output

```text
$ python project.py info project.py
File:     project.py
Size:     2,100 bytes
Modified: 2026-02-24 14:30:00

$ python project.py count project.py
Lines: 75
Words: 280
Chars: 2,100

$ python project.py head project.py --lines 3
"""Module 02 / Project 05 -- Typer Migration.
...first 3 lines...
```

(Output matches Project 02 because the functionality is identical.)

## Alter it

1. Add a `tail` subcommand using Typer syntax. Compare the code to how you would write it in Click.
2. Add a `--json` flag to the `info` command that outputs the file info as a JSON object instead of plain text.
3. Use `typer.colors` to add colored output to the `count` command (e.g., highlight the total in green).

## Break it

1. Remove the type annotation from the `filepath` parameter in `info`. What error does Typer produce?
2. Change `lines: int = 5` to `lines = 5` (remove the type hint) in the `head` command. How does Typer interpret the parameter now?
3. Try using `@app.command` without parentheses (no `()`). What happens?

## Fix it

1. Restore the type annotation and confirm the command works.
2. Restore the type hint on `lines` and verify `--lines` appears as an integer option in `--help`.
3. Add the parentheses back and confirm the subcommand registers correctly.

## Explain it

1. How does Typer figure out that a parameter is an argument vs an option?
2. What role do type annotations play in Typer that decorators play in Click?
3. Typer is built on Click -- what does that mean in practice? Can you mix them?
4. When would you choose Click over Typer, and vice versa?

## Mastery check

You can move on when you can:
- rewrite a Click command as a Typer command from memory,
- explain how Typer uses type annotations to generate the CLI,
- list two advantages of each library,
- add a new subcommand to a Typer app without breaking existing ones.

## Next

Go back to [Module 02 index](../README.md) or continue to the next module.
