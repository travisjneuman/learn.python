# Debugging Methodology

Debugging is the systematic process of finding and fixing bugs. It is not about staring at code until you see the problem — it is a repeatable method that works on any bug, in any language. The best debuggers are not the smartest programmers; they are the most methodical.

## Why This Matters

You will spend more time debugging than writing new code. A systematic approach turns frustrating hours of "why does this not work?" into a predictable process. The method described here — Reproduce, Isolate, Hypothesize, Test, Fix, Verify, Prevent — works for everything from a typo to a race condition.

## The 7-step method

### 1. Reproduce — make the bug happen reliably

Before fixing anything, you need to see the bug yourself. Write down the exact steps:

```
1. Run `python app.py`
2. Enter username "alice"
3. Enter password "test123"
4. Click "View Profile"
5. ERROR: KeyError: 'email'
```

If you cannot reproduce the bug, you cannot verify you fixed it. Ask: "Does this happen every time? Only with certain inputs? Only on certain machines?"

### 2. Isolate — narrow down where the bug is

Remove variables until you find the smallest piece of code that still has the bug:

```python
# The program is 500 lines. Where is the bug?

# Start by adding print statements at key points:
print("DEBUG: got to step 1")
print(f"DEBUG: user_data = {user_data}")
print("DEBUG: got to step 2")

# Or use the binary search method:
# 1. Add a print halfway through the code
# 2. Is the data correct at that point?
#    - YES → bug is in the second half
#    - NO  → bug is in the first half
# 3. Repeat until you find the exact line
```

### 3. Hypothesize — form a theory

Based on the error and where it occurs, make a specific guess:

- "The `email` key is missing because the API response changed format"
- "The variable is None because the database query returned no results"
- "The loop runs one too many times because I used `<=` instead of `<`"

Do NOT start changing code randomly. Have a theory first.

### 4. Test — verify your hypothesis

Test your theory with the smallest possible experiment:

```python
# Hypothesis: user_data doesn't have an 'email' key
# Test: print the actual keys
print(f"DEBUG: keys = {user_data.keys()}")

# Hypothesis: the API is returning a different format
# Test: print the raw response
print(f"DEBUG: response = {response.json()}")
```

If your hypothesis was wrong, go back to step 3 with new information.

### 5. Fix — make the minimum change

Fix only the bug. Do not refactor surrounding code, add features, or "improve" things. Keep the change as small as possible:

```python
# Before (buggy):
email = user_data["email"]

# After (fixed):
email = user_data.get("email", "no-email@example.com")
```

### 6. Verify — confirm the fix works

Run the same reproduction steps from step 1. The bug should be gone. Also check that you did not break anything else — run the test suite.

### 7. Prevent — stop this bug from coming back

Write a test that catches this specific bug:

```python
def test_missing_email_field():
    user_data = {"name": "Alice"}    # No email key
    result = process_user(user_data)
    assert result.email == "no-email@example.com"
```

Ask: "Why did this bug happen? Could it happen elsewhere? Is there a systematic fix?"

## Python debugging tools

### `print()` — the simplest debugger

```python
def process_data(items):
    print(f"DEBUG: items = {items}")          # What did we receive?
    print(f"DEBUG: type = {type(items)}")      # What type is it?
    print(f"DEBUG: len = {len(items)}")        # How many items?

    for i, item in enumerate(items):
        print(f"DEBUG: processing item {i}: {item}")
        result = transform(item)
        print(f"DEBUG: result = {result}")
```

Use f-strings with the `=` shorthand (Python 3.8+):

```python
x = 42
name = "Alice"
print(f"{x=}")        # "x=42"
print(f"{name=}")     # "name='Alice'"
print(f"{len(name)=}")  # "len(name)=5"
```

### `breakpoint()` — drop into the debugger

```python
def process_data(items):
    for item in items:
        if item.get("status") == "error":
            breakpoint()    # Pauses here, opens the debugger
        result = transform(item)
```

When execution hits `breakpoint()`, you get an interactive prompt where you can:

