"""
Challenge: Parse Log File
Difficulty: Intermediate
Concepts: string parsing, regular expressions, dataclasses, structured data
Time: 35 minutes

Parse structured log lines into LogEntry objects. Each log line has the format:
    [TIMESTAMP] LEVEL: message

Where:
- TIMESTAMP is in the format "YYYY-MM-DD HH:MM:SS"
- LEVEL is one of: INFO, WARNING, ERROR, DEBUG
- message is the rest of the line

Implement `parse_log(line)` to parse a single line and `parse_logs(text)` to
parse multiple lines. Invalid lines should be skipped.

Examples:
    >>> entry = parse_log("[2024-01-15 10:30:00] ERROR: Connection failed")
    >>> entry.level
    'ERROR'
    >>> entry.message
    'Connection failed'
"""

import re
from dataclasses import dataclass


@dataclass
class LogEntry:
    timestamp: str
    level: str
    message: str


def parse_log(line: str) -> LogEntry | None:
    """Parse a single log line into a LogEntry, or return None if invalid. Implement this function."""
    # Hint: Use a regex with groups for timestamp, level, and message.
    pass


def parse_logs(text: str) -> list[LogEntry]:
    """Parse multiple log lines, skipping invalid ones. Implement this function."""
    # Hint: Split by newlines, call parse_log on each, filter out None results.
    pass


# --- Tests (do not modify) ---
if __name__ == "__main__":
    # Test 1: Parse single valid line
    entry = parse_log("[2024-01-15 10:30:00] ERROR: Connection failed")
    assert entry is not None, "Valid line should parse"
    assert entry.timestamp == "2024-01-15 10:30:00", "Timestamp failed"
    assert entry.level == "ERROR", "Level failed"
    assert entry.message == "Connection failed", "Message failed"

    # Test 2: Invalid line returns None
    assert parse_log("not a log line") is None, "Invalid line should return None"
    assert parse_log("") is None, "Empty line should return None"

    # Test 3: Parse multiple lines
    log_text = """[2024-01-15 10:30:00] INFO: Server started
[2024-01-15 10:30:01] WARNING: High memory usage
invalid line here
[2024-01-15 10:30:02] ERROR: Disk full"""
    entries = parse_logs(log_text)
    assert len(entries) == 3, f"Should parse 3 valid lines, got {len(entries)}"
    assert entries[0].level == "INFO", "First entry level failed"
    assert entries[1].level == "WARNING", "Second entry level failed"
    assert entries[2].message == "Disk full", "Third entry message failed"

    # Test 4: DEBUG level
    entry = parse_log("[2024-06-01 00:00:00] DEBUG: Variable x = 42")
    assert entry is not None and entry.level == "DEBUG", "DEBUG level failed"

    # Test 5: Message with special characters
    entry = parse_log("[2024-01-15 10:30:00] INFO: User logged in: user@example.com (ID: 123)")
    assert entry is not None, "Special characters should parse"
    assert "user@example.com" in entry.message, "Special chars in message failed"

    print("All tests passed!")
