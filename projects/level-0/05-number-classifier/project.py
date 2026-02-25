"""Level 0 project: Number Classifier.

Read numbers from a file and classify each one:
  - positive / negative / zero
  - even / odd
  - prime / composite

Concepts: if/elif/else decision trees, modulo operator, loops, functions.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def is_even(n: int) -> bool:
    """Return True if the number is even.

    WHY modulo? -- The % operator gives the remainder after division.
    If n % 2 is 0 the number divides evenly by 2, so it is even.
    """
    return n % 2 == 0


def is_prime(n: int) -> bool:
    """Return True if the number is prime.

    A prime number is greater than 1 and only divisible by 1 and itself.

    WHY check up to n**0.5? -- If n has a factor larger than its square
    root, the matching factor must be smaller than the square root.
    So we only need to check up to that point.
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Check odd numbers from 3 up to the square root of n.
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def classify_sign(n: int) -> str:
    """Classify a number as positive, negative, or zero."""
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    else:
        return "zero"


def classify_number(n: int) -> dict:
    """Build a full classification dict for one number.

    Combines sign, parity (even/odd), and primality checks into
    a single dictionary so all info is in one place.
    """
    return {
        "number": n,
        "sign": classify_sign(n),
        "parity": "even" if is_even(n) else "odd",
        "prime": is_prime(n),
    }


def process_file(path: Path) -> list[dict]:
    """Read numbers from a file (one per line) and classify each."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    results = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        try:
            n = int(stripped)
        except ValueError:
            results.append({"input": stripped, "error": "Not an integer"})
            continue

        results.append(classify_number(n))

    return results


def summarise(results: list[dict]) -> dict:
    """Build a summary of all classifications.

    Counts how many numbers fell into each category so the learner
    can see the distribution at a glance.
    """
    valid = [r for r in results if "error" not in r]
    return {
        "total": len(results),
        "valid": len(valid),
        "errors": len(results) - len(valid),
        "positives": sum(1 for r in valid if r["sign"] == "positive"),
        "negatives": sum(1 for r in valid if r["sign"] == "negative"),
        "zeros": sum(1 for r in valid if r["sign"] == "zero"),
        "evens": sum(1 for r in valid if r["parity"] == "even"),
        "odds": sum(1 for r in valid if r["parity"] == "odd"),
        "primes": sum(1 for r in valid if r["prime"]),
    }


def parse_args() -> argparse.Namespace:
    """Define command-line options."""
    parser = argparse.ArgumentParser(description="Number Classifier")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    """Program entry point."""
    args = parse_args()
    results = process_file(Path(args.input))
    summary = summarise(results)

    # Print each classification.
    for r in results:
        if "error" in r:
            print(f"  {r['input']}  =>  ERROR: {r['error']}")
        else:
            prime_label = "prime" if r["prime"] else "composite"
            print(f"  {r['number']:>6}  =>  {r['sign']}, {r['parity']}, {prime_label}")

    print(f"\n  Summary: {summary['primes']} primes out of {summary['valid']} valid numbers")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps({"results": results, "summary": summary}, indent=2),
        encoding="utf-8",
    )
    print(f"  Output written to {output_path}")


if __name__ == "__main__":
    main()
