# Modern Python Tooling — Part 1: uv and ruff

[← Back to Overview](./modern-python-tooling.md) · [Part 2: pyproject.toml and Ecosystem →](./modern-python-tooling-part2.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize |
|:---: | :---: | :---: | :---: | :---: | :---:|
| **You are here** | [Projects](#practice) | — | — | [Flashcards](../practice/flashcards/README.md) | — |

<!-- modality-hub-end -->

---

The Python ecosystem has modernized significantly. This part covers **uv** and **ruff** — the two tools that replace most of the older pip/venv/black/flake8 toolchain.

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

---

| [← Overview](./modern-python-tooling.md) | [Part 2: pyproject.toml and Ecosystem →](./modern-python-tooling-part2.md) |
|:---|---:|
