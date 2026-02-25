"""Level 1 project: Date Difference Helper.

Calculate the number of days between two dates, add or subtract
days from a date, and determine the day of the week.

Concepts: datetime module, strptime/strftime, timedelta, date arithmetic.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path


DATE_FORMAT = "%Y-%m-%d"


def parse_date(date_str: str) -> datetime:
    """Parse a date string in YYYY-MM-DD format.

    WHY strptime? -- It converts a string to a datetime object using
    a format code.  %Y = 4-digit year, %m = month, %d = day.
    """
    return datetime.strptime(date_str.strip(), DATE_FORMAT)


def days_between(date1_str: str, date2_str: str) -> int:
    """Calculate the number of days between two dates.

    Returns a positive number regardless of which date comes first.

    WHY abs()? -- The user might enter the dates in either order.
    abs() ensures we always get a positive count.
    """
    d1 = parse_date(date1_str)
    d2 = parse_date(date2_str)
    delta = d2 - d1
    return abs(delta.days)


def add_days(date_str: str, days: int) -> str:
    """Add (or subtract if negative) days to a date.

    WHY timedelta? -- timedelta represents a duration.  Adding it
    to a datetime shifts the date by that many days.
    """
    d = parse_date(date_str)
    result = d + timedelta(days=days)
    return result.strftime(DATE_FORMAT)


def day_of_week(date_str: str) -> str:
    """Return the day name (Monday, Tuesday, etc.) for a date.

    WHY strftime('%A')? -- The %A format code gives the full weekday name.
    """
    d = parse_date(date_str)
    return d.strftime("%A")


def process_commands(lines: list[str]) -> list[dict]:
    """Process date commands from a list of strings.

    Supported commands:
    - diff DATE1 DATE2          -- days between two dates
    - add DATE DAYS             -- add days to a date
    - weekday DATE              -- day of the week
    """
    results = []
    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue

        cmd = parts[0].lower()

        try:
            if cmd == "diff" and len(parts) == 3:
                gap = days_between(parts[1], parts[2])
                results.append({"command": line.strip(), "days": gap})
            elif cmd == "add" and len(parts) == 3:
                new_date = add_days(parts[1], int(parts[2]))
                results.append({"command": line.strip(), "result": new_date})
            elif cmd == "weekday" and len(parts) == 2:
                name = day_of_week(parts[1])
                results.append({"command": line.strip(), "weekday": name})
            else:
                results.append({"command": line.strip(), "error": "Unknown command or wrong args"})
        except (ValueError, IndexError) as err:
            results.append({"command": line.strip(), "error": str(err)})

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Date Difference Helper")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    path = Path(args.input)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    results = process_commands(lines)

    print("=== Date Difference Helper ===\n")
    for r in results:
        if "error" in r:
            print(f"  ERROR: {r['command']} -- {r['error']}")
        elif "days" in r:
            print(f"  {r['command']}  =>  {r['days']} days")
        elif "result" in r:
            print(f"  {r['command']}  =>  {r['result']}")
        elif "weekday" in r:
            print(f"  {r['command']}  =>  {r['weekday']}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
