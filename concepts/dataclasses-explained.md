# Dataclasses Explained

A **dataclass** is the easy way to create a class that holds data. Instead of writing `__init__`, `__repr__`, and `__eq__` yourself, Python generates them for you.

## The problem dataclasses solve

Here is a plain class that stores a person's information:

```python
class Person:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age}, email={self.email!r})"

    def __eq__(self, other):
        return (self.name == other.name
                and self.age == other.age
                and self.email == other.email)
```

That is 13 lines of repetitive code. Now the same thing with a dataclass:

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    email: str
```

Six lines. Python automatically generates `__init__`, `__repr__`, and `__eq__` from the field definitions.

## Creating and using dataclass instances

```python
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float
    in_stock: bool

# Create an instance — same as a regular class
laptop = Product("ThinkPad", 999.99, True)
mouse = Product("Wireless Mouse", 29.99, True)

print(laptop)
# Product(name='ThinkPad', price=999.99, in_stock=True)

print(laptop.name)    # "ThinkPad"
print(laptop.price)   # 999.99

# Equality compares all fields
laptop2 = Product("ThinkPad", 999.99, True)
print(laptop == laptop2)  # True
```

## Default values

```python
@dataclass
class Config:
    host: str = "localhost"
    port: int = 8080
    debug: bool = False

# Use defaults
dev = Config()
print(dev)  # Config(host='localhost', port=8080, debug=False)

# Override some defaults
prod = Config(host="api.example.com", port=443)
print(prod)  # Config(host='api.example.com', port=443, debug=False)
```

Fields without defaults must come before fields with defaults, just like function arguments.

## Mutable defaults with `field(default_factory)`

You cannot use a mutable value (like a list or dict) as a default directly. Use `field(default_factory=...)` instead:

```python
from dataclasses import dataclass, field

@dataclass
class ShoppingCart:
    owner: str
    items: list[str] = field(default_factory=list)

cart = ShoppingCart("Alice")
cart.items.append("Coffee")
print(cart)  # ShoppingCart(owner='Alice', items=['Coffee'])
```

Why? If you wrote `items: list[str] = []`, every instance would share the same list. `default_factory=list` creates a new list for each instance.

## `__post_init__` — extra setup after creation

Sometimes you need to compute a value from other fields:

```python
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)  # Not passed to __init__

    def __post_init__(self):
        self.area = self.width * self.height

r = Rectangle(5.0, 3.0)
print(r.area)  # 15.0
print(r)       # Rectangle(width=5.0, height=3.0, area=15.0)
```

`field(init=False)` means "don't include this in the constructor." `__post_init__` runs right after `__init__` finishes.

## Frozen dataclasses — immutable data

Add `frozen=True` to make instances read-only:

```python
@dataclass(frozen=True)
class Coordinate:
    latitude: float
    longitude: float

nyc = Coordinate(40.7128, -74.0060)
print(nyc)  # Coordinate(latitude=40.7128, longitude=-74.006)

nyc.latitude = 0  # FrozenInstanceError! Cannot modify.
```

Frozen dataclasses can be used as dictionary keys and in sets because they are hashable.

## Adding methods

Dataclasses are regular classes. You can add any methods you want:

```python
@dataclass
class Temperature:
    celsius: float

    @property
    def fahrenheit(self) -> float:
        return self.celsius * 9 / 5 + 32

    def is_freezing(self) -> bool:
        return self.celsius <= 0

temp = Temperature(100)
print(temp.fahrenheit)    # 212.0
print(temp.is_freezing()) # False
```

## Dataclass vs plain class

| Feature | Plain class | Dataclass |
|---------|------------|-----------|
| `__init__` | Write yourself | Generated |
| `__repr__` | Write yourself | Generated |
| `__eq__` | Write yourself | Generated |
| Custom methods | Yes | Yes |
| Inheritance | Yes | Yes |
| Default values | Yes | Yes |
| Immutability | Manual | `frozen=True` |

**Use a dataclass when:** your class is mainly about storing data.
**Use a plain class when:** your class has complex initialization logic, or you need fine-grained control over every special method.

## Common mistakes

**Mutable default without `field`:**
```python
# WRONG — all instances share the same list
@dataclass
class Bad:
    items: list[str] = []   # ValueError!

# RIGHT
@dataclass
class Good:
    items: list[str] = field(default_factory=list)
```

**Fields without defaults before fields with defaults:**
```python
# WRONG
@dataclass
class Bad:
    name: str = "Unknown"
    age: int               # TypeError! Non-default after default.

# RIGHT
@dataclass
class Good:
    age: int
    name: str = "Unknown"
```

**Trying to modify a frozen dataclass:**
```python
@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
p.x = 5.0  # FrozenInstanceError
```

## Practice

- [Level 2 / 06 Config Parser Pro](../projects/level-2/06-config-parser-pro/README.md)
- [Level 3 / 05 Structured Log System](../projects/level-3/05-structured-log-system/README.md)
- [Level 4 / 01 Schema Validator Toolkit](../projects/level-4/01-schema-validator-toolkit/README.md)

**Quick check:** [Take the quiz](quizzes/dataclasses-explained-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](type-hints-explained.md) | [Home](../README.md) | [Next →](match-case-explained.md) |
|:---|:---:|---:|
