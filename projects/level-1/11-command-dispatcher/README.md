# Level 1 / Project 11 - Command Dispatcher
Home: [README](../../../README.md)

## Focus
- map commands to handler functions

## Why this project exists
Map text commands (upper, lower, reverse, etc.) to handler functions using a dictionary dispatcher. You will learn the function-as-value pattern, where commands are looked up in a dict and called dynamically.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-1/11-command-dispatcher
python project.py --input data/sample_input.txt
pytest -q
```

## Expected terminal output
```text
=== Command Dispatcher ===

  upper "hello world"       => HELLO WORLD
  lower "THIS SHOULD BE..." => this should be lowercase
  reverse "Python is fun"   => nuf si nohtyP

3 commands processed. Output written to data/output.json
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a new command: `replace old new text` that replaces all occurrences of `old` with `new` in the text.
2. Add a `--list` flag that prints all available commands and exits.
3. Re-run script and tests.

## Break it (required)
1. Send a command with no arguments like just `upper` (no text) -- does `dispatch()` handle it?
2. Send an unknown command like `fly to the moon` -- does the error dict include the command name?
3. Send an empty line -- does the dispatcher skip it or crash?

## Fix it (required)
1. Ensure `dispatch()` returns an error dict when no arguments are provided.
2. Include the attempted command name in the "Unknown command" error message.
3. Add a test for the no-arguments case.

## Explain it (teach-back)
1. Why does `COMMANDS` map command names to functions instead of using if/elif?
2. What does `dispatch()` returning a dict (not raising an exception) mean for error handling?
3. Why does `list_commands()` return sorted keys from the `COMMANDS` dict?
4. Where would command dispatchers appear in real software (chatbots, CLI frameworks, REST API routers)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [How Imports Work](../../../concepts/how-imports-work.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Quiz: Errors and Debugging](../../../concepts/quizzes/errors-and-debugging-quiz.py)

---

| [← Prev](../10-ticket-priority-router/README.md) | [Home](../../../README.md) | [Next →](../12-file-extension-counter/README.md) |
|:---|:---:|---:|
