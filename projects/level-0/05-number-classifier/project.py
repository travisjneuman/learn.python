"""Level 0 project: Number Classifier.

Enter numbers and classify each one:
  - positive / negative / zero
  - even / odd
  - prime / composite

Concepts: if/elif/else decision trees, modulo operator, loops, functions.
"""


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


# This guard means the code below only runs when you execute the file
# directly (python project.py), NOT when another file imports it.
if __name__ == "__main__":
    print("=== Number Classifier ===")
    print("Enter numbers one at a time. Type 'quit' to see a summary.\n")

    results = []

    while True:
        text = input("Enter a number (or 'quit'): ")

        if text.strip().lower() in ("quit", "exit", "q"):
            break

        try:
            n = int(text)
        except ValueError:
            print(f"  '{text}' is not a valid integer. Try again.\n")
            continue

        info = classify_number(n)
        prime_label = "prime" if info["prime"] else "composite"
        print(f"  {n} is {info['sign']}, {info['parity']}, {prime_label}")
        results.append(info)
        print()

    # Show summary.
    if results:
        primes = sum(1 for r in results if r["prime"])
        print(f"\n=== Summary ===")
        print(f"  Numbers classified: {len(results)}")
        print(f"  Primes found: {primes}")
        print(f"  Even numbers: {sum(1 for r in results if r['parity'] == 'even')}")
        print(f"  Odd numbers: {sum(1 for r in results if r['parity'] == 'odd')}")
    else:
        print("\nNo numbers entered.")
