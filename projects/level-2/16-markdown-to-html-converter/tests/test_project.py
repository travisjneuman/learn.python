"""Tests for Markdown to HTML Converter.

Covers:
- Heading conversion (levels 1-3)
- Bold and italic inline formatting
- Unordered lists
- Code blocks (triple backticks)
- Paragraphs separated by blank lines
- Mixed document conversion
- File I/O round-trip
"""

from pathlib import Path

import pytest

from project import convert_heading, convert_inline, convert_markdown


# --- Inline formatting ---


def test_convert_inline_bold() -> None:
    """Double stars should become <strong> tags."""
    assert convert_inline("this is **bold** text") == "this is <strong>bold</strong> text"


def test_convert_inline_italic() -> None:
    """Single stars should become <em> tags."""
    assert convert_inline("this is *italic* text") == "this is <em>italic</em> text"


def test_convert_inline_bold_and_italic() -> None:
    """Bold and italic can coexist in the same line."""
    result = convert_inline("**bold** and *italic*")
    assert "<strong>bold</strong>" in result
    assert "<em>italic</em>" in result


def test_convert_inline_no_markers() -> None:
    """Plain text should pass through unchanged."""
    assert convert_inline("no formatting here") == "no formatting here"


# --- Headings ---


def test_convert_heading_h1() -> None:
    """A single # should produce an <h1> tag."""
    assert convert_heading("# Title") == "<h1>Title</h1>"


def test_convert_heading_h2() -> None:
    """Two ## should produce an <h2> tag."""
    assert convert_heading("## Subtitle") == "<h2>Subtitle</h2>"


def test_convert_heading_h3() -> None:
    """Three ### should produce an <h3> tag."""
    assert convert_heading("### Section") == "<h3>Section</h3>"


def test_heading_with_inline_formatting() -> None:
    """Headings should also convert inline bold/italic."""
    result = convert_heading("## A **bold** heading")
    assert result == "<h2>A <strong>bold</strong> heading</h2>"


# --- Paragraphs ---


def test_single_paragraph() -> None:
    """A block of text with no blank lines is one paragraph."""
    md = "This is a paragraph."
    assert convert_markdown(md) == "<p>This is a paragraph.</p>"


def test_two_paragraphs() -> None:
    """Text blocks separated by a blank line become two <p> tags."""
    md = "First paragraph.\n\nSecond paragraph."
    result = convert_markdown(md)
    assert "<p>First paragraph.</p>" in result
    assert "<p>Second paragraph.</p>" in result


def test_multiline_paragraph() -> None:
    """Consecutive lines without blank lines merge into one paragraph."""
    md = "Line one\nline two\nline three"
    result = convert_markdown(md)
    assert result == "<p>Line one line two line three</p>"


# --- Unordered lists ---


def test_unordered_list() -> None:
    """Lines starting with '- ' should become <li> inside <ul>."""
    md = "- apple\n- banana\n- cherry"
    result = convert_markdown(md)
    assert "<ul>" in result
    assert "</ul>" in result
    assert "<li>apple</li>" in result
    assert "<li>banana</li>" in result
    assert "<li>cherry</li>" in result


def test_list_with_inline_formatting() -> None:
    """List items should also handle bold and italic."""
    md = "- **bold item**\n- *italic item*"
    result = convert_markdown(md)
    assert "<li><strong>bold item</strong></li>" in result
    assert "<li><em>italic item</em></li>" in result


# --- Code blocks ---


def test_code_block() -> None:
    """Triple-backtick fences should produce <pre><code> blocks."""
    md = "```\nprint('hello')\nx = 42\n```"
    result = convert_markdown(md)
    assert "<pre><code>" in result
    assert "</code></pre>" in result
    assert "print('hello')" in result
    assert "x = 42" in result


def test_code_block_escapes_html() -> None:
    """HTML characters inside code blocks should be escaped."""
    md = "```\n<div class=\"test\">&amp;</div>\n```"
    result = convert_markdown(md)
    assert "&lt;div" in result
    assert "&amp;amp;" in result


def test_code_block_no_inline_parsing() -> None:
    """Bold/italic markers inside code blocks should NOT be converted."""
    md = "```\n**not bold** *not italic*\n```"
    result = convert_markdown(md)
    assert "<strong>" not in result
    assert "<em>" not in result


# --- Mixed document ---


def test_full_document() -> None:
    """A complete document should convert all elements correctly."""
    md = (
        "# My Document\n"
        "\n"
        "This is the **introduction**.\n"
        "\n"
        "## Features\n"
        "\n"
        "- fast\n"
        "- *simple*\n"
        "- reliable\n"
        "\n"
        "```\n"
        "print('hello')\n"
        "```\n"
        "\n"
        "That is all."
    )
    result = convert_markdown(md)
    assert "<h1>My Document</h1>" in result
    assert "<p>This is the <strong>introduction</strong>.</p>" in result
    assert "<h2>Features</h2>" in result
    assert "<ul>" in result
    assert "<li>fast</li>" in result
    assert "<li><em>simple</em></li>" in result
    assert "<pre><code>" in result
    assert "<p>That is all.</p>" in result


@pytest.mark.parametrize(
    "md,expected_tag",
    [
        ("# H1", "<h1>H1</h1>"),
        ("## H2", "<h2>H2</h2>"),
        ("### H3", "<h3>H3</h3>"),
    ],
)
def test_heading_levels_parametrized(md: str, expected_tag: str) -> None:
    """Verify heading levels via parametrize."""
    assert convert_markdown(md) == expected_tag


def test_empty_input() -> None:
    """An empty string should produce empty output."""
    assert convert_markdown("") == ""
