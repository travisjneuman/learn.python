"""
Python replacement for check_project_readme_contract.sh

Verifies that all project READMEs have required headings, home links,
portable path notes, and next-link format. Works on Windows without
bash or ripgrep.

Usage:
    python tools/check_project_contract.py
"""

import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
PROJECTS_DIR = ROOT_DIR / "projects"

REQUIRED_HEADINGS = [
    "## Run (copy/paste)",
    "## Expected terminal output",
    "## Expected artifacts",
    "## Alter it (required)",
    "## Break it (required)",
    "## Fix it (required)",
    "## Explain it (teach-back)",
    "## Mastery check",
    "## Next",
]

REPO_ROOT_NOTE = (
    "Use `<repo-root>` as the folder containing this repository's `README.md`."
)

HOME_LINK_RE = re.compile(r"^Home: \[README\]\(\.\./\.\./\.\./README\.md\)$")
NEXT_LINK_RE = re.compile(
    r"^Go back to \[Level [0-9]+ index\]\(\.\./README\.md\)\.$"
)

EXPECTED_COUNT = 165


def check_project_readmes() -> bool:
    fail = False
    count = 0

    for level_dir in sorted(PROJECTS_DIR.glob("level-*")):
        if not level_dir.is_dir():
            continue
        # Skip level-00 (no project READMEs with this contract)
        if "level-00" in level_dir.name:
            continue

        for project_dir in sorted(level_dir.iterdir()):
            if not project_dir.is_dir():
                continue
            if not re.match(r"\d{2}-", project_dir.name):
                continue

            readme = project_dir / "README.md"
            if not readme.exists():
                print(f"missing README: {readme.relative_to(ROOT_DIR)}")
                fail = True
                continue

            count += 1
            content = readme.read_text(encoding="utf-8", errors="replace")
            lines = content.splitlines()

            # Check home link on line 2
            if len(lines) >= 2:
                home_line = lines[1].strip()
                if not HOME_LINK_RE.match(home_line):
                    print(f"bad home link: {readme.relative_to(ROOT_DIR)}")
                    fail = True

            # Check required headings
            for heading in REQUIRED_HEADINGS:
                if heading not in content:
                    print(
                        f"missing heading '{heading}': "
                        f"{readme.relative_to(ROOT_DIR)}"
                    )
                    fail = True

            # Check repo-root note
            if REPO_ROOT_NOTE not in content:
                print(
                    f"missing <repo-root> note: {readme.relative_to(ROOT_DIR)}"
                )
                fail = True

            # Check next link format
            has_valid_next = False
            for line in lines:
                if NEXT_LINK_RE.match(line.strip()):
                    has_valid_next = True
                    break
            if not has_valid_next:
                print(
                    f"bad next link format: {readme.relative_to(ROOT_DIR)}"
                )
                fail = True

    if count != EXPECTED_COUNT:
        print(
            f"unexpected project README count: expected {EXPECTED_COUNT}, "
            f"found {count}"
        )
        fail = True

    if fail:
        print("project README contract check failed")
        return False

    print(f"project README contract verified (count={count})")
    return True


def main() -> None:
    success = check_project_readmes()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
