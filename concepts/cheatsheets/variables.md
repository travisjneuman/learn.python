# Variables Cheat Sheet

> A variable is a name that holds a value. Think of it as a labeled jar.

## Key Syntax

```python
# Create a variable (assignment)
name = "Alice"
age = 30
is_student = True

# Use a variable
print(name)           # Alice
next_year = age + 1   # 31

# Embed in strings (f-strings)
print(f"Hello, {name}! Age: {age}")
```

## Common Patterns

```python
# Swap two values
a, b = b, a

# Accumulate a total
total = 0
total = total + 10   # or: total += 10

# Collect user input
answer = input("Your name? ")

# Multiple assignment
x, y, z = 1, 2, 3
```

## Naming Rules

| Rule | Example |
|------|---------|
| Start with letter or `_` | `score`, `_temp` |
| Use `snake_case` | `student_count` |
| Case-sensitive | `Name` and `name` are different |
| No spaces or dashes | `my_var` not `my-var` or `my var` |
| Avoid Python keywords | Do not name a variable `print`, `list`, `type` |

## Common Mistakes

| Mistake | Wrong | Right |
|---------|-------|-------|
| `=` vs `==` | `if x = 5:` | `if x == 5:` |
| Missing quotes | `name = Alice` | `name = "Alice"` |
| Use before create | `print(x)` then `x = 5` | `x = 5` then `print(x)` |
| Missing `f` prefix | `"{name} is here"` | `f"{name} is here"` |
| Overwriting builtins | `list = [1, 2]` | `my_list = [1, 2]` |

## Quick Reference

| Operation | Syntax | Result |
|-----------|--------|--------|
| Create | `x = 10` | Stores 10 |
| Update | `x = x + 1` | Now 11 |
| Shorthand update | `x += 1` | Same as above |
| Check type | `type(x)` | `<class 'int'>` |
| Print value | `print(x)` | Displays 11 |
| F-string | `f"x is {x}"` | `"x is 11"` |

---

[Back to Cheat Sheets](README.md) | [Full Concept Doc](../what-is-a-variable.md)
