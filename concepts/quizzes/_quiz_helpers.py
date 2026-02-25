"""
Shared helpers for quiz input handling.

Normalizes user answers so that "b", "B", "b)", "(b)", "option b", "B."
all resolve to "b".
"""

import re


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
