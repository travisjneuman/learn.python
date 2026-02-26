"""
Fill-In Challenge #4 — String Formatter

Implement the functions below. Each one formats strings for display.
"""


def left_pad(text, width, char=" "):
    """Pad a string on the left to reach the desired width.

    Args:
        text: The string to pad.
        width: The target total width.
        char: The padding character (default space).

    Returns:
        The padded string. If text is already >= width, return it unchanged.

    Example:
        left_pad("42", 5, "0") -> "00042"
        left_pad("hello", 3) -> "hello"
    """
    # YOUR CODE HERE
    pass


def format_table_row(columns, widths):
    """Format a list of values into a fixed-width table row.

    Each column is left-aligned within its width, separated by " | ".

    Args:
        columns: A list of strings (the cell values).
        widths: A list of integers (column widths), same length as columns.

    Returns:
        A single string with aligned columns.

    Example:
        format_table_row(["Name", "Age"], [10, 5]) -> "Name       | Age  "
    """
    # YOUR CODE HERE
    pass


def build_report(title, rows):
    """Build a formatted report with a title and data rows.

    Format:
        === TITLE ===
        Name       | Score
        -----------+------
        Alice      | 95
        Bob        | 87

    Args:
        title: Report title string.
        rows: List of (name, score) tuples.

    Returns:
        The complete report as a single string.
    """
    # YOUR CODE HERE
    pass


def truncate(text, max_length, suffix="..."):
    """Truncate text to max_length, adding suffix if truncated.

    The suffix is included in the max_length count.

    Args:
        text: The string to truncate.
        max_length: Maximum total length of the result.
        suffix: String to append when truncating (default "...").

    Returns:
        The original text if short enough, or truncated text with suffix.

    Example:
        truncate("Hello, world!", 10) -> "Hello, ..."
        truncate("Hi", 10) -> "Hi"
    """
    # YOUR CODE HERE
    pass
