"""
calculator.py — Basic arithmetic operations.

This module provides simple math functions. It exists to demonstrate
how a Python package is structured, not to replace the built-in operators.

Each function is deliberately simple so you can focus on the packaging
concepts rather than complex logic.
"""


def add(a, b):
    """Add two numbers and return the result."""
    return a + b


def subtract(a, b):
    """Subtract b from a and return the result."""
    return a - b


def multiply(a, b):
    """Multiply two numbers and return the result."""
    return a * b


def divide(a, b):
    """
    Divide a by b and return the result.

    Raises ZeroDivisionError if b is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


# ── Entry point for running as a module ──────────────────────────────
#
# This lets you run: python -m mymath.calculator
# The "if __name__" guard means this code only runs when the file
# is executed directly, not when it's imported.

def main():
    """Demo the calculator functions."""
    print("mymath calculator v0.1.0")
    print(f"add(2, 3) = {add(2, 3)}")
    print(f"subtract(10, 4) = {subtract(10, 4)}")
    print(f"multiply(3, 7) = {multiply(3, 7)}")
    print(f"divide(15, 4) = {divide(15, 4)}")


if __name__ == "__main__":
    main()
