# Logging Baseline Tool — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) and [walkthrough](./WALKTHROUGH.md) before reading the solution.

---

## Complete Solution

```python
"""Level 3 project: Logging Baseline Tool."""

from __future__ import annotations

import argparse
import json
import logging
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class LogEntry:
    """A single structured log entry.

    WHY: using a dataclass instead of a dict enforces a consistent
    shape — every log entry has the same fields, so downstream code
    never has to check "does this dict have a 'level' key?".
    """
    timestamp: float
    level: str
    message: str
    source: str = ""
    extra: dict = field(default_factory=dict)


@dataclass
class RunSummary:
    """Summary of a logging run."""
    total_entries: int = 0
    by_level: dict = field(default_factory=dict)
    first_timestamp: Optional[float] = None
    last_timestamp: Optional[float] = None
    duration_seconds: float = 0.0


def parse_log_line(line: str) -> Optional[LogEntry]:
    """Parse a structured log line into a LogEntry.

    Expected format: LEVEL | source | message
    """
    line = line.strip()
    if not line:
        return None

    # WHY: split on "|" to handle the pipe-delimited format.
    # We strip each part to handle inconsistent spacing.
    parts = [p.strip() for p in line.split("|")]

    if len(parts) >= 3:
        level = parts[0].upper()
        source = parts[1]
        # WHY: rejoin remaining parts in case the message itself
        # contains pipe characters — a defensive parsing choice.
        message = "|".join(parts[2:])
    elif len(parts) == 2:
        level = parts[0].upper()
        source = ""
        message = parts[1]
    else:
        level = "INFO"
        source = ""
        message = line

    # WHY: validate against known levels to catch malformed lines.
    # If the "level" field is actually part of the message (e.g. a
    # line without pipe delimiters), we fall back to INFO.
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if level not in valid_levels:
        message = line
        level = "INFO"

    return LogEntry(
        timestamp=time.time(),
        level=level,
        message=message,
        source=source,
    )


def parse_log_file(path: Path) -> list[LogEntry]:
    """Read a log file and parse each line into LogEntry objects."""
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")

    text = path.read_text(encoding="utf-8")
    entries: list[LogEntry] = []

    for line in text.splitlines():
        stripped = line.strip()
        # WHY: skip blanks and comments so users can annotate log files.
        if not stripped or stripped.startswith("#"):
            continue
        entry = parse_log_line(stripped)
        if entry is not None:
            entries.append(entry)

    logger.info("Parsed %d entries from %s", len(entries), path)
    return entries


def summarise_entries(entries: list[LogEntry]) -> RunSummary:
    """Build a summary from a list of log entries."""
    if not entries:
        return RunSummary()

    # WHY: count entries per level using dict.get() with a default
    # of 0. This avoids KeyError without needing collections.Counter.
    by_level: dict[str, int] = {}
    for entry in entries:
        by_level[entry.level] = by_level.get(entry.level, 0) + 1

    timestamps = [e.timestamp for e in entries]
    first = min(timestamps)
    last = max(timestamps)

    return RunSummary(
        total_entries=len(entries),
        by_level=by_level,
        first_timestamp=first,
        last_timestamp=last,
        duration_seconds=round(last - first, 4),
    )


def filter_entries(
    entries: list[LogEntry],
    min_level: str = "DEBUG",
    source: Optional[str] = None,
) -> list[LogEntry]:
    """Filter log entries by minimum level and optional source.

    WHY: the level_order dict assigns numeric ranks so we can compare
    severity with simple integer comparison. This mirrors how Python's
    logging module works internally (DEBUG=10, INFO=20, etc.).
    """
    level_order = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}
    min_rank = level_order.get(min_level.upper(), 0)

    result: list[LogEntry] = []
    for entry in entries:
        rank = level_order.get(entry.level, 0)
        if rank < min_rank:
            continue
        if source and entry.source != source:
            continue
        result.append(entry)

    logger.info("Filtered %d -> %d entries (min_level=%s)",
                len(entries), len(result), min_level)
    return result


def format_entry(entry: LogEntry, fmt: str = "text") -> str:
    """Format a single log entry for display."""
    if fmt == "json":
        return json.dumps(asdict(entry))
    # WHY: fixed-width formatting (`:8s`, `:12s`) aligns columns
    # so the output is scannable by a human.
    return f"[{entry.level:8s}] {entry.source or '-':12s} | {entry.message}"


def setup_logging(level: str = "INFO", log_file: Optional[Path] = None) -> None:
    """Configure the logging module with console and optional file handler.

    WHY: we configure the root logger manually instead of using
    basicConfig so we can add both console AND file handlers.
    basicConfig only lets you pick one.
    """
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    root.addHandler(console)

    if log_file:
        file_handler = logging.FileHandler(str(log_file), encoding="utf-8")
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser with subcommands."""
    parser = argparse.ArgumentParser(description="Logging baseline tool")
    parser.add_argument("--log-level", default="INFO", help="Logging level")

    sub = parser.add_subparsers(dest="command")

    parse = sub.add_parser("parse", help="Parse a log file")
    parse.add_argument("file", help="Path to log file")
    parse.add_argument("--min-level", default="DEBUG", help="Minimum level to show")
    parse.add_argument("--source", default=None, help="Filter by source")
    parse.add_argument("--json", action="store_true", help="JSON output")

    summary = sub.add_parser("summary", help="Summarise a log file")
    summary.add_argument("file", help="Path to log file")

    gen = sub.add_parser("generate", help="Generate sample log entries")
    gen.add_argument("--count", type=int, default=10, help="Number of entries")

    return parser


def main() -> None:
    """Entry point."""
    parser = build_parser()
    args = parser.parse_args()
    setup_logging(args.log_level)

    if args.command == "parse":
        entries = parse_log_file(Path(args.file))
        filtered = filter_entries(entries, min_level=args.min_level, source=args.source)
        fmt = "json" if args.json else "text"
        for entry in filtered:
            print(format_entry(entry, fmt))

    elif args.command == "summary":
        entries = parse_log_file(Path(args.file))
        summary = summarise_entries(entries)
        print(json.dumps(asdict(summary), indent=2))

    elif args.command == "generate":
        import random
        levels = ["DEBUG", "INFO", "INFO", "WARNING", "ERROR"]
        sources = ["auth", "db", "api", "cache"]
        messages = ["Request processed", "Connection opened",
                    "Cache miss", "Timeout", "Login attempt"]
        for _ in range(args.count):
            entry = LogEntry(
                timestamp=time.time(),
                level=random.choice(levels),
                message=random.choice(messages),
                source=random.choice(sources),
            )
            print(format_entry(entry))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Numeric level_order dict for filtering | Mirrors Python's internal logging levels. Lets us compare severity with `<` instead of maintaining a list of "which levels include which". |
| `parse_log_line` returns `Optional[LogEntry]` | Blank lines return `None` instead of raising an error, so the caller can simply filter them out. Graceful handling of imperfect input. |
| Manual handler setup instead of `basicConfig` | `basicConfig` is fire-once and cannot add multiple handlers. Manual setup gives us console + file output simultaneously. |
| Pipe-delimited format (`LEVEL \| source \| message`) | Pipes are uncommon in log messages compared to spaces or colons, making them a reliable delimiter for parsing. |
| `time.time()` as timestamp | Returns a Unix epoch float, which is sortable, storable, and trivially convertible to human-readable format. |

## Alternative Approaches

### Using Python's `configparser` for INI-style logs

```python
import configparser

