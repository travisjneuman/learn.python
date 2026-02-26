# Classes and Objects

> **Try This First:** Before reading, try this in Python: `class Dog: pass` then `my_dog = Dog()` then `print(type(my_dog))`. You just created a class and made an object from it.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | — | [Quiz](quizzes/classes-and-objects-quiz.py) | [Flashcards](../practice/flashcards/README.md) | — |

<!-- modality-hub-end -->

A **class** is a blueprint for creating things. An **object** is a thing created from that blueprint.

## Visualize It

See how Python creates objects and stores attributes on each instance:
[Open in Python Tutor](https://pythontutor.com/render.html#code=class%20Dog%3A%0A%20%20%20%20def%20__init__%28self%2C%20name%29%3A%0A%20%20%20%20%20%20%20%20self.name%20%3D%20name%0A%20%20%20%20%20%20%20%20self.tricks%20%3D%20%5B%5D%0A%20%20%20%20def%20learn%28self%2C%20trick%29%3A%0A%20%20%20%20%20%20%20%20self.tricks.append%28trick%29%0A%0Arex%20%3D%20Dog%28%22Rex%22%29%0Arex.learn%28%22sit%22%29%0Aprint%28rex.tricks%29&cumulative=false&curInstr=0&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D)

## Why classes exist

When you have data that belongs together (a person's name, age, email) and actions that operate on that data (send email, update age), a class bundles them into one unit.

## A simple class

```python
class Dog:
    def __init__(self, name, breed):
        # These are "attributes" — data stored on the object.
        self.name = name
        self.breed = breed
        self.tricks = []

    def learn_trick(self, trick):
        # This is a "method" — a function that belongs to the object.
        self.tricks.append(trick)

    def show_tricks(self):
        if self.tricks:
            return f"{self.name} knows: {', '.join(self.tricks)}"
        return f"{self.name} hasn't learned any tricks yet"
```

## Creating objects (instances)

```python
my_dog = Dog("Rex", "Labrador")      # Create an instance
my_dog.learn_trick("sit")            # Call a method
my_dog.learn_trick("shake")
print(my_dog.show_tricks())          # "Rex knows: sit, shake"
print(my_dog.name)                   # "Rex" — access an attribute
```

## What is `self`?

`self` is the object itself. When you call `my_dog.learn_trick("sit")`, Python translates this to `Dog.learn_trick(my_dog, "sit")`. The `self` parameter receives `my_dog`.

Every method's first parameter must be `self`. You never pass it explicitly — Python does it automatically.

## `__init__` — the constructor

`__init__` runs when you create a new object. It sets up the initial state:

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
            return
        self.balance -= amount
```

## Special methods (dunder methods)

Methods with double underscores have special meaning:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        # Called by print() and str()
        return f"Point({self.x}, {self.y})"

    def __repr__(self):
        # Called in the interactive console and debugger
        return f"Point(x={self.x}, y={self.y})"

    def __eq__(self, other):
        # Called by == operator
        return self.x == other.x and self.y == other.y

p = Point(3, 4)
print(p)              # "Point(3, 4)" — uses __str__
print(p == Point(3, 4))  # True — uses __eq__
```

## Inheritance — building on existing classes

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

animals = [Cat("Whiskers"), Dog("Rex")]
for animal in animals:
    print(animal.speak())
# "Whiskers says Meow!"
# "Rex says Woof!"
```

## When to use classes

**Use a class when:**
- You have data AND behavior that belong together
- You need multiple instances of the same thing
- You want to organize related functions

**Use a plain function when:**
- You just need to do one thing
- There's no state to manage
- A dictionary would work fine for the data

## Common mistakes

**Forgetting `self`:**
```python
class Bad:
    def greet(name):    # Missing self!
        return f"Hello {name}"

b = Bad()
b.greet("Alice")    # TypeError: greet() takes 1 positional argument but 2 were given
```

**Mutable default attributes:**
```python
class Bad:
    def __init__(self, items=[]):    # Shared between ALL instances!
        self.items = items

class Good:
    def __init__(self, items=None):
        self.items = items or []     # Each instance gets its own list
```

## Practice

- [Module 03 / 05 API Client Class](../projects/modules/03-rest-apis/05-api-client-class/)
- [Module 06 Databases & ORM](../projects/modules/06-databases-orm/)
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

**Quick check:** [Take the quiz](quizzes/classes-and-objects-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](how-imports-work.md) | [Home](../README.md) | [Next →](decorators-explained.md) |
|:---|:---:|---:|
