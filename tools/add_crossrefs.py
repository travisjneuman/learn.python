"""
Cross-Reference Linker — Adds "Related Concepts" to project READMEs
and "Practice This" to concept docs.

Run once:
    python tools/add_crossrefs.py

This script is idempotent — it detects existing sections and skips them.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PROJECTS_DIR = REPO_ROOT / "projects"
CONCEPTS_DIR = REPO_ROOT / "concepts"

# ── Concept-to-keyword mapping ──────────────────────────────────────────────
# Maps concept doc filenames to keywords that indicate relevance.
CONCEPT_KEYWORDS = {
    "what-is-a-variable": [
        "variable", "assign", "name", "value", "store", "hello",
        "first-steps", "absolute-beginner", "level-00",
    ],
    "how-loops-work": [
        "loop", "for", "while", "repeat", "iterate", "range",
        "menu-loop", "checklist", "duplicate", "batch",
    ],
    "functions-explained": [
        "function", "def", "return", "parameter", "argument",
        "validator", "checker", "converter", "builder", "calculator",
        "modular", "level-1",
    ],
    "collections-explained": [
        "list", "dict", "set", "tuple", "collection", "array",
        "counter", "frequency", "duplicate", "sort", "group",
        "level-2",
    ],
    "files-and-paths": [
        "file", "read", "write", "path", "csv", "directory",
        "reader", "writer", "finder", "summarizer", "log",
        "level-3", "automation",
    ],
    "errors-and-debugging": [
        "error", "exception", "debug", "try", "except", "raise",
        "handle", "recover", "fault", "level-5",
    ],
    "types-and-conversions": [
        "type", "int", "float", "str", "bool", "convert", "cast",
        "temperature", "number", "classifier",
    ],
    "how-imports-work": [
        "import", "module", "package", "library", "from",
        "toolkit", "plugin", "loader",
    ],
    "classes-and-objects": [
        "class", "object", "oop", "inherit", "method",
        "registry", "emitter", "builder", "card",
    ],
    "decorators-explained": [
        "decorator", "wrapper", "timer", "retry", "cache",
        "rate-limit",
    ],
    "virtual-environments": [
        "venv", "virtual", "pip", "install", "dependency",
        "requirements",
    ],
    "the-terminal-deeper": [
        "terminal", "cli", "command", "shell", "bash",
        "prompt", "arg", "level-0",
    ],
    "http-explained": [
        "http", "request", "response", "url", "status",
        "header", "get", "post", "api", "fetch", "webhook",
        "web-scraping",
    ],
    "api-basics": [
        "api", "rest", "endpoint", "json", "request",
        "client", "auth", "token", "crud",
    ],
    "async-explained": [
        "async", "await", "concurrent", "parallel", "asyncio",
        "producer", "consumer", "server",
    ],
}

# ── Level-to-concept mapping (baseline concepts for each level) ─────────────
LEVEL_CONCEPTS = {
    "level-00-absolute-beginner": [
        "what-is-a-variable", "how-loops-work", "types-and-conversions",
    ],
    "level-0": [
        "what-is-a-variable", "how-loops-work", "the-terminal-deeper",
        "types-and-conversions", "files-and-paths",
    ],
    "level-1": [
        "functions-explained", "how-imports-work", "the-terminal-deeper",
    ],
    "level-2": [
        "collections-explained", "how-loops-work", "functions-explained",
    ],
    "level-3": [
        "files-and-paths", "errors-and-debugging",
    ],
    "level-4": [
        "files-and-paths", "api-basics", "types-and-conversions",
    ],
    "level-5": [
        "errors-and-debugging", "classes-and-objects",
    ],
    "level-6": [
        "files-and-paths", "collections-explained",
    ],
    "level-7": [
        "files-and-paths", "errors-and-debugging", "how-imports-work",
    ],
    "level-8": [
        "http-explained", "api-basics", "async-explained",
    ],
    "level-9": [
        "decorators-explained", "classes-and-objects", "async-explained",
    ],
    "level-10": [
        "api-basics", "async-explained", "errors-and-debugging",
    ],
    "elite-track": [
        "classes-and-objects", "decorators-explained", "async-explained",
    ],
}

# ── Module-to-concept mapping ───────────────────────────────────────────────
MODULE_CONCEPTS = {
    "01-web-scraping": ["http-explained", "files-and-paths"],
    "02-cli-tools": ["the-terminal-deeper", "functions-explained", "how-imports-work"],
    "03-rest-apis-consuming": ["http-explained", "api-basics", "errors-and-debugging"],
    "04-fastapi-web-apps": ["api-basics", "http-explained", "classes-and-objects"],
    "05-async-python": ["async-explained", "functions-explained"],
    "06-databases-orm": ["files-and-paths", "classes-and-objects", "collections-explained"],
    "07-data-analysis": ["collections-explained", "files-and-paths", "types-and-conversions"],
    "08-advanced-testing": ["functions-explained", "decorators-explained", "errors-and-debugging"],
    "09-docker-deployment": ["the-terminal-deeper", "virtual-environments"],
    "10-django-full-stack": ["api-basics", "http-explained", "classes-and-objects"],
    "11-package-publishing": ["how-imports-work", "virtual-environments"],
    "12-cloud-deployment": ["the-terminal-deeper", "api-basics"],
}

MARKER = "## Related Concepts"
PRACTICE_MARKER = "## Practice This"


def get_relative_path(from_file: Path, to_file: Path) -> str:
    """Get relative path from one file to another."""
    try:
        return str(to_file.relative_to(from_file.parent)).replace("\\", "/")
    except ValueError:
        # Not a subpath — compute manually
        from_parts = from_file.parent.parts
        to_parts = to_file.parts
        # Find common prefix
        common = 0
        for a, b in zip(from_parts, to_parts):
            if a == b:
                common += 1
            else:
                break
        ups = len(from_parts) - common
        remainder = to_parts[common:]
        return "/".join([".."] * ups + list(remainder))


def concept_display_name(slug: str) -> str:
    """Convert concept slug to display name."""
    return slug.replace("-", " ").title().replace("And", "and").replace("Is A", "is a")


def match_concepts_for_project(project_dir: Path) -> list[str]:
    """Determine which concepts are relevant to a project."""
    project_name = project_dir.name.lower()
    # Determine level/module
    parent = project_dir.parent.name.lower()
    grandparent = project_dir.parent.parent.name.lower() if project_dir.parent.parent != PROJECTS_DIR.parent else ""

    matched = set()

    # Add level baseline concepts
    if parent in LEVEL_CONCEPTS:
        matched.update(LEVEL_CONCEPTS[parent])
    elif grandparent == "modules" and parent in MODULE_CONCEPTS:
        matched.update(MODULE_CONCEPTS[parent])

    # Keyword matching from project name
    for concept, keywords in CONCEPT_KEYWORDS.items():
        for kw in keywords:
            if kw in project_name or kw in parent:
                matched.add(concept)
                break

    # Also scan the README Focus section for keywords
    readme = project_dir / "README.md"
    if readme.exists():
        content = readme.read_text(encoding="utf-8", errors="replace")
        focus_match = re.search(r"## Focus\s*\n(.*?)(?:\n##|\Z)", content, re.DOTALL)
        if focus_match:
            focus_text = focus_match.group(1).lower()
            for concept, keywords in CONCEPT_KEYWORDS.items():
                for kw in keywords:
                    if kw in focus_text:
                        matched.add(concept)
                        break

    # Limit to 4 most relevant (prioritize keyword matches over level defaults)
    return sorted(matched)[:4]


def add_crossrefs_to_project(readme_path: Path) -> bool:
    """Add Related Concepts section to a project README. Returns True if modified."""
    content = readme_path.read_text(encoding="utf-8", errors="replace")

    if MARKER in content:
        return False  # Already has cross-references

    project_dir = readme_path.parent
    concepts = match_concepts_for_project(project_dir)

    if not concepts:
        return False

    # Build the section
    lines = [f"\n---\n\n{MARKER}\n"]
    for concept in concepts:
        concept_path = CONCEPTS_DIR / f"{concept}.md"
        if concept_path.exists():
            rel = get_relative_path(readme_path, concept_path)
            name = concept_display_name(concept)
            lines.append(f"- [{name}]({rel})")

    # Add quiz link if available
    quiz_dir = CONCEPTS_DIR / "quizzes"
    for concept in concepts:
        quiz_path = quiz_dir / f"{concept}-quiz.py"
        if quiz_path.exists():
            rel = get_relative_path(readme_path, quiz_path)
            name = concept_display_name(concept)
            lines.append(f"- [Quiz: {name}]({rel})")
            break  # Just link one quiz to keep it focused

    section = "\n".join(lines) + "\n"

    # Insert before the "Next" section if it exists, otherwise append
    if "\n## Next\n" in content:
        content = content.replace("\n## Next\n", f"{section}\n## Next\n")
    else:
        content = content.rstrip() + "\n" + section

    readme_path.write_text(content, encoding="utf-8")
    return True


def add_practice_to_concept(concept_path: Path) -> bool:
    """Add Practice This section to a concept doc. Returns True if modified."""
    content = concept_path.read_text(encoding="utf-8", errors="replace")

    if PRACTICE_MARKER in content:
        return False

    slug = concept_path.stem  # e.g. "what-is-a-variable"

    # Find projects that reference this concept
    related_projects = []
    for readme_path in sorted(PROJECTS_DIR.rglob("README.md")):
        if ".pytest_cache" in str(readme_path):
            continue
        project_dir = readme_path.parent
        if project_dir == PROJECTS_DIR:
            continue
        # Check if this is an index README (parent is a level dir)
        if project_dir.parent == PROJECTS_DIR or (project_dir.parent.parent == PROJECTS_DIR and project_dir.parent.name == "modules"):
            continue

        concepts = match_concepts_for_project(project_dir)
        if slug in concepts:
            rel = get_relative_path(concept_path, readme_path)
            name = project_dir.name.replace("-", " ").title()
            # Include level/module context
            parent = project_dir.parent.name
            if parent.startswith("level-"):
                ctx = parent.replace("-", " ").title()
            else:
                ctx = f"Module: {parent.replace('-', ' ').title()}"
            related_projects.append((f"{ctx} / {name}", rel))

    if not related_projects:
        return False

    # Build section
    lines = [f"\n---\n\n{PRACTICE_MARKER}\n"]

    # Limit to 10 most relevant projects
    for name, rel in related_projects[:10]:
        lines.append(f"- [{name}]({rel})")

    # Add quiz link
    quiz_path = CONCEPTS_DIR / "quizzes" / f"{slug}-quiz.py"
    if quiz_path.exists():
        rel = get_relative_path(concept_path, quiz_path)
        lines.append(f"\n**Quick check:** [Take the quiz](quizzes/{slug}-quiz.py)")

    # Add flashcard link — find relevant deck
    flashcard_dir = REPO_ROOT / "practice" / "flashcards"
    for deck in sorted(flashcard_dir.glob("level-*-cards.json")):
        lines.append(f"\n**Review:** [Flashcard decks]({get_relative_path(concept_path, flashcard_dir / 'README.md')})")
        break

    # Add challenge link
    challenge_dir = REPO_ROOT / "practice" / "challenges"
    if challenge_dir.exists():
        lines.append(f"**Practice reps:** [Coding challenges]({get_relative_path(concept_path, challenge_dir / 'README.md')})")

    section = "\n".join(lines) + "\n"
    content = content.rstrip() + "\n" + section
    concept_path.write_text(content, encoding="utf-8")
    return True


def update_concepts_readme() -> bool:
    """Update concepts/README.md with links to quizzes and flashcards."""
    readme = CONCEPTS_DIR / "README.md"
    if not readme.exists():
        return False

    content = readme.read_text(encoding="utf-8", errors="replace")

    if "## Practice Tools" in content:
        return False

    section = """
