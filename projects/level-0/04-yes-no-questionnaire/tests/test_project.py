"""Tests for Yes/No Questionnaire."""

from project import normalise_answer, tally_answers


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


def test_tally_empty_list() -> None:
    """An empty answer list should return zero counts without crashing."""
    result = tally_answers([])
    assert result["total"] == 0
    assert result["yes"] == 0
    assert result["yes_percent"] == 0.0
