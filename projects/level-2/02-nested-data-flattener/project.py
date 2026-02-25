"""Level 2 project: Nested Data Flattener.

Heavily commented beginner-friendly script:
- take a deeply nested dict/JSON structure,
- flatten it to dot-notation keys like "user.address.city",
- unflatten it back to the original structure.

Skills practiced: recursion, nested data structures, dict comprehensions,
try/except for JSON parsing, enumerate, type checking with isinstance.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def flatten(data: dict, prefix: str = "", separator: str = ".") -> dict[str, object]:
    """Flatten a nested dictionary into dot-notation keys.

    Example:
        {"user": {"name": "Ada"}} -> {"user.name": "Ada"}

    Lists are flattened with numeric indices:
        {"tags": ["a", "b"]} -> {"tags.0": "a", "tags.1": "b"}

    Args:
        data: The nested dictionary to flatten.
        prefix: Current key prefix (used in recursion — leave empty).
        separator: Character joining key segments (default ".").

    Returns:
        A flat dict where every key is a dotted path to a leaf value.
    """
    items: dict[str, object] = {}

    for key, value in data.items():
        # Build the new key by joining prefix and current key.
        new_key = f"{prefix}{separator}{key}" if prefix else key

        if isinstance(value, dict):
            # Recurse into nested dicts — this is where the magic happens.
            items.update(flatten(value, prefix=new_key, separator=separator))
        elif isinstance(value, list):
            # Flatten lists by treating each index as a key segment.
            for idx, item in enumerate(value):
                list_key = f"{new_key}{separator}{idx}"
                if isinstance(item, dict):
                    items.update(flatten(item, prefix=list_key, separator=separator))
                else:
                    items[list_key] = item
        else:
            # Base case: leaf value (str, int, float, bool, None).
            items[new_key] = value

    return items


def unflatten(data: dict[str, object], separator: str = ".") -> dict:
    """Reconstruct a nested dictionary from dot-notation keys.

    This is the inverse of flatten().

    Args:
        data: A flat dict with dotted keys.
        separator: The separator used during flattening.

    Returns:
        A nested dict matching the original structure.
    """
    result: dict = {}

    for compound_key, value in data.items():
        parts = compound_key.split(separator)
        target = result

        # Walk through all parts except the last, creating nested dicts.
        for part in parts[:-1]:
            target = target.setdefault(part, {})

        # Set the leaf value.
        target[parts[-1]] = value

    return result


def flatten_from_file(path: Path, separator: str = ".") -> dict[str, object]:
    """Read a JSON file and return the flattened version.

    Raises:
        FileNotFoundError: If the path does not exist.
        ValueError: If the file is not valid JSON.
        TypeError: If the JSON root is not a dict.
    """
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    raw = path.read_text(encoding="utf-8")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise TypeError(f"Expected a JSON object (dict), got {type(data).__name__}")

    return flatten(data, separator=separator)


def depth(data: dict) -> int:
    """Calculate the maximum nesting depth of a dictionary.

    An empty dict or non-dict value has depth 0.
    {"a": {"b": 1}} has depth 2.
    """
    if not isinstance(data, dict) or not data:
        return 0
    return 1 + max(
        depth(v) if isinstance(v, dict) else 0 for v in data.values()
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Flatten or unflatten nested JSON data"
    )
    parser.add_argument("input", help="Path to JSON input file")
    parser.add_argument(
        "--separator", default=".", help="Key separator (default '.')"
    )
    parser.add_argument(
        "--unflatten",
        action="store_true",
        help="Unflatten a previously flattened file",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point: flatten or unflatten a JSON file."""
    args = parse_args()
    path = Path(args.input)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))

    if args.unflatten:
        result = unflatten(data, separator=args.separator)
    else:
        result = flatten(data, separator=args.separator)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
