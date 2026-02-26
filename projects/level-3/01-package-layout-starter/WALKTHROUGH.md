# Package Layout Starter — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. Spend at least 20 minutes attempting it independently.

## Thinking Process

This project is about understanding how Python organizes code at a higher level than single files. Up to now, you have been writing scripts where everything lives in one `.py` file. In real projects, code is split across multiple files organized into **packages** -- directories with an `__init__.py` file that Python treats as importable modules.

Before coding, ask yourself: what information would be useful when analyzing a Python package? You would want to know which `.py` files exist, what functions and classes each file defines, and whether the package has the required structural elements (`__init__.py`, `__main__.py`). Think of this tool as a "health check" for package structure.

The project also introduces **dataclasses**, which are a cleaner way to represent structured data than plain dictionaries. Instead of `info = {"name": "mypackage", "modules": [...]}`, you write a `@dataclass` that gives you type hints, automatic `__init__`, and better IDE support. This is Level 3's major upgrade in how you model data.

## Step 1: Define Data Models with Dataclasses

**What to do:** Create `PackageInfo` and `ModuleInfo` dataclasses to hold the metadata your scanner will collect.

**Why:** Dataclasses give you structured, typed data containers. Compare `info["name"]` (a plain dict -- no autocomplete, easy to mistype the key) with `info.name` (a dataclass -- autocomplete works, typos cause errors at definition time, not runtime).

```python
from dataclasses import dataclass, field, asdict
from typing import Optional

@dataclass
class PackageInfo:
    name: str
    version: str = "0.1.0"
    description: str = ""
    author: str = ""
    modules: list[str] = field(default_factory=list)
    entry_point: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)
```

Two things to notice:

- **`field(default_factory=list)`** is required for mutable defaults. Writing `modules: list[str] = []` would share the same list across all instances (a common Python gotcha).
- **`asdict(self)`** converts the dataclass to a dict, which is useful for JSON serialization.

**Predict:** What would happen if you wrote `modules: list[str] = []` instead of using `field(default_factory=list)`? Try to guess before looking it up.

## Step 2: Scan a Directory for Python Files

**What to do:** Write a `scan_package()` function that examines a directory and returns a `PackageInfo` describing its structure.

**Why:** This is the core feature -- analyzing what is in a directory. The function uses `pathlib.Path.glob()` to find `.py` files, checks for `__init__.py` (which makes a directory a package), and checks for `__main__.py` (which makes a package executable with `python -m`).

```python
def scan_package(root: Path) -> PackageInfo:
    if not root.exists():
        raise FileNotFoundError(f"Package directory not found: {root}")

    logger.info("Scanning package at %s", root)

    has_init = (root / "__init__.py").exists()
    if not has_init:
        logger.warning("No __init__.py found — this is not a proper package")

    py_files = sorted(root.glob("*.py"))
    module_names = [f.stem for f in py_files if f.name != "__init__.py"]

    return PackageInfo(
        name=root.name,
        modules=module_names,
        entry_point="__main__" if (root / "__main__.py").exists() else None,
    )
```

**Predict:** What does `f.stem` give you for a file named `utils.py`? What about `__init__.py`? Why does the code exclude `__init__.py` from the modules list?

## Step 3: Scan a Single Module's Contents

**What to do:** Write a `scan_module()` function that reads a `.py` file and extracts the names of functions, classes, and imports using simple text parsing.

**Why:** This gives you deeper insight into what each module contains. The function uses string matching (`startswith("def ")`) rather than Python's AST module -- this keeps it beginner-friendly while still being useful.

```python
def scan_module(path: Path) -> ModuleInfo:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    functions, classes, imports = [], [], []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("def "):
            name = stripped.split("(")[0].replace("def ", "")
            functions.append(name)
        elif stripped.startswith("class "):
            name = stripped.split("(")[0].split(":")[0].replace("class ", "")
            classes.append(name)
        elif stripped.startswith(("import ", "from ")):
            imports.append(stripped)

    return ModuleInfo(name=path.stem, path=str(path),
                      functions=functions, classes=classes, imports=imports)
```

