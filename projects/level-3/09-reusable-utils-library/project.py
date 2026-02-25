"""Level 3 project: Reusable Utils Library.

Builds a collection of general-purpose utility functions that could
be imported by other projects. Focuses on writing testable, documented,
type-hinted helper functions.

Skills practiced: function design, typing basics, dataclasses,
logging, re module, docstrings, reusable API design.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from dataclasses import dataclass, asdict
from typing import Optional

logger = logging.getLogger(__name__)


# ── String utilities ──────────────────────────────────────────

def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug.

    'Hello World!' -> 'hello-world'
    """
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)  # Remove non-word chars.
    text = re.sub(r"[\s_]+", "-", text)   # Spaces/underscores to hyphens.
    text = re.sub(r"-+", "-", text)       # Collapse multiple hyphens.
    return text.strip("-")


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max_length, adding suffix if truncated.

    truncate('Hello World', 8) -> 'Hello...'
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def snake_to_camel(name: str) -> str:
    """Convert snake_case to camelCase.

    'my_variable_name' -> 'myVariableName'
    """
    parts = name.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case.

    'myVariableName' -> 'my_variable_name'
    """
    result = re.sub(r"([A-Z])", r"_\1", name)
    return result.lower().lstrip("_")


# ── Number utilities ──────────────────────────────────────────

def clamp(value: float, minimum: float, maximum: float) -> float:
    """Clamp a value between minimum and maximum.

    clamp(15, 0, 10) -> 10
    clamp(-5, 0, 10) -> 0
    """
    return max(minimum, min(maximum, value))


def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    """Divide a by b, returning default if b is zero."""
    if b == 0:
        return default
    return a / b


def percentage(part: float, whole: float, decimals: int = 1) -> float:
    """Calculate percentage: (part / whole) * 100.

    Returns 0.0 if whole is zero.
    """
    if whole == 0:
        return 0.0
    return round((part / whole) * 100, decimals)


# ── Collection utilities ──────────────────────────────────────

def chunk(items: list, size: int) -> list[list]:
    """Split a list into chunks of the given size.

    chunk([1,2,3,4,5], 2) -> [[1,2], [3,4], [5]]
    """
    if size <= 0:
        raise ValueError("Chunk size must be positive")
    return [items[i : i + size] for i in range(0, len(items), size)]


def flatten(nested: list) -> list:
    """Flatten one level of nesting.

    flatten([[1, 2], [3, 4]]) -> [1, 2, 3, 4]
    """
    result: list = []
    for item in nested:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result


def unique_ordered(items: list) -> list:
    """Remove duplicates while preserving order.

    unique_ordered([3, 1, 2, 1, 3]) -> [3, 1, 2]
    """
    seen: set = set()
    result: list = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def group_by(items: list[dict], key: str) -> dict[str, list[dict]]:
    """Group a list of dicts by a key field.

    group_by([{'type': 'a'}, {'type': 'b'}, {'type': 'a'}], 'type')
    -> {'a': [{...}, {...}], 'b': [{...}]}
    """
    groups: dict[str, list[dict]] = {}
    for item in items:
        group_key = str(item.get(key, ""))
        groups.setdefault(group_key, []).append(item)
    return groups


# ── Validation utilities ──────────────────────────────────────

@dataclass
class ValidationResult:
    """Result of a validation check."""
    valid: bool
    value: str
    errors: list[str]


def validate_email(email: str) -> ValidationResult:
    """Basic email format validation."""
    errors: list[str] = []
    email = email.strip()

    if not email:
        errors.append("Email is empty")
    elif "@" not in email:
        errors.append("Missing @ symbol")
    elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        errors.append("Invalid email format")

    return ValidationResult(valid=len(errors) == 0, value=email, errors=errors)


def validate_url(url: str) -> ValidationResult:
    """Basic URL format validation."""
    errors: list[str] = []
    url = url.strip()

    if not url:
        errors.append("URL is empty")
    elif not re.match(r"^https?://[^\s]+", url):
        errors.append("URL must start with http:// or https://")

    return ValidationResult(valid=len(errors) == 0, value=url, errors=errors)


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser for demonstrating utilities."""
    parser = argparse.ArgumentParser(description="Reusable utils library")

    sub = parser.add_subparsers(dest="command")

    slug = sub.add_parser("slugify", help="Convert text to slug")
    slug.add_argument("text", help="Text to slugify")

    convert = sub.add_parser("convert", help="Convert naming convention")
    convert.add_argument("name", help="Name to convert")
    convert.add_argument("--to", choices=["camel", "snake"], required=True)

    validate = sub.add_parser("validate", help="Validate a value")
    validate.add_argument("value", help="Value to validate")
    validate.add_argument("--type", choices=["email", "url"], required=True)

    return parser


def main() -> None:
    """Entry point."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "slugify":
        print(slugify(args.text))

    elif args.command == "convert":
        if args.to == "camel":
            print(snake_to_camel(args.name))
        else:
            print(camel_to_snake(args.name))

    elif args.command == "validate":
        if args.type == "email":
            result = validate_email(args.value)
        else:
            result = validate_url(args.value)
        print(json.dumps(asdict(result), indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
