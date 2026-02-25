"""
Python replacement for check_markdown_links.sh

Verifies that all relative markdown links (./path.md) in .md files resolve
to existing files. Works on Windows without bash or ripgrep.

Usage:
    python tools/check_markdown_links.py
"""

import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

LINK_PATTERN = re.compile(r"\]\(\./([^)]+\.md)\)")


def check_markdown_links() -> bool:
    missing = False

    for md_file in sorted(ROOT_DIR.rglob("*.md")):
        # Skip PythonBootcamp directory
        if "PythonBootcamp" in str(md_file):
            continue

        try:
            content = md_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        for line_num, line in enumerate(content.splitlines(), start=1):
            for match in LINK_PATTERN.finditer(line):
                target = match.group(1)
                resolved = md_file.parent / target
                if not resolved.exists():
                    rel_path = md_file.relative_to(ROOT_DIR)
                    print(f"missing link target: {rel_path}:{line_num} -> ./{target}")
                    missing = True

    if missing:
        print("markdown link check failed")
        return False

    print("markdown relative links verified")
    return True


def main() -> None:
    success = check_markdown_links()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
