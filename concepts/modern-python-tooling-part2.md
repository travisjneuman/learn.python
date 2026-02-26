# Modern Python Tooling — Part 2: pyproject.toml, Ecosystem, and Python Version Highlights

[← Part 1: uv and ruff](./modern-python-tooling-part1.md) · [Back to Overview](./modern-python-tooling.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | — | — | [Flashcards](../practice/flashcards/README.md) | — |

<!-- modality-hub-end -->

---

This part covers the modern config file (`pyproject.toml`), the old-to-new toolchain mapping, and quality-of-life improvements in recent Python releases.

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

## Python 3.11-3.14 highlights

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

---

| [← Part 1: uv and ruff](./modern-python-tooling-part1.md) | [Overview](./modern-python-tooling.md) |
|:---|---:|
