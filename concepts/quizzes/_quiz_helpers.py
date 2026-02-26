"""
Shared helpers for quiz input handling.

Normalizes user answers so that "b", "B", "b)", "(b)", "option b", "B."
all resolve to "b".
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
