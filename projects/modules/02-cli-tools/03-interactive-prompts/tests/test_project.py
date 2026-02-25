"""Tests for Module 02 / Project 03 — Interactive Prompts.

Tests the check_answer() helper and the quiz CLI command using CliRunner.
For the interactive quiz, we simulate user input by passing it to CliRunner.

WHY test check_answer() separately?
- It is a pure function (no side effects, no I/O) — easy to unit test.
- Testing it directly gives us confidence that answer checking works,
  independent of the CLI prompt flow.
"""

import sys
import os

import pytest
from click.testing import CliRunner

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import check_answer, show_result, quiz, QUIZ_BANK


# ---------------------------------------------------------------------------
# Tests for check_answer()
# ---------------------------------------------------------------------------

def test_check_answer_correct():
    """check_answer() should return True when the answer matches exactly."""
    assert check_answer("def", "def") is True


def test_check_answer_case_insensitive():
    """check_answer() should be case-insensitive.

    A learner might type 'Def' or 'DEF' — both should be accepted.
    The function lowercases both sides before comparing.
    """
    assert check_answer("DEF", "def") is True
    assert check_answer("Def", "def") is True


def test_check_answer_strips_whitespace():
    """check_answer() should ignore leading and trailing whitespace.

    Users often accidentally add spaces. Stripping prevents false negatives.
    """
    assert check_answer("  def  ", "def") is True


def test_check_answer_wrong():
    """check_answer() should return False when the answer does not match."""
    assert check_answer("class", "def") is False


def test_check_answer_empty_input():
    """check_answer() should return False for empty input."""
    assert check_answer("", "def") is False


# ---------------------------------------------------------------------------
# Tests for show_result()
# ---------------------------------------------------------------------------

def test_show_result_correct(capsys):
    """show_result() should print 'Correct!' when is_correct is True."""
    show_result(True, "def")

    output = capsys.readouterr().out
    assert "Correct" in output


def test_show_result_wrong_shows_answer(capsys):
    """show_result() should show the correct answer when is_correct is False.

    This helps the learner see what the right answer was so they can learn.
    """
    show_result(False, "def")

    output = capsys.readouterr().out
    assert "def" in output


# ---------------------------------------------------------------------------
# Tests for the quiz CLI command
# ---------------------------------------------------------------------------

def test_quiz_skips_on_no_confirm():
    """If the user says 'no' to the ready prompt, the quiz should exit early.

    We simulate typing 'n' when asked 'Ready to start?'.
    """
    runner = CliRunner()
    result = runner.invoke(quiz, [], input="n\n")

    assert result.exit_code == 0
    assert "Come back" in result.output or "No worries" in result.output


def test_quiz_with_no_confirm_flag():
    """--no-confirm should skip the ready prompt and go straight to questions.

    We provide answers for all questions in the quiz bank.
    """
    runner = CliRunner()
    # Build input: one answer per question, all wrong (just type 'x')
    answers = "\n".join(["x"] * len(QUIZ_BANK)) + "\n"
    result = runner.invoke(quiz, ["--no-confirm"], input=answers)

    assert result.exit_code == 0
    assert "Final score" in result.output


def test_quiz_limited_questions():
    """--questions N should only ask N questions instead of all of them."""
    runner = CliRunner()
    # Ask 2 questions, answer both with 'x' (wrong)
    answers = "x\nx\n"
    result = runner.invoke(quiz, ["--no-confirm", "--questions", "2"], input=answers)

    assert result.exit_code == 0
    assert "Final score: 0/2" in result.output


def test_quiz_correct_answers_counted():
    """Correct answers should increase the score.

    We answer the first question correctly and the rest wrong.
    """
    runner = CliRunner()
    # First question's answer is QUIZ_BANK[0]["answer"]
    correct = QUIZ_BANK[0]["answer"]
    answers = f"{correct}\nx\n"
    result = runner.invoke(quiz, ["--no-confirm", "--questions", "2"], input=answers)

    assert result.exit_code == 0
    assert "Final score: 1/2" in result.output


def test_quiz_bank_is_not_empty():
    """QUIZ_BANK should contain at least one question.

    This is a sanity check — if the bank is empty, the quiz does nothing.
    """
    assert len(QUIZ_BANK) > 0

    for entry in QUIZ_BANK:
        assert "question" in entry
        assert "answer" in entry
