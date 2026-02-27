"""Level 0 project: Terminal Hello Lab.

Practice printing to the terminal, using variables, and
understanding how Python sends text to your screen.

Concepts: print(), variables, string concatenation, f-strings, escape characters.
"""


def greet(name: str) -> str:
    """Build a personalised greeting string.

    WHY a function? -- Putting logic in a function makes it testable.
    We can call greet("Ada") in a test without running the whole script.
    """
    return f"Hello, {name}! Welcome to Python."


def build_banner(title: str, width: int = 40) -> str:
    """Create a decorative banner around a title.

    WHY width defaults to 40? -- Default arguments let callers skip
    the parameter when the common case is fine.
    """
    # The * character repeated `width` times makes a horizontal line.
    border = "*" * width

    # .center() pads the title with spaces so it sits in the middle.
    centered_title = title.center(width)

    # We join three lines with newline characters.
    return f"{border}\n{centered_title}\n{border}"


def build_info_card(name: str, language: str, day: int) -> dict[str, str | int]:
    """Collect key facts into a dictionary.

    WHY a dict? -- Dictionaries let you label each piece of data
    with a key, making the output self-documenting.
    """
    return {
        "name": name,
        "language": language,
        "learning_day": day,
        "greeting": greet(name),
    }


def run_hello_lab(name: str, day: int) -> dict[str, str | int]:
    """Execute the full hello-lab workflow and return results.

    Steps:
    1. Print a banner to the terminal.
    2. Print a personalised greeting.
    3. Print learning-day info.
    4. Return a summary dict.
    """
    # --- Terminal output (side effects) ---
    banner = build_banner("TERMINAL HELLO LAB")
    print(banner)
    print()  # blank line for readability

    greeting = greet(name)
    print(greeting)

    # \t is a tab character -- it indents the text.
    print(f"\tDay {day} of your Python journey.")
    print()

    # Escape characters demo: \n inside a string creates a new line.
    print("Fun fact: Python is named after Monty Python,\nnot the snake!")

    # --- Build summary ---
    summary = build_info_card(name, "Python", day)
    return summary


# This guard means the code below only runs when you execute the file
# directly (python project.py), NOT when another file imports it.
if __name__ == "__main__":
    # Ask the user for their name and learning day using input().
    name = input("What is your name? ")
    day_text = input("What day of your Python journey is it? ")

    # Convert the day to an integer. input() always returns a string.
    day = int(day_text)

    summary = run_hello_lab(name, day)

    # Show the summary at the end.
    print("\n--- Your Info Card ---")
    for key, value in summary.items():
        print(f"  {key}: {value}")
