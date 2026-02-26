# Comprehensions Explained

A comprehension is a one-line way to build a list, dictionary, or set from another sequence. Instead of writing a loop that appends to a list, you describe what you want in a single expression. Comprehensions are one of Python's most distinctive features.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | — | [Quiz](quizzes/comprehensions-explained-quiz.py) | [Flashcards](../practice/flashcards/README.md) | — |

<!-- modality-hub-end -->

## Why This Matters

Comprehensions make your code shorter, faster, and more readable — once you learn the pattern. They show up everywhere in Python: filtering data, transforming lists, building dictionaries from pairs, and more. Understanding them is essential from Level 2 onward.

## Visualize It

Watch a list comprehension build a new list, step by step:
[Open in Python Tutor](https://pythontutor.com/render.html#code=numbers%20%3D%20%5B1%2C%202%2C%203%2C%204%2C%205%5D%0Asquares%20%3D%20%5Bn%20**%202%20for%20n%20in%20numbers%5D%0Aprint%28squares%29%0A%0Aevens%20%3D%20%5Bn%20for%20n%20in%20numbers%20if%20n%20%25%202%20%3D%3D%200%5D%0Aprint%28evens%29&cumulative=false&curInstr=0&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D)

## List comprehensions

The most common type. Creates a new list by transforming each item:

```python
# Without comprehension:
squares = []
for n in range(1, 6):
    squares.append(n ** 2)

# With comprehension — same result:
squares = [n ** 2 for n in range(1, 6)]
# [1, 4, 9, 16, 25]
```

The pattern is: `[expression for variable in iterable]`

Read it as: "give me `expression` for each `variable` in `iterable`."

## Filtering with `if`

Add a condition to include only certain items:

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Only even numbers:
evens = [n for n in numbers if n % 2 == 0]
# [2, 4, 6, 8, 10]

# Only words longer than 3 letters:
words = ["cat", "elephant", "dog", "hippopotamus"]
long_words = [w for w in words if len(w) > 3]
# ["elephant", "hippopotamus"]
```

The pattern is: `[expression for variable in iterable if condition]`

## Transforming and filtering together

```python
# Get uppercase versions of long words:
words = ["cat", "elephant", "dog", "hippopotamus"]
result = [w.upper() for w in words if len(w) > 3]
# ["ELEPHANT", "HIPPOPOTAMUS"]
```

The filter (`if`) decides *which* items to include. The expression (`w.upper()`) decides *what* to produce.

## Dictionary comprehensions

Build a dictionary with `{key: value for ...}`:

```python
# Square each number, store as {number: square}
squares = {n: n ** 2 for n in range(1, 6)}
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Flip a dictionary's keys and values:
original = {"a": 1, "b": 2, "c": 3}
flipped = {v: k for k, v in original.items()}
# {1: "a", 2: "b", 3: "c"}

# Filter a dictionary:
scores = {"Alice": 92, "Bob": 67, "Charlie": 85, "Diana": 58}
passing = {name: score for name, score in scores.items() if score >= 70}
# {"Alice": 92, "Charlie": 85}
```

## Set comprehensions

Build a set (unique values only) with `{expression for ...}`:

```python
words = ["hello", "HELLO", "Hello", "world", "WORLD"]
unique_lower = {w.lower() for w in words}
# {"hello", "world"}
```

Note: sets use `{}` just like dicts, but without the `:`. If there is no colon, Python knows it is a set.

## Generator expressions

Use `()` instead of `[]` to create a generator instead of a list. Generators compute values lazily — one at a time — and use almost no memory:

```python
# List comprehension — builds the whole list:
squares_list = [n ** 2 for n in range(1_000_000)]    # Uses ~8 MB

# Generator expression — computes on demand:
squares_gen = (n ** 2 for n in range(1_000_000))      # Uses ~100 bytes

# Pass directly to functions:
total = sum(n ** 2 for n in range(1_000_000))
```

See [Generators and Iterators](./generators-and-iterators.md) for a deeper dive.

## Nested comprehensions

You can nest loops in a comprehension. The order matches the order you would write them as regular loops:

```python
# Flatten a list of lists:
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Equivalent loop:
flat = []
for row in matrix:
    for num in row:
        flat.append(num)
```

For creating a matrix:

```python
# 3x3 grid of zeros:
grid = [[0 for col in range(3)] for row in range(3)]
# [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
```

## Conditional expressions (`if`/`else` in the expression)

You can use `if`/`else` in the *expression* part (not the filter):

```python
numbers = [1, 2, 3, 4, 5]

# "even" or "odd" label for each number:
labels = ["even" if n % 2 == 0 else "odd" for n in numbers]
# ["odd", "even", "odd", "even", "odd"]
```

Note the position:
- **Filter** (which items): `[x for x in items if condition]` — `if` at the end
- **Transform** (what value): `[a if condition else b for x in items]` — `if/else` before `for`

## The walrus operator `:=` in comprehensions

The walrus operator (`:=`, introduced in Python 3.8) lets you assign and use a value in the same expression. This avoids computing the same thing twice:

```python
# Without walrus — calls len() twice:
data = ["hi", "hello", "hey", "howdy", "h"]
result = [(w, len(w)) for w in data if len(w) > 2]

# With walrus — calls len() once:
result = [(w, length) for w in data if (length := len(w)) > 2]
# [("hello", 5), ("hey", 3), ("howdy", 5)]
```

Another example — filtering and transforming expensive function calls:

```python
import math

values = [1, -2, 3, -4, 5, 0]
# Only include values where the computation succeeds and is positive:
results = [
    y
    for x in values
    if (y := math.sqrt(abs(x))) > 1
]
# [1.414..., 1.732..., 2.0, 2.236...]
```

## When to use comprehensions vs loops

Use a comprehension when:
- You are building a new list/dict/set from an existing sequence
- The logic is simple (one transform, one or two filters)
- The result fits on one line (or two with good formatting)

Use a regular loop when:
- You need side effects (printing, writing files, modifying other data)
- The logic is complex (multiple conditions, nested transforms)
- Readability suffers — if you have to squint to understand it, use a loop

```python
# GOOD — simple and clear:
names = [user.name for user in users if user.is_active]

# BAD — too complex for a comprehension:
result = [
    transform(x, y)
    for x in items
    if validate(x)
    for y in x.children
    if y.status == "ready" and y.score > threshold
]
# Use a loop instead — your future self will thank you.
```

## Common Mistakes

**Confusing filter `if` with conditional expression `if/else`:**
```python
# Filter — decides WHICH items (if at end):
[x for x in range(10) if x > 5]          # [6, 7, 8, 9]

# Transform — decides WHAT value (if/else before for):
[x if x > 5 else 0 for x in range(10)]   # [0, 0, 0, 0, 0, 0, 6, 7, 8, 9]

# WRONG — if/else at end:
[x if x > 5 for x in range(10)]           # SyntaxError!
```

**Forgetting that dict/set use `{}` but empty `{}` is a dict:**
```python
empty_dict = {}      # This is a dict, not a set
empty_set = set()    # Use set() for an empty set
```

**Overusing comprehensions:**
```python
# This is not a comprehension — it is abuse:
[print(x) for x in range(10)]    # Works but creates a useless list of Nones
# Just use a for loop for side effects
```

## Practice

- [Level 0 / 06 Word Counter Basic](../projects/level-0/06-word-counter-basic/README.md)
- [Level 1 / 05 CSV First Reader](../projects/level-1/05-csv-first-reader/README.md)
- [Level 2 / 01 JSON Explorer](../projects/level-2/01-json-explorer/README.md)
- [Module 01 Web Scraping](../projects/modules/01-web-scraping/) — transforming scraped data
- [Module 07 Data Analysis](../projects/modules/07-data-analysis/) — pandas-style filtering

**Quick check:** [Take the quiz](quizzes/comprehensions-explained-quiz.py) *(coming soon)*

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

## Further Reading

- [List comprehensions (Python tutorial)](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- [PEP 274 — Dict Comprehensions](https://peps.python.org/pep-0274/)
- [PEP 572 — Assignment Expressions (:=)](https://peps.python.org/pep-0572/)

---

| [← Prev](generators-and-iterators.md) | [Home](../README.md) | [Next →](functools-and-itertools.md) |
|:---|:---:|---:|
