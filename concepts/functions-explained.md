# Functions Explained

A function is a reusable block of code with a name. You define it once, then call it whenever you need it.

## Defining a function

```python
def greet(name):
    return f"Hello, {name}!"
```

- `def` means "I am defining a function"
- `greet` is the name you chose
- `name` is a parameter — a value the function expects to receive
- `return` sends a value back to whoever called the function

## Calling a function

```python
message = greet("Travis")
print(message)  # Hello, Travis!

# Or use it directly
print(greet("Alice"))  # Hello, Alice!
```

## Functions without return

Some functions do something (like printing) but do not return a value:

```python
def say_hello():
    print("Hello!")

say_hello()  # Prints: Hello!
```

If there is no `return`, the function returns `None` automatically.

## Parameters and arguments

**Parameters** are the names in the function definition.
**Arguments** are the values you pass when calling.

```python
def add(a, b):     # a and b are parameters
    return a + b

add(3, 5)          # 3 and 5 are arguments
```

## Default values

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Travis")           # Hello, Travis!
greet("Travis", "Hey")    # Hey, Travis!
```

## Why functions matter

1. **Reuse** — write code once, use it everywhere
2. **Organize** — break big problems into named pieces
3. **Test** — test each piece independently
4. **Read** — `calculate_tax(price)` is clearer than 5 lines of math

## Common mistakes

**Forgetting parentheses when calling:**
```python
greet          # This is the function OBJECT, not a call
greet("Travis") # This CALLS the function
```

**Forgetting to return:**
```python
def add(a, b):
    result = a + b
    # Forgot to return result!

total = add(3, 5)  # total is None, not 8
```

**Defining after calling:**
```python
greet("Travis")    # Error! greet is not defined yet

def greet(name):
    return f"Hello, {name}!"
```

## Related exercises
- [Level 00, Exercise 13 — Functions](../projects/level-00-absolute-beginner/13-functions/)

---

## Practice This

- [Level 0 / 02 Calculator Basics](../projects/level-0/02-calculator-basics/README.md)
- [Level 0 / 03 Temperature Converter](../projects/level-0/03-temperature-converter/README.md)
- [Level 0 / 12 Contact Card Builder](../projects/level-0/12-contact-card-builder/README.md)
- [Level 1 / 01 Input Validator Lab](../projects/level-1/01-input-validator-lab/README.md)
- [Level 1 / 02 Password Strength Checker](../projects/level-1/02-password-strength-checker/README.md)
- [Level 1 / 03 Unit Price Calculator](../projects/level-1/03-unit-price-calculator/README.md)
- [Level 1 / 04 Log Line Parser](../projects/level-1/04-log-line-parser/README.md)
- [Level 1 / 05 Csv First Reader](../projects/level-1/05-csv-first-reader/README.md)
- [Level 1 / 06 Simple Gradebook Engine](../projects/level-1/06-simple-gradebook-engine/README.md)
- [Level 1 / 07 Date Difference Helper](../projects/level-1/07-date-difference-helper/README.md)

**Quick check:** [Take the quiz](quizzes/functions-explained-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](types-and-conversions.md) | [Home](../README.md) | [Next →](../practice/flashcards/README.md) |
|:---|:---:|---:|
