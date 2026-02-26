"""
Fill-In Challenge #3 — File Reader

Implement the functions below. Each one reads and parses text data.
"""


def parse_csv_line(line):
    """Parse a single CSV line into a list of fields.

    Simple CSV: split on commas, strip whitespace from each field.
    No need to handle quoted fields or escaped commas.

    Args:
        line: A string like "Alice, 25, Engineer"

    Returns:
        A list of stripped strings: ["Alice", "25", "Engineer"]
    """
    # YOUR CODE HERE
    pass


def parse_key_value(text):
    """Parse a block of key=value lines into a dictionary.

    Each line has the format "key=value". Blank lines and lines
    starting with '#' should be skipped.

    Args:
        text: A multi-line string.

    Returns:
        A dictionary of string keys to string values.

    Example:
        parse_key_value("name=Alice\\nage=25\\n# comment\\n\\nrole=admin")
        -> {"name": "Alice", "age": "25", "role": "admin"}
    """
    # YOUR CODE HERE
    pass


def parse_table(lines):
    """Parse a list of CSV lines into a list of dictionaries.

    The first line is the header row. Each subsequent line is a data row.
    Use the header values as dictionary keys.

    Args:
        lines: A list of strings. First element is the header.

    Returns:
        A list of dictionaries, one per data row.

    Example:
        parse_table(["name,age", "Alice,25", "Bob,30"])
        -> [{"name": "Alice", "age": "25"}, {"name": "Bob", "age": "30"}]
    """
    # YOUR CODE HERE
    pass
