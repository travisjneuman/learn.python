# *args and **kwargs Explained

`*args` and `**kwargs` let a function accept any number of arguments. `*args` collects extra positional arguments into a tuple. `**kwargs` collects extra keyword arguments into a dictionary. Together, they make functions flexible without requiring a fixed parameter list.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | [Videos](videos/args-kwargs-explained.md) | [Quiz](quizzes/args-kwargs-explained-quiz.py) | [Flashcards](../practice/flashcards/README.md) | [Diagrams](diagrams/args-kwargs-explained.md) |

<!-- modality-hub-end -->

## Why This Matters

You will see `*args` and `**kwargs` in almost every Python library. Understanding them is essential for writing decorators, creating wrapper functions, and understanding how frameworks like Flask and pytest work under the hood. They also appear in function signatures on docs.python.org — you need to read them confidently.

## `*args` — variable positional arguments

The `*` before a parameter name collects all extra positional arguments into a tuple:

```python
def add_all(*args):
    print(type(args))    # <class 'tuple'>
    print(args)          # (1, 2, 3, 4, 5)
    return sum(args)

add_all(1, 2, 3, 4, 5)    # 15
add_all(10, 20)             # 30
add_all()                   # 0
```

The name `args` is a convention — you can use any name. The `*` is what matters:

```python
def greet(*names):
    for name in names:
        print(f"Hello, {name}!")

greet("Alice", "Bob", "Charlie")
```

## `**kwargs` — variable keyword arguments

The `**` before a parameter name collects all extra keyword arguments into a dictionary:

```python
def print_info(**kwargs):
    print(type(kwargs))    # <class 'dict'>
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=30, city="Portland")
# name: Alice
# age: 30
# city: Portland
```

Again, `kwargs` is just a convention. The `**` is what matters.

## Combining regular parameters, `*args`, and `**kwargs`

```python
def make_profile(name, *hobbies, **details):
    print(f"Name: {name}")
    print(f"Hobbies: {hobbies}")
    print(f"Details: {details}")

make_profile("Alice", "reading", "hiking", age=30, city="Portland")
# Name: Alice
# Hobbies: ('reading', 'hiking')
# Details: {'age': 30, 'city': 'Portland'}
```

The order must be: regular parameters, then `*args`, then `**kwargs`.

## Unpacking with `*` and `**`

The `*` and `**` operators also work in the opposite direction — unpacking a sequence or dictionary into function arguments:

```python
def add(a, b, c):
    return a + b + c

# Unpack a list into positional arguments:
numbers = [1, 2, 3]
add(*numbers)    # Same as add(1, 2, 3) → 6

# Unpack a dict into keyword arguments:
params = {"a": 10, "b": 20, "c": 30}
add(**params)    # Same as add(a=10, b=20, c=30) → 60
```

This is extremely useful for forwarding arguments:

```python
def wrapper(*args, **kwargs):
    print("Before the call")
    result = original_function(*args, **kwargs)
    print("After the call")
    return result
```

## Positional-only parameters (`/`)

Python 3.8+ lets you mark parameters as positional-only using `/`:

```python
def greet(name, /, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Alice")                    # OK: "Hello, Alice!"
greet("Alice", greeting="Hi")    # OK: "Hi, Alice!"
greet(name="Alice")              # TypeError! name is positional-only
```

Everything before `/` must be passed by position, not by name. You see this in built-in functions like `len()` — you cannot write `len(obj=[1,2,3])`.

## Keyword-only parameters (`*`)

A bare `*` in the parameter list forces everything after it to be keyword-only:

```python
def connect(host, port, *, timeout=30, retries=3):
    print(f"Connecting to {host}:{port} (timeout={timeout})")

connect("localhost", 8080)                        # OK
connect("localhost", 8080, timeout=10)             # OK
connect("localhost", 8080, 10)                     # TypeError! timeout is keyword-only
```

This prevents mistakes where someone passes arguments in the wrong order.

## The full parameter order

```python
def example(pos_only, /, normal, *, kw_only, **kwargs):
    pass

# pos_only  — must be positional (before /)
# normal    — can be positional or keyword
# kw_only   — must be keyword (after *)
# **kwargs  — catches extra keyword arguments
```

The complete order is:
1. Positional-only parameters (before `/`)
2. Regular parameters
3. `*args`
4. Keyword-only parameters (after `*` or `*args`)
5. `**kwargs`

## Real-world examples

**Decorator that passes through all arguments:**
```python
from functools import wraps

def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

**Config builder:**
```python
def create_config(name, **overrides):
    defaults = {
        "debug": False,
        "port": 8080,
        "host": "localhost",
    }
    return {**defaults, **overrides, "name": name}

config = create_config("myapp", debug=True, port=3000)
# {"debug": True, "port": 3000, "host": "localhost", "name": "myapp"}
```

**Merging dictionaries with `**`:**
```python
defaults = {"color": "blue", "size": "medium"}
user_prefs = {"color": "red", "font": "Arial"}

merged = {**defaults, **user_prefs}
# {"color": "red", "size": "medium", "font": "Arial"}
# Later values override earlier ones
```

## Common Mistakes

**Mutable default arguments (not specific to *args but related):**
```python
# WRONG — the list is shared between all calls:
def add_item(item, items=[]):
    items.append(item)
    return items

add_item("a")    # ["a"]
add_item("b")    # ["a", "b"] — surprise!

# RIGHT — use None as default:
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

**Forgetting to unpack:**
```python
def add(a, b):
    return a + b

args = (1, 2)
add(args)      # TypeError — passes the tuple as a single argument
add(*args)     # 3 — unpacks into two arguments
```

**Wrong order of parameters:**
```python
# WRONG:
def bad(*args, name, **kwargs):    # name after *args is keyword-only
    pass

bad("a", "b", "Alice")    # TypeError! name must be keyword
bad("a", "b", name="Alice")    # OK
```

## Practice

- [Level 2 / 01 JSON Explorer](../projects/level-2/01-json-explorer/README.md)
- [Module 02 CLI Tools](../projects/modules/02-cli-tools/) — Click/Typer use these patterns
- [Module 04 FastAPI Web](../projects/modules/04-fastapi-web/) — endpoint parameter handling

**Quick check:** [Take the quiz](quizzes/args-kwargs-explained-quiz.py) *(coming soon)*

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

## Further Reading

- [More on Defining Functions (Python tutorial)](https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions)
- [PEP 570 — Positional-Only Parameters](https://peps.python.org/pep-0570/)
- [PEP 3102 — Keyword-Only Arguments](https://peps.python.org/pep-3102/)

---

| [← Prev](enums-explained.md) | [Home](../README.md) | [Next →](regex-explained.md) |
|:---|:---:|---:|
