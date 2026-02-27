"""
Shared helpers for quiz input handling.

Normalizes user answers so that "b", "B", "b)", "(b)", "option b", "B."
all resolve to "b".

Also provides helpers for additional question types:
    - ask_true_false(): Present a statement, learner answers True or False
    - ask_code_completion(): Show code with a blank, learner types the missing piece
"""

import re
from pathlib import Path


def normalize_answer(raw: str) -> str:
    """Normalize a quiz answer to a single lowercase letter (or plain value).

    Handles these common input formats:
        "b", "B", "b)", "(b)", "option b", "B.", "answer: b"

    For non-letter answers (e.g. "26", "True"), strips whitespace and lowercases.

    Returns the cleaned answer string.
    """
    cleaned = raw.strip().lower()
    if not cleaned:
        return ""

    # Try to extract a single letter from common answer formats.
    # Matches patterns like: (b), b), b., option b, answer: b, answer b
    match = re.match(
        r"^(?:\(?)?([a-z])(?:\)?\.?)$"          # b | b) | (b) | b.
        r"|^option\s+([a-z])$"                   # option b
        r"|^answer[:\s]+([a-z])$",               # answer: b | answer b
        cleaned,
    )
    if match:
        # Return whichever group matched
        return next(g for g in match.groups() if g is not None)

    return cleaned


def _normalize_bool(raw: str) -> str:
    """Normalize a True/False answer to 'true' or 'false'.

    Accepts: True, true, T, t, Yes, yes, Y, y, 1  -> 'true'
             False, false, F, f, No, no, N, n, 0   -> 'false'

    Returns 'true', 'false', or the raw cleaned string if unrecognized.
    """
    cleaned = raw.strip().lower()
    if cleaned in ("true", "t", "yes", "y", "1"):
        return "true"
    if cleaned in ("false", "f", "no", "n", "0"):
        return "false"
    return cleaned


def ask_true_false(
    question_num: int,
    total: int,
    statement: str,
    correct: bool,
    explanation_correct: str,
    explanation_incorrect: str,
) -> bool:
    """Present a True/False question and return whether the learner got it right.

    Parameters:
        question_num: The question number (e.g. 5)
        total: Total questions in the quiz (e.g. 9)
        statement: The statement the learner evaluates
        correct: True if the statement is true, False if it is false
        explanation_correct: Feedback when the learner answers correctly
        explanation_incorrect: Feedback when the learner answers incorrectly

    Returns True if the learner answered correctly, False otherwise.
    """
    print(f"Question {question_num}/{total} [True/False]:")
    print(f"  \"{statement}\"")
    print()
    print("  Type True or False.")
    print()
    answer = _normalize_bool(input("Your answer: "))
    expected = "true" if correct else "false"

    if answer == expected:
        print(f"Correct! {explanation_correct}")
        print()
        return True

    if answer not in ("true", "false"):
        print(f"Please answer True or False. The correct answer is {expected.title()}.")
    else:
        print(f"Incorrect. The answer is {expected.title()}.")
    print(explanation_incorrect)
    print()
    return False


def ask_code_completion(
    question_num: int,
    total: int,
    prompt: str,
    code_lines: list[str],
    correct_answers: list[str],
    explanation_correct: str,
    explanation_incorrect: str,
    case_sensitive: bool = True,
) -> bool:
    """Present a code-completion question and return whether the learner got it right.

    One of the code_lines should contain '____' to mark the blank.
    The learner types the missing piece.

    Parameters:
        question_num: The question number (e.g. 6)
        total: Total questions in the quiz (e.g. 9)
        prompt: A short description of what the code should do
        code_lines: Lines of code to display (one should contain '____')
        correct_answers: Accepted answers (e.g. [".append(", "append("])
        explanation_correct: Feedback when correct
        explanation_incorrect: Feedback when incorrect
        case_sensitive: Whether to compare case-sensitively (default True)

    Returns True if the learner answered correctly, False otherwise.
    """
    print(f"Question {question_num}/{total} [Fill in the blank]:")
    print(f"  {prompt}")
    print()
    for line in code_lines:
        print(f"  {line}")
    print()
    print("  Type the code that replaces ____")
    print()
    raw = input("Your answer: ").strip()

    if case_sensitive:
        got_it = raw in correct_answers
    else:
        got_it = raw.lower() in [a.lower() for a in correct_answers]

    if got_it:
        print(f"Correct! {explanation_correct}")
        print()
        return True

    print(f"Incorrect. Expected: {correct_answers[0]}")
    print(explanation_incorrect)
    print()
    return False


def award_quiz_xp(quiz_name):
    """Award XP for passing a quiz. Fails silently if tracker unavailable."""
    try:
        import sys
        tools_dir = str(Path(__file__).parent.parent.parent / "tools")
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        from xp_tracker import award_xp
        from streak_tracker import record_activity
        award_xp("quiz_pass", quiz_name)
        record_activity("quiz")
    except Exception:
        pass
