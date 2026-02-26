# Level 0 / Project 01 - Terminal Hello Lab
Home: [README](../../../README.md)

> **Try in Browser:** [Run this exercise online](../../browser/level-0.html?ex=1) — no installation needed!

## Before You Start

Recall these prerequisites before diving in:
- Can you create a variable and print its value? (`name = "Ada"` then `print(name)`)
- Can you use an f-string to combine text and variables? (`f"Hello, {name}"`)

## Focus
- print output, variables, and command execution basics

## Why this project exists
Your very first Python script. You will print text to the terminal, use variables to store data, and see how f-strings build dynamic output. Every programmer starts here.

## Run (copy/paste)
Use `<repo-root>` as the folder containing this repository's `README.md`.

```bash
cd <repo-root>/projects/level-0/01-terminal-hello-lab
python project.py
pytest -q
```

The program will ask for your name and learning day, then print output.

## Expected terminal output
```text
What is your name? Ada
What day of your Python journey is it? 7
****************************************
         TERMINAL HELLO LAB
****************************************

Hello, Ada! Welcome to Python.
	Day 7 of your Python journey.

Fun fact: Python is named after Monty Python,
not the snake!

--- Your Info Card ---
  name: Ada
  language: Python
  learning_day: 7
  greeting: Hello, Ada! Welcome to Python.
5 passed
```

## Expected artifacts
- Passing tests
- Updated `notes.md`

## Worked Example

Here is a similar (but different) problem, solved step by step.

**Problem:** Write a function that builds a welcome message with the current date.

**Step 1: Think about what we need.** We need a name, today's date, and a formatted string.

```python
from datetime import date

def build_welcome(name):
    today = date.today().strftime("%B %d, %Y")
    return f"Welcome, {name}! Today is {today}."
```

**Step 2: Think about the output.** What should this look like?

```python
print(build_welcome("Marcus"))
# Welcome, Marcus! Today is January 15, 2026.
```

**Step 3: Think about edge cases.** What if name is empty?

```python
def build_welcome(name):
    if not name or not name.strip():
        name = "friend"
    today = date.today().strftime("%B %d, %Y")
    return f"Welcome, {name}! Today is {today}."
```

**The thought process:** Start with the simplest version that works. Then add a guard for bad input. This is the pattern you will use in this project and every project after it.

## Alter it (required)
1. Add a `build_greeting_box()` function that wraps the greeting in a box made of `+`, `-`, and `|` characters.
2. Ask the user if they want UPPERCASE output. If they type "yes", print everything in upper case.
3. Re-run script and tests.

## Break it (required)
1. Type nothing when asked for your name (just press Enter) -- what happens to the greeting and banner?
2. Type only spaces as your name -- does `build_banner()` handle it or crash?
3. Try typing letters instead of a number for the day -- what error do you get?

## Fix it (required)
1. Add a guard in `greet()` that returns a default message for empty names.
2. Add a check that the day is a valid positive number, with a helpful error message.
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

## Stuck? Ask AI

If you are stuck after trying for 20 minutes, use one of these prompts. They are designed to help you learn without giving away the answer.

- "I am working on Terminal Hello Lab. I got this error: [paste error]. Can you explain what this error means without giving me the fix?"
- "I am trying to build a banner with asterisks. I know I need `len()` and string multiplication, but my output looks wrong. Can you give me a hint about what I might be calculating incorrectly?"
- "Can you explain f-strings with a simple example that is different from my project?"

---

| [← Prev](../README.md) | [Home](../../../README.md) | [Next →](../02-calculator-basics/README.md) |
|:---|:---:|---:|
