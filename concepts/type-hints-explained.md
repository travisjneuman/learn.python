# Type Hints Explained

Type hints tell Python (and your editor) what kind of data a variable or function expects. They do not change how your code runs — Python ignores them at runtime. But they help you catch mistakes before you run anything.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | [Videos](videos/type-hints-explained.md) | [Quiz](quizzes/type-hints-explained-quiz.py) | [Flashcards](../practice/flashcards/README.md) | [Diagrams](diagrams/type-hints-explained.md) |

<!-- modality-hub-end -->

## Why type hints matter

Without type hints, you have to remember what every function expects:

```python
def greet(name, times):
    for i in range(times):
        print(f"Hello, {name}!")

greet("Alice", "3")  # Bug! "3" is a string, not an int — crashes at runtime
```

With type hints, your editor warns you immediately:

```python
def greet(name: str, times: int) -> None:
    for i in range(times):
        print(f"Hello, {name}!")

greet("Alice", "3")  # Editor underlines "3" — wrong type
```

## Basic syntax

### Variable annotations

```python
name: str = "Alice"
age: int = 30
price: float = 9.99
is_active: bool = True
```

### Function annotations

```python
def add(a: int, b: int) -> int:
    return a + b

def say_hello(name: str) -> None:
    print(f"Hello, {name}")
```

The `-> int` means "this function returns an integer." `-> None` means it returns nothing.

### Collections

```python
# A list of strings
names: list[str] = ["Alice", "Bob", "Charlie"]

# A dictionary mapping strings to integers
scores: dict[str, int] = {"Alice": 95, "Bob": 87}

# A set of integers
unique_ids: set[int] = {1, 2, 3}

# A tuple with specific types
point: tuple[float, float] = (3.14, 2.71)
```

## Optional values

When a value might be `None`, use `| None` (Python 3.10+) or `Optional`:

```python
# Python 3.10+ (preferred)
def find_user(user_id: int) -> dict | None:
    if user_id in database:
        return database[user_id]
    return None

# Older Python (still works everywhere)
from typing import Optional

def find_user(user_id: int) -> Optional[dict]:
    if user_id in database:
        return database[user_id]
    return None
```

## Union types

When a value can be one of several types:

```python
# Python 3.10+
def display(value: str | int | float) -> str:
    return str(value)

# Older Python
from typing import Union

def display(value: Union[str, int, float]) -> str:
    return str(value)
```

## Type aliases

Create shortcuts for complex types:

```python
# Instead of repeating dict[str, list[int]] everywhere:
StudentScores = dict[str, list[int]]

def get_top_students(scores: StudentScores) -> list[str]:
    return [name for name, vals in scores.items() if max(vals) > 90]
```

## Generics with TypeVar

When you want a function to work with any type but keep types consistent:

```python
from typing import TypeVar

T = TypeVar("T")

def first_item(items: list[T]) -> T:
    return items[0]

# Python infers the type:
name = first_item(["Alice", "Bob"])   # name is str
number = first_item([1, 2, 3])       # number is int
```

## Protocol — structural typing

A `Protocol` defines what methods an object must have, without requiring inheritance:

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:
    def draw(self) -> str:
        return "Drawing a circle"

class Square:
    def draw(self) -> str:
        return "Drawing a square"

def render(shape: Drawable) -> None:
    print(shape.draw())

# Both work — they have a draw() method
render(Circle())
render(Square())
```

Neither `Circle` nor `Square` inherits from `Drawable`. They just happen to have a `draw()` method, and that is enough.

## Running a type checker

Type hints are enforced by external tools, not Python itself:

```bash
# Install mypy
pip install mypy

# Check your code
mypy my_script.py
```

Your editor (VS Code with Pylance) checks types automatically as you type.

## Common mistakes

**Forgetting return type:**
```python
def greet(name: str):        # What does this return? Unclear.
    return f"Hello, {name}"

def greet(name: str) -> str:  # Clear: returns a string.
    return f"Hello, {name}"
```

**Using `list` instead of `list[str]`:**
```python
def process(items: list):         # A list of what? Not helpful.
    ...

def process(items: list[str]):    # A list of strings. Much better.
    ...
```

**Confusing `Optional[X]` with `X`:**
```python
def find(name: str) -> Optional[str]:
    ...

result = find("Alice")
print(result.upper())  # Bug! result might be None
# Fix: check first
if result is not None:
    print(result.upper())
```

## When type hints are introduced in this curriculum

- **Level 00:** No type hints (focus on basics)
- **Level 1:** Basic function annotations (`def greet(name: str) -> str`)
- **Level 2:** Collection types (`list[str]`, `dict[str, int]`)
- **Level 3+:** Optional, Union, TypeVar, Protocol

You do not need to learn all of this at once. Come back to this page as you level up.

## Practice

- [Level 1 / 01 Input Validator](../projects/level-1/01-input-validator/README.md)
- [Level 2 / 01 List Comprehension Lab](../projects/level-2/01-list-comprehension-lab/README.md)
- [Level 3 / 01 Package Layout Lab](../projects/level-3/01-package-layout-lab/README.md)

**Quick check:** [Take the quiz](quizzes/type-hints-explained-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](async-explained.md) | [Home](../README.md) | [Next →](dataclasses-explained.md) |
|:---|:---:|---:|
