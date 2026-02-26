# Modern Python Tooling

The Python ecosystem has modernized significantly. This page covers **uv**, **ruff**, and the shift away from the older pip/venv/black/flake8 toolchain.

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | — | [Quiz](quizzes/modern-python-tooling-quiz.py) | [Flashcards](../practice/flashcards/README.md) | — |

<!-- modality-hub-end -->

## uv — the fast Python package manager

**uv** is a single tool that replaces pip, venv, pip-tools, and pyenv. It is written in Rust, and it is extremely fast — often 10-100x faster than pip.

### Installing uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip (works everywhere)
pip install uv
```

### Creating a project with uv

```bash
# Create a virtual environment (replaces python -m venv .venv)
uv venv

# Activate it — same as before
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows Git Bash:
source .venv/Scripts/activate

# Install packages (replaces pip install)
uv pip install requests flask pytest

# Install from requirements file (replaces pip install -r)
uv pip install -r requirements.txt

# Save dependencies (replaces pip freeze)
uv pip freeze > requirements.txt
```

### The uv workflow

```bash
# 1. Create project folder.
mkdir my_project && cd my_project

# 2. Create virtual environment.
uv venv

# 3. Activate it.
source .venv/bin/activate    # or .venv\Scripts\Activate.ps1 on Windows

# 4. Install packages.
uv pip install requests pytest

# 5. Save dependencies.
uv pip freeze > requirements.txt

# 6. Work on your project...

# 7. When done, deactivate.
deactivate
```

Notice this is almost identical to the pip workflow — just replace `pip` with `uv pip` and `python -m venv` with `uv venv`.

### Why uv over pip?

| Feature | pip | uv |
|---------|-----|----|
| Install speed | Slow (downloads sequentially) | Fast (parallel, cached) |
| Dependency resolution | Basic | Advanced (like cargo/npm) |
| Virtual environments | Separate tool (`python -m venv`) | Built-in (`uv venv`) |
| Lock files | No (need pip-tools) | Built-in (`uv lock`) |
| Python version management | No (need pyenv) | Built-in (`uv python`) |

### If you prefer pip

All `uv pip` commands have pip equivalents. If uv is not available on your machine, replace:

```bash
uv venv          →  python -m venv .venv
uv pip install X  →  pip install X
uv pip freeze     →  pip freeze
```

The rest of the workflow stays the same.

## ruff — the fast linter and formatter

**ruff** replaces flake8 (linter), black (formatter), and isort (import sorter) in a single tool.

### Installing ruff

```bash
uv pip install ruff
# or
pip install ruff
```

### Using ruff

```bash
# Check for problems (replaces flake8)
ruff check .

# Fix problems automatically
ruff check . --fix

# Format code (replaces black)
ruff format .

# Check formatting without changing files
ruff format . --check
```

### Example

```python
# before.py — has issues
import os
import sys
import os  # duplicate import
x=1  # missing spaces

def greet(name ):  # extra space
    print( f"Hello, {name}" )
```

```bash
$ ruff check before.py
before.py:3:1: F811 Redefinition of unused `os` from line 1

$ ruff check before.py --fix
Found 1 error (1 fixed, 0 remaining).

$ ruff format before.py
1 file reformatted.
```

After:
```python
# before.py — cleaned up
import os
import sys

x = 1


def greet(name):
    print(f"Hello, {name}")
```

### Configuring ruff

Add to `pyproject.toml` (the modern Python config file):

```toml
[tool.ruff]
line-length = 88  # Same as black default

[tool.ruff.lint]
select = ["E", "F", "I"]  # Errors, pyflakes, isort
```

## pyproject.toml — the modern config file

Modern Python projects use `pyproject.toml` instead of `setup.py`, `setup.cfg`, and separate config files:

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31",
    "flask>=3.0",
]

[tool.ruff]
line-length = 88

[tool.pytest.ini_options]
testpaths = ["tests"]
```

One file, all configuration. No more scattered config files.

## The modern Python toolchain

