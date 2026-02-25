"""Module 02 / Project 03 -- Interactive Prompts.

An interactive quiz game that demonstrates:
  - click.prompt() for user input
  - click.confirm() for yes/no questions
  - click.echo() + click.style() for colored output

Run it with:
    python project.py
    python project.py --questions 3
    python project.py --no-confirm
"""

import click

# The quiz bank is a list of dictionaries. Each entry has a question
# and the expected answer (lowercased for case-insensitive comparison).
QUIZ_BANK = [
    {
        "question": "What keyword defines a function in Python?",
        "answer": "def",
    },
    {
        "question": "What built-in function returns the length of a list?",
        "answer": "len",
    },
    {
        "question": "What data type uses curly braces and key:value pairs?",
        "answer": "dict",
    },
    {
        "question": "What keyword starts a loop that repeats for each item in a sequence?",
        "answer": "for",
    },
    {
        "question": "What method adds an item to the end of a list?",
        "answer": "append",
    },
]


def check_answer(user_answer, correct_answer):
    """Compare user's answer to the correct one (case-insensitive).

    Returns True if the answer matches, False otherwise.
    Stripping whitespace and lowering case prevents false negatives
    from extra spaces or capitalization.
    """
    return user_answer.strip().lower() == correct_answer.lower()


def show_result(is_correct, correct_answer):
    """Print a colored result message.

    click.style() wraps text with ANSI color codes.
    The terminal interprets those codes and shows colored text.
    If output is redirected to a file, Click strips the codes automatically.
    """
    if is_correct:
        # Green text with "bold=True" for emphasis.
        styled = click.style("Correct!", fg="green", bold=True)
        click.echo(styled)
    else:
        # Red text for wrong answers, plus the right answer for learning.
        styled = click.style(f"Wrong! The answer is: {correct_answer}", fg="red", bold=True)
        click.echo(styled)


@click.command()
@click.option(
    "--questions", "-q",
    default=None,
    type=int,
    help="Number of questions to ask (default: all).",
)
@click.option(
    "--no-confirm",
    is_flag=True,
    help="Skip the 'ready to start?' confirmation.",
)
def quiz(questions, no_confirm):
    """An interactive Python quiz with colored feedback."""

    # Print a styled title.
    title = click.style("Welcome to the Python Quiz!", fg="cyan", bold=True)
    click.echo(title)

    # click.confirm() asks a yes/no question and returns True or False.
    # "default=True" means pressing Enter without typing counts as "yes".
    # If the user says "no", we exit gracefully.
    if not no_confirm:
        ready = click.confirm("Ready to start?", default=True)
        if not ready:
            click.echo("No worries. Come back when you're ready!")
            return

    # Decide how many questions to ask.
    # If the user passed --questions, use that. Otherwise, use all of them.
    selected = QUIZ_BANK[:questions] if questions else QUIZ_BANK
    total = len(selected)
    score = 0

    click.echo("")  # blank line for readability

    for index, entry in enumerate(selected, start=1):
        # Print the question number with styling.
        header = click.style(f"Question {index} of {total}", fg="yellow")
        click.echo(header)

        # click.prompt() prints the question and waits for input.
        # Unlike input(), it handles encoding on Windows and works
        # correctly when stdin is piped from a file.
        user_answer = click.prompt(entry["question"])

        # Check the answer and show the result.
        correct = check_answer(user_answer, entry["answer"])
        show_result(correct, entry["answer"])

        if correct:
            score += 1

        click.echo("")  # blank line between questions

    # Show the final score with color based on performance.
    click.echo(click.style("---", fg="cyan"))

    # Build the score message.
    score_text = f"Final score: {score}/{total}"

    # Color the score based on how well the user did.
    if score == total:
        click.echo(click.style(score_text, fg="green", bold=True))
        click.echo(click.style("Great job!", fg="green"))
    elif score >= total // 2:
        click.echo(click.style(score_text, fg="yellow", bold=True))
        click.echo(click.style("Not bad! Review the ones you missed.", fg="yellow"))
    else:
        click.echo(click.style(score_text, fg="red", bold=True))
        click.echo(click.style("Keep practicing -- you'll get there.", fg="red"))


# Entry-point guard.
if __name__ == "__main__":
    quiz()
