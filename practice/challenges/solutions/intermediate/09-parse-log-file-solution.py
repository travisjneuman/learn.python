"""
Solution: Parse Log File

Approach: Use a regular expression to match the log line format:
[timestamp] LEVEL: message. The regex captures three groups: timestamp,
level, and message. Lines that don't match the pattern return None.
"""

import re
from dataclasses import dataclass


@dataclass
class LogEntry:
    timestamp: str
    level: str
    message: str


# Pattern matches: [YYYY-MM-DD HH:MM:SS] LEVEL: message
_LOG_PATTERN = re.compile(
    r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (INFO|WARNING|ERROR|DEBUG): (.+)$"
)


def parse_log(line: str) -> LogEntry | None:
    match = _LOG_PATTERN.match(line.strip())
    if not match:
        return None
    return LogEntry(
        timestamp=match.group(1),
        level=match.group(2),
        message=match.group(3),
    )


def parse_logs(text: str) -> list[LogEntry]:
    entries = []
    for line in text.strip().split("\n"):
        entry = parse_log(line)
        if entry is not None:
            entries.append(entry)
    return entries


if __name__ == "__main__":
    entry = parse_log("[2024-01-15 10:30:00] ERROR: Connection failed")
    assert entry is not None
    assert entry.timestamp == "2024-01-15 10:30:00"
    assert entry.level == "ERROR"
    assert entry.message == "Connection failed"

    assert parse_log("not a log line") is None
    assert parse_log("") is None

    log_text = """[2024-01-15 10:30:00] INFO: Server started
[2024-01-15 10:30:01] WARNING: High memory usage
invalid line here
[2024-01-15 10:30:02] ERROR: Disk full"""
    entries = parse_logs(log_text)
    assert len(entries) == 3
    assert entries[0].level == "INFO"
    assert entries[1].level == "WARNING"
    assert entries[2].message == "Disk full"

    entry = parse_log("[2024-06-01 00:00:00] DEBUG: Variable x = 42")
    assert entry is not None and entry.level == "DEBUG"

    entry = parse_log("[2024-01-15 10:30:00] INFO: User logged in: user@example.com (ID: 123)")
    assert entry is not None
    assert "user@example.com" in entry.message

    print("All tests passed!")
