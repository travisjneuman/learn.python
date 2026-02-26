# Package Layout Starter — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 3 project: Package Layout Starter."""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

# WHY: module-level logger uses __name__ so log messages show which
# module they came from — critical when debugging multi-file packages.
logger = logging.getLogger(__name__)


# WHY: dataclass auto-generates __init__, __repr__, and __eq__,
# eliminating boilerplate while keeping the data structure explicit.
@dataclass
class PackageInfo:
    """Metadata about a Python package."""
    name: str
    version: str = "0.1.0"
    description: str = ""
    author: str = ""
    # WHY: field(default_factory=list) avoids the mutable default trap.
    # If you wrote `modules: list = []`, all instances would share
    # the same list — a classic Python gotcha.
    modules: list[str] = field(default_factory=list)
    entry_point: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dict for JSON serialisation."""
        # WHY: asdict() recursively converts dataclass fields to dicts,
        # making the result safe for json.dumps().
        return asdict(self)


@dataclass
class ModuleInfo:
    """Metadata about a single module within a package."""
    name: str
    path: str
    functions: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)


def scan_package(root: Path) -> PackageInfo:
    """Scan a directory to discover Python package structure."""
    # WHY: fail fast with a clear error rather than producing
    # confusing results from a non-existent path.
    if not root.exists():
        raise FileNotFoundError(f"Package directory not found: {root}")

    logger.info("Scanning package at %s", root)

    # WHY: __init__.py is what makes a directory a Python package
    # (required before Python 3.3, optional after — but still best practice).
    has_init = (root / "__init__.py").exists()
    if not has_init:
        logger.warning("No __init__.py found — this is not a proper package")

    # WHY: glob("*.py") only matches immediate children, not recursive.
    # sorted() ensures deterministic output across platforms.
    py_files = sorted(root.glob("*.py"))
    # WHY: exclude __init__.py from the module list — it is the package
    # initialiser, not a standalone module.
    module_names = [f.stem for f in py_files if f.name != "__init__.py"]

    logger.info("Found %d modules: %s", len(module_names), module_names)

    return PackageInfo(
        name=root.name,
        modules=module_names,
        # WHY: __main__.py lets a package run with `python -m package_name`.
        entry_point="__main__" if (root / "__main__.py").exists() else None,
    )


def scan_module(path: Path) -> ModuleInfo:
    """Scan a single .py file to extract function and class names.

    Uses simple text parsing (not AST) to stay beginner-friendly.
    """
    if not path.exists():
        raise FileNotFoundError(f"Module not found: {path}")

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    functions: list[str] = []
    classes: list[str] = []
    imports: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("def "):
            # WHY: split on "(" to isolate the function name from parameters,
            # then strip the "def " prefix.
            name = stripped.split("(")[0].replace("def ", "")
            functions.append(name)
        elif stripped.startswith("class "):
            # WHY: classes can use either "class Foo:" or "class Foo(Base):",
            # so we split on both "(" and ":" to handle both cases.
            name = stripped.split("(")[0].split(":")[0].replace("class ", "")
            classes.append(name)
        elif stripped.startswith(("import ", "from ")):
            imports.append(stripped)

    return ModuleInfo(
        name=path.stem,
        path=str(path),
        functions=functions,
        classes=classes,
        imports=imports,
    )


def generate_init_py(package_info: PackageInfo) -> str:
    """Generate __init__.py content for a package."""
    lines = [
        f'"""Package: {package_info.name}."""',
        "",
        f"__version__ = \"{package_info.version}\"",
        "",
    ]

    # WHY: __all__ controls what `from package import *` exposes.
    # Without it, star-imports pull in everything — a maintenance risk.
    if package_info.modules:
        lines.append("__all__ = [")
        for mod in sorted(package_info.modules):
            lines.append(f'    "{mod}",')
        lines.append("]")

    return "\n".join(lines) + "\n"


def validate_package(root: Path) -> list[dict]:
    """Check a package for common structural issues."""
    issues: list[dict] = []

    if not (root / "__init__.py").exists():
        issues.append({
            "severity": "error",
            "message": "Missing __init__.py — directory is not a package",
        })

    # WHY: circular imports are a common pain point in packages.
    # If __init__.py imports from its own package name, that often
    # triggers circular dependency issues at import time.
    py_files = list(root.glob("*.py"))
    for py_file in py_files:
        text = py_file.read_text(encoding="utf-8")
        if f"from {root.name}" in text and py_file.name == "__init__.py":
            issues.append({
                "severity": "warning",
                "message": f"__init__.py imports from own package — potential circular import",
            })

    if not py_files:
        issues.append({
            "severity": "warning",
            "message": "No .py files found in package directory",
        })

    logger.info("Validation found %d issues", len(issues))
    return issues


def configure_logging(level: str = "INFO") -> None:
    """Set up structured logging with file and console handlers."""
    # WHY: getattr(logging, level.upper()) converts the string "INFO"
    # to logging.INFO (the integer 20). Falls back to INFO if invalid.
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments with subcommands."""
    parser = argparse.ArgumentParser(description="Package layout starter")
    # WHY: subcommands give the CLI a "git-like" interface:
    # `project.py scan .` vs `project.py validate .`
    sub = parser.add_subparsers(dest="command", help="Available commands")

    scan = sub.add_parser("scan", help="Scan a package directory")
    scan.add_argument("path", help="Path to package directory")

    validate = sub.add_parser("validate", help="Validate package structure")
    validate.add_argument("path", help="Path to package directory")

    init = sub.add_parser("init", help="Generate __init__.py")
    init.add_argument("path", help="Path to package directory")

    parser.add_argument("--log-level", default="INFO", help="Logging level")
    return parser.parse_args()


