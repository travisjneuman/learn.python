# Reading Documentation

Learning to read documentation is one of the most valuable skills a programmer can develop. The official Python docs at docs.python.org are comprehensive but can be intimidating at first. This page teaches you how to navigate them efficiently so you can answer your own questions faster.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | — | [Quiz](quizzes/reading-documentation-quiz.py) | [Flashcards](../practice/flashcards/README.md) | — |

<!-- modality-hub-end -->

## Why This Matters

No one memorizes every function in Python. Even experienced developers look things up constantly. The difference between a beginner and an expert is often just speed at finding answers in the docs. Learning to read documentation makes you self-sufficient — you stop needing to search for tutorials and Stack Overflow answers for every question.

## Navigating docs.python.org

The Python docs have several sections. Here is where to find things:

| Section | What it contains | When to use it |
|---------|-----------------|----------------|
| **Tutorial** | Step-by-step introduction | Learning a topic for the first time |
| **Library Reference** | Every module in the standard library | Looking up a specific function or module |
| **Language Reference** | How Python syntax works | Understanding `for`, `with`, `class`, etc. |
| **HOWTOs** | Practical guides on specific topics | "How do I do X?" |
| **FAQ** | Common questions and answers | Troubleshooting common issues |

The **Library Reference** is what you will use most. Bookmark it.

## Reading a function signature

Here is a real entry from the docs:

```
str.split(sep=None, maxsplit=-1)
```

Breaking it down:
- `str` — the type this method belongs to (string)
- `.split` — the method name
- `sep=None` — first parameter, defaults to `None` (split on whitespace)
- `maxsplit=-1` — second parameter, defaults to `-1` (no limit)

The defaults tell you what happens when you do not pass an argument:
```python
"hello world foo".split()           # sep=None → split on whitespace: ["hello", "world", "foo"]
"hello-world-foo".split("-")        # sep="-": ["hello", "world", "foo"]
"hello-world-foo".split("-", 1)     # maxsplit=1: ["hello", "world-foo"]
```

## Understanding type annotations in docs

Modern Python docs use type hints:

```
json.loads(s: str | bytes, *, cls=None, ...) -> Any
```

- `s: str | bytes` — the `s` parameter accepts a string or bytes
- `*` — everything after this is keyword-only
- `-> Any` — the return type (in this case, it depends on the JSON)

Common type patterns:
| Notation | Meaning |
|----------|---------|
| `str` | A string |
| `int` | An integer |
| `bool` | True or False |
| `None` | No value / nothing returned |
| `list[str]` | A list of strings |
| `dict[str, int]` | A dict with string keys and integer values |
| `str \| None` | A string or None |
| `Optional[str]` | Same as `str \| None` |
| `Iterable[int]` | Anything you can loop over that yields ints |
| `Callable[[int], str]` | A function taking an int and returning a str |

## Reading module documentation

When you look up a module (like `os.path` or `json`), the page usually has:

1. **Module description** — what the module does
2. **Functions/classes** — listed with signatures and descriptions
3. **Examples** — code showing how to use it
4. **Notes** — edge cases and platform differences
5. **See also** — related modules

**Strategy:** Start with the module description, scan the function list for what you need, then read that specific function's entry. Do not try to read the entire page.

## The help() function

Python has built-in documentation you can access from the REPL:

```python
# Get help on a function:
help(str.split)

# Get help on a module:
import json
help(json)

# Get help on a type:
help(list)
```

`help()` shows the docstring — the same text that appears in the official docs, but right in your terminal.

```python
# Quick signature check with dir():
dir(str)    # Lists all methods on string objects
# ['capitalize', 'casefold', 'center', 'count', 'encode', ...]
```

## Finding what you need

### Strategy 1: Search the docs

Go to docs.python.org and use the search bar. Search for the function name or describe what you want: "read file", "sort list", "parse JSON".

### Strategy 2: "python" + your question

Searching "python read csv file" will usually return the relevant docs page in the first few results.

### Strategy 3: Module index

The docs have a [Global Module Index](https://docs.python.org/3/py-modindex.html) — an alphabetical list of every standard library module. Browse it when you are not sure what module to use.

### Strategy 4: Start from what you know

```python
# You have a string and want to know what you can do with it:
s = "hello"
dir(s)    # Shows all string methods
help(s.replace)    # Read about a specific method
```

## Standard library vs third-party docs

The standard library (modules that ship with Python) is documented at docs.python.org. Third-party packages (installed with pip) have their own documentation sites:

| Package | Docs |
|---------|------|
| requests | docs.python-requests.org |
| Flask | flask.palletsprojects.com |
| FastAPI | fastapi.tiangolo.com |
| pytest | docs.pytest.org |
| SQLAlchemy | docs.sqlalchemy.org |
| pandas | pandas.pydata.org |

Third-party docs vary in quality. Good ones (like requests and FastAPI) have tutorials, API references, and examples. When docs are lacking, look at the project's GitHub README and examples folder.

## Reading error messages as documentation

Error messages are documentation too. They tell you exactly what went wrong:

```python
>>> "hello" + 42
TypeError: can only concatenate str (not "int") to str
```

This tells you:
- **What happened**: `TypeError` — wrong type
- **Why**: you tried to concatenate a str and an int
- **The fix**: convert the int to a string first: `"hello" + str(42)`

See [Reading Error Messages](./reading-error-messages.md) for a deeper dive.

## Common Mistakes

**Skipping the "Parameters" section:**
The parameters section tells you what each argument does, what types it accepts, and what the defaults are. Read it carefully — it often answers your question faster than reading the prose description.

**Not reading the "Raises" section:**
Many functions document which exceptions they raise and when. This tells you what errors to handle:

```
str.index(sub)
    Like find(), but raise ValueError when the substring is not found.
```

**Only reading tutorials, never the reference:**
Tutorials teach concepts but are incomplete. The reference docs are the authoritative source. Once you are past the "learning" phase, go straight to the reference.

## Practice

- Every time you learn a new function, look it up in the official docs
- Use `help()` in the Python REPL before searching the web
- Read the docs for one new standard library module each week

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

## Further Reading

- [The Python Standard Library (docs.python.org)](https://docs.python.org/3/library/)
- [Python Tutorial (docs.python.org)](https://docs.python.org/3/tutorial/)
- [Global Module Index](https://docs.python.org/3/py-modindex.html)

---

| [← Prev](regex-explained.md) | [Home](../README.md) | [Next →](git-basics.md) |
|:---|:---:|---:|
