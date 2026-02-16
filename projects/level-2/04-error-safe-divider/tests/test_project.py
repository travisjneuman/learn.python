"""Beginner test module with heavy comments.

Why these tests exist:
- They prove file-reading behavior for normal input.
- They prove failure behavior for missing files.
- They show how tiny tests protect core assumptions.
"""

# pathlib.Path is used to create temporary files and paths in tests.
from pathlib import Path

# Import the function under test directly from the project module.
from project import load_items


def test_load_items_strips_blank_lines(tmp_path: Path) -> None:
    """Happy-path test for input cleanup behavior."""
    # Arrange:
    # Create a temporary file with blank lines and padded whitespace.
    sample = tmp_path / "sample.txt"
    sample.write_text("alpha\n\n beta \n", encoding="utf-8")

    # Act:
    # Run the loader function that should clean and filter lines.
    items = load_items(sample)

    # Assert:
    # Verify that blank lines are removed and spaces are trimmed.
    assert items == ["alpha", "beta"]


def test_load_items_missing_file_raises(tmp_path: Path) -> None:
    """Failure-path test for missing-file safety."""
    # Arrange:
    # Point to a file that does not exist.
    missing = tmp_path / "missing.txt"

    # Act + Assert:
    # We expect FileNotFoundError. If not raised, the test must fail.
    try:
        load_items(missing)
    except FileNotFoundError:
        # Expected path: behavior is correct.
        assert True
        return

    # Unexpected path: function failed to enforce missing-file guardrail.
    assert False, "Expected FileNotFoundError"
