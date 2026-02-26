"""Validate that all modality hub links resolve to existing files.

CI check: scans every markdown file for '<!-- modality-hub-start -->' blocks
and verifies every relative link inside points to an existing file.

Usage:
    python tools/check_modality_hubs.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HUB_START = "<!-- modality-hub-start -->"
HUB_END = "<!-- modality-hub-end -->"

# Match markdown links: [text](path)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def check_file(file_path: Path) -> list[str]:
    """Check all links in the modality hub block of a file."""
    content = file_path.read_text(encoding="utf-8")
    errors: list[str] = []

    start_idx = content.find(HUB_START)
    if start_idx == -1:
        return errors

    end_idx = content.find(HUB_END, start_idx)
    if end_idx == -1:
        errors.append(f"{file_path.relative_to(ROOT)}: missing {HUB_END}")
        return errors

    hub_block = content[start_idx:end_idx]

    for match in LINK_RE.finditer(hub_block):
        link_text = match.group(1)
        link_target = match.group(2)

        # Skip anchors, external links, and "You are here" markers
        if link_target.startswith("#") or link_target.startswith("http"):
            continue

        # Strip query strings (e.g., ?ex=1 for browser links)
        clean_target = link_target.split("?")[0]

        # Resolve relative to the file's directory
        target_path = (file_path.parent / clean_target).resolve()

        if not target_path.exists():
            rel_path = file_path.relative_to(ROOT)
            errors.append(f"{rel_path}: broken link [{link_text}]({link_target})")

    return errors


def main() -> int:
    """Scan all markdown files for hub blocks and validate links."""
    all_errors: list[str] = []
    files_checked = 0
    hubs_found = 0

    for md_file in sorted(ROOT.rglob("*.md")):
        # Skip hidden dirs, venv, node_modules
        rel_str = str(md_file.relative_to(ROOT))
        if any(skip in rel_str for skip in [".venv", "node_modules", "__pycache__", ".git"]):
            continue

        files_checked += 1
        content = md_file.read_text(encoding="utf-8")
        if HUB_START in content:
            hubs_found += 1
            errors = check_file(md_file)
            all_errors.extend(errors)

    print(f"Checked {files_checked} markdown files, found {hubs_found} modality hubs.")

    if all_errors:
        print(f"\n{len(all_errors)} broken link(s) found:")
        for err in all_errors:
            print(f"  ERROR: {err}")
        return 1

    print("All modality hub links are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
