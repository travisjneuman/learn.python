# Solution: Level 1 / Project 07 - Date Difference Helper

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 1 project: Date Difference Helper.

Calculate the number of days between two dates, add or subtract
days from a date, and determine the day of the week.

Concepts: datetime module, strptime/strftime, timedelta, date arithmetic.
"""


import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path


# WHY a module-level constant: The date format "YYYY-MM-DD" is used
# in multiple functions.  Defining it once prevents typos and makes
# it easy to change if the format needs to be different.
DATE_FORMAT = "%Y-%m-%d"


# WHY parse_date: Centralising date parsing means every function that
# needs a date object calls this one function.  If the format changes,
# you update one place, not five.
def parse_date(date_str: str) -> datetime:
    """Parse a date string in YYYY-MM-DD format.

    WHY strptime? -- It converts a string to a datetime object using
    a format code.  %Y = 4-digit year, %m = month, %d = day.
    """
    # WHY strip: Trailing spaces or tabs in input would cause strptime
    # to fail with a confusing "unconverted data remains" error.
    return datetime.strptime(date_str.strip(), DATE_FORMAT)


# WHY days_between: Calculating the gap between two dates is the most
# common date operation in business software — billing cycles, project
# deadlines, subscription periods all need this.
def days_between(date1_str: str, date2_str: str) -> int:
    """Calculate the number of days between two dates.

    Returns a positive number regardless of which date comes first.
    """
    d1 = parse_date(date1_str)
    d2 = parse_date(date2_str)
    # WHY subtract datetimes: Subtracting two datetime objects produces
    # a timedelta object, which has a .days attribute giving the
    # integer number of days between them.
    delta = d2 - d1
    # WHY abs(): The user might enter dates in either order (start
    # before end, or end before start).  abs() ensures we always
    # return a positive count, avoiding confusing negative numbers.
    return abs(delta.days)


# WHY add_days: Adding or subtracting days from a date is used for
# calculating due dates, expiration dates, and scheduling.
def add_days(date_str: str, days: int) -> str:
    """Add (or subtract if negative) days to a date.

    WHY timedelta? -- timedelta represents a duration.  Adding it
    to a datetime shifts the date by that many days.
    """
    d = parse_date(date_str)
    # WHY timedelta(days=days): You cannot just add an integer to a
    # datetime — Python does not know if you mean days, hours, or
    # seconds.  timedelta makes the unit explicit.
    result = d + timedelta(days=days)
    # WHY strftime: Converts the datetime back to a string in the
    # same YYYY-MM-DD format.  This keeps input and output consistent.
    return result.strftime(DATE_FORMAT)


# WHY day_of_week: Knowing what day a date falls on is useful for
# scheduling, reporting, and human-readable date displays.
def day_of_week(date_str: str) -> str:
    """Return the day name (Monday, Tuesday, etc.) for a date.

    WHY strftime('%A')? -- The %A format code gives the full weekday
    name.  %a would give the abbreviated name (Mon, Tue).
    """
    d = parse_date(date_str)
    return d.strftime("%A")


# WHY process_commands: This function reads a file of commands and
# dispatches each to the right function.  It is a simple command
# processor — the same pattern used in the Command Dispatcher project.
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

        # WHY try/except: Invalid dates (like "2024-02-30") or bad
        # integers (like "add 2024-01-01 abc") would crash without
        # error handling.  Catching them produces an error dict.
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


# WHY parse_args: Standard argparse for flexible input/output paths.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Date Difference Helper")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


# WHY main: Orchestrates reading, processing, displaying, and saving.
# Individual date functions remain importable for testing.
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| `DATE_FORMAT` as module-level constant | Single source of truth for the date format; changing it from `%Y-%m-%d` to `%d/%m/%Y` updates all functions at once | Hardcode the format string in each function — easy to introduce format mismatches |
| `abs()` for day differences | Users should not need to worry about which date comes first; negative day counts would be confusing | Return signed result — could be useful for "is date2 after date1?" checks, but adds complexity for the primary use case |
| `parse_date()` as a shared helper | All date functions need the same string-to-datetime conversion; centralising it eliminates duplication | Inline `datetime.strptime()` in each function — works but duplicates the format string and strip logic |
| Command dispatch via if/elif | Simple and transparent for three commands; a dict dispatcher (like Project 11) would be overkill here | Dict mapping command names to functions — better for 10+ commands, over-engineered for 3 |

## Alternative approaches

### Approach B: Using `dateutil` for flexible date parsing

```python
# NOTE: dateutil is a third-party library (pip install python-dateutil).
# It is not part of the standard library, but it is extremely common.

from dateutil import parser as dateutil_parser
from dateutil.relativedelta import relativedelta

def parse_date_flexible(date_str: str) -> datetime:
    """Parse dates in almost any format using dateutil."""
    # WHY dateutil: It handles "Jan 15, 2024", "15/01/2024",
    # "2024-01-15", and dozens of other formats automatically.
    return dateutil_parser.parse(date_str.strip())

def add_months(date_str: str, months: int) -> str:
    """Add months to a date — something timedelta cannot do."""
    # WHY relativedelta: timedelta only handles days/seconds/weeks.
    # relativedelta handles months and years, accounting for varying
    # month lengths (Feb has 28/29 days, etc.).
    d = parse_date_flexible(date_str)
    result = d + relativedelta(months=months)
    return result.strftime(DATE_FORMAT)
```

**Trade-off:** `dateutil` is more flexible and handles ambiguous date formats. But it is a third-party dependency, and at Level 1 it is better to learn `strptime` format codes explicitly so you understand what `%Y-%m-%d` means. Use `dateutil` in production when you need to parse user-submitted dates in unknown formats.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Invalid date like `"2024-02-30"` | `datetime.strptime()` raises ValueError because Feb 30 does not exist; caught by try/except in `process_commands()` | The error dict records the failed command with the ValueError message |
| Reversed date order in `diff` | `days_between("2024-12-31", "2024-01-01")` returns 365 (positive) thanks to `abs()` | The `abs()` call ensures the result is always non-negative |
| Misspelled command like `"dif"` | Falls into the `else` branch with "Unknown command or wrong args" | The if/elif/else structure catches any unrecognised command |
| Negative days in `add` (e.g., `add 2024-03-01 -1`) | `timedelta(days=-1)` correctly subtracts one day, returning `2024-02-29` (leap year) | timedelta handles negative values natively; no special case needed |

## Key takeaways

1. **`datetime.strptime()` and `strftime()` are inverse operations.** `strptime` parses a string into a datetime (string-parse-time), and `strftime` formats a datetime back into a string (string-format-time). Memorise the common format codes: `%Y` (year), `%m` (month), `%d` (day), `%H` (hour), `%M` (minute).
2. **`timedelta` makes date arithmetic explicit.** You cannot add `5` to a datetime because Python does not know if you mean 5 days, 5 hours, or 5 seconds. `timedelta(days=5)` makes the unit unambiguous. This explicitness prevents a category of bugs that plague other languages.
3. **Date calculations appear everywhere in real software.** Billing cycles ("30 days until payment"), SLA tracking ("how many hours since the ticket was opened"), scheduling ("what is the next Tuesday?"), and analytics ("group sales by week") all use the same `datetime` + `timedelta` patterns you learned here.