| Old tool | Modern replacement | Why |
|----------|-------------------|-----|
| `pip` | `uv pip` | 10-100x faster, better dependency resolution |
| `python -m venv` | `uv venv` | Faster, bundled with uv |
| `pyenv` | `uv python` | Manages Python versions |
| `pip-tools` | `uv lock` | Lockfiles for reproducible installs |
| `flake8` | `ruff check` | 10-100x faster, more rules |
| `black` | `ruff format` | Same style, faster |
| `isort` | `ruff check --select I` | Included in ruff |
| `setup.py` | `pyproject.toml` | Standard, declarative |

You do not need to adopt everything at once. Start with `uv` for package management, add `ruff` for linting, and switch to `pyproject.toml` when you create your own packages.

## Python 3.11–3.14 highlights

Recent Python releases have brought significant quality-of-life improvements.

### Better error messages (3.11+)

Python 3.11 points directly to the exact expression that caused an error:

```
Traceback (most recent call last):
  File "example.py", line 3, in <module>
    result = data["users"][0]["email"]
                               ^^^^^^^
KeyError: 'email'
```

Before 3.11, you would only get the line number — now Python underlines the exact problematic expression.

### `f"{x=}"` debugging (3.8+)

Add `=` inside an f-string to print both the variable name and its value:

```python
x = 42
name = "Alice"
items = [1, 2, 3]

print(f"{x=}")            # x=42
print(f"{name=}")         # name='Alice'
print(f"{len(items)=}")   # len(items)=3
```

### `tomllib` — built-in TOML parser (3.11+)

Read `pyproject.toml` and other TOML files without a third-party library:

```python
import tomllib

with open("pyproject.toml", "rb") as f:
    config = tomllib.load(f)

print(config["project"]["name"])
```

### `StrEnum` (3.11+)

Enum members that behave like strings — no need for `.value`:

```python
from enum import StrEnum

class Color(StrEnum):
    RED = "red"
    BLUE = "blue"

print(Color.RED == "red")    # True
print(f"Color is {Color.RED}")    # "Color is red"
```

See [Enums Explained](./enums-explained.md) for more.

### `pip audit` — dependency vulnerability scanning

Check your installed packages for known security vulnerabilities:

```bash
pip install pip-audit
pip audit
```

### New interactive REPL (3.13+)

Python 3.13 introduces an improved REPL with:
- Multi-line editing with proper indentation
- Color-coded output
- Paste mode for multi-line code blocks
- History search with Ctrl+R

### Exception groups and `except*` (3.11+)

Handle multiple exceptions raised simultaneously (useful for async code):

```python
try:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(task1())
        tg.create_task(task2())
except* ValueError as eg:
    print(f"Value errors: {eg.exceptions}")
except* TypeError as eg:
    print(f"Type errors: {eg.exceptions}")
```

## Common mistakes

**Mixing pip and uv in the same environment:**
Pick one and stick with it. Both write to the same `.venv/`, so they are compatible, but mixing them can cause confusion about what is installed.

**Forgetting to activate the environment:**
```bash
uv pip install requests    # Installs into .venv, but...
python my_script.py        # ...might use system Python if .venv is not activated!
```

Always check for `(.venv)` in your prompt.

**Running ruff without saving first:**
ruff reads files from disk, not your editor buffer. Save before running `ruff check`.

## Related concepts

- [Virtual Environments](./virtual-environments.md) — deeper dive into venv concepts
- [How Imports Work](./how-imports-work.md) — understanding the module system

---

## Practice

- [03 Setup All Platforms](../03_SETUP_ALL_PLATFORMS.md) (setup uses uv)
- [Level 0 projects](../projects/level-0/) (first projects with the toolchain)
- [Level 3 / 10 Dependency Boundary Lab](../projects/level-3/10-dependency-boundary-lab/README.md)

**Quick check:** Take the Virtual Environments quiz — it covers package management too: [Take the quiz](quizzes/virtual-environments-quiz.py)

**Review:** [Flashcard decks](../practice/flashcards/README.md)
**Practice reps:** [Coding challenges](../practice/challenges/README.md)

---

| [← Prev](match-case-explained.md) | [Home](../README.md) | [Next →](../04_FOUNDATIONS.md) |
|:---|:---:|---:|
