"""Level 0 project: Yes/No Questionnaire.

Present questions one at a time, collect yes/no answers,
tally the results, and show a summary.

Concepts: boolean logic, input normalisation, counters, lists, dicts.
"""


def normalise_answer(raw: str) -> str:
    """Convert a raw answer string to 'yes', 'no', or 'invalid'.

    WHY normalise? -- Users type in many ways: 'YES', 'y', 'Yeah'.
    Normalising means we only have to check a small set of values
    instead of every possible spelling.
    """
    cleaned = raw.strip().lower()

    # Accept several common ways people say yes or no.
    if cleaned in ("yes", "y", "yeah", "yep", "true", "1"):
        return "yes"
    if cleaned in ("no", "n", "nah", "nope", "false", "0"):
        return "no"

    return "invalid"


def tally_answers(answers: list[str]) -> dict[str, int | float]:
    """Count how many yes, no, and invalid answers were given.

    WHY return a dict? -- Dicts let us label each count with a
    descriptive key, making the output self-documenting.
    """
    counts = {"yes": 0, "no": 0, "invalid": 0}

    for answer in answers:
        normalised = normalise_answer(answer)
        counts[normalised] += 1

    total = len(answers)
    counts["total"] = total

    # Calculate percentages (avoid dividing by zero).
    if total > 0:
        counts["yes_percent"] = round(counts["yes"] / total * 100, 1)
        counts["no_percent"] = round(counts["no"] / total * 100, 1)
    else:
        counts["yes_percent"] = 0.0
        counts["no_percent"] = 0.0

    return counts


# This guard means the code below only runs when you execute the file
# directly (python project.py), NOT when another file imports it.
if __name__ == "__main__":
    # Define some questions directly in the program.
    questions = [
        "Do you enjoy learning new things?",
        "Have you used a computer before today?",
        "Do you like solving puzzles?",
        "Are you excited to learn Python?",
        "Do you prefer working alone?",
    ]

    print("=== Yes/No Questionnaire ===")
    print(f"Answer {len(questions)} questions with yes or no.\n")

    answers = []
    for i, question in enumerate(questions, start=1):
        answer = input(f"  {i}. {question} ")
        answers.append(answer)

    # Show results.
    tally = tally_answers(answers)

    print("\n=== Results ===")
    print(f"  Total responses: {tally['total']}")
    print(f"  Yes: {tally['yes']} ({tally['yes_percent']}%)")
    print(f"  No:  {tally['no']} ({tally['no_percent']}%)")
    print(f"  Invalid: {tally['invalid']}")
