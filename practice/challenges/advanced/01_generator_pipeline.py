"""
Challenge 01: Generator Pipeline
Difficulty: Level 6
Topic: Chain generators to process large data streams

Build a pipeline of generators that reads lines of text, filters them,
transforms them, and yields results — all lazily, without loading everything
into memory at once.

Concepts: yield, generator functions, generator chaining, lazy evaluation.
Review: concepts/functions-explained.md (generators section)

Instructions:
    1. Implement `lines_from_data` — yield each string from the input list.
    2. Implement `strip_blank` — yield only non-empty stripped lines.
    3. Implement `to_upper` — yield each line uppercased.
    4. Implement `pipeline` — chain all three generators together and return
       the final generator.
"""

from collections.abc import Generator, Iterable


def lines_from_data(data: list[str]) -> Generator[str, None, None]:
    """Yield each string from *data* as-is."""
    # YOUR CODE HERE
    ...


def strip_blank(lines: Iterable[str]) -> Generator[str, None, None]:
    """Yield only lines that are non-empty after stripping whitespace.

    Each yielded line should be stripped of leading/trailing whitespace.
    """
    # YOUR CODE HERE
    ...


def to_upper(lines: Iterable[str]) -> Generator[str, None, None]:
    """Yield each line converted to uppercase."""
    # YOUR CODE HERE
    ...


def pipeline(data: list[str]) -> Generator[str, None, None]:
    """Chain the three generators: lines_from_data -> strip_blank -> to_upper."""
    # YOUR CODE HERE
    ...


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sample = [
        "hello world",
        "   ",
        "",
        "  Python is great  ",
        "generators rock",
        "",
        "   lazy evaluation   ",
    ]

    result = list(pipeline(sample))
    assert result == [
        "HELLO WORLD",
        "PYTHON IS GREAT",
        "GENERATORS ROCK",
        "LAZY EVALUATION",
    ], f"Expected 4 uppercased lines, got {result}"

    # Empty input
    assert list(pipeline([])) == [], "Empty input should yield nothing"

    # All blank
    assert list(pipeline(["", "   ", "\t"])) == [], "All-blank input should yield nothing"

    # Verify laziness: pipeline() should return a generator, not a list
    gen = pipeline(["test"])
    assert hasattr(gen, "__next__"), "pipeline must return a generator"

    print("All tests passed.")
