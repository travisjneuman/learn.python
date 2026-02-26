# Solution: Level 0 / Project 05 - Number Classifier

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
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
    # WHY == 0: We compare the remainder to 0.  If there is no remainder,
    # the number is perfectly divisible by 2.
    return n % 2 == 0


def is_prime(n: int) -> bool:
    """Return True if the number is prime.

    A prime number is greater than 1 and only divisible by 1 and itself.

    WHY check up to n**0.5? -- If n has a factor larger than its square
    root, the matching factor must be smaller than the square root.
    So we only need to check up to that point.  For n=100, we check
    up to 10 instead of 99 — much faster.
    """
    # WHY n < 2 returns False: 0 and 1 are not prime by mathematical
    # definition.  Negative numbers are also not prime.
    if n < 2:
        return False
    # WHY special-case 2: 2 is the only even prime.  Handling it here
    # lets us skip all even numbers in the loop below.
    if n == 2:
        return True
    # WHY check n % 2: If n is even and not 2, it is divisible by 2,
    # so it cannot be prime.  This eliminates half of all numbers
    # before the loop even starts.
    if n % 2 == 0:
        return False

    # WHY start at 3 and step by 2: We already handled even numbers,
    # so we only need to check odd divisors (3, 5, 7, 9, ...).
    i = 3
    # WHY i * i <= n instead of i <= sqrt(n): Multiplying is faster
    # than computing a square root, and avoids importing math.
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def classify_sign(n: int) -> str:
    """Classify a number as positive, negative, or zero."""
    # WHY if/elif/else: This is a decision tree.  Exactly one branch
    # executes for any input.  The three cases are mutually exclusive
    # and exhaustive — every integer is positive, negative, or zero.
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    else:
        return "zero"


def classify_number(n: int) -> dict:
    """Build a full classification dict for one number.

    WHY return a dict? -- Combines sign, parity, and primality into
    a single structure.  The caller gets all info in one place instead
    of calling three separate functions.
    """
    return {
        "number": n,
        "sign": classify_sign(n),
        # WHY inline conditional: "even" if is_even(n) else "odd" is a
        # concise way to pick between two string values based on a boolean.
        "parity": "even" if is_even(n) else "odd",
        "prime": is_prime(n),
    }


if __name__ == "__main__":
    print("=== Number Classifier ===")
    print("Enter numbers one at a time. Type 'quit' to see a summary.\n")

    results = []

    while True:
        text = input("Enter a number (or 'quit'): ")

        if text.strip().lower() in ("quit", "exit", "q"):
            break

        # WHY try/except: The user might type "abc" instead of a number.
        # int() raises ValueError for non-integer strings.
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

    # WHY a summary section: After classifying many numbers, a summary
    # gives a quick overview.  This uses generator expressions with sum()
    # to count items matching a condition — a very Pythonic pattern.
    if results:
        primes = sum(1 for r in results if r["prime"])
        print(f"\n=== Summary ===")
        print(f"  Numbers classified: {len(results)}")
        print(f"  Primes found: {primes}")
        print(f"  Even numbers: {sum(1 for r in results if r['parity'] == 'even')}")
        print(f"  Odd numbers: {sum(1 for r in results if r['parity'] == 'odd')}")
    else:
        print("\nNo numbers entered.")
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `is_even()` and `is_prime()` return `bool` | Boolean returns integrate naturally with `if` statements and conditional expressions. `if is_prime(n)` reads like English | Return strings like `"even"` or `"prime"` — harder to combine with other logic |
| `is_prime()` checks up to square root only | Reduces iterations dramatically: checking 97 requires 4 iterations instead of 95. For large numbers, this is the difference between instant and slow | Check every number from 2 to n-1 — works but is very slow for large numbers |
| `classify_number()` bundles all checks in one dict | The caller gets a complete picture with one function call. Useful for both display and storage | Return three separate values — forces the caller to call three functions and manage three variables |
| `classify_sign()` is its own function | Isolates the sign logic so it can be tested independently (`assert classify_sign(-5) == "negative"`) | Inline the if/elif/else inside `classify_number()` — works but mixes concerns |

## Alternative approaches

### Approach B: Using `all()` for primality check

```python
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    # Check if n is NOT divisible by any number from 2 to sqrt(n).
    # all() returns True only if every element in the iterable is True.
    return all(n % i != 0 for i in range(2, int(n ** 0.5) + 1))
```

**Trade-off:** The `all()` approach is more concise and Pythonic — it expresses the prime definition in a single line. However, it checks even divisors too (2, 4, 6...) which is redundant after checking 2, and it imports the concept of generator expressions, which may be unfamiliar at Level 0. The manual while loop in the primary solution makes every step visible and teaches the loop-with-early-return pattern.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| User enters `0` | `classify_number(0)` returns `sign: "zero", parity: "even", prime: False`. But 0 is technically neither prime nor composite | Add a special label: `"neither"` for 0 and 1 instead of `"composite"` |
| User enters `1` | `is_prime(1)` correctly returns `False` because 1 is not prime by definition. But labeling it "composite" is mathematically inaccurate | Same fix — treat 1 as "neither prime nor composite" |
| User enters a negative number like `-7` | `is_prime(-7)` returns `False` (correct — primes are positive by definition). `is_even(-7)` returns `False` (correct — `-7 % 2` is `-1`, not 0 in Python... actually `-7 % 2` is `1` in Python) | Already handled correctly. Python's modulo always returns a non-negative result when the divisor is positive |
| User enters a very large number like `999999999989` | `is_prime()` checks up to ~999999 — might be slow but will finish. No crash | For Level 0 this is acceptable. Production code would use probabilistic tests like Miller-Rabin |
| User enters a float like `3.5` | `int("3.5")` raises `ValueError` — the program says "not a valid integer" | Already handled by the try/except. Could also accept floats and truncate, but that changes semantics |

## Key takeaways

1. **The modulo operator `%` is the key to divisibility checks.** `n % 2 == 0` (is even), `n % i == 0` (is divisible by i), and `n % 10` (last digit) are all common patterns. You will use modulo in data validation, pagination, and cyclic indexing throughout your career.
2. **Decision trees with if/elif/else partition inputs into categories.** Every integer is exactly one of positive/negative/zero. Every integer is exactly one of even/odd. These "mutually exclusive, collectively exhaustive" branches are the building blocks of all classification logic.
3. **Checking up to the square root is a fundamental optimisation.** It applies to prime checking, factor finding, and many search algorithms. Understanding WHY it works (if a factor > sqrt(n) exists, then a matching factor < sqrt(n) must also exist) builds mathematical intuition for algorithm design.
4. **Boolean-returning functions compose naturally.** `if is_prime(n)` and `"even" if is_even(n) else "odd"` read like English. Writing small functions that return `True`/`False` makes your code more expressive and testable.
