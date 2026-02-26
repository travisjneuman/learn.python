# Solution: Level 0 / Project 02 - Calculator Basics

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 0 project: Calculator Basics.

A four-operation calculator that takes input from the user
and computes results interactively.

Concepts: arithmetic operators, float/int conversion, input validation, functions.
"""


# WHY separate functions for each operation: Each function does exactly one
# thing, making it trivial to test.  assert add(2, 3) == 5 is crystal clear.
def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of two numbers."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return the quotient of two numbers.

    WHY check for zero? -- Dividing by zero crashes the program with
    ZeroDivisionError.  Checking first lets us raise ValueError with
    a clear message that explains what went wrong.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def calculate(expression: str) -> dict:
    """Parse a simple expression like '10 + 5' and return the result.

    WHY split on spaces? -- We expect the format 'number operator number'.
    Splitting on whitespace gives us exactly three pieces to work with.
    """
    parts = expression.strip().split()

    # WHY check length: If the user typed "5" or "1 + 2 + 3", we cannot
    # parse it as a simple binary expression.  Return an error dict
    # instead of crashing.
    if len(parts) != 3:
        return {"expression": expression.strip(), "error": "Expected format: number operator number"}

    raw_a, operator, raw_b = parts

    # WHY try/except: float() raises ValueError if the string is not a
    # number.  Catching it lets us return a helpful error instead of
    # a scary traceback.
    try:
        a = float(raw_a)
        b = float(raw_b)
    except ValueError:
        return {"expression": expression.strip(), "error": f"Invalid numbers: {raw_a}, {raw_b}"}

    # WHY a dict mapping operators to functions: This replaces a long
    # if/elif/else chain.  Adding a new operator means adding one line
    # to the dict instead of another elif branch.
    operations = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
    }

    if operator not in operations:
        return {"expression": expression.strip(), "error": f"Unknown operator: {operator}"}

    # WHY another try/except: divide() can raise ValueError for zero
    # division.  We catch it here so calculate() always returns a dict,
    # never crashes.
    try:
        result = operations[operator](a, b)
    except ValueError as err:
        return {"expression": expression.strip(), "error": str(err)}

    return {"expression": expression.strip(), "result": result}


if __name__ == "__main__":
    print("=== Calculator ===")
    print("Type an expression like '10 + 5' or 'quit' to exit.\n")
    print("Supported operators: +  -  *  /\n")

    # WHY while True with break: This is the standard "loop until quit"
    # pattern.  The loop runs forever; only the break statement exits it.
    while True:
        expression = input("Enter expression: ")

        if expression.strip().lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        result = calculate(expression)

        if "error" in result:
            print(f"  ERROR: {result['error']}")
        else:
            print(f"  {result['expression']} = {result['result']}")

        print()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Separate `add`, `subtract`, `multiply`, `divide` functions | Each is independently testable with a single `assert`. Tests read naturally: `assert add(2, 3) == 5` | One big `calculate()` that does everything — harder to test individual operations |
| `operations` dict maps operator strings to functions | Adding a new operator (like `%` or `**`) requires one new dict entry instead of another `elif` branch | `if/elif/else` chain — works but gets long as operators grow; does not demonstrate dict-as-dispatch |
| `calculate()` returns a dict with either `"result"` or `"error"` | The caller checks one key to know if it worked. No exceptions leak out of `calculate()` | Raise exceptions for errors — forces the caller to use try/except, which is more complex at Level 0 |
| `divide()` raises `ValueError` instead of returning a special value | Exceptions are Python's standard way to signal errors. The caller in `calculate()` catches it and converts to an error dict | Return `None` or `float('inf')` — hides the error, and the caller may not notice |

## Alternative approaches

### Approach B: if/elif chain instead of dict dispatch

```python
def calculate(expression: str) -> dict:
    parts = expression.strip().split()
    if len(parts) != 3:
        return {"expression": expression.strip(), "error": "Expected format: number operator number"}

    raw_a, operator, raw_b = parts
    a = float(raw_a)
    b = float(raw_b)

    # Direct if/elif chain — no dict needed.
    if operator == "+":
        result = a + b
    elif operator == "-":
        result = a - b
    elif operator == "*":
        result = a * b
    elif operator == "/":
        if b == 0:
            return {"expression": expression.strip(), "error": "Cannot divide by zero"}
        result = a / b
    else:
        return {"expression": expression.strip(), "error": f"Unknown operator: {operator}"}

    return {"expression": expression.strip(), "result": result}
```

**Trade-off:** The if/elif approach is easier for an absolute beginner to read because it uses no advanced concepts like "storing functions in a dict." However, the dict dispatch approach scales better — adding modulo or exponentiation is one line instead of another branch. In real codebases, dict dispatch is the standard pattern for this kind of routing.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| User types `10 / 0` | `divide()` raises `ValueError("Cannot divide by zero")`, caught by `calculate()` — returns error dict | Already handled; the outer try/except catches it |
| User types `hello + world` | `float("hello")` raises `ValueError`, caught in the try/except — returns error dict | Already handled by the input validation block |
| User types just `5` (no operator) | `parts` has length 1, not 3 — returns "Expected format" error | Already handled by the length check |
| User types `10+5` (no spaces) | `split()` gives `["10+5"]` — length 1, returns format error | Document that spaces are required; alternatively, use regex to parse |
| User types `10 + 5 + 3` | `parts` has length 5, not 3 — returns format error | Only binary expressions are supported; extending to multi-operand requires a proper parser |

## Key takeaways

1. **Dict dispatch replaces long if/elif chains.** Mapping `"+"` to `add` and `"*"` to `multiply` is cleaner and more extensible than branching for every operator. This pattern appears in web frameworks, CLI tools, and game engines.
2. **`float()` and `int()` convert strings to numbers, but they crash on bad input.** Always wrap them in `try/except ValueError` when the data comes from a user or file. You will use this pattern in every project that reads numeric input.
3. **Returning error dicts keeps the caller simple.** Instead of raising exceptions that force try/except everywhere, `calculate()` returns `{"error": "..."}` so the caller just checks `if "error" in result`. This is a beginner-friendly version of the "Result type" pattern used in many languages.
4. **Functions that do one thing are easier to test.** `assert add(2, 3) == 5` is a one-line test. If `add` also handled parsing and printing, the test would need to set up input and capture output — much harder.
