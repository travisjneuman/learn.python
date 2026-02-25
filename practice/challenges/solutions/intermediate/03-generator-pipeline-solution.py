"""
Solution: Generator Pipeline

Approach: Each stage is a generator function that yields items one at a time.
Generators are lazy -- they only produce values when asked. Chaining them
means data flows through the pipeline one item at a time without building
intermediate lists.
"""


def read_lines(text: str):
    """Yield each line from a multi-line string."""
    for line in text.split("\n"):
        yield line


def filter_nonempty(lines):
    """Yield only lines that contain non-whitespace characters."""
    for line in lines:
        if line.strip():
            yield line.strip()


def to_upper(lines):
    """Yield each line converted to uppercase."""
    for line in lines:
        yield line.upper()


def pipeline(text: str) -> list[str]:
    """Chain the three generators and collect results into a list."""
    return list(to_upper(filter_nonempty(read_lines(text))))


if __name__ == "__main__":
    assert pipeline("hello\n\nworld\n  \nfoo") == ["HELLO", "WORLD", "FOO"]
    assert pipeline("\n\n  \n") == []
    assert pipeline("test") == ["TEST"]

    gen = read_lines("a\nb")
    assert hasattr(gen, "__next__")

    gen = filter_nonempty(iter(["hello", "", "world"]))
    assert next(gen) == "hello"
    assert next(gen) == "world"

    assert pipeline("") == []

    print("All tests passed!")
