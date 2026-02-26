# Exercise 01 — Mystery Function

Open `codebase.py`. Read it carefully. Do NOT run it yet.

## Tasks

### 1. What does this code do?

Read all four functions. In your own words, describe:
- What does `transform()` do? What role does `key` play?
- What does `analyze()` compute? What does the return value represent?
- What is `REFERENCE` and why does it exist?
- What does `score()` measure?
- What does `solve()` do, and how does it use the other three functions?
- What is the overall purpose of this module?

Write your answers in a file called `my_answers.md` before continuing.

### 2. Trace through with real input

Without running the code, trace through these calls by hand:

```python
transform("Hello", 3)
transform("Khoor", -3)
analyze("aabbbc")
```

Write down what you expect each call to return. Then run Python and check.

### 3. What would happen if...

Answer these questions by reasoning about the code, then verify:

- What does `transform("Hello!", 0)` return? Why?
- What does `transform("Hello", 26)` return? Why?
- What does `transform("Hello", -1)` return?
- What happens if you call `analyze("")`?
- What happens if `solve()` receives text that is not actually encrypted?

### 4. Add docstrings

Write a clear docstring for each of the four functions. A good docstring explains what the function does, what its parameters mean, and what it returns.

### 5. Write tests

Write at least 3 tests for this module in a file called `test_codebase.py`:
- A test that verifies `transform` with a known input/output pair
- A test that verifies `transform` is reversible (encrypt then decrypt returns original)
- A test that verifies `solve` can crack a known encrypted message

## What you are practicing

- Reading unfamiliar code and inferring its purpose
- Mental execution (tracing code without running it)
- Reasoning about edge cases
- Writing documentation for existing code
- Writing tests for existing code
