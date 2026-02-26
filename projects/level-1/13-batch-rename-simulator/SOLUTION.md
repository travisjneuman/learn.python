# Solution: Level 1 / Project 13 - Batch Rename Simulator

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 1 project: Batch Rename Simulator.

Plan file renames without actually moving or renaming anything.
Read a list of filenames, apply renaming rules, and show a preview
of what would change.

Concepts: string methods, Path manipulation, safe simulation patterns.
"""


import argparse
import json
import re
from pathlib import Path


# WHY apply_rule_lower: Lowercasing filenames is the most common
# normalisation.  It prevents case-sensitivity bugs when moving files
# between Windows (case-insensitive) and Linux (case-sensitive).
def apply_rule_lower(name: str) -> str:
    """Rename by lowercasing the entire filename."""
    return name.lower()


# WHY apply_rule_replace_spaces: Spaces in filenames cause problems in
# shell commands (require quoting), URLs (need %20 encoding), and
# many programming languages.  Replacing with underscores is a
# universal safe alternative.
def apply_rule_replace_spaces(name: str) -> str:
    """Replace spaces with underscores."""
    return name.replace(" ", "_")


# WHY apply_rule_add_prefix: Batch-prefixing is a real-world pattern
# used for backups ("backup_config.json"), versioning ("v2_schema.sql"),
# and dated snapshots ("2024-01-15_report.pdf").
def apply_rule_add_prefix(name: str, prefix: str = "backup_") -> str:
    """Prepend a prefix to the filename (not the directory part)."""
    p = Path(name)
    # WHY check parent != ".": If the name has no directory part
    # (just "file.txt"), Path.parent returns Path(".").  In that case,
    # we prepend directly without the "." appearing in the result.
    return str(p.parent / f"{prefix}{p.name}") if str(p.parent) != "." else f"{prefix}{p.name}"


# WHY apply_rule_strip_numbers: Removing leading numbers from filenames
# like "001_photo.jpg" or "42-notes.txt" normalises names from numbered
# downloads, photo exports, and ordered file systems.
def apply_rule_strip_numbers(name: str) -> str:
    """Remove leading digits and separators from the filename stem."""
    p = Path(name)
    # WHY regex: The pattern ^\d+[\-_ ]* matches one or more digits
    # at the start, followed by optional dashes, underscores, or spaces.
    # "001_photo" -> "photo", "42-notes" -> "notes".
    stem = re.sub(r"^\d+[\-_ ]*", "", p.stem)
    # WHY fallback: If the entire stem is digits (e.g., "12345.txt"),
    # stripping all digits would leave an empty stem, which is not a
    # valid filename.  Keep the original stem in that case.
    if not stem:
        stem = p.stem
    # WHY p.suffix: Preserve the original extension.
    return stem + p.suffix


# WHY RULES dict: Same dispatch pattern as the Command Dispatcher
# (Project 11).  Mapping rule names to functions makes it easy to
# add new rules and lets argparse validate choices automatically.
RULES: dict[str, object] = {
    "lower": apply_rule_lower,
    "replace_spaces": apply_rule_replace_spaces,
    "add_prefix": apply_rule_add_prefix,
    "strip_numbers": apply_rule_strip_numbers,
}


# WHY simulate_rename: The key design decision — this function
# applies a rule and returns the before/after mapping WITHOUT
# actually renaming any files.  This is the simulation pattern.
def simulate_rename(filename: str, rule_name: str) -> dict[str, str]:
    """Apply a single rule and return the before/after mapping."""
    filename = filename.strip()
    # WHY raise ValueError: An empty filename is not a valid input.
    # Failing early with a clear message prevents confusing results
    # downstream.
    if not filename:
        raise ValueError("Filename cannot be empty")

    rule_fn = RULES.get(rule_name)
    if rule_fn is None:
        raise ValueError(f"Unknown rule: {rule_name}")

    new_name = rule_fn(filename)
    # WHY "changed" flag: Knowing whether the name actually changed
    # lets the display skip unchanged files.  "my_file.txt" with the
    # replace_spaces rule does not change (no spaces), so showing it
    # as "no change" avoids noise.
    return {"original": filename, "renamed": new_name, "changed": filename != new_name}


# WHY simulate_batch: Real rename operations work on many files at
# once.  Processing a list is the realistic pattern — you never
# rename just one file in a batch operation.
def simulate_batch(filenames: list[str], rule_name: str) -> list[dict[str, str]]:
    """Apply a rule to every filename in the list."""
    results = []
    for name in filenames:
        name = name.strip()
        # WHY skip blanks: Input files often have blank lines between
        # groups.  Skipping them prevents ValueError from empty filenames.
        if not name:
            continue
        results.append(simulate_rename(name, rule_name))
    return results


# WHY detect_conflicts: This is the core safety feature of a simulator.
# If two files would rename to the same target, one would overwrite
# the other.  Detecting this BEFORE acting is the entire point of
# previewing instead of directly renaming.
def detect_conflicts(results: list[dict[str, str]]) -> list[str]:
    """Find renamed filenames that would collide (duplicates)."""
    seen: dict[str, int] = {}
    for r in results:
        target = r["renamed"]
        # WHY count occurrences: If two files both rename to "report.txt",
        # that target appears twice.  Any count > 1 is a conflict.
        seen[target] = seen.get(target, 0) + 1
    return [name for name, count in seen.items() if count > 1]


# WHY format_plan: A human-readable preview shows exactly what would
# happen before any destructive action.  Conflicts are marked with *
# so the user can resolve them before proceeding.
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


# WHY parse_args: The --rule argument uses choices= to restrict input
# to valid rule names.  argparse rejects invalid rules automatically
# with a helpful error message.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Batch Rename Simulator")
    parser.add_argument("--input", default="data/sample_input.txt",
                        help="File with one filename per line")
    parser.add_argument("--rule", default="lower",
                        choices=list(RULES.keys()),
                        help="Renaming rule to apply")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


# WHY main: Orchestrates the simulation pipeline — read, simulate,
# detect conflicts, preview, and save.
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Simulation (preview) instead of actual renaming | Preview-then-act is the safest pattern for destructive operations; the user sees exactly what would happen before committing | Direct rename — one mistake could overwrite or lose files with no undo |
| RULES dict mapping names to functions | Same dispatch pattern as Projects 10 and 11; adding a new rule is one function + one dict entry | If/elif chain — does not integrate with argparse `choices=` as cleanly |
| Conflict detection as a separate step | Decouples the "apply rule" step from the "check safety" step; each can be tested independently | Check conflicts inside `simulate_batch` — mixes concerns and makes testing harder |
| `re.sub` for stripping numbers | Regex handles varied formats ("001_", "42-", "7 ") in one pattern; string methods would need multiple checks | Multiple `lstrip` calls — fragile, would not handle mixed separators |

## Alternative approaches

### Approach B: Chaining multiple rules

```python
def simulate_chain(filename: str, rule_names: list[str]) -> dict:
    """Apply multiple rules in sequence to a single filename."""
    current = filename.strip()
    # WHY chaining: Real rename workflows often combine rules —
    # lowercase AND replace spaces AND strip numbers.  Chaining
    # applies each rule to the result of the previous one.
    for rule_name in rule_names:
        rule_fn = RULES.get(rule_name)
        if rule_fn is None:
            raise ValueError(f"Unknown rule: {rule_name}")
        current = rule_fn(current)

    return {"original": filename, "renamed": current, "changed": filename != current}

# Usage: simulate_chain("001 My File.TXT", ["strip_numbers", "lower", "replace_spaces"])
# Result: "my_file.txt"
```

**Trade-off:** Chaining is more powerful — it lets users compose multiple transformations. The single-rule approach is simpler to understand and debug at Level 1. When you need chaining, the function-as-value pattern makes it trivial: just loop through the rule functions and apply each one.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Two files rename to the same target (e.g., `A.TXT` and `a.txt` both become `a.txt` with `lower`) | `detect_conflicts()` flags `a.txt` as a conflict; the plan marks it with `*` | The conflict detection step catches this before any action is taken |
| Empty filename (blank line in input) | `simulate_batch()` skips blank lines; `simulate_rename()` raises ValueError if called directly with `""` | The `if not name: continue` guard handles this |
| Unknown rule name on command line | `argparse` rejects it with an error message listing valid choices, before the code even runs | The `choices=list(RULES.keys())` parameter in argparse handles this |
| Filename is entirely numeric (`"12345.txt"` with strip_numbers) | The regex strips all digits, leaving an empty stem; the `if not stem` guard keeps the original stem | The fallback prevents creating an extensionless file |

## Key takeaways

1. **Always simulate before executing destructive operations.** The preview-then-commit pattern is used by `git diff` (before commit), `terraform plan` (before apply), database migration `--dry-run`, and `rsync --dry-run`. Building this habit early prevents data loss.
2. **`re.sub()` replaces text matching a pattern.** `re.sub(r"^\d+[\-_ ]*", "", stem)` removes leading digits and separators. The `^` anchors to the start so it only strips from the beginning, not the middle. You will use `re.sub()` extensively for data cleaning.
3. **Conflict detection is the key insight of this project.** Any batch operation that maps inputs to outputs can produce collisions. Database migrations, URL routing, and environment variable naming all need conflict detection. The pattern — count target names, flag duplicates — is universal.
