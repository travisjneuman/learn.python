"""
Challenge: Generator Pipeline
Difficulty: Intermediate
Concepts: generators, yield, chaining, lazy evaluation
Time: 30 minutes

Build a data processing pipeline using generators. Implement three generator
functions that can be chained together:

1. `read_lines(text)` -- yields each line from a multi-line string
2. `filter_nonempty(lines)` -- yields only non-empty, non-whitespace lines
3. `to_upper(lines)` -- yields each line converted to uppercase

Then implement `pipeline(text)` that chains all three and returns a list.

Examples:
    >>> pipeline("hello\\n\\nworld\\n  \\nfoo")
    ['HELLO', 'WORLD', 'FOO']
"""


def read_lines(text: str):
    """Yield each line from a multi-line string. Implement this generator."""
    # Hint: Use text.split("\\n") and yield each element.
    pass


def filter_nonempty(lines):
    """Yield only lines that are not empty or whitespace-only. Implement this generator."""
    # Hint: Use .strip() to check if a line has content.
    pass


def to_upper(lines):
    """Yield each line converted to uppercase. Implement this generator."""
    # Hint: Use .upper() on each line.
    pass


def pipeline(text: str) -> list[str]:
    """Chain the three generators and return the result as a list. Implement this function."""
    # Hint: Pass the output of one generator as input to the next.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Basic pipeline
    assert pipeline("hello\n\nworld\n  \nfoo") == ["HELLO", "WORLD", "FOO"], "Basic pipeline failed"

    # Test 2: All empty lines
    assert pipeline("\n\n  \n") == [], "All empty lines failed"

    # Test 3: Single line
    assert pipeline("test") == ["TEST"], "Single line failed"

    # Test 4: read_lines is a generator
    gen = read_lines("a\nb")
    assert hasattr(gen, "__next__"), "read_lines should be a generator"

    # Test 5: Generators are lazy (filter_nonempty)
    gen = filter_nonempty(iter(["hello", "", "world"]))
    assert next(gen) == "hello", "filter_nonempty laziness failed"
    assert next(gen) == "world", "filter_nonempty second yield failed"

    # Test 6: Empty input
    assert pipeline("") == [], "Empty input failed"

    print("All tests passed!")
