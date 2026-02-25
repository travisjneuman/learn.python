# Reading Error Messages

Error messages are Python's way of telling you exactly what went wrong and where. This guide teaches you how to decode them.

## Anatomy of a traceback

```
Traceback (most recent call last):
  File "app.py", line 12, in main
    result = process(data)
  File "app.py", line 7, in process
    return data["name"].upper()
TypeError: 'NoneType' object has no attribute 'upper'
```

Read a traceback **bottom to top**:

1. **Last line** -- the error type and message: `TypeError: 'NoneType' object has no attribute 'upper'`
2. **Lines above** -- the call stack, showing each function that was called. The bottom frame is where it actually broke.
3. **File and line number** -- tells you exactly where to look: `File "app.py", line 7`
4. **Code snippet** -- the exact line that failed: `return data["name"].upper()`

The call stack shows the path Python took to reach the error. In this example: `main()` called `process()`, and `process()` broke on line 7.

## The 10 most common errors

### 1. SyntaxError -- Python cannot parse your code

```python
# Missing colon
if x > 5
    print("big")
```

```
  File "script.py", line 1
    if x > 5
           ^
SyntaxError: expected ':'
```

**What it means:** Your code has a grammar mistake. Python could not even begin running it.
**Common causes:** Missing colons, unmatched parentheses/quotes, typos in keywords.

### 2. NameError -- a name does not exist

```python
print(username)
```

```
NameError: name 'username' is not defined
```

**What it means:** You used a name Python has never seen. It does not exist in the current scope.
**Common causes:** Typos in variable names, using a variable before defining it, forgetting an import.

### 3. TypeError -- wrong type for the operation

```python
age = 25
print("Age: " + age)
```

```
TypeError: can only concatenate str (not "int") to str
```

**What it means:** You tried to do something with the wrong type of value.
**Common causes:** Adding strings and numbers, calling something that is not a function, wrong number of arguments.

### 4. ValueError -- right type, wrong value

```python
number = int("hello")
```

```
ValueError: invalid literal for int() with base 10: 'hello'
```

**What it means:** The type is correct (it is a string), but the specific value cannot be used.
**Common causes:** Converting non-numeric strings to numbers, unpacking the wrong number of values.

### 5. IndexError -- list index out of range

```python
items = ["a", "b", "c"]
print(items[5])
```

```
IndexError: list index out of range
```

**What it means:** You asked for a position that does not exist in the list.
**Common causes:** Off-by-one errors, looping past the end, empty lists.

### 6. KeyError -- dict key does not exist

```python
person = {"name": "Alice"}
print(person["email"])
```

```
KeyError: 'email'
```

**What it means:** You asked for a dictionary key that is not there.
**Fix:** Use `.get("email")` for safe access, or check with `if "email" in person:` first.

### 7. AttributeError -- object does not have that attribute

```python
name = None
print(name.upper())
```

```
AttributeError: 'NoneType' object has no attribute 'upper'
```

**What it means:** You tried to access a method or property that does not exist on this type.
**Common causes:** Calling methods on `None` (a function returned nothing), typos in method names.

### 8. ImportError / ModuleNotFoundError -- cannot find the module

```python
import pandas
```

```
ModuleNotFoundError: No module named 'pandas'
```

**What it means:** Python cannot find the module you are trying to import.
**Common causes:** Package not installed (`pip install pandas`), wrong virtual environment, file named the same as a module.

### 9. FileNotFoundError -- file does not exist

```python
with open("data.csv") as f:
    data = f.read()
```

```
FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'
```

**What it means:** The file path you gave does not point to an existing file.
**Common causes:** Wrong filename, wrong directory, typo in the path.

### 10. IndentationError -- inconsistent indentation

```python
def greet():
print("hello")
```

```
IndentationError: expected an indented block after function definition on line 1
```

**What it means:** Python expected indented code but found something at the wrong level.
**Common causes:** Missing indentation after `if`/`for`/`def`/`class`, mixing tabs and spaces.

## How to read each part of a traceback

```
Traceback (most recent call last):       ← Start of the call chain
  File "main.py", line 15, in <module>   ← Which file, which line, which scope
    run()                                 ← The code on that line
  File "main.py", line 10, in run        ← One level deeper
    total = add_prices(items)             ← The code that called the next level
  File "main.py", line 5, in add_prices  ← Where it actually broke
    total += item["price"]               ← The exact failing line
KeyError: 'price'                        ← What went wrong (THE ANSWER)
```

**Step-by-step reading process:**

1. Look at the **very last line** -- this is the error type and message
2. Look at the **frame just above** -- this is where the error actually happened
3. Note the **file name and line number** -- open your file and go to that line
4. Read the **code snippet** -- does the code match what you expected?
5. If needed, trace **upward** through the call stack to understand how you got there

## The `friendly` library

The `friendly` library rewrites Python error messages in plain English:

```bash
pip install friendly
```

```python
# Instead of running: python script.py
# Run: python -m friendly script.py
```

It turns cryptic messages into explanations like:

```
A NameError exception indicates that a variable or function name
is not known to Python. Most often, this is because there is a
spelling mistake. However, sometimes it is because the name is
used before being defined or given a value.

Did you mean 'username'?
```

This is especially helpful while you are still learning to read tracebacks on your own.

---

## Practice

- [Level 00 / 08 Making Decisions](../projects/level-00-absolute-beginner/08-making-decisions/)
- [Level 00 / 15 Putting It Together](../projects/level-00-absolute-beginner/15-putting-it-together/)
- [Level 0 / 07 First File Reader](../projects/level-0/07-first-file-reader/README.md)
- [Level 1 / 01 Input Validator Lab](../projects/level-1/01-input-validator-lab/README.md)
- [Level 2 / 04 Error Safe Divider](../projects/level-2/04-error-safe-divider/README.md)
- [Level 2 / 11 Retry Loop Practice](../projects/level-2/11-retry-loop-practice/README.md)

**Quick check:** [Take the quiz](quizzes/reading-error-messages-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](errors-and-debugging.md) | [Home](../README.md) | [Next →](the-terminal-deeper.md) |
|:---|:---:|---:|
