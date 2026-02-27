# Strings Cheat Sheet

> A string is text -- any sequence of characters between quotes.

## Key Syntax

```python
# Create strings (single or double quotes both work)
name = "Alice"
name = 'Alice'

# Multi-line string
message = """This is
a multi-line
string."""

# F-strings (embed variables)
greeting = f"Hello, {name}!"

# String length
len("hello")    # 5
```

## Essential Methods

```python
text = "  Hello, World!  "

text.strip()         # "Hello, World!" -- remove surrounding whitespace
text.lower()         # "  hello, world!  "
text.upper()         # "  HELLO, WORLD!  "
text.replace("World", "Python")   # "  Hello, Python!  "
text.split(",")      # ["  Hello", " World!  "]
text.startswith("  H")  # True
text.endswith("!  ")    # True
text.count("l")      # 3
text.find("World")   # 9 (index), -1 if not found
```

## Common Patterns

```python
# Join a list into a string
words = ["hello", "world"]
sentence = " ".join(words)      # "hello world"
csv_line = ",".join(words)      # "hello,world"

# Split a string into parts
"a,b,c".split(",")             # ["a", "b", "c"]
"hello world".split()          # ["hello", "world"]

# Check contents
"hello".isdigit()              # False
"42".isdigit()                 # True
"hello".isalpha()              # True
"Hello".islower()              # False

# Slice a string
word = "Python"
word[0]          # "P"
word[-1]         # "n"
word[0:3]        # "Pyt" (index 0, 1, 2)
word[2:]         # "thon" (index 2 to end)
word[:2]         # "Py" (start to index 2)

# Repeat
"ha" * 3         # "hahaha"
```

## F-String Formatting

```python
name = "Alice"
score = 95.678

f"{name}"              # "Alice"
f"{score:.2f}"         # "95.68" (2 decimal places)
f"{score:>10}"         # "    95.678" (right-align, 10 wide)
f"{1000000:,}"         # "1,000,000" (comma separator)
f"{'yes' if score > 90 else 'no'}"  # "yes" (inline logic)
```

## Common Mistakes

| Mistake | Wrong | Right |
|---------|-------|-------|
| Strings are immutable | `name[0] = "a"` crashes | `name = "a" + name[1:]` |
| Concatenate str + int | `"age: " + 25` crashes | `f"age: {25}"` or `"age: " + str(25)` |
| Forget `f` prefix | `"{name}"` prints literally | `f"{name}"` |
| `split()` vs `split(" ")` | `split(" ")` keeps empty strings | `split()` handles any whitespace |
| `find()` returns -1 | Not checking the return value | `if text.find("x") != -1:` or use `in` |

## Quick Reference

| Operation | Syntax | Result |
|-----------|--------|--------|
| Length | `len(s)` | Number of characters |
| Lowercase | `s.lower()` | All lowercase |
| Uppercase | `s.upper()` | All uppercase |
| Strip whitespace | `s.strip()` | No leading/trailing spaces |
| Contains? | `"x" in s` | `True` / `False` |
| Replace | `s.replace("a", "b")` | New string with replacements |
| Split | `s.split(",")` | List of parts |
| Join | `",".join(lst)` | Single string from list |
| First char | `s[0]` | First character |
| Last char | `s[-1]` | Last character |
| Slice | `s[1:4]` | Characters at index 1, 2, 3 |

---

[Back to Cheat Sheets](README.md) | [Full Concept Doc](../what-is-a-variable.md)