def main() -> None:
    """Entry point: run the requested command."""
    args = parse_args()
    configure_logging(args.log_level)

    if args.command == "scan":
        info = scan_package(Path(args.path))
        print(json.dumps(info.to_dict(), indent=2))
    elif args.command == "validate":
        issues = validate_package(Path(args.path))
        for issue in issues:
            print(f"[{issue['severity'].upper()}] {issue['message']}")
        if not issues:
            print("No issues found.")
    elif args.command == "init":
        info = scan_package(Path(args.path))
        content = generate_init_py(info)
        print(content)
    else:
        print("Use --help to see available commands.")


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| `@dataclass` for PackageInfo and ModuleInfo | Eliminates boilerplate `__init__`, `__repr__`, and `__eq__` while keeping the structure self-documenting. Easier to read than a plain dict. |
| Text parsing instead of `ast` module | The `ast` module would be more accurate, but text parsing is easier to understand at this level and teaches string manipulation. |
| `field(default_factory=list)` for mutable defaults | Prevents the shared-mutable-default bug where all instances accidentally share the same list object. |
| Subcommands via `argparse` | Each action (scan, validate, init) is a distinct operation, making the CLI discoverable and extensible. |
| `__all__` in generated `__init__.py` | Controls public API surface — prevents accidental export of internal implementation details. |

## Alternative Approaches

### Using the `ast` module for module scanning

```python
import ast

def scan_module_ast(path: Path) -> ModuleInfo:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
    return ModuleInfo(name=path.stem, path=str(path), functions=functions, classes=classes)
```

**Trade-off:** The `ast` approach correctly parses any valid Python (even functions defined inside strings or unusual formatting), but it is harder for beginners to understand. The text-based approach is "good enough" for standard code and teaches regex/string skills you will use everywhere.

### Using `importlib` for package inspection

```python
import importlib

spec = importlib.util.spec_from_file_location("pkg", init_path)
```

**Trade-off:** This actually *imports* the package, which can trigger side effects. Our approach only reads the filesystem, making it safe to run on untrusted code.

## Common Pitfalls

1. **Forgetting `__init__.py`** — Without it (pre-3.3), Python cannot import from the directory. Even in Python 3.3+ where namespace packages exist, omitting `__init__.py` breaks relative imports and makes the package harder to reason about. Always include it.

2. **Mutable default arguments** — Writing `modules: list = []` in a dataclass (or any function default) means every instance shares the same list. Always use `field(default_factory=list)` for mutable defaults.

3. **Circular imports in `__init__.py`** — If `__init__.py` imports from a submodule that imports from `__init__.py`, Python raises `ImportError`. The fix is to either defer imports or restructure so `__init__.py` only re-exports, never defines core logic.