def parse_structured_log(path: Path) -> dict:
    """Parse logs stored in INI-like sections."""
    config = configparser.ConfigParser()
    config.read(path)
    return {section: dict(config[section]) for section in config.sections()}
```

**Trade-off:** Works well when logs have a section-based structure (like `[2024-01-15]`), but most real-world logs are line-oriented. The line-by-line parser is more universally applicable.

### Using the `re` module for stricter parsing

```python
import re
LOG_PATTERN = re.compile(r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)\s*\|\s*(\w*)\s*\|\s*(.+)$")

def parse_strict(line: str) -> Optional[LogEntry]:
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None
    return LogEntry(time.time(), match.group(1), match.group(3), match.group(2))
```

**Trade-off:** Regex is more precise (rejects malformed lines outright) but harder to debug when formats change slightly. The string-split approach is more forgiving, which is usually what you want for log parsing.

## Common Pitfalls

1. **Confusing `print()` with `logging`** — `print()` goes to stdout and cannot be filtered by level. `logging` goes to configurable handlers, can be filtered, timestamped, and routed to files. Use `print()` for user-facing output, `logging` for diagnostic information.

2. **Calling `basicConfig()` multiple times** — It only takes effect the first time. If a library calls it before your code, your configuration is silently ignored. Use `getLogger()` and `addHandler()` for reliable setup.

3. **Not stripping whitespace from parsed parts** — `"INFO | auth | login"`.split("|") produces `["INFO ", " auth ", " login"]` with spaces. Always `.strip()` after splitting on delimiters.
