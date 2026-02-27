"""Level 1 project: Log Line Parser.

Parse structured log lines into components: timestamp, level, and message.
Count entries by level and filter by severity.

Concepts: string splitting, datetime parsing, dictionaries, filtering.
"""


import argparse
from datetime import datetime
from pathlib import Path


def parse_log_line(line: str) -> dict[str, str]:
    """Parse a single log line into its components.

    Expected format: 2024-01-15 09:30:00 [INFO] Server started
    Components: timestamp, level, message

    WHY split with maxsplit? -- The message might contain spaces,
    so we split carefully: date (1), time (2), [LEVEL] (3), rest is message.
    """
    parts = line.strip().split(maxsplit=3)

    if len(parts) < 4:
        return {"raw": line.strip(), "error": "Expected: DATE TIME [LEVEL] MESSAGE"}

    date_str = parts[0]
    time_str = parts[1]
    level_raw = parts[2]
    message = parts[3]

    # Extract level from brackets: [INFO] -> INFO
    if not (level_raw.startswith("[") and level_raw.endswith("]")):
        return {"raw": line.strip(), "error": f"Level must be in brackets, got: {level_raw}"}

    level = level_raw[1:-1].upper()

    # Try to parse the timestamp.
    timestamp_str = f"{date_str} {time_str}"
    try:
        datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return {"raw": line.strip(), "error": f"Invalid timestamp: {timestamp_str}"}

    return {
        "timestamp": timestamp_str,
        "level": level,
        "message": message,
    }


def count_by_level(entries: list[dict[str, str]]) -> dict[str, int]:
    """Count log entries by their level.

    WHY count by level? -- In operations, knowing how many errors
    vs info messages you have gives a quick health check.
    """
    counts = {}
    for entry in entries:
        if "error" in entry:
            continue
        level = entry["level"]
        counts[level] = counts.get(level, 0) + 1
    return counts


def filter_by_level(entries: list[dict[str, str]], level: str) -> list[dict[str, str]]:
    """Return only entries matching the specified level."""
    level = level.upper()
    return [e for e in entries if e.get("level") == level]


def process_file(path: Path) -> list[dict[str, str]]:
    """Read a log file and parse each line."""
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    return [parse_log_line(line) for line in lines if line.strip()]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Log Line Parser")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/report.txt")
    parser.add_argument("--level", default=None, help="Filter by log level")
    return parser.parse_args()


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

    # Print level summary as a formatted table.
    print(f"\n  {'Level':<10} {'Count':>6}")
    print(f"  {'-'*10} {'-'*6}")
    for level, count in sorted(counts.items()):
        print(f"  {level:<10} {count:>6}")

    skipped = sum(1 for e in entries if "error" in e)
    if skipped:
        print(f"\n  Skipped {skipped} unparseable lines")

    # Write a plain-text report instead of JSON.
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
