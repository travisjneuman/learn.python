# Reusable Utils Library — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Level 3 project: Reusable Utils Library."""

from __future__ import annotations

import argparse
import json
import logging
import re
from dataclasses import dataclass, asdict
from typing import Optional

logger = logging.getLogger(__name__)


# -- String utilities -----------------------------------------------------

def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug.

    WHY: URLs cannot contain spaces or special characters. Slugs
    are used in blog post URLs, file names, and API identifiers.
    The three-step regex pipeline handles this reliably.
    """
    text = text.lower().strip()
    # WHY: remove non-word characters (anything that is not a letter,
    # digit, underscore, space, or hyphen).
    text = re.sub(r"[^\w\s-]", "", text)
    # WHY: convert spaces and underscores to hyphens.
    text = re.sub(r"[\s_]+", "-", text)
    # WHY: collapse multiple consecutive hyphens into one.
    text = re.sub(r"-+", "-", text)
    # WHY: strip leading/trailing hyphens that result from edge cases.
    return text.strip("-")


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max_length, adding suffix if truncated.

    WHY: displaying long text in fixed-width UIs (tables, terminals)
    requires controlled truncation. The suffix signals that text
    was cut off.
    """
    if len(text) <= max_length:
        return text
    # WHY: subtract suffix length so total output is exactly max_length.
    return text[: max_length - len(suffix)] + suffix


def snake_to_camel(name: str) -> str:
    """Convert snake_case to camelCase.

    WHY: Python uses snake_case; JavaScript uses camelCase.
    Converting between them is needed when building APIs that
    bridge both languages.
    """
    parts = name.split("_")
    # WHY: first part stays lowercase (camelCase, not PascalCase).
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case.

    WHY: the reverse of snake_to_camel. Inserts an underscore
    before each uppercase letter, then lowercases everything.
    """
    # WHY: ([A-Z]) captures each uppercase letter. r"_\1" inserts
    # an underscore before it. "myVar" -> "_my_Var" -> "my_var".
    result = re.sub(r"([A-Z])", r"_\1", name)
    return result.lower().lstrip("_")


# -- Number utilities -----------------------------------------------------

def clamp(value: float, minimum: float, maximum: float) -> float:
    """Clamp a value between minimum and maximum.

    WHY: clamping is used everywhere — limiting slider values,
    bounding coordinates, preventing negative prices. The nested
    min/max idiom is the standard Python approach.
    """
    return max(minimum, min(maximum, value))


def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    """Divide a by b, returning default if b is zero.

    WHY: division by zero crashes programs. This is one of the most
    common runtime errors. A safe_divide utility prevents it at
    every call site without repetitive if/else checks.
    """
    if b == 0:
        return default
    return a / b


def percentage(part: float, whole: float, decimals: int = 1) -> float:
    """Calculate percentage: (part / whole) * 100.

    WHY: percentage calculation is repeated throughout data analysis
    code. A utility function ensures consistent handling of the
    divide-by-zero edge case (returns 0.0 when whole is 0).
    """
    if whole == 0:
        return 0.0
    return round((part / whole) * 100, decimals)


# -- Collection utilities -------------------------------------------------

def chunk(items: list, size: int) -> list[list]:
    """Split a list into chunks of the given size.

    WHY: batch processing (sending emails in groups of 50, paging
    API results) requires chunking. The slice-based approach is
    clean and handles the last partial chunk automatically.
    """
    if size <= 0:
        raise ValueError("Chunk size must be positive")
    # WHY: range(0, len, size) produces start indices: 0, size, 2*size...
    # Each slice items[i:i+size] grabs one chunk. The last chunk may
    # be shorter, which is correct — [1,2,3,4,5] chunked by 2 gives
    # [[1,2], [3,4], [5]].
    return [items[i : i + size] for i in range(0, len(items), size)]


def flatten(nested: list) -> list:
    """Flatten one level of nesting.

    WHY: flattening only one level is intentional. Deep flattening
    is ambiguous (should strings be flattened into characters?).
    One level is predictable and covers the common case.
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

    WHY: set() removes duplicates but destroys order. This function
    uses a seen-set for O(1) membership checks while building the
    result list in insertion order.
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

    WHY: grouping is fundamental to data analysis. This utility
    replaces the repetitive setdefault/append pattern with a
    single function call.
    """
    groups: dict[str, list[dict]] = {}
    for item in items:
        group_key = str(item.get(key, ""))
        groups.setdefault(group_key, []).append(item)
    return groups


# -- Validation utilities -------------------------------------------------

@dataclass
class ValidationResult:
    """Result of a validation check."""
    valid: bool
    value: str
    errors: list[str]


def validate_email(email: str) -> ValidationResult:
    """Basic email format validation.

    WHY: this is a heuristic, not an RFC-compliant validator.
    For real applications, use a library like email-validator.
    This version catches the most common mistakes.
    """
    errors: list[str] = []
    email = email.strip()

    if not email:
        errors.append("Email is empty")
    elif "@" not in email:
        errors.append("Missing @ symbol")
    elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        # WHY: this pattern checks: something@something.something
        # with no spaces. It rejects "user@", "@domain", and "user@domain"
        # (no TLD). Not perfect, but catches 95% of typos.
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
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Small, single-purpose functions | Each function does one thing and can be tested with one line: `assert slugify("Hello World!") == "hello-world"`. Composability comes from calling multiple utilities together. |
| `chunk` raises ValueError for size <= 0 | An infinite loop or empty results would be confusing. Explicit errors are better than silent misbehaviour. |
| `flatten` only one level deep | Deep flattening is ambiguous (strings are iterable — should "abc" become ["a", "b", "c"]?). One-level flatten is predictable. |
| Regex for slugify instead of translate tables | The three-step pipeline (remove, replace, collapse) is readable and handles Unicode well. `str.translate` is faster but harder to read and modify. |
| `ValidationResult` dataclass | Returning a structured result (valid flag + errors list) is more useful than returning a bare boolean. The caller gets both the answer and the reason. |

## Alternative Approaches

### Using `python-slugify` library

```python
from slugify import slugify

result = slugify("Hello World!")  # "hello-world"
```

**Trade-off:** The library handles Unicode transliteration (e.g., "Hllo Wrld" becomes "hello-world"), which the manual regex approach does not. But adding a dependency for a 5-line function is often not worth it for simple projects.

### Using `itertools` for chunking

```python
from itertools import islice

def chunk_iter(items, size):
    it = iter(items)
    while batch := list(islice(it, size)):
        yield batch
```

**Trade-off:** This is more memory-efficient for very large lists (yields chunks lazily instead of building a full list). But the walrus operator (`:=`) and `islice` are harder for beginners to read than the slice-based approach.

## Common Pitfalls

1. **`chunk(items, 0)` causing an infinite loop** — `range(0, len(items), 0)` raises `ValueError` in Python, but if you implemented chunking with a while-loop, size=0 would loop forever. The explicit check prevents this.

2. **`slugify` producing empty strings** — Input like `"!!!"` removes all characters and returns `""`. Depending on use case, you may want to return a fallback like `"untitled"` instead.

3. **`camel_to_snake` on already-snake strings** — `camel_to_snake("my_var")` produces `"my_var"` (correct), but `camel_to_snake("MyVar")` produces `"my_var"` while `camel_to_snake("myVAR")` produces `"my_v_a_r"`. Consecutive uppercase letters (acronyms) need special handling in production code.
