# Solution: Level 1 / Project 04 - Log Line Parser

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 1 project: Log Line Parser.

Parse structured log lines into components: timestamp, level, and message.
Count entries by level and filter by severity.

Concepts: string splitting, datetime parsing, dictionaries, filtering.
"""


import argparse
from datetime import datetime
from pathlib import Path


# WHY parse_log_line: Each log line has a fixed structure. Parsing it
# into a dict makes the data easy to filter, count, and display.
# This is the core of the project — turning unstructured text into
# structured data.
def parse_log_line(line: str) -> dict:
    """Parse a single log line into its components.

    Expected format: 2024-01-15 09:30:00 [INFO] Server started
    """
    # WHY split with maxsplit=3: The message part may contain spaces
    # (e.g., "Server started on port 8080"), so we only split into
    # 4 parts: date, time, [LEVEL], and the rest is the message.
    parts = line.strip().split(maxsplit=3)

    # WHY check length: A malformed line like "hello" would have fewer
    # than 4 parts.  Returning an error dict instead of crashing lets
    # the caller skip bad lines gracefully.
    if len(parts) < 4:
        return {"raw": line.strip(), "error": "Expected: DATE TIME [LEVEL] MESSAGE"}

    date_str = parts[0]
    time_str = parts[1]
    level_raw = parts[2]
    message = parts[3]

    # WHY check brackets: The log level should be wrapped in brackets
    # like [INFO] or [ERROR].  Without brackets, we might misparse a
    # word from the message as the level.
    if not (level_raw.startswith("[") and level_raw.endswith("]")):
        return {"raw": line.strip(), "error": f"Level must be in brackets, got: {level_raw}"}

    # WHY slice [1:-1]: This strips the brackets from "[INFO]" to get
    # just "INFO".  .upper() normalises case so "info" and "INFO" match.
    level = level_raw[1:-1].upper()

    # WHY parse the timestamp: Validating the timestamp format ensures
    # we actually have a real date, not random text that happened to
    # split into the right number of parts.
    timestamp_str = f"{date_str} {time_str}"
    try:
        # WHY strptime: It parses a string into a datetime object using
        # format codes.  %Y = 4-digit year, %m = month, %d = day,
        # %H = hour (24h), %M = minute, %S = second.
        datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return {"raw": line.strip(), "error": f"Invalid timestamp: {timestamp_str}"}

    return {
        "timestamp": timestamp_str,
        "level": level,
        "message": message,
    }


# WHY count_by_level: Knowing the distribution of log levels is the
# first thing operations engineers look at — "how many errors vs info
# messages?" gives a quick health check of a system.
def count_by_level(entries: list[dict]) -> dict[str, int]:
    """Count log entries by their level."""
    counts = {}
    for entry in entries:
        # WHY skip errors: Entries with parse errors have no "level"
        # key.  Trying to access it would raise KeyError.
        if "error" in entry:
            continue
        level = entry["level"]
        # WHY .get(level, 0) + 1: This is the standard Python counting
        # pattern.  .get() returns 0 if the key does not exist yet,
        # then we add 1.  This avoids a KeyError on the first occurrence.
        counts[level] = counts.get(level, 0) + 1
    return counts


# WHY filter_by_level: Real log analysis tools let you filter by
# severity.  When debugging, you want to see only ERROR entries
# without scrolling through hundreds of INFO lines.
def filter_by_level(entries: list[dict], level: str) -> list[dict]:
    """Return only entries matching the specified level."""
    # WHY .upper(): Normalising to uppercase means the caller can pass
    # "error", "Error", or "ERROR" and get the same result.
    level = level.upper()
    return [e for e in entries if e.get("level") == level]


# WHY process_file: Separating file I/O from parsing logic means
# parse_log_line() can be tested with plain strings.
def process_file(path: Path) -> list[dict]:
    """Read a log file and parse each line."""
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    # WHY list comprehension with filter: Skip blank lines that
    # commonly appear between log groups in real log files.
    return [parse_log_line(line) for line in lines if line.strip()]


# WHY parse_args: The --level flag lets users filter from the command
# line (e.g., --level ERROR), which is exactly how real log tools
# like grep or journalctl work.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Log Line Parser")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/report.txt")
    parser.add_argument("--level", default=None, help="Filter by log level")
    return parser.parse_args()


# WHY main: Orchestrates the full workflow — parse, count, filter,
# display, and save.  Keeping it in main() makes the module importable.
def main() -> None:
    args = parse_args()
    entries = process_file(Path(args.input))
    counts = count_by_level(entries)

    display = entries
    if args.level:
        display = filter_by_level(entries, args.level)
        print(f"=== Log entries filtered by {args.level.upper()} ===\n")
    else:
        print("=== All Log Entries ===\n")

    for entry in display:
        if "error" in entry:
            print(f"  PARSE ERROR: {entry['error']}")
        else:
            print(f"  [{entry['level']:<7}] {entry['timestamp']} - {entry['message']}")

    print(f"\n  {'Level':<10} {'Count':>6}")
    print(f"  {'-'*10} {'-'*6}")
    for level, count in sorted(counts.items()):
        print(f"  {level:<10} {count:>6}")

    skipped = sum(1 for e in entries if "error" in e)
    if skipped:
        print(f"\n  Skipped {skipped} unparseable lines")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_lines = []
    report_lines.append("LOG ANALYSIS REPORT")
    report_lines.append("=" * 60)
    for entry in display:
        if "error" in entry:
            report_lines.append(f"PARSE ERROR: {entry['error']}")
        else:
            report_lines.append(f"[{entry['level']:<7}] {entry['timestamp']} - {entry['message']}")
    report_lines.append("")
    report_lines.append("LEVEL SUMMARY")
    report_lines.append(f"{'Level':<10} {'Count':>6}")
    for level, count in sorted(counts.items()):
        report_lines.append(f"{level:<10} {count:>6}")
    output_path.write_text("\n".join(report_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `split(maxsplit=3)` for log parsing | The message field may contain spaces; limiting the split to 4 parts preserves the full message text | Regex with capture groups — more precise but harder to understand at Level 1 |
| Error dict for malformed lines | Lets the program continue parsing remaining lines instead of stopping at the first bad line | Raise an exception — would require try/except in the caller and lose the remaining lines |
| `dict.get(level, 0) + 1` counting pattern | Standard Python idiom for counting occurrences without needing `defaultdict` or `Counter` (which come later) | `collections.Counter` — more concise but introduces a new import and concept at Level 1 |
| Case-insensitive level filtering | Users should not need to remember whether to type "ERROR" or "error"; normalising removes friction | Case-sensitive — would frustrate users who type the wrong case |

## Alternative approaches

### Approach B: Using `collections.Counter` for level counting

```python
from collections import Counter

def count_by_level_counter(entries: list[dict]) -> dict[str, int]:
    """Count log levels using Counter — more concise."""
    # WHY Counter: It is purpose-built for counting.  You pass it an
    # iterable of items and it returns a dict-like object with counts.
    levels = [e["level"] for e in entries if "error" not in e]
    return dict(Counter(levels))
```

**Trade-off:** `Counter` is more concise and handles the counting automatically. The manual `.get(level, 0) + 1` pattern teaches you how counting works under the hood, which is valuable when you encounter similar accumulation patterns (summing values, building frequency tables). Once you know `Counter` exists, prefer it for simple counting tasks.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Malformed line like `"not a log entry"` | `parse_log_line()` returns `{"raw": ..., "error": "Expected: DATE TIME [LEVEL] MESSAGE"}` because `split(maxsplit=3)` produces fewer than 4 parts | The length check catches this; the error dict is displayed as "PARSE ERROR" |
| Invalid timestamp like `"9999-99-99 00:00:00"` | `datetime.strptime()` raises ValueError, caught by try/except, returned as error dict | The try/except around strptime handles this gracefully |
| Filtering by a level with no entries (`--level CRITICAL`) | `filter_by_level()` returns an empty list; the program prints nothing and reports zero entries | Empty list is a valid result; the display loop simply has nothing to iterate |
| Level without brackets like `INFO Server started` | The bracket check catches this and returns an error dict with "Level must be in brackets" | The `startswith("[")` and `endswith("]")` guard is explicit |

## Key takeaways

1. **`split(maxsplit=N)` is essential for parsing structured text.** Without it, splitting "2024-01-15 09:30:00 [INFO] Server started on port 8080" would break the message into separate words. The `maxsplit` parameter controls how many splits happen, preserving the rest of the string as one piece.
2. **`datetime.strptime()` converts strings to dates using format codes.** Memorise the common ones: `%Y` (4-digit year), `%m` (month), `%d` (day), `%H` (hour), `%M` (minute), `%S` (second). The inverse is `strftime()`, which formats a datetime back into a string.
3. **Log parsing is a foundational skill for operations and monitoring.** Every web server, database, and application produces logs. The parse-count-filter pattern you learn here is exactly what tools like Splunk, Datadog, and the ELK stack do at scale.
