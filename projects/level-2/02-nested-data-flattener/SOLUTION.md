# Nested Data Flattener — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Nested Data Flattener — complete annotated solution."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def flatten(data: dict, prefix: str = "", separator: str = ".") -> dict[str, object]:
    """Flatten a nested dictionary into dot-notation keys.

    Example: {"user": {"name": "Ada"}} -> {"user.name": "Ada"}
    """
    items: dict[str, object] = {}

    for key, value in data.items():
        # WHY: Build the full path by joining prefix and key. On the first call
        # prefix is empty so we just use the key itself. On recursive calls,
        # prefix carries the parent path (e.g. "user" -> "user.name").
        new_key = f"{prefix}{separator}{key}" if prefix else key

        if isinstance(value, dict):
            # WHY: Recursion — when the value is itself a dict, we go deeper.
            # items.update() merges the returned flat keys into our result.
            items.update(flatten(value, prefix=new_key, separator=separator))
        elif isinstance(value, list):
            # WHY: Lists are flattened by treating each index as a key segment.
            # {"tags": ["a", "b"]} becomes {"tags.0": "a", "tags.1": "b"}.
            for idx, item in enumerate(value):
                list_key = f"{new_key}{separator}{idx}"
                if isinstance(item, dict):
                    # WHY: List items can themselves be dicts, so recurse again.
                    items.update(flatten(item, prefix=list_key, separator=separator))
                else:
                    items[list_key] = item
        else:
            # WHY: Base case — leaf values (str, int, float, bool, None)
            # get stored directly under the fully-qualified key.
            items[new_key] = value

    return items


def unflatten(data: dict[str, object], separator: str = ".") -> dict:
    """Reconstruct a nested dictionary from dot-notation keys."""
    result: dict = {}

    for compound_key, value in data.items():
        parts = compound_key.split(separator)
        target = result

        # WHY: Walk through all parts except the last, creating intermediate
        # dicts as needed. setdefault returns the existing dict if already
        # created, or creates a new empty one — no need for an if/else check.
        for part in parts[:-1]:
            target = target.setdefault(part, {})

        # WHY: Set the leaf value at the final key segment.
        target[parts[-1]] = value

    return result


def flatten_from_file(path: Path, separator: str = ".") -> dict[str, object]:
    """Read a JSON file and return the flattened version."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    raw = path.read_text(encoding="utf-8")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc

    # WHY: Guard against non-dict roots. A JSON array [1,2,3] would break
    # flatten() because it iterates .items() which only dicts have.
    if not isinstance(data, dict):
        raise TypeError(f"Expected a JSON object (dict), got {type(data).__name__}")

    return flatten(data, separator=separator)


def depth(data: dict) -> int:
    """Calculate the maximum nesting depth of a dictionary."""
    # WHY: Base case for recursion — an empty or non-dict value has depth 0.
    if not isinstance(data, dict) or not data:
        return 0
    # WHY: 1 (this level) + the deepest child. max() with a generator
    # expression avoids creating an intermediate list.
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
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Recursion for flattening | Nested data has arbitrary depth. Recursion naturally mirrors the structure — each level handles its own children and delegates deeper nesting to recursive calls. |
| `separator` as a parameter | Different systems use different separators (`.` for JSON paths, `/` for filesystem paths, `__` for environment variables). Making it configurable costs nothing and adds flexibility. |
| `setdefault` in unflatten | `setdefault` atomically checks "does this key exist?" and creates it if not, all in one call. This avoids the common `if key not in dict: dict[key] = {}` pattern. |
| Type guard in `flatten_from_file` | A JSON file whose root is an array `[1,2,3]` would cause `flatten()` to crash with a confusing `AttributeError`. Checking early produces a clear error message. |
| Lists indexed as `"key.0"`, `"key.1"` | This preserves list ordering in the flat representation. Without it, list data would be lost during flattening. |

## Alternative Approaches

### Using a stack instead of recursion

```python
def flatten_iterative(data: dict, separator: str = ".") -> dict:
    """Flatten using an explicit stack instead of recursion."""
    result = {}
    stack = [("", data)]  # (prefix, value) pairs
    while stack:
        prefix, current = stack.pop()
        for key, value in current.items():
            new_key = f"{prefix}{separator}{key}" if prefix else key
            if isinstance(value, dict):
                stack.append((new_key, value))
            else:
                result[new_key] = value
    return result
```

This avoids Python's recursion depth limit (default 1000). For extremely deep JSON structures this is safer, but the recursive version is far more readable for a learning context.

### Using `json_normalize` from pandas

For production data work, `pandas.json_normalize()` flattens nested JSON into a DataFrame in one call. The manual approach here teaches the underlying algorithm that library functions hide.

## Common Pitfalls

1. **Keys containing the separator character** — If an original key is `"a.b"` and the separator is `"."`, the flattened key `"a.b"` becomes ambiguous (is it a nested path or a literal key?). The unflatten step will incorrectly split it into `{"a": {"b": value}}`. Real systems escape the separator or use a character that never appears in keys.

2. **Assuming roundtrip fidelity** — Flatten then unflatten does not always produce the original structure. Lists become dicts with numeric string keys (`{"0": "a", "1": "b"}` instead of `["a", "b"]`). If you need perfect roundtrips, you must store type metadata alongside the flat keys.

3. **Infinite recursion from circular references** — If a dict contains a reference to itself (rare in JSON, possible in Python), `flatten()` will recurse forever and hit the stack limit. JSON files cannot have circular references, but programmatic dicts can.
