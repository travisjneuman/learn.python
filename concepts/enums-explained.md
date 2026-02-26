# Enums Explained

An enum (enumeration) is a set of named constants. Instead of scattering magic strings like `"active"`, `"inactive"`, `"pending"` throughout your code, you define them once in an enum and get autocomplete, typo protection, and clear documentation for free.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | [Videos](videos/enums-explained.md) | [Quiz](quizzes/enums-explained-quiz.py) | [Flashcards](../practice/flashcards/README.md) | [Diagrams](diagrams/enums-explained.md) |

<!-- modality-hub-end -->

## Why This Matters

Magic strings and magic numbers are a top source of bugs. If you mistype `"actve"` instead of `"active"`, Python will not catch it — your code will silently do the wrong thing. Enums make invalid values impossible: `Status.ACTVE` raises an `AttributeError` immediately.

## Basic enum

```python
from enum import Enum

class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

# Usage:
my_color = Color.RED
print(my_color)          # Color.RED
print(my_color.name)     # "RED"
print(my_color.value)    # "red"
```

## Comparing enums

```python
# Use `is` or `==` to compare:
if my_color is Color.RED:
    print("It's red!")

if my_color == Color.RED:
    print("Also red!")

# Enums are NOT equal to their values:
Color.RED == "red"       # False
Color.RED.value == "red" # True
```

## `IntEnum` — when you need integer values

`IntEnum` members behave like integers, so you can compare them with numbers and use them in math:

```python
from enum import IntEnum

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

# Works like an integer:
Priority.HIGH > Priority.LOW     # True
Priority.MEDIUM + 1              # 3
Priority.HIGH == 3               # True (unlike regular Enum)

# Sort by priority:
tasks = [Priority.HIGH, Priority.LOW, Priority.CRITICAL]
sorted(tasks)    # [Priority.LOW, Priority.HIGH, Priority.CRITICAL]
```

## `StrEnum` — when you need string values (Python 3.11+)

`StrEnum` members behave like strings:

```python
from enum import StrEnum

class Status(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

# Works like a string:
Status.ACTIVE == "active"        # True
print(f"User is {Status.ACTIVE}")  # "User is active"

# Great for API responses, database values, etc.
```

If you are on Python 3.10 or earlier, use `class Status(str, Enum):` instead.

## `auto()` — automatic values

When you do not care about the specific values, let Python assign them:

```python
from enum import Enum, auto

class Direction(Enum):
    NORTH = auto()    # 1
    SOUTH = auto()    # 2
    EAST = auto()     # 3
    WEST = auto()     # 4
```

`auto()` assigns incrementing integers starting from 1. Useful when the value does not matter — only the name.

## Pattern matching with enums (Python 3.10+)

Enums work beautifully with `match/case`:

```python
from enum import Enum, auto

class Command(Enum):
    START = auto()
    STOP = auto()
    PAUSE = auto()
    RESUME = auto()

def handle(cmd: Command) -> str:
    match cmd:
        case Command.START:
            return "Starting..."
        case Command.STOP:
            return "Stopping..."
        case Command.PAUSE:
            return "Pausing..."
        case Command.RESUME:
            return "Resuming..."

print(handle(Command.START))    # "Starting..."
```

## Real-world example — HTTP status codes

```python
from enum import IntEnum

class HTTPStatus(IntEnum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    SERVER_ERROR = 500

def check_response(status_code: int):
    try:
        status = HTTPStatus(status_code)
    except ValueError:
        print(f"Unknown status: {status_code}")
        return

    if status < 400:
        print(f"{status.name}: Success")
    else:
        print(f"{status.name}: Error")

check_response(200)    # OK: Success
check_response(404)    # NOT_FOUND: Error
```

## Iterating over enums

```python
class Season(Enum):
    SPRING = auto()
    SUMMER = auto()
    AUTUMN = auto()
    WINTER = auto()

# List all members:
for season in Season:
    print(f"{season.name} = {season.value}")

# Get all values:
values = [s.value for s in Season]

# Get all names:
names = [s.name for s in Season]
```

## Looking up enum members

```python
# By name:
Color["RED"]         # Color.RED

# By value:
Color("red")         # Color.RED

# Check membership:
"RED" in Color.__members__    # True
```

## Common Mistakes

**Comparing an enum to its value (with regular Enum):**
```python
class Color(Enum):
    RED = "red"

Color.RED == "red"    # False! Use Color.RED.value == "red"
```

Use `StrEnum` or `IntEnum` if you need value comparisons to work naturally.

**Forgetting that enum members are singletons:**
```python
# You cannot create new instances with the same value:
Color("red") is Color.RED    # True — same object, not a copy
```

**Trying to modify enum values:**
```python
Color.RED = "crimson"    # AttributeError — enums are immutable
```

## Practice

- [Level 3 / 01 Plugin Loader](../projects/level-3/01-plugin-loader/README.md)
- [Module 04 FastAPI Web](../projects/modules/04-fastapi-web/) — status enums in API responses
- [Elite Track / 06 Event Driven Architecture Lab](../projects/elite-track/06-event-driven-architecture-lab/README.md)

**Quick check:** [Take the quiz](quizzes/enums-explained-quiz.py) *(coming soon)*

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

## Further Reading

- [enum — Support for enumerations (Python docs)](https://docs.python.org/3/library/enum.html)
- [PEP 435 — Adding an Enum type to the Python standard library](https://peps.python.org/pep-0435/)
- [StrEnum (Python 3.11+)](https://docs.python.org/3/library/enum.html#enum.StrEnum)

---

| [← Prev](security-basics.md) | [Home](../README.md) | [Next →](functools-and-itertools.md) |
|:---|:---:|---:|
