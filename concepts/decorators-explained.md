# Decorators Explained

A decorator is a function that wraps another function to add extra behavior. The `@` symbol is shorthand for applying a decorator.

## Visualize It

See how a decorator wraps a function and changes its behavior:
[Open in Python Tutor](https://pythontutor.com/render.html#code=def%20shout%28func%29%3A%0A%20%20%20%20def%20wrapper%28%29%3A%0A%20%20%20%20%20%20%20%20result%20%3D%20func%28%29%0A%20%20%20%20%20%20%20%20return%20result.upper%28%29%0A%20%20%20%20return%20wrapper%0A%0A%40shout%0Adef%20greet%28%29%3A%0A%20%20%20%20return%20%22hello%2C%20world%22%0A%0Aprint%28greet%28%29%29&cumulative=false&curInstr=0&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D)

## What decorators look like

```python
@app.get("/")
def home():
    return "Hello!"
```

The `@app.get("/")` is a decorator. It takes the `home` function and registers it as a web endpoint. You see decorators everywhere in FastAPI, Flask, Click, and pytest.

## How decorators work

A decorator is just a function that takes a function and returns a new function:

```python
def shout(func):
    def wrapper():
        result = func()
        return result.upper()
    return wrapper

@shout
def greet():
    return "hello, world"

print(greet())    # "HELLO, WORLD"
```

The `@shout` line is equivalent to:

```python
def greet():
    return "hello, world"

greet = shout(greet)    # Replace greet with the wrapped version
```

## Decorators with arguments

If the original function takes arguments, the wrapper must pass them through:

```python
def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_call
def add(a, b):
    return a + b

add(3, 5)
# Calling add with args=(3, 5), kwargs={}
# add returned 8
```

## Real-world examples

**Flask / FastAPI — route registration:**
```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id}
```

**pytest — parametrized tests:**
```python
@pytest.mark.parametrize("input,expected", [(1, 1), (2, 4), (3, 9)])
def test_square(input, expected):
    assert input ** 2 == expected
```

**Click — CLI commands:**
```python
@click.command()
@click.option("--name", default="World")
def hello(name):
    click.echo(f"Hello, {name}!")
```

**Timing a function:**
```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.2f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "done"
```

## Stacking decorators

You can apply multiple decorators. They apply bottom-up:

```python
@decorator_a
@decorator_b
def my_function():
    pass

# Equivalent to:
my_function = decorator_a(decorator_b(my_function))
```

## Common mistakes

**Forgetting `functools.wraps`:**
```python
from functools import wraps

def my_decorator(func):
    @wraps(func)    # Preserves the original function's name and docstring
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

Without `@wraps`, the decorated function loses its original name, which makes debugging harder.

**Calling instead of decorating:**
```python
@my_decorator()    # Note the () — this CALLS the decorator
def func(): pass

@my_decorator      # No () — this APPLIES the decorator
def func(): pass
```

Whether you need `()` depends on how the decorator was written. Some take arguments (like `@app.get("/")`), some don't (like `@timer`).

## Practice

- [Module 02 CLI Tools](../projects/modules/02-cli-tools/)
- [Module 04 FastAPI](../projects/modules/04-fastapi-web/)
- [Module 08 Advanced Testing](../projects/modules/08-testing-advanced/)
- [Module: Elite Track / 01 Algorithms Complexity Lab](../projects/elite-track/01-algorithms-complexity-lab/README.md)
- [Module: Elite Track / 02 Concurrent Job System](../projects/elite-track/02-concurrent-job-system/README.md)
- [Module: Elite Track / 03 Distributed Cache Simulator](../projects/elite-track/03-distributed-cache-simulator/README.md)
- [Module: Elite Track / 04 Secure Auth Gateway](../projects/elite-track/04-secure-auth-gateway/README.md)
- [Module: Elite Track / 05 Performance Profiler Workbench](../projects/elite-track/05-performance-profiler-workbench/README.md)
- [Module: Elite Track / 06 Event Driven Architecture Lab](../projects/elite-track/06-event-driven-architecture-lab/README.md)
- [Module: Elite Track / 07 Observability Slo Platform](../projects/elite-track/07-observability-slo-platform/README.md)
- [Module: Elite Track / 08 Policy Compliance Engine](../projects/elite-track/08-policy-compliance-engine/README.md)
- [Module: Elite Track / 09 Open Source Maintainer Simulator](../projects/elite-track/09-open-source-maintainer-simulator/README.md)
- [Module: Elite Track / 10 Staff Engineer Capstone](../projects/elite-track/10-staff-engineer-capstone/README.md)

**Quick check:** [Take the quiz](quizzes/decorators-explained-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](classes-and-objects.md) | [Home](../README.md) | [Next →](virtual-environments.md) |
|:---|:---:|---:|
