# Module 02 / Project 02 -- Multi-Command CLI

Home: [README](../../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

- `@click.group()` to bundle related commands under one tool
- Defining subcommands with `@group.command()`
- Sharing options across subcommands
- Building a practical file utility

## Why this project exists

Real CLI tools rarely do just one thing. Git has `commit`, `push`, `log`. Docker has `build`, `run`, `stop`. Click's group system lets you organize multiple commands under a single entry point so users type `tool info myfile.txt` instead of remembering five separate scripts. This project shows you how to build that structure.

## Run

```bash
cd projects/modules/02-cli-tools/02-multi-command-cli

# Show top-level help
python project.py --help

# Show file info (size, modified date)
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
Size:     2,341 bytes
Modified: 2026-02-24 14:30:00

$ python project.py count project.py
Lines: 87
Words: 312
Chars: 2,341

$ python project.py head project.py --lines 3
"""Module 02 / Project 02 -- Multi-Command CLI.
...first 3 lines of file...
```

(Exact numbers will vary depending on the file.)

## Alter it

1. Add a `tail` subcommand that shows the last N lines of a file.
2. Add a `--bytes` flag to the `info` subcommand that displays size in KB or MB when the file is large enough.
3. Add a `search` subcommand that takes a `--pattern` option and prints matching lines with line numbers.

## Break it

1. Remove the `@cli.command()` decorator from `info`. Run `python project.py info project.py`. What happens?
2. Pass a filename that does not exist to `count`. How does the tool respond?
3. Change `@click.group()` to `@click.command()` and try running a subcommand. What error appears?

## Fix it

1. Restore the decorator and confirm `info` appears in `--help` again.
2. Add a file-existence check before opening the file, and print a clear error message if the file is missing.
3. Revert to `@click.group()` and verify all subcommands work.

## Explain it

1. What is the relationship between `@click.group()` and `@cli.command()`?
2. How does Click know which subcommand the user wants to run?
3. Why is `click.Path(exists=True)` useful and how does it differ from checking `os.path.exists()` yourself?
4. If two subcommands need the same option, what are your options for avoiding duplication?

## Mastery check

You can move on when you can:
- create a group with at least three subcommands from memory,
- explain how Click dispatches to the correct subcommand,
- add a new subcommand without breaking existing ones,
- handle missing-file errors gracefully.

---

## Related Concepts

- [Collections Explained](../../../../concepts/collections-explained.md)
- [Files and Paths](../../../../concepts/files-and-paths.md)
- [Functions Explained](../../../../concepts/functions-explained.md)
- [How Imports Work](../../../../concepts/how-imports-work.md)
- [Quiz: Collections Explained](../../../../concepts/quizzes/collections-explained-quiz.py)

## Next

Continue to [03 - Interactive Prompts](../03-interactive-prompts/).
