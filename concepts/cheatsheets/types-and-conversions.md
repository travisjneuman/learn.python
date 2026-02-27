# Types and Conversions Cheat Sheet

> Every value in Python has a type. The type determines what you can do with it.

## Basic Types

| Type | Holds | Examples |
|------|-------|---------|
| `str` | Text | `"hello"`, `'world'`, `"123"` |
| `int` | Whole number | `42`, `-3`, `0` |
| `float` | Decimal number | `3.14`, `-0.5`, `2.0` |
| `bool` | True or False | `True`, `False` |
| `None` | Nothing / empty | `None` |

## Checking Types

```python
type("hello")     # <class 'str'>
type(42)          # <class 'int'>
type(3.14)        # <class 'float'>
type(True)        # <class 'bool'>

isinstance(42, int)           # True
isinstance("hi", (str, int))  # True (either type)
```

## Converting Between Types

| Function | Converts to | Example | Result |
|----------|------------|---------|--------|
| `str()` | String | `str(42)` | `"42"` |
| `int()` | Integer | `int("42")` | `42` |
| `float()` | Float | `float("3.14")` | `3.14` |
| `bool()` | Boolean | `bool(0)` | `False` |
| `list()` | List | `list("abc")` | `["a", "b", "c"]` |

## Why Conversion Matters

`input()` always returns a string. You must convert before doing math:

```python
age_text = input("Age? ")   # "30" (string!)
age = int(age_text)          # 30 (integer)
print(age + 1)               # 31

# Without conversion:
print("30" + 1)              # TypeError!
```

## Truthy and Falsy

Python treats some values as `False` in conditions:

| Falsy (acts as False) | Truthy (acts as True) |
|---|---|
| `False` | `True` |
| `0`, `0.0` | Any non-zero number |
| `""` (empty string) | Any non-empty string |
| `[]`, `{}`, `set()` | Any non-empty collection |
| `None` | Everything else |

```python
name = ""
if name:              # False -- empty string is falsy
    print("has name")
else:
    print("no name")  # This runs
```

## Common Patterns

```python
# Safe string-to-number conversion
text = input("Number? ")
if text.isdigit():
    number = int(text)

# Convert with a fallback
try:
    value = int(user_input)
except ValueError:
    value = 0

# Boolean from comparison
is_adult = age >= 18          # True or False
has_items = len(cart) > 0     # True or False
```

## Common Mistakes

| Mistake | Wrong | Right |
|---------|-------|-------|
| Compare str to int | `"5" == 5` is `False` | `int("5") == 5` |
| int() on decimal string | `int("3.14")` crashes | `int(float("3.14"))` |
| int() on non-number | `int("hello")` crashes | Use `try/except` or `.isdigit()` |
| Forget input is a string | `age = input()` then `age + 1` | `age = int(input())` |

## Quick Reference

| Operation | Syntax | Result |
|-----------|--------|--------|
| Check type | `type(x)` | `<class 'int'>` |
| Is it this type? | `isinstance(x, int)` | `True` / `False` |
| To string | `str(42)` | `"42"` |
| To integer | `int("42")` | `42` |
| To float | `float("3.14")` | `3.14` |
| To boolean | `bool("")` | `False` |
| Is it digit? | `"42".isdigit()` | `True` |

---

[Back to Cheat Sheets](README.md) | [Full Concept Doc](../types-and-conversions.md)
