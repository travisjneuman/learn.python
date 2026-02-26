# Solution: 03-your-first-script

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
# Step 1: Print a greeting.
print("Welcome to your first Python script!")  # WHY: This is the first line Python runs — it tells the user the script has started

# Step 2: Do some math and print the result.
print("Let me calculate something for you...")     # WHY: Gives context for what is about to happen — good programs tell you what they are doing
print("If you have 24 hours in a day and 7 days in a week:")  # WHY: Explains the calculation in plain English before showing the math
print("That is", 24 * 7, "hours in a week.")       # WHY: Python calculates 24*7=168 and prints it between the two text strings

# Step 3: Print a blank line for readability.
print()  # WHY: A blank line separates sections visually — without it, all the text runs together

# Step 4: Print a closing message.
print("This script ran from top to bottom.")   # WHY: Reinforces the key lesson — Python executes line 1, then line 2, then line 3, and so on
print("Every line executed in order.")          # WHY: There are no jumps or skips (yet) — the order in the file IS the order of execution
print("That is how all Python scripts work.")   # WHY: This top-to-bottom flow is called "sequential execution" and is the foundation of all programs
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Write commands in a file instead of interactive mode | Files let you save, edit, and re-run your code — interactive mode loses everything when you close it | Interactive mode (Exercise 01) is good for experimenting, but real programs live in files |
| Use comments (lines starting with #) | Comments explain WHY the code does something — they are notes for humans that Python ignores entirely | Could write code without comments, but then you would forget what each line does tomorrow |
| Calculate `24 * 7` inline inside print() | Keeps the example simple — no variables needed yet (those come in Exercise 04) | Could store the result in a variable first, but that adds a concept not yet introduced |
| End with a message about sequential execution | The most important lesson is that scripts run top-to-bottom — this makes the lesson explicit | Could leave it implicit, but beginners benefit from having concepts stated directly |

## Alternative approaches

### Approach B: A personal introduction script

```python
# My personal introduction script
# This file tells the world about me.

print("=== About Me ===")           # WHY: The === creates a visual header — it makes the output look organized
print()                              # WHY: Blank line after the header for readability
print("Name: Alice")                 # WHY: Each print() is one line of output — put one fact per line
print("Hobby: Learning Python")      # WHY: You can put any text you want — make it personal
print("Fun fact: I just ran my first script!")  # WHY: This is YOUR script — personalize it
print()                              # WHY: Spacing before the closing line
print("Script complete!")            # WHY: A clear ending tells you the script finished successfully
```

**Trade-off:** Both scripts teach the same concept (top-to-bottom execution). Making it personal helps you feel ownership over the code — it is YOUR script, not just an exercise you copied.

### Approach C: A script with commented-out lines

```python
print("Line 1: I will print")         # WHY: This line runs because it is valid Python code
# print("Line 2: I am commented out") # WHY: The # at the start makes Python skip this entire line
print("Line 3: I will also print")    # WHY: Python skips the comment and continues to the next real line
```

**Trade-off:** This version directly teaches commenting and un-commenting. Try adding and removing the `#` to see lines appear and disappear from the output.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Running `python exercise.py` from the wrong folder | `FileNotFoundError` — Python cannot find the file because you are not in the right directory | Use `cd` to navigate to the folder first, then run the command. The terminal prompt usually shows your current folder |
| Misspelling the filename: `python exorcise.py` | `FileNotFoundError` or `No such file or directory` — the filename must match exactly | Check the spelling. Tab-completion (pressing Tab after typing a few letters) can auto-fill the filename |
| Forgetting to save the file before running | Python runs the last saved version, not what is currently on screen | Always save (Ctrl+S) before running. Some editors auto-save, but do not rely on it |
| Adding code with wrong indentation | `IndentationError` — Python is strict about spacing at the beginning of lines | For now, start every line at the very left edge (no spaces before print). Indentation becomes important in Exercise 08 |
| Using a `.txt` extension instead of `.py` | The file might still run, but your editor will not give you Python syntax highlighting, making it harder to read | Always name Python files with the `.py` extension |

## Key takeaways

1. **A Python script is just a text file full of commands that run top-to-bottom** — the order you write them is the order Python executes them. This is the most fundamental concept in programming: you are writing a sequence of instructions.
2. **Comments (lines starting with #) are notes for humans** — Python ignores them completely. Use comments to explain what your code does and why. Your future self will thank you when you re-read your code weeks later.
3. **The ability to save code in a file changes everything** — unlike interactive mode, files let you build up complex programs, edit them, share them, and run them as many times as you want. Every real program you use (websites, apps, games) started as files of code like this one.
