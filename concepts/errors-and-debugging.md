# Errors and Debugging

> **Try This First:** Before reading, try running `print(1/0)` in Python. What happens? Read the error message -- it tells you exactly what went wrong.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | [Videos](videos/errors-and-debugging.md) | [Quiz](quizzes/errors-and-debugging-quiz.py) | [Flashcards](../practice/flashcards/README.md) | [Diagrams](diagrams/errors-and-debugging.md) |

<!-- modality-hub-end -->

Errors are not failures. They are Python telling you exactly what went wrong and where. Learning to read error messages is one of the most valuable skills in programming.

## Visualize It

See what happens when Python hits an error — watch the execution stop:
[Open in Python Tutor](https://pythontutor.com/render.html#code=x%20%3D%2010%0Ay%20%3D%200%0Aprint%28%22before%22%29%0Aresult%20%3D%20x%20%2F%20y%0Aprint%28%22after%22%29&cumulative=false&curInstr=0&mode=display&origin=opt-frontend.js&py=3&rawInputLstJSON=%5B%5D)

## Anatomy of an error message

```
Traceback (most recent call last):
  File "exercise.py", line 5, in <module>
    print(score)
NameError: name 'score' is not defined
```

Read it bottom-up:
1. **`NameError: name 'score' is not defined`** — what went wrong
2. **`File "exercise.py", line 5`** — where it happened
3. **`print(score)`** — the exact line that caused it

## Common error types

| Error | Meaning | Example |
|-------|---------|---------|
| `SyntaxError` | Python cannot understand your code | Missing colon, unmatched quotes |
| `NameError` | You used a name that does not exist | Typo in variable name |
| `TypeError` | Wrong type for the operation | Adding a string and a number |
| `IndexError` | List index out of range | `my_list[99]` when list has 5 items |
| `KeyError` | Dict key does not exist | `my_dict["missing_key"]` |
| `FileNotFoundError` | File does not exist at that path | Wrong filename or directory |
| `ValueError` | Right type but wrong value | `int("hello")` |
| `IndentationError` | Indentation is inconsistent | Mixed tabs and spaces |

## Debugging strategy

When something goes wrong:

1. **Read the error message.** It usually tells you exactly what happened.
2. **Look at the line number.** Go to that line in your file.
3. **Check spelling.** Typos in variable names cause `NameError`.
4. **Print things.** Add `print(variable_name)` before the error line to see what values actually are.
5. **Simplify.** Remove code until you find the smallest version that still breaks.

## The print() debugging method

The simplest debugging technique: print values to see what is happening.

```python
data = load_file("input.txt")
print("data is:", data)          # What did we actually load?
print("type is:", type(data))    # Is it a list? a string? None?
print("length is:", len(data))   # How many items?

for item in data:
    print("processing:", item)   # See each item as it is processed
```

## Common mistakes and fixes

**SyntaxError — missing colon:**
```python
if x > 5       # Missing colon!
    print("big")

if x > 5:      # Fixed
    print("big")
```

**TypeError — mixing strings and numbers:**
```python
age = 30
print("I am " + age)           # Error! Cannot add string + int
print("I am " + str(age))      # Fixed with str()
print(f"I am {age}")           # Better — use f-string
```

**IndentationError:**
```python
if True:
print("hello")     # Error! Must be indented

if True:
    print("hello") # Fixed — 4 spaces of indentation
```

## Top 5 beginner mistakes

These five mistakes account for the vast majority of errors new programmers hit. Learning to spot them quickly will save you hours of frustration.

### 1. IndentationError — your code is not lined up

Python uses indentation (spaces at the start of a line) to know which code belongs inside an `if`, `for`, or function. If the spacing is off, Python refuses to run your code at all.

**The error message:**
```
IndentationError: expected an indented block after 'if' statement on line 1
```

**Broken code:**
```python
if temperature > 100:
print("Too hot!")        # Not indented — Python does not know this belongs to the if
```

**The fix:**
```python
if temperature > 100:
    print("Too hot!")    # 4 spaces in — now Python knows this is inside the if
```

**Why it happens:** Unlike most languages, Python does not use curly braces `{}` to group code. It uses indentation instead. Every line inside an `if`, `for`, `while`, or `def` must be indented by the same amount (use 4 spaces — not tabs).

---

### 2. NameError — Python does not recognize a name

This usually means you misspelled a variable name, or you tried to use a variable before creating it.

**The error message:**
```
NameError: name 'mesage' is not defined
```

**Broken code:**
```python
message = "Hello there"
print(mesage)            # Typo! "mesage" instead of "message"
```

**The fix:**
```python
message = "Hello there"
print(message)           # Spelling matches — Python finds the variable
```

**Why it happens:** Python is case-sensitive and spelling-sensitive. `message`, `Message`, and `mesage` are three completely different names. Python only knows about names you have already created on a previous line.

---

### 3. SyntaxError — missing colon after if/for/while/def

Every `if`, `elif`, `else`, `for`, `while`, and `def` line must end with a colon `:`. Forget it, and Python cannot understand your code.

**The error message:**
```
SyntaxError: expected ':'
```

**Broken code:**
```python
for name in guest_list
    print(name)
```

**The fix:**
```python
for name in guest_list:   # Colon at the end
    print(name)
```

**Why it happens:** The colon tells Python "the next indented block belongs to this statement." Without it, Python sees an incomplete line and does not know what you meant. This is easy to forget because colons do not exist in everyday writing the same way.

---

### 4. SyntaxError — mismatched parentheses or brackets

Every opening `(`, `[`, or `{` needs a matching closing `)`, `]`, or `}`. Miss one and Python gets confused, sometimes pointing to a line that looks perfectly fine.

**The error message:**
```
SyntaxError: unexpected EOF while parsing
```

**Broken code:**
```python
scores = [90, 85, 77, 92
print(scores)            # Python is still looking for the closing ]
```

**The fix:**
```python
scores = [90, 85, 77, 92]
print(scores)            # Now the list is properly closed
```

**Why it happens:** Python reads your code from top to bottom. When it sees `[`, it expects everything until `]` to be part of the list. Without the closing bracket, it keeps reading into the next line and gets confused. The error message often points to a different line than where the real problem is, so check the lines *above* where Python complains.

**Tip:** Most code editors highlight matching brackets. If you place your cursor next to a `(` and its partner does not light up, that is your clue.

---

### 5. TypeError — forgetting to convert types

Python will not automatically turn a number into a string or vice versa. If you try to combine them, you get a `TypeError`.

**The error message:**
```
TypeError: can only concatenate str (not "int") to str
```

**Broken code:**
```python
age = 25
print("I am " + age + " years old")   # Cannot glue a string and an integer
```

**The fix (three ways):**
```python
age = 25

# Option 1 — convert with str()
print("I am " + str(age) + " years old")

# Option 2 — f-string (recommended, cleanest)
print(f"I am {age} years old")

# Option 3 — comma in print (adds spaces automatically)
print("I am", age, "years old")
```

**Why it happens:** Python keeps types strict on purpose. A number `25` and the text `"25"` look the same to us, but Python stores them differently. Requiring you to convert explicitly prevents subtle bugs — for example, `"2" + "5"` gives `"25"` (text joined together), while `2 + 5` gives `7` (math). Python wants you to be clear about which one you mean.

## Practice

- [Level 00 / 08 Making Decisions](../projects/level-00-absolute-beginner/08-making-decisions/)
- [Level 00 / 14 Reading Files](../projects/level-00-absolute-beginner/14-reading-files/)
- [Level 00 / 15 Putting It Together](../projects/level-00-absolute-beginner/15-putting-it-together/)
- [Level 0 / 07 First File Reader](../projects/level-0/07-first-file-reader/README.md)
- [Level 1 / 01 Input Validator Lab](../projects/level-1/01-input-validator-lab/README.md)
- [Level 1 / 08 Path Exists Checker](../projects/level-1/08-path-exists-checker/README.md)
- [Level 1 / 11 Command Dispatcher](../projects/level-1/11-command-dispatcher/README.md)
- [Level 2 / 04 Error Safe Divider](../projects/level-2/04-error-safe-divider/README.md)
- [Level 2 / 11 Retry Loop Practice](../projects/level-2/11-retry-loop-practice/README.md)

**Quick check:** [Take the quiz](quizzes/errors-and-debugging-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](../09_QUALITY_TOOLING.md) | [Home](../README.md) | [Next →](the-terminal-deeper.md) |
|:---|:---:|---:|
