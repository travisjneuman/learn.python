# Errors and Debugging Cheat Sheet

> Errors are not failures. They are Python telling you exactly what went wrong and where.

## Reading an Error Message

```
Traceback (most recent call last):
  File "app.py", line 5, in <module>
    print(score)
NameError: name 'score' is not defined
```

Read it **bottom to top**:

1. Last line: **what** went wrong -- `NameError: name 'score' is not defined`
2. Line above: **where** it happened -- `File "app.py", line 5`
3. Code snippet: **which line** -- `print(score)`

## Common Error Types

| Error | Means | Typical Cause |
|-------|-------|---------------|
| `SyntaxError` | Code grammar is wrong | Missing `:`, unmatched `(`, bad indent |
| `NameError` | Name does not exist | Typo, used before defining |
| `TypeError` | Wrong type for operation | `"hi" + 5`, wrong number of args |
| `ValueError` | Right type, wrong value | `int("hello")` |
| `IndexError` | List index out of range | `my_list[99]` on a short list |
| `KeyError` | Dict key missing | `d["nope"]` -- use `d.get("nope")` |
| `FileNotFoundError` | File does not exist | Wrong path or filename |
| `IndentationError` | Bad indentation | Mixed tabs/spaces, missing indent |
| `AttributeError` | Method does not exist on type | Calling `.upper()` on `None` |

## Try / Except

```python
# Catch a specific error
try:
    number = int(input("Enter a number: "))
except ValueError:
    print("That is not a valid number.")

# Catch multiple errors
try:
    result = data[key]
except (KeyError, IndexError):
    result = None

# Catch and inspect
try:
    risky_operation()
except Exception as e:
    print(f"Error: {e}")
```

## Debugging Strategy

1. **Read the error message** -- it usually tells you exactly what happened
2. **Go to the line number** -- open the file, find the line
3. **Check spelling** -- typos cause `NameError`
4. **Print things** -- add `print(variable)` before the broken line
5. **Simplify** -- remove code until you find the smallest version that breaks

## The print() Debugging Method

```python
data = load_file("input.txt")
print("data:", data)           # What did we load?
print("type:", type(data))     # Is it what we expect?
print("len:", len(data))       # How many items?
```

## Common Mistakes

| Mistake | What happens | Fix |
|---------|-------------|-----|
| Bare `except:` | Catches everything, hides bugs | Catch specific errors: `except ValueError:` |
| Ignoring the message | Random guessing | Read the last line of the traceback first |
| Missing colon | `SyntaxError` | `if x > 5:` not `if x > 5` |
| Mixing `str` + `int` | `TypeError` | Use `f"Age: {age}"` or `str(age)` |
| Wrong indent | `IndentationError` | Use 4 spaces consistently |

## Quick Reference

| Operation | Syntax |
|-----------|--------|
| Handle an error | `try: ... except ErrorType: ...` |
| Get error details | `except ValueError as e:` |
| Raise your own error | `raise ValueError("bad input")` |
| Always run cleanup | `try: ... finally: ...` |
| Check type | `type(x)` |
| Check value | `print(repr(x))` -- shows quotes, escapes |

---

[Back to Cheat Sheets](README.md) | [Full Concept Doc](../errors-and-debugging.md)
