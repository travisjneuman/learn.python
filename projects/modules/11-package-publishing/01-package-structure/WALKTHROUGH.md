# Package Structure — Step-by-Step Walkthrough

[<- Back to Project README](./README.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 20 minutes attempting it independently. The goal is to understand the `src` layout for Python packages, the role of `pyproject.toml`, and how `__init__.py` controls imports. If you can run `python -m mymath.calculator` and see the output, you are on the right track.

## Thinking Process

Every Python project you have written so far has been a script — a single file (or a few files) that you run directly. A package is different: it is a library that other people install with `pip install` and import in their own code. The transition from "script that runs" to "package that others can install" requires a specific file structure and configuration.

The `src` layout puts your package code inside a `src/` directory. This prevents a common bug where tests accidentally import the local source code instead of the installed package. When your code is in `src/mymath/`, you cannot accidentally `import mymath` from the project root — you must install the package first. This catches import errors early.

`pyproject.toml` is the single source of truth for your package. It tells build tools the package name, version, dependencies, where to find the code, and how to build it. Before `pyproject.toml` existed, Python packaging required `setup.py`, `setup.cfg`, and sometimes `MANIFEST.in`. Now everything goes in one file.

## Step 1: Understand the src Layout

**What to do:** Examine the directory structure of this project.

**Why:** The file structure is the foundation of a Python package. Every file and directory has a specific purpose. Getting this wrong means your package cannot be installed or imported.

```
01-package-structure/
├── pyproject.toml         # Package metadata and build config
├── README.md              # Rendered on PyPI
├── LICENSE                # MIT license
├── src/
│   └── mymath/
│       ├── __init__.py    # Makes mymath a package, exports version
│       ├── calculator.py  # Core math functions
│       └── statistics.py  # Mean, median, mode functions
└── tests/
    ├── test_calculator.py
    └── test_statistics.py
```

Three directories to understand:

- **`src/mymath/`** — the actual package code. The directory name `mymath` becomes the import name.
- **`tests/`** — test files live outside the package so they are not included in the distribution.
- **Root directory** — contains `pyproject.toml`, README, and LICENSE, which are metadata, not code.

**Predict:** What happens if you rename the `mymath/` directory to `my_math/`? What would need to change in the rest of the project?

## Step 2: Understand __init__.py

**What to do:** Read `src/mymath/__init__.py` and understand what it does when someone writes `import mymath`.

**Why:** `__init__.py` serves two purposes. First, it marks the directory as a Python package (without it, `import mymath` fails). Second, it controls what is available when someone imports the package. By importing key functions here, users can write `from mymath import add` instead of the longer `from mymath.calculator import add`.

```python
__version__ = "0.1.0"

from mymath.calculator import add, subtract, multiply, divide
from mymath.statistics import mean, median, mode
```

Three things this file does:

- **Sets `__version__`** — a single source of truth for the package version that tools can read.
- **Re-exports functions** from submodules — `from mymath import add` works because `__init__.py` imports `add` from `calculator.py`.
- **Exists as a file** — its mere presence tells Python "this directory is a package."

**Predict:** If you remove the `from mymath.calculator import ...` line, can you still use `from mymath.calculator import add`? What about `from mymath import add`?

## Step 3: Write a Module with Functions

**What to do:** Examine `calculator.py` and `statistics.py` — the two modules inside the package.

**Why:** A module is a single `.py` file. A package is a directory containing modules (plus `__init__.py`). Each module should have a focused purpose. `calculator.py` does arithmetic. `statistics.py` does statistics. This separation makes the code easier to navigate and test.

```python
# calculator.py
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b
```

```python
# statistics.py
from collections import Counter

def mean(numbers):
    if not numbers:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(numbers) / len(numbers)

def mode(numbers):
    if not numbers:
        raise ValueError("Cannot calculate mode of empty list")
    counts = Counter(numbers)
    return counts.most_common(1)[0][0]
```

Both modules validate their inputs (empty lists, division by zero) and raise clear errors. This is good practice for any library code — the caller should get a useful error message, not a cryptic traceback.

**Predict:** Why does `calculator.py` have a `main()` function and an `if __name__ == "__main__"` guard? What does `python -m mymath.calculator` do?

## Step 4: Configure pyproject.toml

**What to do:** Read `pyproject.toml` and understand each section.

**Why:** `pyproject.toml` is the configuration file that build tools read to create an installable package. Without it, `pip install .` does not know the package name, version, or where to find the code.

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mymath-demo"
version = "0.1.0"
description = "A simple math utilities package"
requires-python = ">=3.10"
dependencies = []

[tool.setuptools.packages.find]
where = ["src"]
```

Three sections to understand:

- **`[build-system]`** — tells pip which tool builds the package (setuptools is the most common).
- **`[project]`** — the metadata that appears on PyPI: name, version, description, author.
- **`[tool.setuptools.packages.find]`** — tells setuptools to look in the `src/` directory for packages.

**Predict:** What happens if you change `where = ["src"]` to `where = ["."]`? Where would setuptools look for packages?

## Step 5: Run the Package as a Module

**What to do:** Run the calculator module directly and verify the output.

**Why:** The `if __name__ == "__main__"` guard in `calculator.py` lets you run the file as a script with `python -m mymath.calculator`. The `-m` flag tells Python to find the module inside the package and execute it. This is useful for demos, CLIs, and quick testing.

```bash
python -m mymath.calculator
```

Expected output:
```text
mymath calculator v0.1.0
add(2, 3) = 5
subtract(10, 4) = 6
multiply(3, 7) = 21
divide(15, 4) = 3.75
```

**Predict:** What is the difference between `python calculator.py` and `python -m mymath.calculator`? Which one uses the package's import system?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| `ModuleNotFoundError: No module named 'mymath'` | Package not installed or wrong directory | Run from project root, or `pip install -e .` for editable install |
| Deleting `__init__.py` breaks imports | It marks the directory as a package | Always include `__init__.py`, even if empty |
| Tests import wrong version of code | Flat layout imports local code, not installed | Use `src` layout to force importing the installed version |
| Version number out of sync | Version in multiple places | Keep `__version__` in `__init__.py` as the single source of truth |

## Testing Your Solution

Run the tests:

```bash
pytest tests/ -v
```

Expected output:
```text
tests/test_calculator.py::test_add PASSED
tests/test_calculator.py::test_subtract PASSED
tests/test_calculator.py::test_multiply PASSED
tests/test_calculator.py::test_divide PASSED
tests/test_calculator.py::test_divide_by_zero PASSED
tests/test_statistics.py::test_mean PASSED
tests/test_statistics.py::test_median PASSED
tests/test_statistics.py::test_mode PASSED
...
```

Also verify the module runs directly:
```bash
python -m mymath.calculator
```

## What You Learned

- **The `src` layout** puts package code in `src/<package>/`, preventing accidental imports of local code instead of the installed package.
- **`__init__.py`** marks a directory as a Python package and controls what is importable — re-exporting functions from submodules creates a clean public API.
- **`pyproject.toml`** is the single configuration file for package metadata, build system, and tool settings — it replaces the older `setup.py` approach.
- **Modules vs packages** — a module is a single `.py` file, a package is a directory with `__init__.py` and one or more modules. Packages can be installed with pip and imported by anyone.