---

## Practice Tools

| Tool | Description | How to use |
|------|-------------|------------|
| **Concept Quizzes** | Interactive terminal quizzes for each concept | `python concepts/quizzes/<name>-quiz.py` |
| **Flashcard Decks** | Spaced repetition cards organized by level | `python practice/flashcards/review-runner.py` |
| **Coding Challenges** | Short focused exercises (beginner + intermediate) | See `practice/challenges/README.md` |
| **Diagnostic Assessments** | Test your readiness before starting a level | `python tools/diagnose.py` |

### Available Quizzes

Each concept doc has a matching quiz in `concepts/quizzes/`:

"""
    quiz_dir = CONCEPTS_DIR / "quizzes"
    if quiz_dir.exists():
        for quiz in sorted(quiz_dir.glob("*-quiz.py")):
            name = quiz.stem.replace("-quiz", "").replace("-", " ").title()
            section += f"- [{name}](quizzes/{quiz.name})\n"

    content = content.rstrip() + "\n" + section
    readme.write_text(content, encoding="utf-8")
    return True


def main():
    modified_projects = 0
    modified_concepts = 0
    skipped = 0

    # Process all project READMEs
    print("Adding cross-references to project READMEs...")
    for readme_path in sorted(PROJECTS_DIR.rglob("README.md")):
        if ".pytest_cache" in str(readme_path):
            continue
        # Skip index READMEs (directly in level/module dirs)
        project_dir = readme_path.parent
        if project_dir == PROJECTS_DIR:
            continue
        if project_dir.parent == PROJECTS_DIR:
            continue  # Level index README
        if project_dir.parent.parent == PROJECTS_DIR and project_dir.parent.name == "modules":
            continue  # Module index README

        if add_crossrefs_to_project(readme_path):
            modified_projects += 1
        else:
            skipped += 1

    print(f"  Modified: {modified_projects}, Skipped: {skipped}")

    # Process concept docs
    print("\nAdding practice links to concept docs...")
    for concept_path in sorted(CONCEPTS_DIR.glob("*.md")):
        if concept_path.name == "README.md":
            continue
        if add_practice_to_concept(concept_path):
            modified_concepts += 1
            print(f"  + {concept_path.name}")

    # Update concepts README
    print("\nUpdating concepts/README.md...")
    if update_concepts_readme():
        print("  + Added Practice Tools section")

    print(f"\nDone. {modified_projects} project READMEs + {modified_concepts} concept docs updated.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Cross-reference linker. Adds 'Related Concepts' sections to "
        "project READMEs and 'Practice This' sections to concept docs. "
        "Idempotent — skips files that already have cross-references.",
    )
    parser.parse_args()
    main()
