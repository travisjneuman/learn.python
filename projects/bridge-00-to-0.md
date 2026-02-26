# Bridge Exercise: Level 00 to Level 0

You have completed Level 00. You can write Python scripts, use variables, loops, and functions. Now you are about to enter Level 0, where two new things appear: **pytest** (automated testing) and **functions that return values**.

This bridge exercise introduces both concepts gently before you dive into the full projects.

---

## What Changes in Level 0

In Level 00, you wrote scripts and checked the output by eye. In Level 0, you will write **functions** that return values, and **pytest** will check those values automatically.

Here is the key shift:

```python
# Level 00 style: print and check manually
def greet(name):
    print(f"Hello, {name}!")

greet("Ada")  # You look at the terminal to see if it is right
```

```python
# Level 0 style: return values so tests can check
def greet(name):
    return f"Hello, {name}!"

# A test can now verify the result automatically
assert greet("Ada") == "Hello, Ada!"
```

The difference: `print()` shows output to you. `return` gives output back to the code that called the function. Tests need `return` because they compare the result to an expected value.

---

## Exercise: Your First Tested Function

### Step 1: Write the function

Create a file called `bridge_00.py` with this content:

```python
def double(n):
    """Return the input number multiplied by 2."""
    return n * 2
```

That is the entire file. No `print()`, no `input()`, no `if __name__`. Just a function that takes a number and returns it doubled.

### Step 2: Test it manually in the Python shell

Open a terminal and type:

```bash
python -c "from bridge_00 import double; print(double(5))"
```

You should see `10`.

### Step 3: Write a test file

Create a file called `test_bridge_00.py` in the same folder:

```python
from bridge_00 import double


def test_double_positive():
    assert double(5) == 10


def test_double_zero():
    assert double(0) == 0


def test_double_negative():
    assert double(-3) == -6
```

**What is happening here:**
- `from bridge_00 import double` loads your function from `bridge_00.py`.
- Each function starting with `test_` is a test case that pytest will find and run.
- `assert` checks that the expression is `True`. If it is `False`, the test fails.

### Step 4: Run pytest

```bash
pytest test_bridge_00.py -v
```

You should see:

```text
test_bridge_00.py::test_double_positive PASSED
test_bridge_00.py::test_double_zero PASSED
test_bridge_00.py::test_double_negative PASSED
```

Congratulations. You just wrote and ran your first automated tests.

### Step 5: Break it on purpose

Change your `double` function to return `n * 3` instead. Run pytest again. Read the failure message. It tells you exactly what was expected and what it got. Change it back to `n * 2` and confirm the tests pass again.

---

## Challenge: Write Your Own

Write a function called `is_even(n)` that returns `True` if `n` is even, `False` if odd. Then write three test cases for it. Run pytest and make sure they all pass.

**Hint:** The `%` operator gives you the remainder of division. `10 % 2` is `0` (even), `7 % 2` is `1` (odd).

---

## You Are Ready

If you can write a function that returns a value, import it in a test file, and run pytest, you are ready for Level 0. Every project from here on uses this pattern.

---

| [Level 00 Projects](level-00-absolute-beginner/README.md) | [Home](../README.md) | [Level 0 Projects](level-0/README.md) |
|:---|:---:|---:|
