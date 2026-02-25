"""Tests for Yes/No Questionnaire."""

from pathlib import Path

from project import load_questions, normalise_answer, tally_answers


def test_normalise_yes_variants() -> None:
    """All common yes spellings should normalise to 'yes'."""
    for word in ["yes", "YES", "Y", "Yeah", "yep", "TRUE", "1"]:
        assert normalise_answer(word) == "yes"


def test_normalise_no_variants() -> None:
    """All common no spellings should normalise to 'no'."""
    for word in ["no", "NO", "n", "Nah", "nope", "false", "0"]:
        assert normalise_answer(word) == "no"


def test_normalise_garbage_is_invalid() -> None:
    """Anything that is not a yes/no variant should be 'invalid'."""
    assert normalise_answer("banana") == "invalid"
    assert normalise_answer("") == "invalid"


def test_tally_answers_counts_correctly() -> None:
    """tally_answers should produce correct counts and percentages."""
    answers = ["yes", "no", "y", "N", "maybe"]
    result = tally_answers(answers)
    assert result["yes"] == 2
    assert result["no"] == 2
    assert result["invalid"] == 1
    assert result["total"] == 5


def test_load_questions_skips_blanks(tmp_path: Path) -> None:
    """Blank lines in the questions file should be skipped."""
    f = tmp_path / "q.txt"
    f.write_text("Do you like Python?\n\nIs the sky blue?\n", encoding="utf-8")
    questions = load_questions(f)
    assert len(questions) == 2
