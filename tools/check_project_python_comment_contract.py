"""Python replacement for check_project_python_comment_contract.sh

Verifies that each project.py starts with a docstring and has a minimum
number of comment lines. Also checks test_project.py files. Works on
Windows without bash or ripgrep.

Usage:
    python tools/check_project_python_comment_contract.py
"""

import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


def first_non_empty_line(text: str) -> str:
    """Return the first non-blank line from text."""
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


def count_comment_lines(text: str) -> int:
    """Count lines that are comments (start with optional whitespace + #)."""
    return sum(1 for line in text.splitlines() if re.match(r"^\s*#", line))


def check() -> bool:
    fail = False

    # --- project.py checks ---
    project_files = sorted(
        ROOT_DIR.glob("projects/level-*/[0-9][0-9]-*/project.py")
    )
    project_count = len(project_files)

    for pf in project_files:
        text = pf.read_text(encoding="utf-8", errors="replace")
        rel = pf.relative_to(ROOT_DIR).as_posix()

        first = first_non_empty_line(text)
        if not first.startswith('"""'):
            print(f"missing module docstring at top: {rel}")
            fail = True

        comments = count_comment_lines(text)
        if comments < 3:
            print(f"too few comment lines in {rel}: {comments} (min 3)")
            fail = True

    if project_count != 165:
        print(f"unexpected project.py count: expected 165, found {project_count}")
        fail = True

    # --- test_project.py checks ---
    test_files = sorted(
        ROOT_DIR.glob("projects/level-*/[0-9][0-9]-*/tests/test_project.py")
    )
    test_count = len(test_files)

    for tf in test_files:
        text = tf.read_text(encoding="utf-8", errors="replace")
        rel = tf.relative_to(ROOT_DIR).as_posix()

        first = first_non_empty_line(text)
        if not first.startswith('"""'):
            print(f"missing test module docstring at top: {rel}")
            fail = True

        comments = count_comment_lines(text)
        if comments < 2:
            print(f"too few comment lines in {rel}: {comments} (min 2)")
            fail = True

    if test_count != 165:
        print(f"unexpected test_project.py count: expected 165, found {test_count}")
        fail = True

    if fail:
        print("project python comment/docstring contract check failed")
        return False

    print("project python comment/docstring contract verified")
    return True


def main() -> None:
    success = check()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
