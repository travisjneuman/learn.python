"""Generate SOLUTION.md skeleton files from existing project.py files.

Reads each project.py, extracts function signatures and docstrings,
and generates a SOLUTION.md with WHY-comment placeholders ready for
human or AI review.

Usage:
    python tools/generate_solution_skeletons.py
    python tools/generate_solution_skeletons.py --level 0
    python tools/generate_solution_skeletons.py --dry-run
    python tools/generate_solution_skeletons.py --overwrite   # Regenerate existing
"""

from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


WARNING_BANNER = """\
> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first — it guides
> your thinking without giving away the answer.

---

"""


def extract_functions(source: str) -> list[dict[str, str]]:
    """Extract function names, signatures, and docstrings from Python source."""
    functions: list[dict[str, str]] = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return functions

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Get the source line for the signature
            args = []
            for arg in node.args.args:
                ann = ""
                if arg.annotation:
                    ann = f": {ast.unparse(arg.annotation)}"
                args.append(f"{arg.arg}{ann}")

            returns = ""
            if node.returns:
                returns = f" -> {ast.unparse(node.returns)}"

            sig = f"def {node.name}({', '.join(args)}){returns}:"
            docstring = ast.get_docstring(node) or ""

            functions.append({
                "name": node.name,
                "signature": sig,
                "docstring": docstring,
            })

    return functions


def generate_skeleton(project_dir: Path) -> str:
    """Generate a SOLUTION.md skeleton from the project files."""
    readme = project_dir / "README.md"
    project_py = project_dir / "project.py"

    # Get project title from README
    title = project_dir.name
    if readme.exists():
        first_line = readme.read_text(encoding="utf-8").split("\n")[0]
        if first_line.startswith("# "):
            title = first_line[2:].strip()

    # Read project.py source
    source = ""
    if project_py.exists():
        source = project_py.read_text(encoding="utf-8")

    functions = extract_functions(source) if source else []

    lines: list[str] = []
    lines.append(f"# Solution: {title}")
    lines.append("")
    lines.append(WARNING_BANNER)

    # Complete solution section
    lines.append("## Complete solution")
    lines.append("")
    if source:
        lines.append("```python")
        # Add WHY-comment placeholders to each function
        for func in functions:
            lines.append(f"# WHY {func['name']}: [explain the design reason]")
        lines.append("")
        lines.append("# [paste the complete working solution here]")
        lines.append("# Include WHY comments on every non-obvious line.")
        lines.append("```")
    else:
        lines.append("```python")
        lines.append("# [paste the complete working solution here]")
        lines.append("```")
    lines.append("")

    # Design decisions table
    lines.append("## Design decisions")
    lines.append("")
    lines.append("| Decision | Why | Alternative considered |")
    lines.append("|----------|-----|----------------------|")
    for func in functions[:3]:
        lines.append(f"| {func['name']} function | [reason] | [alternative] |")
    if not functions:
        lines.append("| [decision 1] | [reason] | [alternative] |")
    lines.append("")

    # Alternative approaches
    lines.append("## Alternative approaches")
    lines.append("")
    lines.append("### Approach B: [Name]")
    lines.append("")
    lines.append("```python")
    lines.append("# [Different valid approach with trade-offs explained]")
    lines.append("```")
    lines.append("")
    lines.append("**Trade-off:** [When you would prefer this approach vs the primary one]")
    lines.append("")

    # What could go wrong
    lines.append("## What could go wrong")
    lines.append("")
    lines.append("| Scenario | What happens | Prevention |")
    lines.append("|----------|-------------|------------|")
    lines.append("| [bad input] | [error/behavior] | [how to handle] |")
    lines.append("| [edge case] | [behavior] | [how to handle] |")
    lines.append("")

    # Key takeaways
    lines.append("## Key takeaways")
    lines.append("")
    lines.append("1. [Most important lesson from this project]")
    lines.append("2. [Second lesson]")
    lines.append("3. [Connection to future concepts]")
    lines.append("")

    return "\n".join(lines)


def process_level(level_dir: Path, *, dry_run: bool = False, overwrite: bool = False) -> int:
    """Process all projects in a level directory."""
    count = 0
    for project_dir in sorted(level_dir.iterdir()):
        if not project_dir.is_dir():
            continue
        if not re.match(r"\d{2}-", project_dir.name):
            continue

        solution_file = project_dir / "SOLUTION.md"
        if solution_file.exists() and not overwrite:
            continue

        skeleton = generate_skeleton(project_dir)
        if dry_run:
            print(f"  WOULD CREATE: {solution_file.relative_to(ROOT)}")
        else:
            solution_file.write_text(skeleton, encoding="utf-8")
            print(f"  CREATED: {solution_file.relative_to(ROOT)}")
        count += 1

    return count


def main() -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(description="Generate SOLUTION.md skeletons")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--level", type=str, help="Only process a specific level")
    parser.add_argument("--overwrite", action="store_true", help="Regenerate existing files")
    args = parser.parse_args()

    total = 0
    projects_dir = ROOT / "projects"

    for level_dir in sorted(projects_dir.iterdir()):
        if not level_dir.is_dir():
            continue
        if args.level and level_dir.name != f"level-{args.level}" and args.level not in level_dir.name:
            continue

        if re.match(r"level-", level_dir.name):
            print(f"\n=== {level_dir.name.upper()} ===")
            total += process_level(level_dir, dry_run=args.dry_run, overwrite=args.overwrite)
        elif level_dir.name == "elite-track":
            print("\n=== ELITE TRACK ===")
            total += process_level(level_dir, dry_run=args.dry_run, overwrite=args.overwrite)
        elif level_dir.name == "modules":
            for module_dir in sorted(level_dir.iterdir()):
                if module_dir.is_dir():
                    print(f"\n=== MODULE {module_dir.name} ===")
                    total += process_level(module_dir, dry_run=args.dry_run, overwrite=args.overwrite)

    action = "would create" if args.dry_run else "created"
    print(f"\nDone. {total} skeleton files {action}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
