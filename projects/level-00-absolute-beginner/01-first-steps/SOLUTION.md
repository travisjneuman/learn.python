# Solution: 01-first-steps

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

This exercise is done in Python's **interactive mode** (the `>>>` prompt), not by writing a file. Here is what you should have typed and seen:

```python
# Step 1: Open your terminal and type "python" to start interactive mode.
# You should see the >>> prompt.

# Step 2: Try basic math.
2 + 2          # WHY: This tests that Python is working — it should respond with 4
10 - 3         # WHY: Subtraction works with the minus sign, just like on paper
5 * 6          # WHY: The * symbol means multiply (the x key is used for variable names)
100 / 4        # WHY: The / symbol means divide — Python gives you 25.0 (a decimal number)

# Step 3: Print a message.
print("Hello, I am learning Python!")  # WHY: print() displays text on screen — the quotes mark where the text starts and ends

# Step 4: Exit interactive mode.
exit()         # WHY: This tells Python you are done — it closes the interactive session
```

If you ran the `exercise.py` file directly, here is what it does:

```python
print("If you can see this, you successfully ran a Python file!")  # WHY: Confirms the file ran — if you see this, Python found and executed the file
print()                                                            # WHY: Prints a blank line to add visual spacing between sections
print("Here is some math Python can do:")                          # WHY: Labels the section so you know what comes next
print("2 + 2 =", 2 + 2)      # WHY: Python calculates 2+2 and prints the label and result together
print("10 - 3 =", 10 - 3)    # WHY: Shows subtraction — the comma between items adds a space automatically
print("5 * 6 =", 5 * 6)      # WHY: Shows multiplication — * is the multiply symbol in programming
print("100 / 4 =", 100 / 4)  # WHY: Shows division — notice the result is 25.0 (decimal), not 25
print()                        # WHY: Another blank line for visual breathing room
print("You are off to a great start.")  # WHY: Encouragement — learning to code is a big step
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Use interactive mode first | Seeing instant results builds confidence — you type something, Python responds immediately | Could have started with writing a file, but that adds extra steps before seeing results |
| Show math before text | Numbers are familiar to everyone — math gives instant proof that Python works | Could have started with print(), but math is more concrete and universal |
| Use `*` for multiply and `/` for divide | These are the standard symbols in all programming languages — your keyboard does not have a x or / key for math | None — this is universal across programming |
| Include `exit()` instruction | New users often get stuck in interactive mode, not knowing how to get back to their terminal | Could use Ctrl+D (Mac/Linux) or Ctrl+Z (Windows), but exit() works everywhere |

## Alternative approaches

### Approach B: Run the file directly instead of using interactive mode

```python
# Save this in a file called first_steps.py and run it with: python first_steps.py
print(2 + 2)          # WHY: Same math, but written in a file instead of typed interactively
print(10 - 3)         # WHY: Every line runs automatically, top to bottom
print(5 * 6)          # WHY: You do not have to wait for each result — they all print at once
print(100 / 4)        # WHY: This is how you will write most Python code going forward
print("Hello, I am learning Python!")  # WHY: Files let you save and re-run your code
```

**Trade-off:** Running a file is how you will work most of the time, but interactive mode is better for experimenting because you see each result immediately. Interactive mode is like a calculator; a file is like a recipe.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Typing `python` and getting "command not found" | Python is not installed, or your terminal cannot find it | Revisit the setup guide (03_SETUP_ALL_PLATFORMS.md) and make sure Python is on your PATH |
| Seeing `>>>` but not knowing what to do | You are in interactive mode — Python is waiting for you to type something | Type any math like `2 + 2` and press Enter. Type `exit()` to leave |
| Forgetting the quotes around text in print() | You get a `NameError` because Python thinks the words are variable names, not text | Always wrap text in quotes: `print("Hello")` not `print(Hello)` |
| Typing `print "Hello"` without parentheses | You get a `SyntaxError` — Python 3 requires parentheses around print | Always use `print("Hello")` with parentheses |
| Pressing Enter after `python exercise.py` and nothing happens | You might be in the wrong folder — your terminal cannot find the file | Use `cd` to navigate to the folder containing exercise.py first |

## Key takeaways

1. **Python's interactive mode (`>>>`) is your playground** — use it to experiment, test ideas, and see instant results. You will use it throughout your learning.
2. **Python does math with symbols you mostly know** — `+` for add, `-` for subtract, `*` for multiply (not x), `/` for divide.
3. **`print()` is how you make Python talk to you** — everything you want to display on screen goes inside `print()`. This is the foundation of every program you will write from here on.
