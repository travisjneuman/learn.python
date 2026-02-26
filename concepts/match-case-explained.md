# Match/Case Explained

Python 3.10 introduced **structural pattern matching** — the `match`/`case` statement. It is like `if`/`elif`, but designed for matching the shape and content of data.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | — | [Quiz](quizzes/match-case-explained-quiz.py) | [Flashcards](../practice/flashcards/README.md) | — |

<!-- modality-hub-end -->

## Basic syntax

```python
command = input("Enter command: ")

match command:
    case "quit":
        print("Goodbye!")
    case "help":
        print("Available commands: quit, help, status")
    case "status":
        print("All systems running.")
    case _:
        print(f"Unknown command: {command}")
```

The `_` is a wildcard — it matches anything. Think of it as the `else` branch.

## Why not just use if/elif?

For simple string matching, `if`/`elif` works fine. `match`/`case` shines when you need to match the **structure** of data — not just its value.

```python
# if/elif version — clunky for structured data
def handle_event(event):
    if isinstance(event, dict):
        if event.get("type") == "click" and "x" in event and "y" in event:
            print(f"Click at ({event['x']}, {event['y']})")
        elif event.get("type") == "keypress" and "key" in event:
            print(f"Key pressed: {event['key']}")
        else:
            print("Unknown event")

# match/case version — reads like a description of the data
def handle_event(event):
    match event:
        case {"type": "click", "x": x, "y": y}:
            print(f"Click at ({x}, {y})")
        case {"type": "keypress", "key": key}:
            print(f"Key pressed: {key}")
        case _:
            print("Unknown event")
```

## Pattern types

### Literal patterns

Match exact values:

```python
def describe_status(code: int) -> str:
    match code:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Server Error"
        case _:
            return f"Status {code}"
```

### Capture patterns

Capture the matched value into a variable:

```python
match point:
    case (0, 0):
        print("Origin")
    case (x, 0):
        print(f"On x-axis at {x}")
    case (0, y):
        print(f"On y-axis at {y}")
    case (x, y):
        print(f"Point at ({x}, {y})")
```

When Python matches `(x, 0)`, it captures the first element into `x` and checks that the second element equals `0`.

### OR patterns

Match any of several options:

```python
def classify(status: str) -> str:
    match status:
        case "active" | "enabled" | "on":
            return "Running"
        case "inactive" | "disabled" | "off":
            return "Stopped"
        case _:
            return "Unknown"
```

### Guard clauses

Add conditions with `if`:

```python
def categorize_age(age: int) -> str:
    match age:
        case n if n < 0:
            return "Invalid"
        case n if n < 13:
            return "Child"
        case n if n < 18:
            return "Teenager"
        case n if n < 65:
            return "Adult"
        case _:
            return "Senior"
```

### Sequence patterns

Match lists and tuples by shape:

```python
def process_command(parts: list[str]) -> str:
    match parts:
        case ["quit"]:
            return "Exiting..."
        case ["greet", name]:
            return f"Hello, {name}!"
        case ["add", *numbers]:
            total = sum(int(n) for n in numbers)
            return f"Sum: {total}"
        case []:
            return "Empty command"
        case _:
            return f"Unknown: {parts}"

process_command(["greet", "Alice"])     # "Hello, Alice!"
process_command(["add", "1", "2", "3"]) # "Sum: 6"
```

The `*numbers` captures the rest of the list, like `*args` in function definitions.

### Mapping patterns (dictionaries)

Match dictionaries by their keys:

```python
def process_config(config: dict) -> None:
    match config:
        case {"database": {"host": host, "port": port}}:
            print(f"Connecting to {host}:{port}")
        case {"database": {"url": url}}:
            print(f"Connecting to {url}")
        case _:
            print("Invalid config")

process_config({"database": {"host": "localhost", "port": 5432}})
# "Connecting to localhost:5432"
```

### Class patterns

Match against class instances:

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

@dataclass
class Circle:
    center: Point
    radius: float

@dataclass
class Rectangle:
    top_left: Point
    width: float
    height: float

def describe(shape) -> str:
    match shape:
        case Circle(center=Point(x=0, y=0), radius=r):
            return f"Circle at origin with radius {r}"
        case Circle(radius=r) if r > 100:
            return f"Large circle with radius {r}"
        case Circle(center=c, radius=r):
            return f"Circle at ({c.x}, {c.y}) with radius {r}"
        case Rectangle(width=w, height=h) if w == h:
            return f"Square with side {w}"
        case Rectangle(width=w, height=h):
            return f"Rectangle {w}x{h}"
        case _:
            return "Unknown shape"
```

## When to use match/case

**Good uses:**
- Parsing commands or messages with varying structure
- Handling different shapes of data (API responses, config files)
- State machines and event handling
- Replacing complex `isinstance` chains

**Overkill for:**
- Simple value comparisons (`if x == 1` is fine)
- Two or three branches (use `if`/`elif`)

## Common mistakes

**Forgetting the wildcard:**
```python
# If no case matches and there is no _, Python silently does nothing.
match value:
    case 1:
        print("One")
    case 2:
        print("Two")
    # value is 3 → nothing happens, no error
```

Always include `case _:` unless you intentionally want to skip unmatched values.

**Using a variable name that shadows a constant:**
```python
STATUS_OK = 200

match code:
    case STATUS_OK:  # This does NOT compare to 200!
        # It captures `code` into a new variable named STATUS_OK
        print("OK")
```

Bare names in patterns are **capture variables**, not references to existing variables. To match a constant, use a dotted name or a literal:

```python
match code:
    case 200:       # Literal — works correctly
        print("OK")
```

**Requires Python 3.10+:**
```python
# If you are on Python 3.9 or earlier, match/case is a syntax error.
# Use if/elif instead.
```

## Practice

- [Level 2 / 08 Multi Format Exporter](../projects/level-2/08-multi-format-exporter/README.md)
- [Level 4 / 03 Pipeline Composition Toolkit](../projects/level-4/03-pipeline-composition-toolkit/README.md)
- [Level 7 / 01 Rest Api Client](../projects/level-7/01-rest-api-client/README.md)

**Quick check:** [Take the quiz](quizzes/match-case-explained-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](dataclasses-explained.md) | [Home](../README.md) | [Next →](modern-python-tooling.md) |
|:---|:---:|---:|
