"""Level 1 project: Batch Rename Simulator.

Plan file renames without actually moving or renaming anything.
Read a list of filenames, apply renaming rules, and show a preview
of what would change.

Concepts: string methods, Path manipulation, safe simulation patterns.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def apply_rule_lower(name: str) -> str:
    """Rename by lowercasing the entire filename.

    WHY lowercase? -- Consistent naming avoids case-sensitivity bugs
    across operating systems (Linux is case-sensitive, Windows is not).
    """
    return name.lower()


def apply_rule_replace_spaces(name: str) -> str:
    """Replace spaces with underscores.

    WHY underscores? -- Spaces in filenames cause problems in shell
    commands and URLs.  Underscores are a common safe alternative.
    """
    return name.replace(" ", "_")


def apply_rule_add_prefix(name: str, prefix: str = "backup_") -> str:
    """Prepend a prefix to the filename (not the directory part).

    WHY prefix? -- Batch-prefixing is a real-world pattern for
    organising backups, versions, or dated snapshots.
    """
    p = Path(name)
    return str(p.parent / f"{prefix}{p.name}") if str(p.parent) != "." else f"{prefix}{p.name}"


def apply_rule_strip_numbers(name: str) -> str:
    """Remove leading digits and separators from the filename stem.

    WHY strip numbers? -- Numbered prefixes like '001_' or '01-' are
    common in downloads; removing them normalises the name.
    """
    p = Path(name)
    stem = re.sub(r"^\d+[\-_ ]*", "", p.stem)
    if not stem:
        stem = p.stem
    return stem + p.suffix


RULES: dict[str, object] = {
    "lower": apply_rule_lower,
    "replace_spaces": apply_rule_replace_spaces,
    "add_prefix": apply_rule_add_prefix,
    "strip_numbers": apply_rule_strip_numbers,
}


def simulate_rename(filename: str, rule_name: str) -> dict[str, str]:
    """Apply a single rule and return the before/after mapping.

    WHY return a dict? -- Returning structured data instead of
    printing makes the function testable and composable.
    """
    filename = filename.strip()
    if not filename:
        raise ValueError("Filename cannot be empty")

    rule_fn = RULES.get(rule_name)
    if rule_fn is None:
        raise ValueError(f"Unknown rule: {rule_name}")

    new_name = rule_fn(filename)
    return {"original": filename, "renamed": new_name, "changed": filename != new_name}


def simulate_batch(filenames: list[str], rule_name: str) -> list[dict[str, str]]:
    """Apply a rule to every filename in the list.

    WHY batch? -- Real rename operations almost always work on many
    files at once.  Processing a list is the realistic pattern.
    """
    results = []
    for name in filenames:
        name = name.strip()
        if not name:
            continue
        results.append(simulate_rename(name, rule_name))
    return results


def detect_conflicts(results: list[dict[str, str]]) -> list[str]:
    """Find renamed filenames that would collide (duplicates).

    WHY check conflicts? -- If two files rename to the same target,
    one would overwrite the other.  Detecting this before acting is
    the whole point of a *simulator*.
    """
    seen: dict[str, int] = {}
    for r in results:
        target = r["renamed"]
        seen[target] = seen.get(target, 0) + 1
    return [name for name, count in seen.items() if count > 1]


def format_plan(results: list[dict[str, str]], conflicts: list[str]) -> str:
    """Format a human-readable rename plan."""
    lines = ["=== Batch Rename Plan ===", ""]
    changed = 0
    for r in results:
        marker = " *" if r["renamed"] in conflicts else ""
        if r["changed"]:
            lines.append(f"  {r['original']:<30} -> {r['renamed']}{marker}")
            changed += 1
        else:
            lines.append(f"  {r['original']:<30}    (no change)")

    lines.append("")
    lines.append(f"  Total files: {len(results)}")
    lines.append(f"  Would rename: {changed}")
    if conflicts:
        lines.append(f"  CONFLICTS: {', '.join(conflicts)}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Batch Rename Simulator")
    parser.add_argument("--input", default="data/sample_input.txt",
                        help="File with one filename per line")
    parser.add_argument("--rule", default="lower",
                        choices=list(RULES.keys()),
                        help="Renaming rule to apply")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    path = Path(args.input)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    filenames = path.read_text(encoding="utf-8").splitlines()
    results = simulate_batch(filenames, args.rule)
    conflicts = detect_conflicts(results)

    print(format_plan(results, conflicts))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_data = {"rule": args.rule, "renames": results, "conflicts": conflicts}
    output_path.write_text(json.dumps(output_data, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
