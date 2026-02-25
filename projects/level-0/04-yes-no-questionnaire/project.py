"""Level 0 project: Yes/No Questionnaire.

Read questions from a file, present them one at a time, tally
yes/no/invalid answers, and write a results summary.

Concepts: boolean logic, input normalisation, counters, lists, dicts.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


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


def load_questions(path: Path) -> list[str]:
    """Load questions from a text file (one per line).

    Blank lines are skipped so extra whitespace in the file
    does not create empty questions.
    """
    if not path.exists():
        raise FileNotFoundError(f"Questions file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip()]


def tally_answers(answers: list[str]) -> dict:
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


def run_questionnaire(questions: list[str], answers: list[str]) -> dict:
    """Pair each question with its answer and build a full report.

    Returns a dict with the question-answer pairs and the tally.
    """
    pairs = []
    for i, question in enumerate(questions):
        raw_answer = answers[i] if i < len(answers) else ""
        pairs.append({
            "question": question,
            "raw_answer": raw_answer,
            "normalised": normalise_answer(raw_answer),
        })

    tally = tally_answers(answers)
    return {"responses": pairs, "tally": tally}


def parse_args() -> argparse.Namespace:
    """Define command-line options."""
    parser = argparse.ArgumentParser(description="Yes/No Questionnaire")
    parser.add_argument("--questions", default="data/sample_input.txt",
                        help="File with questions (one per line)")
    parser.add_argument("--answers", default="data/answers.txt",
                        help="File with answers (one per line)")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    """Program entry point."""
    args = parse_args()

    questions = load_questions(Path(args.questions))
    # Try to load pre-written answers; if no file, use empty list.
    answers_path = Path(args.answers)
    if answers_path.exists():
        answers = [line.strip() for line in
                   answers_path.read_text(encoding="utf-8").splitlines()
                   if line.strip()]
    else:
        answers = []

    report = run_questionnaire(questions, answers)

    # Print the tally to the terminal.
    tally = report["tally"]
    print("=== Questionnaire Results ===")
    print(f"  Total responses: {tally['total']}")
    print(f"  Yes: {tally['yes']} ({tally['yes_percent']}%)")
    print(f"  No:  {tally['no']} ({tally['no_percent']}%)")
    print(f"  Invalid: {tally['invalid']}")

    # Write full report to JSON.
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nFull report written to {output_path}")


if __name__ == "__main__":
    main()
