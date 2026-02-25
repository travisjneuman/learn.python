"""Level 3 project: Logging Baseline Tool.

Demonstrates Python's logging module: handlers, formatters, levels,
and structured log output for auditing and diagnostics.

Skills practiced: logging module, dataclasses, typing basics,
file I/O, JSON output, argparse subcommands.
"""

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
    """A single structured log entry."""
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
    Lines that don't match are returned as INFO entries.
    """
    line = line.strip()
    if not line:
        return None

    parts = [p.strip() for p in line.split("|")]

    if len(parts) >= 3:
        level = parts[0].upper()
        source = parts[1]
        message = "|".join(parts[2:])  # Rejoin in case message had pipes.
    elif len(parts) == 2:
        level = parts[0].upper()
        source = ""
        message = parts[1]
    else:
        level = "INFO"
        source = ""
        message = line

    # Validate the level is a known Python logging level.
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if level not in valid_levels:
        message = line  # Treat entire line as message.
        level = "INFO"

    return LogEntry(
        timestamp=time.time(),
        level=level,
        message=message,
        source=source,
    )


def parse_log_file(path: Path) -> list[LogEntry]:
    """Read a log file and parse each line into LogEntry objects.

    Skips blank lines and comment lines (starting with #).
    """
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")

    text = path.read_text(encoding="utf-8")
    entries: list[LogEntry] = []

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        entry = parse_log_line(stripped)
        if entry is not None:
            entries.append(entry)

    logger.info("Parsed %d entries from %s", len(entries), path)
    return entries


def summarise_entries(entries: list[LogEntry]) -> RunSummary:
    """Build a summary from a list of log entries.

    Counts entries by level and computes duration.
    """
    if not entries:
        return RunSummary()

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

    Level ordering: DEBUG < INFO < WARNING < ERROR < CRITICAL.
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

    logger.info("Filtered %d -> %d entries (min_level=%s)", len(entries), len(result), min_level)
    return result


def format_entry(entry: LogEntry, fmt: str = "text") -> str:
    """Format a single log entry for display.

    Supports 'text' (human-readable) and 'json' formats.
    """
    if fmt == "json":
        return json.dumps(asdict(entry))
    return f"[{entry.level:8s}] {entry.source or '-':12s} | {entry.message}"


def setup_logging(level: str = "INFO", log_file: Optional[Path] = None) -> None:
    """Configure the logging module with console and optional file handler."""
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    # Console handler.
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    root.addHandler(console)

    # Optional file handler.
    if log_file:
        file_handler = logging.FileHandler(str(log_file), encoding="utf-8")
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser with subcommands."""
    parser = argparse.ArgumentParser(description="Logging baseline tool")
    parser.add_argument("--log-level", default="INFO", help="Logging level")

    sub = parser.add_subparsers(dest="command")

    # Parse subcommand.
    parse = sub.add_parser("parse", help="Parse a log file")
    parse.add_argument("file", help="Path to log file")
    parse.add_argument("--min-level", default="DEBUG", help="Minimum level to show")
    parse.add_argument("--source", default=None, help="Filter by source")
    parse.add_argument("--json", action="store_true", help="JSON output")

    # Summary subcommand.
    summary = sub.add_parser("summary", help="Summarise a log file")
    summary.add_argument("file", help="Path to log file")

    # Generate subcommand — creates sample log entries.
    gen = sub.add_parser("generate", help="Generate sample log entries")
    gen.add_argument("--count", type=int, default=10, help="Number of entries")

    return parser


def main() -> None:
    """Entry point: parse args and run the requested command."""
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
        messages = ["Request processed", "Connection opened", "Cache miss", "Timeout", "Login attempt"]
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
