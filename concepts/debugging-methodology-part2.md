# Debugging Methodology — Part 2: Tools and Techniques

[← Part 1: Approach and Mental Models](./debugging-methodology-part1.md) · [Back to Overview](./debugging-methodology.md)

---

This part covers the practical debugging tools available in Python: print debugging, the built-in debugger (`pdb`/`breakpoint`), and third-party tools like `icecream` and `snoop`.

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

---

| [← Part 1: Approach and Mental Models](./debugging-methodology-part1.md) | [Overview](./debugging-methodology.md) |
|:---|---:|