| Command | Action |
|---------|--------|
| `n` | Execute next line |
| `s` | Step into a function call |
| `c` | Continue until next breakpoint |
| `p variable` | Print a variable's value |
| `pp variable` | Pretty-print a variable |
| `l` | Show surrounding code |
| `q` | Quit the debugger |

```
> process.py(5)process_data()
-> result = transform(item)
(Pdb) p item
{'id': 42, 'status': 'error', 'data': None}
(Pdb) p item['data']
None
(Pdb) n
> process.py(6)process_data()
```

### `pdb` — the Python debugger

`breakpoint()` uses `pdb` by default. You can also run a script under the debugger:

```bash
# Run with debugger from the start:
python -m pdb my_script.py

# Post-mortem debugging — analyze after a crash:
python -c "import pdb; pdb.pm()"
```

### `icecream` — better print debugging

The `icecream` library makes print debugging cleaner:

```bash
pip install icecream
```

```python
from icecream import ic

x = 42
ic(x)                  # ic| x: 42
ic(x * 2)             # ic| x * 2: 84

def add(a, b):
    ic(a, b)           # ic| a: 3, b: 5
    return a + b

result = add(3, 5)
ic(result)             # ic| result: 8
```

`ic()` automatically prints the variable name and value — no more writing `print(f"x={x}")`.

### `snoop` — trace function execution

```bash
pip install snoop
```

```python
import snoop

@snoop
def process(items):
    total = 0
    for item in items:
        total += item
    return total

process([1, 2, 3])
```

Output shows every line as it executes, with variable values:

```
12:34:56.78 >>> Call to process in File "test.py", line 4
12:34:56.78 ...... items = [1, 2, 3]
12:34:56.78    5 |     total = 0
12:34:56.78 ...... total = 0
12:34:56.78    6 |     for item in items:
12:34:56.78 ...... item = 1
12:34:56.78    7 |         total += item
12:34:56.78 ...... total = 1
...
```

## Debugging strategies by error type

### `TypeError`
Usually means you passed the wrong type. Print the types of all arguments:
```python
print(f"DEBUG: {type(x)=}, {type(y)=}")
```

### `KeyError` / `IndexError`
Print the actual keys/length before accessing:
```python
print(f"DEBUG: keys = {data.keys()}")
print(f"DEBUG: len = {len(my_list)}")
```

### `AttributeError`
The object is not the type you think. Print what it actually is:
```python
print(f"DEBUG: {type(obj)=}, {dir(obj)=}")
```

### Logic errors (wrong output, no crash)
Add assertions to check your assumptions:
```python
assert len(results) > 0, "Expected results but got empty list"
assert isinstance(user, dict), f"Expected dict, got {type(user)}"
```

## Common Mistakes

**Changing code randomly instead of forming a hypothesis:**
Random changes waste time and can introduce new bugs. Always hypothesize first.

**Not reading the full error message:**
The traceback shows the entire chain of function calls. Read from the bottom up — the last line is where the error occurred, and the lines above show how you got there.

**Removing debug prints and losing your work:**
Use a consistent prefix like `DEBUG:` so you can find and remove them all:
```bash
# Find all debug prints:
grep -n "DEBUG:" *.py
```

Or use `icecream` and `ic.disable()` to turn off all debug output at once.

## Practice

- [Level 0 projects](../projects/level-0/) — practice debugging failing tests
- [Module 08 Advanced Testing](../projects/modules/08-testing-advanced/) — systematic testing catches bugs early
- [Errors and Debugging](./errors-and-debugging.md) — understanding Python errors
- [Reading Error Messages](./reading-error-messages.md) — traceback anatomy

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

## Further Reading

- [pdb — The Python Debugger (Python docs)](https://docs.python.org/3/library/pdb.html)
- [icecream on PyPI](https://pypi.org/project/icecream/)
- [snoop on PyPI](https://pypi.org/project/snoop/)

---

| [← Prev](testing-strategies.md) | [Home](../README.md) | [Next →](errors-and-debugging.md) |
|:---|:---:|---:|
