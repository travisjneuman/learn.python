# Level 0 / Project 01 - Terminal Hello Lab
Home: [README](../../../README.md)

## Focus
- print output, variables, and command execution basics

## Why this project exists
Your very first Python script. You will print text to the terminal, use variables to store data, and see how f-strings build dynamic output. Every programmer starts here.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/01-terminal-hello-lab
python project.py --name Ada --day 7
pytest -q
```

## Expected terminal output
```text
****************************************
         TERMINAL HELLO LAB
****************************************

Hello, Ada! Welcome to Python.
	Day 7 of your Python journey.

Fun fact: Python is named after Monty Python,
not the snake!

Summary written to data/output.json
5 passed
```

## Expected artifacts
- `data/output.json`
- Passing tests
- Updated `notes.md`

## Alter it (required)
1. Add a `build_greeting_box()` function that wraps the greeting in a box made of `+`, `-`, and `|` characters.
2. Add a `--uppercase` flag that prints all output in UPPER CASE.
3. Re-run script and tests.

## Break it (required)
1. Pass an empty string as the name in `data/sample_input.txt` -- what happens to the greeting and banner?
2. Add a line with only spaces -- does `build_banner()` handle it or crash?
3. Try a very long name (200+ characters) -- does the banner overflow?

## Fix it (required)
1. Add a guard in `greet()` that returns a default message for empty names.
2. Strip whitespace-only lines in `run_hello_lab()` before processing.
3. Add a test that verifies empty-name handling.

## Explain it (teach-back)
1. What does `f"Hello, {name}!"` do differently from `"Hello, " + name + "!"`?
2. Why does `build_banner()` use `len(text) + 4` for the border width?
3. How does the `if __name__ == "__main__"` guard work and why is it needed?
4. Where would greeting templates be used in real software (email systems, CLI tools)?

## Mastery check
You can move on when you can:
- run baseline without docs,
- explain one core function line-by-line,
- break and recover in one session,
- keep tests passing after your change.

---

## Related Concepts

- [Files and Paths](../../../concepts/files-and-paths.md)
- [How Loops Work](../../../concepts/how-loops-work.md)
- [The Terminal Deeper](../../../concepts/the-terminal-deeper.md)
- [Types and Conversions](../../../concepts/types-and-conversions.md)
- [Quiz: Files and Paths](../../../concepts/quizzes/files-and-paths-quiz.py)

---

| [← Prev](../README.md) | [Home](../../../README.md) | [Next →](../02-calculator-basics/README.md) |
|:---|:---:|---:|
