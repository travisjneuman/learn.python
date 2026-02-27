"""Python replacement for check_level_index_contract.sh

Verifies that each level directory has a README with proper home links,
project links, and navigation. Works on Windows without bash or ripgrep.

Usage:
    python tools/check_level_index_contract.py
"""

import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
PROJECTS_DIR = ROOT_DIR / "projects"


def check() -> bool:
    fail = False

    # --- projects/README.md ---
    projects_index = PROJECTS_DIR / "README.md"
    if not projects_index.exists():
        print("missing projects index: projects/README.md")
        return False

    index_text = projects_index.read_text(encoding="utf-8", errors="replace")
    index_lines = index_text.splitlines()

    # Home link on second non-blank line
    non_blank = [line.strip() for line in index_lines if line.strip()]
    if len(non_blank) < 2 or non_blank[1] != "Home: [README](../README.md)":
        print("bad projects index home link")
        fail = True

    # Each level linked
    for level in range(11):
        pattern = f"- [level-{level}](./level-{level}/README.md)"
        if pattern not in index_text:
            print(f"missing level link in projects index: level-{level}")
            fail = True

    # --- Per-level checks ---
    for level in range(11):
        level_readme = PROJECTS_DIR / f"level-{level}" / "README.md"
        if not level_readme.exists():
            print(f"missing level readme: projects/level-{level}/README.md")
            fail = True
            continue

        content = level_readme.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()

        # Home link
        non_blank = [line.strip() for line in lines if line.strip()]
        if len(non_blank) < 2 or non_blank[1] != "Home: [README](../../README.md)":
            print(f"bad home line: projects/level-{level}/README.md")
            fail = True

        # Count project links (pattern: - [NN-slug](./NN-slug/README.md) - description)
        project_links = re.findall(
            r"^- \[\d{2}-[^\]]+\]\(\./\d{2}-[^)]+/README\.md\)",
            content,
            re.MULTILINE,
        )
        # Count actual project directories to validate against
        actual_dirs = sorted(
            d.name
            for d in (PROJECTS_DIR / f"level-{level}").iterdir()
            if d.is_dir() and re.match(r"\d{2}-", d.name)
        )
        expected_count = len(actual_dirs)
        if len(project_links) != expected_count:
            print(
                f"bad project link count in projects/level-{level}/README.md: "
                f"expected {expected_count}, got {len(project_links)}"
            )
            fail = True

        # Validate each linked project README exists
        for match in re.finditer(
            r"^- \[\d{2}-[^\]]+\]\(\./([\d]{2}-[^)]+/README\.md)\)",
            content,
            re.MULTILINE,
        ):
            rel_path = match.group(1)
            target = PROJECTS_DIR / f"level-{level}" / rel_path
            if not target.exists():
                print(f"missing linked project README in level-{level} index: {rel_path}")
                fail = True

        # ## Next heading
        if "## Next" not in content:
            print(f"missing ## Next in projects/level-{level}/README.md")
            fail = True

        # Continue link to next level
        if level < 10:
            next_level = level + 1
            continue_pattern = f"- Continue to [level-{next_level}](../level-{next_level}/README.md)."
            if continue_pattern not in content:
                print(f"missing continue link in projects/level-{level}/README.md")
                fail = True

        # Return link
        return_pattern = "- Return to [projects index](../README.md)."
        if return_pattern not in content:
            print(f"missing return link in projects/level-{level}/README.md")
            fail = True

    if fail:
        print("level index contract check failed")
        return False

    print("level index contract verified")
    return True


def main() -> None:
    success = check()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
