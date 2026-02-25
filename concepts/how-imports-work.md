# How Imports Work

When your Python file needs code from another file or library, you use `import`.

## Basic import

```python
import math
print(math.sqrt(16))    # 4.0
```

## Import specific things

```python
from math import sqrt, pi
print(sqrt(16))          # 4.0 — no "math." prefix needed
print(pi)                # 3.14159...
```

## Import your own files

If you have two files in the same folder:

```
my_project/
├── main.py
└── helpers.py
```

```python
# helpers.py
def greet(name):
    return f"Hello, {name}!"

# main.py
from helpers import greet
print(greet("Alice"))
```

## Packages — folders of modules

A **package** is a folder that contains Python files and an `__init__.py`:

```
my_package/
├── __init__.py      # Makes this folder a package (can be empty)
├── calculator.py    # A module
└── statistics.py    # Another module
```

```python
from my_package.calculator import add
from my_package import statistics
```

## What `__init__.py` does

`__init__.py` runs when you import the package. It controls what gets exported:

```python
# my_package/__init__.py
from my_package.calculator import add, subtract
from my_package.statistics import mean

# Now users can do:
# from my_package import add, mean
```

Without `__init__.py`, Python does not recognize the folder as a package.

## The import search path

When you write `import something`, Python looks in this order:

1. **Current directory** (the folder your script is in)
2. **Installed packages** (`site-packages/` — things you installed with pip)
3. **Standard library** (modules that come with Python, like `os`, `json`, `math`)

You can see the full search path:

```python
import sys
print(sys.path)
```

## Common patterns

**Alias (rename on import):**
```python
import pandas as pd
import numpy as np
```

**Import everything (avoid this):**
```python
from math import *    # Bad — pollutes your namespace, hard to track what came from where
```

**Conditional import:**
```python
try:
    import ujson as json    # Faster JSON library
except ImportError:
    import json             # Fall back to standard library
```

## Common mistakes

**Circular imports:**
```python
# file_a.py
from file_b import helper_b    # file_b imports from file_a → circular!

# file_b.py
from file_a import helper_a    # Fails with ImportError
```
Fix: restructure so both files import from a third file, or move imports inside functions.

**Naming conflicts:**
```python
# Don't name your file "random.py" — it shadows the built-in random module!
import random    # Imports YOUR random.py instead of Python's
```

**Missing `__init__.py`:**
```python
# If my_package/ has no __init__.py:
from my_package import calculator    # May fail in some Python versions
```

## Related exercises

- [Module 11 — Package Publishing](../projects/modules/11-package-publishing/) (creating packages)
- [Level 01 projects](../projects/level-1/) (using imports in projects)

---

## Practice This

- [Level 0 / 15 Level0 Mini Toolkit](../projects/level-0/15-level0-mini-toolkit/README.md)
- [Level 1 / 01 Input Validator Lab](../projects/level-1/01-input-validator-lab/README.md)
- [Level 1 / 02 Password Strength Checker](../projects/level-1/02-password-strength-checker/README.md)
- [Level 1 / 03 Unit Price Calculator](../projects/level-1/03-unit-price-calculator/README.md)
- [Level 1 / 04 Log Line Parser](../projects/level-1/04-log-line-parser/README.md)
- [Level 1 / 05 Csv First Reader](../projects/level-1/05-csv-first-reader/README.md)
- [Level 1 / 06 Simple Gradebook Engine](../projects/level-1/06-simple-gradebook-engine/README.md)
- [Level 1 / 07 Date Difference Helper](../projects/level-1/07-date-difference-helper/README.md)
- [Level 1 / 08 Path Exists Checker](../projects/level-1/08-path-exists-checker/README.md)
- [Level 1 / 09 Json Settings Loader](../projects/level-1/09-json-settings-loader/README.md)

**Quick check:** [Take the quiz](quizzes/how-imports-work-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)
