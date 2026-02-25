# Module 02 / Project 01 -- Click Basics

Home: [README](../../../../README.md)

## Focus

- `@click.command()` decorator to define a CLI entry point
- `@click.option()` for optional flags like `--shout`
- `@click.argument()` for required positional values
- Automatic `--help` text generation

## Why this project exists

Most Python scripts start with `if __name__ == "__main__"` and a handful of `input()` calls. That works for throwaway code, but real tools need named options, help text, and predictable argument parsing. Click handles all of that with decorators you stack on top of a plain function. This project shows you how.

## Run

```bash
cd projects/modules/02-cli-tools/01-click-basics

# Basic greeting
python project.py World

# Greeting with the --shout flag
python project.py World --shout

# View auto-generated help
python project.py --help

# Greeting with a custom greeting word
python project.py World --greeting Howdy
```

## Expected output

```text
$ python project.py World
Hello, World!

$ python project.py World --shout
HELLO, WORLD!

$ python project.py World --greeting Howdy
Howdy, World!

$ python project.py --help
Usage: project.py [OPTIONS] NAME

  Greet someone by name. A small first step into Click.

Options:
  --greeting TEXT  Word to use for the greeting.  [default: Hello]
  --shout          Uppercase the entire output.
  --help           Show this message and exit.
```

## Alter it

1. Add a `--repeat` option (integer, default 1) that prints the greeting N times.
2. Add a `--farewell` flag that prints a goodbye message after the greeting.
3. Change the default greeting word from "Hello" to something else and confirm `--help` reflects the change.

## Break it

1. Remove the `@click.argument("name")` decorator and run the script. What error do you get?
2. Change `is_flag=True` on `--shout` to `type=int`. Try running with `--shout`. What happens?
3. Pass two positional arguments instead of one. How does Click respond?

## Fix it

1. Restore the missing decorator and confirm the greeting works again.
2. Revert `--shout` back to a boolean flag and verify `--shout` toggles uppercasing.
3. Read the Click docs on `nargs` and decide whether your tool should accept multiple names.

## Explain it

1. What does `@click.command()` do that a bare function does not?
2. How does Click generate the `--help` text -- where does it pull the description from?
3. What is the difference between `@click.option()` and `@click.argument()` in terms of required vs optional?
4. Why does Click use decorators instead of requiring you to subclass something?

## Mastery check

You can move on when you can:
- write a Click command from scratch without copying this file,
- explain what `is_flag=True` does vs a typed option,
- add a new option, re-run `--help`, and confirm it appears,
- break and recover in one session.

## Next

Continue to [02 - Multi-Command CLI](../02-multi-command-cli/).
