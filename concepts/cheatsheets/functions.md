# Functions Cheat Sheet

> A function is a reusable block of code with a name. Define it once, call it whenever you need it.

## Key Syntax

```python
# Define a function
def greet(name):
    return f"Hello, {name}!"

# Call a function
message = greet("Alice")   # "Hello, Alice!"
print(greet("Bob"))        # Hello, Bob!

# Function with no return value
def say_hello():
    print("Hello!")

say_hello()   # Prints: Hello! (returns None)
```

## Common Patterns

```python
# Default parameter values
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Alice")          # "Hello, Alice!"
greet("Alice", "Hey")   # "Hey, Alice!"

# Multiple return values
def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([3, 1, 7])   # lo=1, hi=7

# Early return (guard clause)
def divide(a, b):
    if b == 0:
        return None
    return a / b

# Function that takes a list
def total(prices):
    result = 0
    for p in prices:
        result += p
    return result
```

## Parameters vs Arguments

```python
def add(a, b):    # a, b are PARAMETERS (the names)
    return a + b

add(3, 5)         # 3, 5 are ARGUMENTS (the values)
```

## Keyword Arguments

```python
def tag(text, bold=False, color="black"):
    ...

tag("hi")                          # defaults
tag("hi", bold=True)               # named argument
tag("hi", color="red", bold=True)  # any order when named
```

## Common Mistakes

| Mistake | Wrong | Right |
|---------|-------|-------|
| Forget parentheses | `greet` | `greet("Alice")` |
| Forget return | `result = a + b` (no return) | `return a + b` |
| Define after call | Call then define | Define first, call second |
| Use print instead of return | `print(a + b)` inside function | `return a + b` |
| Mutable default arg | `def f(items=[]):` | `def f(items=None):` then `items = items or []` |

## Why Functions Matter

1. **Reuse** -- write once, call everywhere
2. **Organize** -- name your logic (`calculate_tax` vs 5 lines of math)
3. **Test** -- test small pieces independently
4. **Read** -- functions make code self-documenting

## Quick Reference

| Operation | Syntax |
|-----------|--------|
| Define | `def name(params):` |
| Return a value | `return value` |
| Default param | `def f(x, y=10):` |
| Call | `name(args)` |
| Multiple returns | `return a, b` |
| Unpack returns | `x, y = func()` |
| Docstring | `"""Describes the function."""` as first line |

---

[Back to Cheat Sheets](README.md) | [Full Concept Doc](../functions-explained.md)
