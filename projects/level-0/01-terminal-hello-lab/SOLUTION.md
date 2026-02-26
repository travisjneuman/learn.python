# Solution: Level 0 / Project 01 - Terminal Hello Lab

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 0 project: Terminal Hello Lab.

Practice printing to the terminal, using variables, and
understanding how Python sends text to your screen.

Concepts: print(), variables, string concatenation, f-strings, escape characters.
"""


# WHY greet is a function: Wrapping the greeting in a function makes it
# reusable and testable.  Tests can call greet("Ada") directly without
# running the whole script or simulating user input.
def greet(name: str) -> str:
    """Build a personalised greeting string."""
    # WHY f-string: f"..." lets us embed variables directly inside the string.
    # It is cleaner than "Hello, " + name + "! Welcome to Python."
    return f"Hello, {name}! Welcome to Python."


# WHY width defaults to 40: Default arguments let callers skip the parameter
# when the common case is fine.  A 40-character banner fits comfortably in
# most terminals.
def build_banner(title: str, width: int = 40) -> str:
    """Create a decorative banner around a title."""
    # WHY "*" * width: String repetition creates a horizontal rule.
    # The * character repeated `width` times makes one border line.
    border = "*" * width

    # WHY .center(): It pads the title with spaces so it sits in the middle.
    # This keeps the output visually balanced regardless of the title length.
    centered_title = title.center(width)

    # WHY join with \n: We build all three lines and combine them with
    # newline characters so the function returns one complete string.
    return f"{border}\n{centered_title}\n{border}"


# WHY build_info_card returns a dict: Dictionaries label each piece of data
# with a key, making the output self-documenting.  Code that receives the
# dict can access card["name"] instead of guessing what index 0 means.
def build_info_card(name: str, language: str, day: int) -> dict:
    """Collect key facts into a dictionary."""
    return {
        "name": name,
        "language": language,
        "learning_day": day,
        # WHY call greet() here: Reusing the greet function avoids duplicating
        # the greeting logic.  If the format changes, we only fix it once.
        "greeting": greet(name),
    }


# WHY run_hello_lab exists: It groups all the "do stuff" steps into one
# callable unit.  The script's __main__ block stays tiny, and tests could
# call this function to verify the full workflow.
def run_hello_lab(name: str, day: int) -> dict:
    """Execute the full hello-lab workflow and return results."""
    # --- Terminal output (side effects) ---
    banner = build_banner("TERMINAL HELLO LAB")
    print(banner)
    print()  # WHY blank line: Visual breathing room between sections.

    greeting = greet(name)
    print(greeting)

    # WHY \t: The tab character indents the text, showing how escape
    # characters control formatting inside strings.
    print(f"\tDay {day} of your Python journey.")
    print()

    # WHY \n inside the string: Demonstrates that escape characters work
    # inside f-strings too — this prints on two lines from one print() call.
    print("Fun fact: Python is named after Monty Python,\nnot the snake!")

    # --- Build summary ---
    summary = build_info_card(name, "Python", day)
    return summary


# WHY __name__ == "__main__": This guard means the code below only runs
# when you execute the file directly (python project.py), NOT when
# another file imports it.  Tests import greet() and build_banner()
# without triggering the interactive input prompts.
if __name__ == "__main__":
    name = input("What is your name? ")
    day_text = input("What day of your Python journey is it? ")

    # WHY int(): input() always returns a string.  We need an integer
    # for the day number so we can do math with it later.
    day = int(day_text)

    summary = run_hello_lab(name, day)

    print("\n--- Your Info Card ---")
    # WHY .items(): Iterating over key-value pairs lets us print
    # every field without knowing the exact keys in advance.
    for key, value in summary.items():
        print(f"  {key}: {value}")
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `greet()` as a standalone function | Makes the greeting testable in isolation — tests call `greet("Ada")` without running the whole script | Inline the greeting with `print(f"Hello, {name}!")` directly — simpler but untestable |
| `build_banner()` uses a `width` default parameter | Callers get a sensible 40-char banner without passing extra arguments, but can customise when needed | Hard-code the width to 40 — less flexible if the title is very long |
| `build_info_card()` returns a `dict` | Keys like `"name"` and `"language"` make data self-documenting; any code can access fields by name | Return a tuple `(name, language, day)` — shorter but relies on positional order, which is fragile |
| `run_hello_lab()` both prints and returns | Lets the interactive script show output AND lets tests inspect the returned dict | Print-only with no return — tests would have to capture stdout, which is harder for beginners |

## Alternative approaches

### Approach B: String concatenation instead of f-strings

```python
def greet(name: str) -> str:
    # Using + to join strings instead of f-strings.
    return "Hello, " + name + "! Welcome to Python."

def build_banner(title: str, width: int = 40) -> str:
    border = "*" * width
    # Using .format() instead of f-strings.
    centered_title = "{:^{}}".format(title, width)
    return border + "\n" + centered_title + "\n" + border
```

**Trade-off:** String concatenation with `+` is the most basic approach and works in all Python versions. However, f-strings (available since Python 3.6) are easier to read when mixing text and variables. You can see at a glance what the output looks like. The `.format()` method is a middle ground — more powerful than `+` but less readable than f-strings. For beginners, f-strings are the recommended default.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| User presses Enter without typing a name (empty string) | `greet("")` returns `"Hello, ! Welcome to Python."` — an awkward blank space | Add a guard: `if not name.strip(): name = "friend"` before calling `greet()` |
| User types letters for the day number (e.g. "seven") | `int("seven")` raises `ValueError` and the program crashes | Wrap `int(day_text)` in a `try/except ValueError` and ask again |
| User types a negative day number (e.g. "-3") | `int("-3")` succeeds, and the program says "Day -3" — technically wrong | Check `if day < 1:` and ask again or default to 1 |
| User types only spaces as their name | `greet("   ")` returns `"Hello,    ! Welcome to Python."` — looks messy | Use `.strip()` on the name and check if it is empty after stripping |

## Key takeaways

1. **Functions make code testable.** By wrapping logic in `greet()` and `build_banner()`, tests can verify each piece independently without simulating user input. This is why every project from here on uses functions.
2. **f-strings are your go-to for mixing text and variables.** The syntax `f"Hello, {name}!"` is clearer than concatenation and will be used in nearly every Python project you encounter.
3. **The `if __name__ == "__main__"` guard separates "library code" from "script code."** This pattern appears in every project going forward and becomes essential when you start importing modules in Level 1+.
4. **Dictionaries bundle related data with meaningful labels.** The `build_info_card()` function previews a pattern you will use constantly — returning structured data from functions instead of just printing it.
