# Error Safe Divider — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Error Safe Divider — complete annotated solution."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def safe_divide(numerator: object, denominator: object) -> dict:
    """Perform division with full error handling.

    Instead of crashing, always returns a structured result dict.
    """
    try:
        # WHY: Convert to float first — this catches strings like "abc",
        # None values, and other non-numeric types before we attempt division.
        # If conversion fails, we get ValueError or TypeError.
        num = float(numerator)
        den = float(denominator)

        # WHY: Division happens inside the try block so ZeroDivisionError
        # is caught alongside conversion errors, keeping all error handling
        # in one place.
        result = num / den

        return {
            "success": True,
            "result": result,
            "error": None,
            "error_type": None,
        }

    except ZeroDivisionError:
        # WHY: Catching this specifically lets us give a domain-appropriate
        # message. "Cannot divide by zero" is clearer than the raw Python
        # error "float division by zero".
        return {
            "success": False,
            "result": None,
            "error": "Cannot divide by zero",
            "error_type": "ZeroDivisionError",
        }

    except (ValueError, TypeError) as exc:
        # WHY: Catching both ValueError and TypeError in one clause because
        # the recovery is identical for both. ValueError covers "abc" -> float(),
        # TypeError covers None -> float() or list -> float().
        # Using `type(exc).__name__` gives us the specific error class name.
        return {
            "success": False,
            "result": None,
            "error": f"Invalid input: {exc}",
            "error_type": type(exc).__name__,
        }


def batch_divide(operations: list[tuple[object, object]]) -> list[dict]:
    """Run many division operations and collect all results."""
    results = []
    for idx, (num, den) in enumerate(operations):
        result = safe_divide(num, den)
        # WHY: Tracking index and original input makes debugging easier.
        # When operation 47 fails, the caller knows exactly which input caused it.
        result["index"] = idx
        result["input"] = {"numerator": str(num), "denominator": str(den)}
        results.append(result)
    return results


def summarise_results(results: list[dict]) -> dict:
    """Summarise a batch of division results with error counts."""
    successes = [r for r in results if r["success"]]
    failures = [r for r in results if not r["success"]]

    # WHY: dict.get with a default of 0 lets us count occurrences without
    # needing to check "is this key already in the dict?" first.
    error_counts: dict[str, int] = {}
    for r in failures:
        err_type = r["error_type"]
        error_counts[err_type] = error_counts.get(err_type, 0) + 1

    # WHY: Sorting by result value helps spot patterns — are all small
    # results from one source? Are there clusters?
    sorted_successes = sorted(successes, key=lambda r: r["result"])

    return {
        "total": len(results),
        "successes": len(successes),
        "failures": len(failures),
        "error_counts": error_counts,
        # WHY: Guard against empty results to prevent ZeroDivisionError
        # in our own summary function — ironic if a division error tool crashed
        # on division by zero.
        "success_rate": round(len(successes) / len(results) * 100, 1) if results else 0,
        "sorted_results": [r["result"] for r in sorted_successes],
    }


def parse_operations_file(path: Path) -> list[tuple[str, str]]:
    """Parse a file of division operations (one per line, comma-separated)."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    operations: list[tuple[str, str]] = []
    lines = path.read_text(encoding="utf-8").splitlines()

    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        parts = stripped.split(",")
        if len(parts) != 2:
            # WHY: Instead of crashing on malformed lines, store them so
            # safe_divide reports the parse error gracefully.
            operations.append((stripped, "PARSE_ERROR"))
            continue

        operations.append((parts[0].strip(), parts[1].strip()))

    return operations


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Error-safe division calculator"
    )
    parser.add_argument(
        "--input",
        default="data/sample_input.txt",
        help="File with 'numerator,denominator' lines",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Enter interactive mode for single divisions",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point: run batch divisions or interactive mode."""
    args = parse_args()

    if args.interactive:
        print("Error Safe Divider — interactive mode (Ctrl+C to quit)")
        try:
            while True:
                num = input("  numerator: ")
                den = input("  denominator: ")
                result = safe_divide(num, den)
                print(f"  -> {json.dumps(result)}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
        return

    operations = parse_operations_file(Path(args.input))
    results = batch_divide(operations)
    summary = summarise_results(results)

    print("=== Division Results ===")
    for r in results:
        status = "OK" if r["success"] else "FAIL"
        val = r["result"] if r["success"] else r["error"]
        print(f"  [{status}] {r['input']['numerator']} / {r['input']['denominator']} = {val}")

    print(f"\n=== Summary ===")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Return result dicts instead of raising exceptions | The whole point of this project is graceful failure. Raising exceptions would push error handling onto every caller. Returning structured results means callers never need try/except. |
| Convert to `float` before dividing | This catches type errors early with a clear message. Without it, dividing `"abc" / 5` would produce a confusing `TypeError: unsupported operand type(s)`. |
| Catch `(ValueError, TypeError)` together | Both indicate "bad input that cannot be a number." The recovery is the same for both, so grouping them avoids code duplication. |
| Store malformed file lines as `(line, "PARSE_ERROR")` | This lets `safe_divide` handle the error uniformly rather than requiring the file parser to have its own error reporting path. |
| `type(exc).__name__` for error classification | Gives the exact exception class name (e.g. "ValueError") as a string, which is useful for error counting and logging without importing exception types. |

## Alternative Approaches

### Using `isinstance` checks instead of try/except

```python
def safe_divide_with_checks(numerator, denominator):
    if not isinstance(numerator, (int, float)):
        try:
            numerator = float(numerator)
        except (ValueError, TypeError) as exc:
            return {"success": False, "error": f"Invalid numerator: {exc}"}
    if denominator == 0:
        return {"success": False, "error": "Cannot divide by zero"}
    return {"success": True, "result": numerator / denominator}
```

This "look before you leap" style checks conditions explicitly. The try/except ("ask forgiveness, not permission") style is more Pythonic and handles edge cases that explicit checks might miss (like `float('nan')`).

### Using `decimal.Decimal` for precise division

For financial calculations, `float` arithmetic introduces rounding errors (`0.1 + 0.2 != 0.3`). Python's `decimal.Decimal` type provides exact decimal arithmetic. This project uses `float` because it is simpler and sufficient for learning error handling patterns.

## Common Pitfalls

1. **Bare `except:` catches everything** — Writing `except:` without specifying a type catches `KeyboardInterrupt` and `SystemExit`, which prevents the user from pressing Ctrl+C to stop the program. Always catch specific exception types.

2. **Forgetting `float('inf')` and `float('nan')`** — Dividing very large floats can produce infinity, and `0.0 / 0.0` does not raise `ZeroDivisionError` for floats (it returns `nan`). Production code should check `math.isinf()` and `math.isnan()` on results.

3. **Division by zero only applies to integers** — `1 / 0` raises `ZeroDivisionError`, but `1.0 / 0.0` also raises it in Python. However, `float('inf') / float('inf')` silently returns `nan`. Edge cases in floating-point arithmetic are subtle.
