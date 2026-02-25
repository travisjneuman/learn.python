# Module 02 -- CLI Tools

Home: [README](../../../README.md)

## Overview

This module teaches you how to build real command-line tools in Python using two popular libraries: Click and Typer. Instead of parsing `sys.argv` by hand or wiring up `argparse` boilerplate, you will use decorators and type annotations to create polished CLIs with help text, subcommands, colored output, and progress bars.

By the end of the module you will be comfortable building the kind of CLI utilities that professional Python developers ship every day.

## Prerequisites

- **Level 2 complete.** You should be comfortable with functions, dictionaries, file I/O, and basic error handling.

## Learning objectives

1. Declare CLI commands, options, and arguments with Click decorators.
2. Organize related commands into groups (subcommands).
3. Build interactive prompts with confirmation and colored output.
4. Process real files with progress feedback using Rich.
5. Compare Click and Typer so you can choose the right tool for a project.

## Projects

| # | Project | Focus |
|---|---------|-------|
| 01 | [Click Basics](./01-click-basics/) | `@click.command()`, `@click.option()`, `@click.argument()`, help text |
| 02 | [Multi-Command CLI](./02-multi-command-cli/) | `click.group()`, subcommands, shared options |
| 03 | [Interactive Prompts](./03-interactive-prompts/) | `click.prompt()`, `click.confirm()`, `click.echo()`, `click.style()` |
| 04 | [File Processor CLI](./04-file-processor-cli/) | Progress bars, file globbing, real-world file processing |
| 05 | [Typer Migration](./05-typer-migration/) | Typer as a modern Click alternative, syntax comparison |

## Installing dependencies

Create a virtual environment and install the module requirements before starting:

```bash
cd projects/modules/02-cli-tools
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

See [concepts/virtual-environments.md](../../../concepts/virtual-environments.md) for a full explanation.

## How to work through each project

1. Read the project README.
2. Run the baseline script and study the output.
3. **Alter** -- make a small change and re-run.
4. **Break** -- introduce a deliberate mistake and observe the failure.
5. **Fix** -- repair the break and confirm everything works again.
6. **Explain** -- answer the teach-back questions in `notes.md`.