**Predict:** This parser uses simple string matching. Can you think of a situation where it would give a wrong result? (Hint: what about `def` inside a string or a comment?)

## Step 4: Validate Package Structure

**What to do:** Write a `validate_package()` function that checks for common structural problems and returns a list of issues with severity levels.

**Why:** Validation is separate from scanning. Scanning tells you what exists; validation tells you what is wrong. This separation means you can scan without validating (for quick summaries) or validate without displaying the full scan (for CI checks).

```python
def validate_package(root: Path) -> list[dict]:
    issues = []

    if not (root / "__init__.py").exists():
        issues.append({
            "severity": "error",
            "message": "Missing __init__.py — directory is not a package",
        })

    py_files = list(root.glob("*.py"))
    for py_file in py_files:
        text = py_file.read_text(encoding="utf-8")
        if f"from {root.name}" in text and py_file.name == "__init__.py":
            issues.append({
                "severity": "warning",
                "message": "__init__.py imports from own package — potential circular import",
            })

    if not py_files:
        issues.append({"severity": "warning", "message": "No .py files found"})

    return issues
```

**Predict:** Why is a missing `__init__.py` an "error" but an empty directory is only a "warning"? Think about the practical consequences of each.

## Step 5: Generate __init__.py Content

**What to do:** Write a `generate_init_py()` function that creates proper `__init__.py` content with `__version__` and `__all__`.

**Why:** This turns your scanner into a productivity tool. Instead of just reporting what exists, it can bootstrap the boilerplate that every package needs.

```python
def generate_init_py(package_info: PackageInfo) -> str:
    lines = [
        f'"""Package: {package_info.name}."""',
        "",
        f"__version__ = \"{package_info.version}\"",
        "",
    ]
    if package_info.modules:
        lines.append("__all__ = [")
        for mod in sorted(package_info.modules):
            lines.append(f'    "{mod}",')
        lines.append("]")

    return "\n".join(lines) + "\n"
```

**Predict:** What is `__all__` and why does it matter? (Hint: try `from mypackage import *` with and without `__all__` defined.)

## Step 6: Build the CLI with Subcommands

**What to do:** Use `argparse` with subcommands (`scan`, `validate`, `init`) so one tool serves multiple purposes.

**Why:** Subcommands are how real CLI tools work (think `git commit`, `git push`, `git log`). The user picks the action, and the tool runs the right function.

```python
def parse_args():
    parser = argparse.ArgumentParser(description="Package layout starter")
    sub = parser.add_subparsers(dest="command", help="Available commands")

    scan = sub.add_parser("scan", help="Scan a package directory")
    scan.add_argument("path", help="Path to package directory")

    validate = sub.add_parser("validate", help="Validate package structure")
    validate.add_argument("path", help="Path to package directory")

    init = sub.add_parser("init", help="Generate __init__.py")
    init.add_argument("path", help="Path to package directory")

    return parser.parse_args()
```

**Predict:** What happens if the user runs `python project.py` with no subcommand? How does `dest="command"` help you handle that?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Using `modules: list = []` in a dataclass | Mutable default trap -- all instances share the same list | Use `field(default_factory=list)` |
| Forgetting `encoding="utf-8"` when reading files | Works on some systems, fails on others | Always specify encoding explicitly |
| Parsing `def` inside strings or comments | Simple text parsing has limits | Acceptable for this project; note it as a known limitation |
| Not handling non-existent paths | `Path.glob()` on missing directory | Check `root.exists()` first and raise `FileNotFoundError` |

## Testing Your Solution

```bash
pytest -q
```

Expected output:
```text
8 passed
```

Test from the command line:

```bash
python project.py scan .
python project.py validate .
python project.py init .
```

## What You Learned

- **Dataclasses** replace ad-hoc dicts with typed, structured containers. They auto-generate `__init__`, `__repr__`, and `__eq__`, and they work with `asdict()` for easy JSON conversion.
- **`__init__.py`** makes a directory a Python package. It can be empty or can define `__all__` to control what `from package import *` exports.
- **Argparse subcommands** let one tool do multiple things, just like `git` has `commit`, `push`, `log`. The `dest="command"` parameter tells you which subcommand the user chose.
