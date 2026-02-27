"""Level 2 project: Markdown to HTML Converter.

Heavily commented beginner-friendly script:
- parse Markdown syntax into HTML elements,
- handle headings, bold, italic, lists, code blocks, paragraphs,
- read a .md file from command-line args and write an .html file.

Skills practiced: string methods (startswith, strip, replace),
state machines (tracking code blocks), regular expressions for
inline patterns, file I/O, command-line arguments.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def convert_inline(text: str) -> str:
    """Convert inline Markdown formatting to HTML.

    Handles bold (**text**) and italic (*text*) markers.
    Bold is checked first so **double stars** are not mistaken
    for two italic markers.

    Returns:
        The text with inline Markdown replaced by HTML tags.
    """
    # Bold: **text** -> <strong>text</strong>
    # The regex uses a non-greedy match (.+?) so it stops at the
    # first closing ** rather than consuming the whole line.
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)

    # Italic: *text* -> <em>text</em>
    # This runs AFTER bold so leftover single stars are italic.
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)

    return text


def convert_heading(line: str) -> str:
    """Convert a Markdown heading line to an HTML heading tag.

    Supports levels 1 through 6 (# through ######).

    Returns:
        An HTML heading string like '<h2>Title</h2>'.
    """
    # Count leading '#' characters to determine heading level.
    level = 0
    for ch in line:
        if ch == "#":
            level += 1
        else:
            break

    # Clamp to valid HTML heading levels (1-6).
    level = min(level, 6)

    # Everything after the '#' characters is the heading text.
    content = line[level:].strip()
    content = convert_inline(content)

    return f"<h{level}>{content}</h{level}>"


def convert_markdown(text: str) -> str:
    """Convert a full Markdown document to HTML.

    Processes the text line by line, tracking state for multi-line
    constructs like code blocks and unordered lists.

    Returns:
        A complete HTML string.
    """
    lines = text.split("\n")
    html_parts: list[str] = []

    in_code_block = False
    in_list = False
    paragraph_lines: list[str] = []

    def flush_paragraph() -> None:
        """Emit any accumulated paragraph lines as a <p> tag."""
        if paragraph_lines:
            joined = " ".join(paragraph_lines)
            joined = convert_inline(joined)
            html_parts.append(f"<p>{joined}</p>")
            paragraph_lines.clear()

    def close_list() -> None:
        """Close an open unordered list."""
        nonlocal in_list
        if in_list:
            html_parts.append("</ul>")
            in_list = False

    for line in lines:
        stripped = line.rstrip()

        # --- Code block toggle (triple backticks) ---
        if stripped.startswith("```"):
            if not in_code_block:
                # Opening a code block. Flush any open paragraph/list.
                flush_paragraph()
                close_list()
                # Text after ``` is the optional language hint — ignored.
                html_parts.append("<pre><code>")
                in_code_block = True
            else:
                # Closing the code block.
                html_parts.append("</code></pre>")
                in_code_block = False
            continue

        # Inside a code block, emit lines verbatim (no Markdown parsing).
        if in_code_block:
            # Escape HTML special characters so code displays correctly.
            safe = stripped.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            html_parts.append(safe)
            continue

        # --- Blank line: ends paragraphs and lists ---
        if not stripped:
            flush_paragraph()
            close_list()
            continue

        # --- Headings (lines starting with #) ---
        if stripped.startswith("#"):
            flush_paragraph()
            close_list()
            html_parts.append(convert_heading(stripped))
            continue

        # --- Unordered list items (lines starting with '- ') ---
        if stripped.startswith("- "):
            flush_paragraph()
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            item_text = stripped[2:].strip()
            item_text = convert_inline(item_text)
            html_parts.append(f"<li>{item_text}</li>")
            continue

        # --- Paragraph text (anything else) ---
        paragraph_lines.append(stripped)

    # End of document — flush any remaining open constructs.
    flush_paragraph()
    close_list()
    if in_code_block:
        html_parts.append("</code></pre>")

    return "\n".join(html_parts)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert a Markdown file to HTML"
    )
    parser.add_argument(
        "input",
        help="Path to the Markdown (.md) file to convert",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path for the output HTML file (default: same name with .html)",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point: read Markdown, convert, write HTML."""
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    markdown_text = input_path.read_text(encoding="utf-8")
    html_output = convert_markdown(markdown_text)

    # Determine output path: use --output if given, else replace extension.
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix(".html")

    output_path.write_text(html_output, encoding="utf-8")
    print(f"Converted: {input_path} -> {output_path}")
    print(f"Output size: {len(html_output)} characters")


if __name__ == "__main__":
    main()
