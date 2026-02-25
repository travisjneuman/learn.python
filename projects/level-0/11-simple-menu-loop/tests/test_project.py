"""Tests for Simple Menu Loop."""

from project import action_greet, action_reverse, execute_choice, run_batch


def test_action_greet() -> None:
    """Greet should return a greeting string."""
    result = action_greet()
    assert "Hello" in result


def test_action_reverse() -> None:
    """Reverse should reverse the input string."""
    result = action_reverse("hello")
    assert "olleh" in result


def test_execute_choice_unknown() -> None:
    """An invalid choice should return an error message."""
    result = execute_choice("99")
    assert "Unknown option" in result


def test_execute_choice_quit() -> None:
    """Choice 5 should say goodbye."""
    assert execute_choice("5") == "Goodbye!"


def test_run_batch_stops_at_quit() -> None:
    """Batch mode should stop processing when it hits choice 5."""
    commands = ["1", "4 world", "5", "1"]
    results = run_batch(commands)
    # Should have 3 results: greet, reverse, goodbye (not the final '1').
    assert len(results) == 3
    assert results[-1]["output"] == "Goodbye!"
