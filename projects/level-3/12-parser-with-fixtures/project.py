"""Level 3 project: Parser With Fixtures.

Builds a configurable text parser that handles multiple formats
(INI-like, key=value, CSV). Tests use pytest fixtures to create
temporary input files for each format.

Skills practiced: pytest fixtures, text parsing, dataclasses,
typing basics, logging, file I/O patterns.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ParsedSection:
    """A section from an INI-style file."""
    name: str
    entries: dict[str, str] = field(default_factory=dict)


@dataclass
class ParseResult:
    """Result of parsing a file."""
    format: str
    source: str
    sections: list[ParsedSection] = field(default_factory=list)
    records: list[dict] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    line_count: int = 0


def parse_ini(text: str) -> ParseResult:
    """Parse INI-style text into sections with key-value pairs.

    Format:
        [section_name]
        key = value
        another_key = another_value
    """
    sections: list[ParsedSection] = []
    current: Optional[ParsedSection] = None
    errors: list[str] = []
    line_count = 0

    for line_num, line in enumerate(text.splitlines(), 1):
        line_count += 1
        stripped = line.strip()

        # Skip blank lines and comments.
        if not stripped or stripped.startswith("#") or stripped.startswith(";"):
            continue

        # Section header.
        match = re.match(r"^\[(.+)\]$", stripped)
        if match:
            current = ParsedSection(name=match.group(1).strip())
            sections.append(current)
            continue

        # Key-value pair.
        if "=" in stripped:
            key, _, value = stripped.partition("=")
            if current is None:
                current = ParsedSection(name="default")
                sections.append(current)
            current.entries[key.strip()] = value.strip()
        else:
            errors.append(f"Line {line_num}: Unrecognised format: {stripped!r}")

    return ParseResult(
        format="ini",
        source="text",
        sections=sections,
        line_count=line_count,
        errors=errors,
    )


def parse_key_value(text: str, delimiter: str = "=") -> ParseResult:
    """Parse flat key=value text (no sections).

    Each line is key<delimiter>value.
    """
    records: list[dict] = []
    errors: list[str] = []

    for line_num, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if delimiter in stripped:
            key, _, value = stripped.partition(delimiter)
            records.append({"key": key.strip(), "value": value.strip()})
        else:
            errors.append(f"Line {line_num}: No delimiter '{delimiter}' found")

    return ParseResult(
        format="key_value",
        source="text",
        records=records,
        line_count=len(text.splitlines()),
        errors=errors,
    )


def parse_csv_simple(text: str) -> ParseResult:
    """Parse simple CSV text (comma-separated, first row is header).

    Uses basic splitting — not the csv module (for learning purposes).
    """
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return ParseResult(format="csv", source="text", line_count=0)

    headers = [h.strip() for h in lines[0].split(",")]
    records: list[dict] = []
    errors: list[str] = []

    for line_num, line in enumerate(lines[1:], 2):
        values = [v.strip() for v in line.split(",")]
        if len(values) != len(headers):
            errors.append(f"Line {line_num}: Expected {len(headers)} columns, got {len(values)}")
            continue
        records.append(dict(zip(headers, values)))

    return ParseResult(
        format="csv",
        source="text",
        records=records,
        line_count=len(lines),
        errors=errors,
    )


# Format registry.
PARSERS = {
    "ini": parse_ini,
    "kv": parse_key_value,
    "csv": parse_csv_simple,
}


def detect_format(text: str) -> str:
    """Auto-detect file format from content."""
    lines = [l.strip() for l in text.splitlines() if l.strip() and not l.startswith("#")]
    if not lines:
        return "kv"

    if re.match(r"^\[.+\]$", lines[0]):
        return "ini"
    if "," in lines[0] and lines[0].count(",") >= 2:
        return "csv"
    return "kv"


def parse_file(path: Path, fmt: Optional[str] = None) -> ParseResult:
    """Parse a file, auto-detecting format if not specified."""
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    text = path.read_text(encoding="utf-8")

    if fmt is None:
        fmt = detect_format(text)
        logger.info("Auto-detected format: %s", fmt)

    parser_fn = PARSERS.get(fmt)
    if parser_fn is None:
        raise ValueError(f"Unknown format: {fmt}")

    result = parser_fn(text)
    result.source = str(path)
    return result


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser."""
    parser = argparse.ArgumentParser(description="Parser with fixtures")
    parser.add_argument("file", help="File to parse")
    parser.add_argument("--format", choices=["ini", "kv", "csv"], help="Force format")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--log-level", default="INFO")
    return parser


def main() -> None:
    """Entry point."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = build_parser()
    args = parser.parse_args()

    result = parse_file(Path(args.file), args.format)

    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        print(f"Format: {result.format}, Lines: {result.line_count}")
        if result.sections:
            for section in result.sections:
                print(f"\n[{section.name}]")
                for k, v in section.entries.items():
                    print(f"  {k} = {v}")
        if result.records:
            for rec in result.records:
                print(f"  {rec}")
        if result.errors:
            print(f"\nErrors ({len(result.errors)}):")
            for err in result.errors:
                print(f"  {err}")


if __name__ == "__main__":
    main()
