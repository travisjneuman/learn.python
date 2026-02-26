"""Report markdown files exceeding a line-count threshold with split-point suggestions.

Scans concept docs and root docs for files that are too long for
comfortable reading, and suggests natural split points at ## headings.

Usage:
    python tools/audit_doc_length.py
    python tools/audit_doc_length.py --threshold 150
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_THRESHOLD = 200


def analyze_file(file_path: Path, threshold: int) -> dict | None:
    """Analyze a markdown file and return info if it exceeds the threshold."""
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    line_count = len(lines)

    if line_count <= threshold:
        return None

    # Find ## headings as potential split points
    headings: list[tuple[int, str]] = []
    for i, line in enumerate(lines, 1):
        if re.match(r"^## ", line):
            headings.append((i, line.strip()))

    return {
        "path": file_path.relative_to(ROOT),
        "lines": line_count,
        "over_by": line_count - threshold,
        "headings": headings,
    }


def main() -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(description="Audit markdown doc lengths")
    parser.add_argument(
        "--threshold", type=int, default=DEFAULT_THRESHOLD,
        help=f"Line count threshold (default: {DEFAULT_THRESHOLD})",
    )
    args = parser.parse_args()

    results: list[dict] = []

    # Check concept docs
    concepts_dir = ROOT / "concepts"
    if concepts_dir.exists():
        for md_file in sorted(concepts_dir.glob("*.md")):
            if md_file.name == "README.md":
                continue
            result = analyze_file(md_file, args.threshold)
            if result:
                results.append(result)

    # Check root docs
    for md_file in sorted(ROOT.glob("*.md")):
        if md_file.name in ("README.md", "CLAUDE.md", "PROGRESS.md"):
            continue
        result = analyze_file(md_file, args.threshold)
        if result:
            results.append(result)

    # Check curriculum docs
    curriculum_dir = ROOT / "curriculum"
    if curriculum_dir.exists():
        for md_file in sorted(curriculum_dir.glob("*.md")):
            result = analyze_file(md_file, args.threshold)
            if result:
                results.append(result)

    # Report
    if not results:
        print(f"All docs are under {args.threshold} lines. No action needed.")
        return 0

    print(f"Found {len(results)} file(s) exceeding {args.threshold} lines:\n")

    for r in sorted(results, key=lambda x: x["lines"], reverse=True):
        print(f"  {r['path']} — {r['lines']} lines (+{r['over_by']} over threshold)")
        if r["headings"]:
            print(f"    Potential split points ({len(r['headings'])} headings):")
            for line_num, heading in r["headings"][:8]:
                print(f"      Line {line_num}: {heading}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
