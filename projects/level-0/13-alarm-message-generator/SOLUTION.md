# Solution: Level 0 / Project 13 - Alarm Message Generator

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 0 project: Alarm Message Generator.

Read alarm definitions from a file and generate formatted
notification messages with severity levels and timestamps.

Concepts: f-strings, template strings, dictionaries, string formatting.
"""


import argparse
import json
from pathlib import Path


# WHY module-level constants: Severity icons and ordering are used by
# multiple functions.  Defining them once at the top makes them easy
# to update and impossible to accidentally define differently in two places.
SEVERITY_ICONS = {
    "critical": "[!!!]",
    "warning": "[!!]",
    "info": "[i]",
}

# WHY a separate ordering dict: Alphabetical sort would put "critical"
# before "info" (correct) but "warning" after "info" (wrong).
# Explicit numeric ordering ensures critical=0 sorts first.
SEVERITY_ORDER = {"critical": 0, "warning": 1, "info": 2}


def parse_alarm(line: str) -> dict:
    """Parse an alarm definition line.

    Expected format: SEVERITY | SOURCE | MESSAGE
    Example: critical | web-server-01 | CPU usage above 95%

    WHY pipe-separated? -- Pipes are less common in regular text
    than commas, so they work better as delimiters when messages
    might contain commas.
    """
    parts = line.split("|")

    # WHY check for 3 parts: The format requires exactly 3 pipe-delimited
    # fields.  Fewer parts means the line is malformed.
    if len(parts) < 3:
        return {"raw": line.strip(), "error": "Expected: SEVERITY | SOURCE | MESSAGE"}

    # WHY .strip().lower() on severity: Users might type "Critical" or
    # "CRITICAL" or "  critical  ".  Normalising ensures we match our
    # SEVERITY_ICONS keys consistently.
    severity = parts[0].strip().lower()
    source = parts[1].strip()
    message = parts[2].strip()

    # WHY validate severity: Unknown severity levels would cause a KeyError
    # when looking up the icon.  Checking first produces a clear error.
    if severity not in SEVERITY_ICONS:
        return {"raw": line.strip(), "error": f"Unknown severity: {severity}"}

    return {
        "severity": severity,
        "source": source,
        "message": message,
    }


def format_alarm(alarm: dict, timestamp: str = "2024-01-15 09:30:00") -> str:
    """Format an alarm dict into a human-readable notification.

    WHY a timestamp parameter? -- In real systems the timestamp comes
    from the system clock.  Making it a parameter lets us test with
    predictable values instead of the ever-changing real time.
    """
    if "error" in alarm:
        return f"  PARSE ERROR: {alarm['error']} ({alarm['raw']})"

    icon = SEVERITY_ICONS[alarm["severity"]]
    severity_upper = alarm["severity"].upper()

    # WHY multi-line f-string: Each field on its own line makes the
    # notification scannable.  Indentation with spaces aligns the
    # values vertically for quick reading.
    return (
        f"{icon} {severity_upper} ALARM\n"
        f"    Time:    {timestamp}\n"
        f"    Source:  {alarm['source']}\n"
        f"    Message: {alarm['message']}"
    )


def process_alarms(lines: list[str]) -> list[dict]:
    """Parse all alarm lines and return structured data."""
    alarms = []
    for line in lines:
        stripped = line.strip()
        # WHY skip blank lines: Empty lines between alarm definitions
        # are common.  Skipping them avoids false parse errors.
        if not stripped:
            continue
        alarms.append(parse_alarm(stripped))
    return alarms


def sort_by_severity(alarms: list[dict]) -> list[dict]:
    """Sort alarms so critical ones appear first.

    WHY sort? -- In operations, the most urgent alarms should be
    seen first.  We use SEVERITY_ORDER to define the priority.
    """
    def severity_key(alarm: dict) -> int:
        """Return a numeric priority for sorting.

        WHY inner function? -- This function is only used by sorted()
        and has no meaning outside this context.  Nesting it makes
        the scope clear.
        """
        # WHY errors go last: Parse errors are not urgent alarms.
        # Putting them at the end keeps the real alarms front and center.
        if "error" in alarm:
            return 99
        return SEVERITY_ORDER.get(alarm["severity"], 50)

    # WHY sorted() instead of .sort(): sorted() returns a new list,
    # leaving the original unchanged.  This is safer when other code
    # might still reference the original order.
    return sorted(alarms, key=severity_key)


def alarm_summary(alarms: list[dict]) -> dict:
    """Build a summary counting alarms by severity.

    WHY count by severity? -- A summary like "3 critical, 2 warning,
    5 info" tells an operator whether the situation is urgent at a
    glance, without reading every individual alarm.
    """
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Pipe `\|` delimiter instead of comma | Alarm messages often contain commas ("CPU usage above 95%, check immediately"). Pipes are rare in prose, so they are safer delimiters | Comma-separated — would break on messages containing commas, requiring CSV quoting |
| `SEVERITY_ORDER` dict for custom sorting | Alphabetical sorting puts "info" before "warning", which is wrong for urgency. Explicit numeric ordering gives full control | Sort alphabetically — simple but produces incorrect priority order |
| `format_alarm()` takes a `timestamp` parameter | Hardcoded default makes tests deterministic. Real usage would pass `datetime.now()`. Testability over convenience | Call `datetime.now()` inside the function — makes output unpredictable, tests would need time mocking |
| `sort_by_severity()` uses `sorted()` (not `.sort()`) | Returns a new sorted list without modifying the original. Safer when the original order is needed elsewhere (e.g., for the summary) | Use `.sort()` in-place — mutates the list, which could surprise callers who still hold a reference |

## Alternative approaches

### Approach B: Using dataclasses for alarm structure

```python
from dataclasses import dataclass

@dataclass
class Alarm:
    severity: str
    source: str
    message: str

    @property
    def icon(self) -> str:
        return SEVERITY_ICONS.get(self.severity, "[?]")

    @property
    def priority(self) -> int:
        return SEVERITY_ORDER.get(self.severity, 50)

    def format(self, timestamp: str = "2024-01-15 09:30:00") -> str:
        return (
            f"{self.icon} {self.severity.upper()} ALARM\n"
            f"    Time:    {timestamp}\n"
            f"    Source:  {self.source}\n"
            f"    Message: {self.message}"
        )

# Sort becomes trivial:
# sorted(alarms, key=lambda a: a.priority)
```

**Trade-off:** Dataclasses give each alarm a proper type with methods and properties. `alarm.severity` is clearer than `alarm["severity"]`, and the IDE can autocomplete field names. However, dataclasses are a Level 2+ concept. At Level 0, plain dicts keep things simple — no imports, no class definitions, no `self` parameter to explain. Once you learn classes (Level 2-3), refactoring from dicts to dataclasses is a natural progression.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Unknown severity like `"danger"` | `parse_alarm()` returns an error dict: `"Unknown severity: danger"`. The alarm is counted as an error in the summary | Already handled by the severity validation |
| Line with fewer than 3 pipe-delimited fields | Returns error dict: `"Expected: SEVERITY \| SOURCE \| MESSAGE"` | Already handled by the `len(parts) < 3` check |
| Line with extra pipes (e.g. `"critical \| server \| CPU \| 95%"`) | `split("\|")` produces 4 parts. We take the first 3. The `"95%"` portion is lost from the message | Use `split("\|", maxsplit=2)` to keep everything after the second pipe as the message |
| All alarms have the same severity | Sorting produces a valid result — all critical alarms grouped together. No crash | Already handled |
| No alarms in the file | `process_alarms([])` returns `[]`. Summary shows all zeros. No crash | Already handled |

## Key takeaways

1. **Custom sorting with a key function gives you complete control.** `sorted(items, key=severity_key)` sorts by priority instead of alphabetically. The key function translates each item into a comparable value. This pattern works for sorting by date, price, priority, or any custom criterion.
2. **Choosing the right delimiter prevents parsing headaches.** Commas are common in text, so comma-delimited data needs quoting rules. Pipes (`|`) or tabs are rarer in prose and work better as delimiters when field content is unpredictable. This is a real-world data engineering decision.
3. **Parameterising things that change (like timestamps) makes code testable.** If `format_alarm()` called `datetime.now()` internally, tests would produce different output every second. Passing the timestamp as a parameter gives tests control over the value. This is called "dependency injection" and is a fundamental testing technique.
4. **Module-level constants are a single source of truth.** `SEVERITY_ICONS` and `SEVERITY_ORDER` are defined once and used by multiple functions. If you add a new severity level, you update two dicts — everything else adapts automatically.
