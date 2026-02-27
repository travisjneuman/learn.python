"""Level 0 project: Alarm Message Generator.

Read alarm definitions from a file and generate formatted
notification messages with severity levels and timestamps.

Concepts: f-strings, template strings, dictionaries, string formatting.
"""


import argparse
import json
from pathlib import Path


# Severity levels and their visual indicators.
SEVERITY_ICONS = {
    "critical": "[!!!]",
    "warning": "[!!]",
    "info": "[i]",
}

SEVERITY_ORDER = {"critical": 0, "warning": 1, "info": 2}


def parse_alarm(line: str) -> dict[str, str]:
    """Parse an alarm definition line.

    Expected format: SEVERITY | SOURCE | MESSAGE
    Example: critical | web-server-01 | CPU usage above 95%

    WHY pipe-separated? -- Pipes are less common in regular text
    than commas, so they work better as delimiters when messages
    might contain commas.
    """
    parts = line.split("|")

    if len(parts) < 3:
        return {"raw": line.strip(), "error": "Expected: SEVERITY | SOURCE | MESSAGE"}

    severity = parts[0].strip().lower()
    source = parts[1].strip()
    message = parts[2].strip()

    if severity not in SEVERITY_ICONS:
        return {"raw": line.strip(), "error": f"Unknown severity: {severity}"}

    return {
        "severity": severity,
        "source": source,
        "message": message,
    }


def format_alarm(alarm: dict[str, str], timestamp: str = "2024-01-15 09:30:00") -> str:
    """Format an alarm dict into a human-readable notification.

    WHY a timestamp parameter? -- In real systems the timestamp comes
    from the system clock.  Making it a parameter lets us test with
    predictable values.
    """
    if "error" in alarm:
        return f"  PARSE ERROR: {alarm['error']} ({alarm['raw']})"

    icon = SEVERITY_ICONS[alarm["severity"]]
    severity_upper = alarm["severity"].upper()

    # Build a formatted alert message.
    return (
        f"{icon} {severity_upper} ALARM\n"
        f"    Time:    {timestamp}\n"
        f"    Source:  {alarm['source']}\n"
        f"    Message: {alarm['message']}"
    )


def process_alarms(lines: list[str]) -> list[dict[str, str]]:
    """Parse all alarm lines and return structured data."""
    alarms = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        alarms.append(parse_alarm(stripped))
    return alarms


def sort_by_severity(alarms: list[dict[str, str]]) -> list[dict[str, str]]:
    """Sort alarms so critical ones appear first.

    WHY sort? -- In operations, the most urgent alarms should be
    seen first.  We use SEVERITY_ORDER to define the priority.
    """
    def severity_key(alarm: dict[str, str]) -> int:
        if "error" in alarm:
            return 99  # Errors go last.
        return SEVERITY_ORDER.get(alarm["severity"], 50)

    return sorted(alarms, key=severity_key)


def alarm_summary(alarms: list[dict[str, str]]) -> dict[str, int | dict[str, int]]:
    """Build a summary counting alarms by severity."""
    valid = [a for a in alarms if "error" not in a]
    counts = {"critical": 0, "warning": 0, "info": 0}
    for alarm in valid:
        counts[alarm["severity"]] += 1

    return {
        "total": len(alarms),
        "valid": len(valid),
        "errors": len(alarms) - len(valid),
        "by_severity": counts,
    }


def parse_args() -> argparse.Namespace:
    """Define command-line options."""
    parser = argparse.ArgumentParser(description="Alarm Message Generator")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    """Program entry point."""
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    lines = input_path.read_text(encoding="utf-8").splitlines()
    alarms = process_alarms(lines)
    sorted_alarms = sort_by_severity(alarms)

    print("=== Alarm Notifications ===\n")
    for alarm in sorted_alarms:
        print(format_alarm(alarm))
        print()

    summary = alarm_summary(alarms)
    print(f"Summary: {summary['by_severity']['critical']} critical, "
          f"{summary['by_severity']['warning']} warning, "
          f"{summary['by_severity']['info']} info")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps({"alarms": sorted_alarms, "summary": summary}, indent=2),
        encoding="utf-8",
    )
    print(f"Output written to {output_path}")


if __name__ == "__main__":
    main()
