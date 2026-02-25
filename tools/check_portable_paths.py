"""
Python replacement for check_portable_paths.sh

Verifies that no markdown file contains user-specific absolute paths
(/Users/... or C:\\Users\\...). Works on Windows without bash or ripgrep.

Usage:
    python tools/check_portable_paths.py
"""

import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

# Match /Users/ (macOS/Linux) or X:\Users\ (Windows)
PATH_PATTERN = re.compile(r"/Users/|[A-Za-z]:\\Users\\")


def check_portable_paths() -> bool:
    found = False

    for md_file in sorted(ROOT_DIR.rglob("*.md")):
        # Skip PythonBootcamp directory
        if "PythonBootcamp" in str(md_file):
            continue

        try:
            content = md_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        for line_num, line in enumerate(content.splitlines(), start=1):
            if PATH_PATTERN.search(line):
                rel_path = md_file.relative_to(ROOT_DIR)
                print(f"non-portable path: {rel_path}:{line_num}: {line.strip()}")
                found = True

    if found:
        print("non-portable absolute user path found in markdown docs")
        return False

    print("portable path contract verified")
    return True


def main() -> None:
    success = check_portable_paths()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
