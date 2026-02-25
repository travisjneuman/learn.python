"""
SVG Level Badge Generator

Generates shields.io-style SVG badges for each curriculum level.
Badges use a color gradient from green (beginner) to gold (elite).

Usage:
    python tools/generate_badges.py              # generate all badges
    python tools/generate_badges.py --preview    # print badge paths only

No external dependencies — uses only Python standard library.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
BADGES_DIR = REPO_ROOT / "badges"

# Badge definitions: (filename, label, message, left_color, right_color)
BADGE_DEFS = [
    ("level-00", "Level 00", "Absolute Beginner", "#555", "#4c1"),
    ("level-0", "Level 0", "Terminal & I/O", "#555", "#44cc11"),
    ("level-1", "Level 1", "Functions", "#555", "#57d114"),
    ("level-2", "Level 2", "Collections", "#555", "#6ad617"),
    ("level-3", "Level 3", "File Automation", "#555", "#7dda1a"),
    ("level-4", "Level 4", "JSON & Data", "#555", "#97d31c"),
    ("level-5", "Level 5", "Exceptions", "#555", "#a4cf1e"),
    ("level-6", "Level 6", "SQL Basics", "#555", "#b7c820"),
    ("level-7", "Level 7", "ETL Pipelines", "#555", "#c9c023"),
    ("level-8", "Level 8", "APIs & Async", "#555", "#d4b526"),
    ("level-9", "Level 9", "Advanced", "#555", "#dfaa28"),
    ("level-10", "Level 10", "Systems", "#555", "#e69d2b"),
    ("elite", "Elite Track", "Complete", "#555", "#f5a623"),
    ("modules", "Expansion", "Modules", "#555", "#e8b830"),
    ("complete", "Python Mastery", "Complete", "#1a1a2e", "#ffd700"),
]


def estimate_text_width(text: str) -> int:
    """Estimate pixel width of text at ~11px font size (shields.io style)."""
    # Rough character widths (proportional approximation)
    narrow = set("fijlrt!|()[]{}.,;: '")
    wide = set("mwMWGOQD@%")
    width = 0
    for ch in text:
        if ch in narrow:
            width += 5
        elif ch in wide:
            width += 9
        elif ch.isupper():
            width += 8
        else:
            width += 6.5
    return round(width) + 12  # padding


def generate_badge_svg(
    label: str, message: str, left_color: str, right_color: str
) -> str:
    """Generate a shields.io-style flat SVG badge."""
    label_width = estimate_text_width(label)
    message_width = estimate_text_width(message)
    total_width = label_width + message_width

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="20" role="img" aria-label="{label}: {message}">
  <title>{label}: {message}</title>
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="r">
    <rect width="{total_width}" height="20" rx="3" fill="#fff"/>
  </clipPath>
  <g clip-path="url(#r)">
    <rect width="{label_width}" height="20" fill="{left_color}"/>
    <rect x="{label_width}" width="{message_width}" height="20" fill="{right_color}"/>
    <rect width="{total_width}" height="20" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="110">
    <text aria-hidden="true" x="{label_width * 5}" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="{(label_width - 10) * 10}">{label}</text>
    <text x="{label_width * 5}" y="140" transform="scale(.1)" fill="#fff" textLength="{(label_width - 10) * 10}">{label}</text>
    <text aria-hidden="true" x="{(label_width + message_width / 2) * 10}" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="{(message_width - 10) * 10}">{message}</text>
    <text x="{(label_width + message_width / 2) * 10}" y="140" transform="scale(.1)" fill="#fff" textLength="{(message_width - 10) * 10}">{message}</text>
  </g>
</svg>'''


def main() -> None:
    preview = "--preview" in sys.argv

    BADGES_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Generating {len(BADGE_DEFS)} badges...\n")

    for filename, label, message, left_color, right_color in BADGE_DEFS:
        output_path = BADGES_DIR / f"{filename}.svg"

        if preview:
            print(f"  {output_path.relative_to(REPO_ROOT)}")
            continue

        svg = generate_badge_svg(label, message, left_color, right_color)
        output_path.write_text(svg, encoding="utf-8")
        print(f"  Created: {output_path.relative_to(REPO_ROOT)}")

    print(f"\nDone! Badges saved to {BADGES_DIR.relative_to(REPO_ROOT)}/")

    if not preview:
        # Generate README for badges directory
        readme_content = "# Level Badges\n\n"
        readme_content += "SVG badges for each curriculum level. "
        readme_content += "Add these to your GitHub profile or project README.\n\n"
        readme_content += "## Usage\n\n"
        readme_content += "Copy the badge image into your README:\n\n"
        readme_content += "```markdown\n"
        readme_content += "![Level 0 Complete](badges/level-0.svg)\n"
        readme_content += "```\n\n"
        readme_content += "## Available Badges\n\n"
        readme_content += "| Badge | File |\n"
        readme_content += "|-------|------|\n"
        for filename, label, message, _, _ in BADGE_DEFS:
            readme_content += f"| {label}: {message} | `{filename}.svg` |\n"

        readme_path = BADGES_DIR / "README.md"
        readme_path.write_text(readme_content, encoding="utf-8")
        print(f"  Created: {readme_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
