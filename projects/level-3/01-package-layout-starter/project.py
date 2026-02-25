"""Level 3 project: Package Layout Starter.

Demonstrates how to structure a Python package with proper imports,
__init__.py files, and clean module boundaries.

Skills practiced: packages/modules, typing basics, dataclasses,
logging, proper import patterns.
"""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

# Configure a module-level logger — standard pattern in real packages.
logger = logging.getLogger(__name__)


@dataclass
class PackageInfo:
    """Metadata about a Python package.

    Dataclasses auto-generate __init__, __repr__, and __eq__.
    This is cleaner than writing a class with manual __init__.
    """
    name: str
    version: str = "0.1.0"
    description: str = ""
    author: str = ""
    modules: list[str] = field(default_factory=list)
    entry_point: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dict for JSON serialisation."""
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
    """Scan a directory to discover Python package structure.

    Looks for __init__.py, .py files, and builds a PackageInfo.

    Args:
        root: The directory to scan.

    Returns:
        PackageInfo describing what was found.
    """
    if not root.exists():
        raise FileNotFoundError(f"Package directory not found: {root}")

    logger.info("Scanning package at %s", root)

    # Check for __init__.py — this makes a directory a package.
    has_init = (root / "__init__.py").exists()
    if not has_init:
        logger.warning("No __init__.py found — this is not a proper package")

    # Find all .py files (modules).
    py_files = sorted(root.glob("*.py"))
    module_names = [f.stem for f in py_files if f.name != "__init__.py"]

    logger.info("Found %d modules: %s", len(module_names), module_names)

    return PackageInfo(
        name=root.name,
        modules=module_names,
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
            # Extract function name: "def my_func(...):" -> "my_func"
            name = stripped.split("(")[0].replace("def ", "")
            functions.append(name)
        elif stripped.startswith("class "):
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
    """Generate __init__.py content for a package.

    Creates proper __all__ list and imports.
    """
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


def validate_package(root: Path) -> list[dict]:
    """Check a package for common structural issues.

    Returns a list of issue dicts with severity and message.
    """
    issues: list[dict] = []

    if not (root / "__init__.py").exists():
        issues.append({
            "severity": "error",
            "message": "Missing __init__.py — directory is not a package",
        })

    # Check for circular import patterns (simple heuristic).
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
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments with subcommands."""
    parser = argparse.ArgumentParser(description="Package layout starter")
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # Scan subcommand.
    scan = sub.add_parser("scan", help="Scan a package directory")
    scan.add_argument("path", help="Path to package directory")

    # Validate subcommand.
    validate = sub.add_parser("validate", help="Validate package structure")
    validate.add_argument("path", help="Path to package directory")

    # Init subcommand.
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
