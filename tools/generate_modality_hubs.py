"""Insert or update 'Learn Your Way' modality hub tables in project READMEs and concept docs.

Scans every project README and concept doc, checks which modality files exist
for that topic (walkthrough, solution, diagram, video, quiz, flashcard, browser),
and inserts a consistent navigation table linking to all available modalities.

Idempotent: safe to run repeatedly. Replaces existing hub blocks on each run.

Usage:
    python tools/generate_modality_hubs.py
    python tools/generate_modality_hubs.py --dry-run
    python tools/generate_modality_hubs.py --level 0      # Only process level 0
    python tools/generate_modality_hubs.py --concepts      # Only process concept docs
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Marker comments that delimit the hub block for idempotent replacement
HUB_START = "<!-- modality-hub-start -->"
HUB_END = "<!-- modality-hub-end -->"


def rel(from_file: Path, to_file: Path) -> str:
    """Compute a POSIX relative path from one file to another."""
    from_dir = from_file.parent
    try:
        return to_file.relative_to(from_dir).as_posix()
    except ValueError:
        common = from_dir
        ups = 0
        while True:
            try:
                remainder = to_file.relative_to(common)
                return "../" * ups + remainder.as_posix()
            except ValueError:
                common = common.parent
                ups += 1


def find_concept_slug(readme_path: Path) -> str | None:
    """Try to match a project to its related concept by reading the README."""
    # Map levels to their primary concepts
    level_concept_map: dict[str, list[str]] = {
        "level-00-absolute-beginner": [
            "what-is-a-variable", "how-loops-work", "types-and-conversions",
            "functions-explained", "collections-explained", "files-and-paths",
        ],
        "level-0": [
            "errors-and-debugging", "the-terminal-deeper",
            "collections-explained", "files-and-paths",
        ],
        "level-1": ["how-imports-work", "files-and-paths", "errors-and-debugging"],
        "level-2": ["collections-explained", "errors-and-debugging", "types-and-conversions"],
    }
    for level_name, concepts in level_concept_map.items():
        if level_name in str(readme_path):
            return concepts[0] if concepts else None
    return None


def build_hub_block(
    file_path: Path,
    *,
    is_concept: bool = False,
    concept_slug: str = "",
) -> str:
    """Build the Learn Your Way markdown table for a given file."""
    cells: list[tuple[str, str]] = []

    if is_concept:
        # This IS a concept doc
        slug = file_path.stem
        concept_link = "**You are here**"
        cells.append(("Read", concept_link))

        # Build link — find related projects via practice section
        cells.append(("Build", "[Projects](#practice)"))

        # Watch — video link
        video_file = ROOT / "concepts" / "videos" / f"{slug}.md"
        if video_file.exists():
            cells.append(("Watch", f"[Videos](videos/{slug}.md)"))
        else:
            cells.append(("Watch", "\u2014"))

        # Test — quiz link
        quiz_file = ROOT / "concepts" / "quizzes" / f"{slug}-quiz.py"
        if quiz_file.exists():
            cells.append(("Test", f"[Quiz](quizzes/{slug}-quiz.py)"))
        else:
            cells.append(("Test", "\u2014"))

        # Review — flashcards
        cells.append(("Review", f"[Flashcards]({rel(file_path, ROOT / 'practice/flashcards/README.md')})"))

        # Visualize — diagram
        diagram_file = ROOT / "concepts" / "diagrams" / f"{slug}.md"
        if diagram_file.exists():
            cells.append(("Visualize", f"[Diagrams](diagrams/{slug}.md)"))
        else:
            cells.append(("Visualize", "\u2014"))

    else:
        # This is a project README
        project_dir = file_path.parent

        # Read — concept link
        if concept_slug:
            concept_file = ROOT / "concepts" / f"{concept_slug}.md"
            if concept_file.exists():
                cells.append(("Read", f"[Concept]({rel(file_path, concept_file)})"))
            else:
                cells.append(("Read", "\u2014"))
        else:
            cells.append(("Read", "\u2014"))

        # Build
        cells.append(("Build", "**This project**"))

        # Watch — walkthrough
        walkthrough = project_dir / "WALKTHROUGH.md"
        if walkthrough.exists():
            cells.append(("Watch", "[Walkthrough](./WALKTHROUGH.md)"))
        else:
            cells.append(("Watch", "\u2014"))

        # Test — quiz
        if concept_slug:
            quiz_file = ROOT / "concepts" / "quizzes" / f"{concept_slug}-quiz.py"
            if quiz_file.exists():
                cells.append(("Test", f"[Quiz]({rel(file_path, quiz_file)})"))
            else:
                cells.append(("Test", "\u2014"))
        else:
            cells.append(("Test", "\u2014"))

        # Review — flashcards
        cells.append(("Review", f"[Flashcards]({rel(file_path, ROOT / 'practice/flashcards/README.md')})"))

        # Visualize — diagram
        if concept_slug:
            diagram_file = ROOT / "concepts" / "diagrams" / f"{concept_slug}.md"
            if diagram_file.exists():
                cells.append(("Visualize", f"[Diagram]({rel(file_path, diagram_file)})"))
            else:
                cells.append(("Visualize", "\u2014"))
        else:
            cells.append(("Visualize", "\u2014"))

        # Try — browser exercise
        # Check if a browser exercise exists for this level
        level_match = re.search(r"level-(\d+)", str(project_dir))
        if level_match:
            level_num = int(level_match.group(1))
            browser_file = ROOT / "browser" / f"level-{level_num}.html"
            if browser_file.exists():
                cells.append(("Try", f"[Browser]({rel(file_path, browser_file)})"))
            else:
                cells.append(("Try", "\u2014"))
        else:
            cells.append(("Try", "\u2014"))

    # Build the table
    headers = " | ".join(h for h, _ in cells)
    aligns = " | ".join(":---:" for _ in cells)
    values = " | ".join(v for _, v in cells)

    return (
        f"{HUB_START}\n"
        f"\n### Learn Your Way\n\n"
        f"| {headers} |\n"
        f"|{aligns}|\n"
        f"| {values} |\n"
        f"\n{HUB_END}"
    )


def insert_hub(file_path: Path, hub_block: str, *, dry_run: bool = False) -> bool:
    """Insert or replace the hub block in a markdown file. Returns True if changed."""
    content = file_path.read_text(encoding="utf-8")

    # Replace existing hub block
    if HUB_START in content:
        pattern = re.compile(
            re.escape(HUB_START) + r".*?" + re.escape(HUB_END),
            flags=re.DOTALL,
        )
        new_content = pattern.sub(hub_block, content)
    else:
        # Insert after "## Before You Start" section (projects) or after first paragraph (concepts)
        # For projects: after "## Before You Start" block
        before_start = re.search(r"(## Before You Start\n.*?\n)(\n## )", content, re.DOTALL)
        if before_start:
            insert_pos = before_start.end(1)
            new_content = content[:insert_pos] + "\n" + hub_block + "\n" + content[insert_pos:]
        else:
            # For concepts or docs without "Before You Start": after first paragraph
            first_blank = content.find("\n\n", content.find("\n") + 1)
            if first_blank != -1:
                insert_pos = first_blank + 2
                new_content = content[:insert_pos] + hub_block + "\n\n" + content[insert_pos:]
            else:
                new_content = content + "\n\n" + hub_block + "\n"

    if new_content == content:
        return False

    if not dry_run:
        file_path.write_text(new_content, encoding="utf-8")
    return True


def process_concepts(*, dry_run: bool = False) -> int:
    """Process all concept docs."""
    concepts_dir = ROOT / "concepts"
    count = 0
    for md_file in sorted(concepts_dir.glob("*.md")):
        if md_file.name == "README.md":
            continue
        hub = build_hub_block(md_file, is_concept=True)
        if insert_hub(md_file, hub, dry_run=dry_run):
            print(f"  {'WOULD UPDATE' if dry_run else 'UPDATED'}: {md_file.relative_to(ROOT)}")
            count += 1
        else:
            print(f"  (unchanged): {md_file.relative_to(ROOT)}")
    return count


def process_level(level_dir: Path, *, dry_run: bool = False) -> int:
    """Process all project READMEs in a level directory."""
    count = 0
    for project_dir in sorted(level_dir.iterdir()):
        if not project_dir.is_dir():
            continue
        readme = project_dir / "README.md"
        if not readme.exists():
            continue
        concept_slug = find_concept_slug(readme) or ""
        hub = build_hub_block(readme, concept_slug=concept_slug)
        if insert_hub(readme, hub, dry_run=dry_run):
            print(f"  {'WOULD UPDATE' if dry_run else 'UPDATED'}: {readme.relative_to(ROOT)}")
            count += 1
        else:
            print(f"  (unchanged): {readme.relative_to(ROOT)}")
    return count


def main() -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(description="Generate modality hub tables")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    parser.add_argument("--level", type=str, help="Only process a specific level (e.g., '0', '00')")
    parser.add_argument("--concepts", action="store_true", help="Only process concept docs")
    args = parser.parse_args()

    total = 0

    if args.concepts or not args.level:
        print("=== CONCEPT DOCS ===")
        total += process_concepts(dry_run=args.dry_run)

    if not args.concepts:
        projects_dir = ROOT / "projects"
        for level_dir in sorted(projects_dir.iterdir()):
            if not level_dir.is_dir():
                continue
            if args.level and args.level not in level_dir.name:
                continue
            if re.match(r"level-", level_dir.name):
                print(f"\n=== {level_dir.name.upper()} ===")
                total += process_level(level_dir, dry_run=args.dry_run)
            elif level_dir.name in ("elite-track", "capstones"):
                print(f"\n=== {level_dir.name.upper()} ===")
                total += process_level(level_dir, dry_run=args.dry_run)
            elif level_dir.name == "modules":
                for module_dir in sorted(level_dir.iterdir()):
                    if module_dir.is_dir():
                        print(f"\n=== MODULE {module_dir.name} ===")
                        total += process_level(module_dir, dry_run=args.dry_run)

    action = "would update" if args.dry_run else "updated"
    print(f"\nDone. {total} files {action}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
