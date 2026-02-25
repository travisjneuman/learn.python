"""Level 2 project: Error Safe Divider.

Heavily commented beginner-friendly script:
- perform division with comprehensive error handling,
- catch ZeroDivisionError, TypeError, ValueError,
- process batch division operations from a file.

Skills practiced: try/except with multiple exception types,
nested data structures, enumerate, dict comprehensions, sorting with key.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def safe_divide(numerator: object, denominator: object) -> dict:
    """Perform division with full error handling.

    Instead of crashing, this function always returns a result dict
    describing either the successful result or the error that occurred.

    Args:
        numerator: The value to divide (should be a number).
        denominator: The value to divide by (should be a non-zero number).

    Returns:
        A dict with keys: success, result, error, error_type.
    """
    try:
        # Try converting to float first — this catches strings and None.
        num = float(numerator)
        den = float(denominator)

        # Perform the division — may raise ZeroDivisionError.
        result = num / den

        return {
            "success": True,
            "result": result,
            "error": None,
            "error_type": None,
        }

    except ZeroDivisionError:
        # Division by zero is a math error, not a code error.
        return {
            "success": False,
            "result": None,
            "error": "Cannot divide by zero",
            "error_type": "ZeroDivisionError",
        }

    except (ValueError, TypeError) as exc:
        # ValueError: string that cannot be converted to float, e.g. "abc".
        # TypeError: something that float() cannot handle, e.g. a list.
        return {
            "success": False,
            "result": None,
            "error": f"Invalid input: {exc}",
            "error_type": type(exc).__name__,
        }


def batch_divide(operations: list[tuple[object, object]]) -> list[dict]:
    """Run many division operations and collect all results.

    Each operation is a (numerator, denominator) tuple.
    Results include the original index for traceability.
    """
    results = []
    for idx, (num, den) in enumerate(operations):
        result = safe_divide(num, den)
        result["index"] = idx
        result["input"] = {"numerator": str(num), "denominator": str(den)}
        results.append(result)
    return results


def summarise_results(results: list[dict]) -> dict:
    """Summarise a batch of division results.

    Groups results by success/failure and counts error types.
    Uses dict comprehension and sorting with key functions.
    """
    successes = [r for r in results if r["success"]]
    failures = [r for r in results if not r["success"]]

    # Dict comprehension to count each error type.
    error_counts: dict[str, int] = {}
    for r in failures:
        err_type = r["error_type"]
        error_counts[err_type] = error_counts.get(err_type, 0) + 1

    # Sort successes by result value (smallest first).
    sorted_successes = sorted(successes, key=lambda r: r["result"])

    return {
        "total": len(results),
        "successes": len(successes),
        "failures": len(failures),
        "error_counts": error_counts,
        "success_rate": round(len(successes) / len(results) * 100, 1) if results else 0,
        "sorted_results": [r["result"] for r in sorted_successes],
    }


def parse_operations_file(path: Path) -> list[tuple[str, str]]:
    """Parse a file of division operations.

    Expected format: one operation per line, 'numerator,denominator'.
    Lines starting with '#' are comments.  Blank lines are skipped.
    """
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    operations: list[tuple[str, str]] = []
    lines = path.read_text(encoding="utf-8").splitlines()

    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()

        # Skip blanks and comments.
        if not stripped or stripped.startswith("#"):
            continue

        parts = stripped.split(",")
        if len(parts) != 2:
            # Store bad lines as-is so safe_divide reports the error.
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

    # Batch mode: read operations from file.
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
