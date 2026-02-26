# Parser With Fixtures — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 3 project: Parser With Fixtures."""

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
    """Result of parsing a file.

    WHY: a single return type for all parsers. Whether the input
    was INI, CSV, or key-value, the caller gets a ParseResult with
    sections and/or records. This uniform interface simplifies
    downstream code.
    """
    format: str
    source: str
    sections: list[ParsedSection] = field(default_factory=list)
    records: list[dict] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    line_count: int = 0


def parse_ini(text: str) -> ParseResult:
    """Parse INI-style text into sections with key-value pairs.

    WHY: INI is one of the simplest structured formats. Understanding
    how to parse it teaches stateful line-by-line parsing — the
    parser tracks "which section am I in?" as it reads.
    """
    sections: list[ParsedSection] = []
    current: Optional[ParsedSection] = None
    errors: list[str] = []
    line_count = 0

    for line_num, line in enumerate(text.splitlines(), 1):
        line_count += 1
        stripped = line.strip()

        # WHY: skip blanks and comments to make files human-readable.
        if not stripped or stripped.startswith("#") or stripped.startswith(";"):
            continue

        # WHY: regex matches [section_name] — the brackets are literal,
        # (.+) captures everything between them.
        match = re.match(r"^\[(.+)\]$", stripped)
        if match:
            current = ParsedSection(name=match.group(1).strip())
            sections.append(current)
            continue

        # WHY: partition on "=" splits "key = value" into ("key", "=", "value").
        # Unlike split("="), partition handles values that contain "=" signs.
        if "=" in stripped:
            key, _, value = stripped.partition("=")
            if current is None:
                # WHY: key-value pairs before any [section] go into "default".
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

    WHY: simpler than INI — just key-value pairs, one per line.
    Configuration files, .env files, and properties files use this.
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

    WHY: uses basic splitting instead of the csv module. This teaches
    the mechanics of CSV parsing — but in production, always use
    the csv module (it handles quoting, escaping, and edge cases).
    """
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return ParseResult(format="csv", source="text", line_count=0)

    headers = [h.strip() for h in lines[0].split(",")]
    records: list[dict] = []
    errors: list[str] = []

    for line_num, line in enumerate(lines[1:], 2):
        values = [v.strip() for v in line.split(",")]
        # WHY: column count mismatch indicates a malformed row.
        # Log it and skip rather than producing a corrupt record.
        if len(values) != len(headers):
            errors.append(
                f"Line {line_num}: Expected {len(headers)} columns, got {len(values)}")
            continue
        # WHY: zip(headers, values) pairs each header with its value,
        # and dict() turns the pairs into a record dict.
        records.append(dict(zip(headers, values)))

    return ParseResult(
        format="csv",
        source="text",
        records=records,
        line_count=len(lines),
        errors=errors,
    )


# WHY: the PARSERS registry maps format names to functions. This is
# the same pattern used in the normalizer (NORMALISERS) and CLI
# (CONVERTERS). Adding a new format is one dict entry + one function.
PARSERS = {
    "ini": parse_ini,
    "kv": parse_key_value,
    "csv": parse_csv_simple,
}


def detect_format(text: str) -> str:
    """Auto-detect file format from content.

    WHY: heuristic detection frees the user from specifying --format
    every time. The rules are simple: [section] means INI, many
    commas means CSV, otherwise assume key-value.
    """
    lines = [l.strip() for l in text.splitlines()
             if l.strip() and not l.startswith("#")]
    if not lines:
        return "kv"

    # WHY: check most specific patterns first.
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
    parser = argparse.ArgumentParser(description="Parser with fixtures")
    parser.add_argument("file", help="File to parse")
    parser.add_argument("--format", choices=["ini", "kv", "csv"],
                        help="Force format")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--log-level", default="INFO")
    return parser


def main() -> None:
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
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Registry pattern (PARSERS dict) | Maps format names to parser functions. Adding YAML support is one function + one dict entry. No if/elif chains to modify. |
| Heuristic format detection | Checking for `[section]` headers (INI) and comma counts (CSV) covers the common cases. The `--format` override exists for ambiguous input. |
| `partition("=")` instead of `split("=")` | `"key=val=ue".split("=")` gives `["key", "val", "ue"]`. `partition("=")` gives `("key", "=", "val=ue")` — the value is preserved intact even if it contains the delimiter. |
| Simple CSV parser (no csv module) | Teaching how parsing works mechanically. The csv module handles quoting, but using `.split(",")` makes the limitations visible and teaches why the csv module exists. |
| Error list in ParseResult | Errors are collected, not raised. The parser processes as much as it can and reports problems at the end — same approach as the error handler project. |

## Alternative Approaches

### Using `configparser` for INI files

```python
import configparser
from io import StringIO

def parse_ini_stdlib(text: str) -> dict:
    parser = configparser.ConfigParser()
    parser.read_string(text)
    return {s: dict(parser[s]) for s in parser.sections()}
```

**Trade-off:** `configparser` handles interpolation, multiline values, and escape sequences that our simple parser ignores. But it lowercases all keys by default and has opinions about formatting that may not match your files. The manual parser gives you full control.

## Common Pitfalls

1. **Duplicate section names in INI** — If a file has two `[database]` sections, our parser creates two `ParsedSection` objects. `configparser` merges them, which silently overwrites values. Neither behaviour is universally correct — document your choice.

2. **CSV fields containing commas** — `"Alice, Inc.",42` splits into three fields with `.split(",")` but should be two. The `csv` module handles quoted fields correctly. Our simple parser explicitly does not — this is a documented limitation.

3. **Auto-detection guessing wrong** — A line like `key=a,b,c` has commas and an equals sign. `detect_format` might pick CSV when the user meant key-value. The `--format` override exists precisely for these ambiguous cases.
