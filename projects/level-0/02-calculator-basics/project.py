"""Level 0 project: Calculator Basics.

A four-operation calculator that takes input from the user
and computes results interactively.

Concepts: arithmetic operators, float/int conversion, input validation, functions.
"""


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

    WHY check for zero? -- Dividing by zero crashes the program.
    Checking first lets us return a clear error message instead.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def calculate(expression: str) -> dict:
    """Parse a simple expression like '10 + 5' and return the result.

    WHY split on spaces? -- We expect the format 'number operator number'.
    Splitting on whitespace gives us exactly three pieces to work with.

    Returns a dict with the original expression and computed result,
    or an error message if parsing fails.
    """
    parts = expression.strip().split()

    if len(parts) != 3:
        return {"expression": expression.strip(), "error": "Expected format: number operator number"}

    raw_a, operator, raw_b = parts

    # Try converting strings to numbers. If the user typed 'abc' this fails.
    try:
        a = float(raw_a)
        b = float(raw_b)
    except ValueError:
        return {"expression": expression.strip(), "error": f"Invalid numbers: {raw_a}, {raw_b}"}

    # Map the operator string to the right function.
    operations = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
    }

    if operator not in operations:
        return {"expression": expression.strip(), "error": f"Unknown operator: {operator}"}

    try:
        result = operations[operator](a, b)
    except ValueError as err:
        return {"expression": expression.strip(), "error": str(err)}

    return {"expression": expression.strip(), "result": result}


# This guard means the code below only runs when you execute the file
# directly (python project.py), NOT when another file imports it.
if __name__ == "__main__":
    print("=== Calculator ===")
    print("Type an expression like '10 + 5' or 'quit' to exit.\n")
    print("Supported operators: +  -  *  /\n")

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
