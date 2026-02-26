# Solution: Level 1 / Project 10 - Ticket Priority Router

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
"""Level 1 project: Ticket Priority Router.

Route support tickets to priority queues based on keywords.
Tickets containing urgent words go to high priority, etc.

Concepts: keyword matching, dictionaries, string search, business rules.
"""


import argparse
import json
from pathlib import Path


# WHY PRIORITY_KEYWORDS at module level: Business rules belong in
# data, not in nested if/elif logic.  A dict of keyword lists is
# easy to read, edit, and eventually load from a configuration file.
PRIORITY_KEYWORDS = {
    "critical": ["down", "outage", "crash", "data loss", "security breach"],
    "high": ["error", "broken", "failing", "urgent", "blocked"],
    "medium": ["slow", "degraded", "intermittent", "bug", "issue"],
    "low": ["question", "request", "enhancement", "feature", "how to"],
}


# WHY classify_ticket: This is the core business logic — matching
# ticket text against keyword lists to determine urgency.  Isolating
# it in a pure function makes it easy to test with specific strings.
def classify_ticket(text: str) -> str:
    """Determine the priority of a ticket based on keywords.

    WHY check critical first? -- Priority keywords overlap.  By checking
    the highest priority first, a ticket mentioning 'crash' gets
    classified as critical even if it also mentions 'slow'.
    """
    # WHY lowercase: Case-insensitive matching means "CRASH", "Crash",
    # and "crash" all trigger the same rule.
    lower_text = text.lower()

    # WHY explicit priority order: The list ["critical", "high", ...]
    # ensures we always check the most severe level first.  If we
    # iterated the dict directly, Python 3.7+ preserves insertion order,
    # but being explicit about the order is clearer and safer.
    for priority in ["critical", "high", "medium", "low"]:
        for keyword in PRIORITY_KEYWORDS[priority]:
            # WHY 'keyword in lower_text': This checks if the keyword
            # appears anywhere in the ticket text as a substring.
            # "data loss" matches "We experienced data loss at 3am".
            if keyword in lower_text:
                return priority

    # WHY default to low: If no keywords match, the ticket is not
    # urgent.  Defaulting to low ensures every ticket gets a priority.
    return "low"


# WHY route_ticket: Wraps classification with a ticket ID and the
# original text into a structured record.  This is the unit of work
# that gets passed to the grouping function.
def route_ticket(ticket_id: int, text: str) -> dict:
    """Build a routed ticket record."""
    priority = classify_ticket(text)
    return {
        "id": ticket_id,
        "text": text.strip(),
        "priority": priority,
    }


# WHY process_tickets: Reads raw lines and converts them into routed
# ticket records, assigning sequential IDs.
def process_tickets(lines: list[str]) -> list[dict]:
    """Process a list of ticket descriptions."""
    tickets = []
    # WHY enumerate with start=1: Ticket IDs starting at 1 are more
    # natural for users than 0-based indices.
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        # WHY skip blanks: Real ticket files may have blank lines
        # between entries.  Skipping them prevents empty-text tickets.
        if not stripped:
            continue
        tickets.append(route_ticket(i, stripped))
    return tickets


# WHY group_by_priority: Operations teams work through tickets by
# priority — fix critical issues first, then high, etc.  Grouping
# makes it easy to see the most urgent queue at a glance.
def group_by_priority(tickets: list[dict]) -> dict[str, list[dict]]:
    """Group tickets into priority queues."""
    # WHY pre-initialise all keys: Even if no tickets match a priority,
    # the key exists with an empty list.  This prevents KeyError when
    # iterating over all priority levels for display.
    groups = {"critical": [], "high": [], "medium": [], "low": []}
    for ticket in tickets:
        groups[ticket["priority"]].append(ticket)
    return groups


# WHY parse_args: Standard argparse for flexible input/output.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ticket Priority Router")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


# WHY main: Orchestrates the full pipeline — read, classify, group,
# display, and save.
def main() -> None:
    args = parse_args()
    path = Path(args.input)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    tickets = process_tickets(lines)
    groups = group_by_priority(tickets)

    print("=== Ticket Priority Router ===\n")
    for priority in ["critical", "high", "medium", "low"]:
        queue = groups[priority]
        print(f"  [{priority.upper()}] ({len(queue)} tickets)")
        for t in queue:
            # WHY truncate to 60: Long ticket descriptions would
            # destroy the table layout.  60 chars gives enough context.
            print(f"    #{t['id']}: {t['text'][:60]}")
        print()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps({"tickets": tickets, "queues": {k: len(v) for k, v in groups.items()}}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Dict mapping priority levels to keyword lists | Data-driven rules are easy to modify without touching logic; adding a keyword is one list item | If/elif chain with hardcoded keywords — works but mixes data with logic |
| Check priorities in descending severity order | Ensures a ticket mentioning both "crash" and "slow" is classified as "critical", not "medium" | Check all priorities and pick the highest match — more complex, same result |
| Substring matching (`keyword in text`) | Catches keywords in any context ("the server crashed" matches "crash") | Word-boundary matching with regex — more precise but overkill at Level 1 |
| Pre-initialise group dict with all priority keys | Guarantees all priority levels appear in output even when empty, simplifying display logic | Build groups dynamically with `setdefault` — works but might miss empty levels |

## Alternative approaches

### Approach B: Scoring-based classification

```python
def classify_ticket_scored(text: str) -> str:
    """Classify by counting keyword matches across all levels."""
    lower_text = text.lower()
    scores = {}

    # WHY scoring: Instead of returning on the first match, count
    # how many keywords match at each level.  The level with the
    # most matches wins.
    for priority, keywords in PRIORITY_KEYWORDS.items():
        scores[priority] = sum(1 for kw in keywords if kw in lower_text)

    # WHY max with key: Find the priority with the highest match count.
    best = max(scores, key=lambda p: scores[p])
    if scores[best] == 0:
        return "low"
    return best
```

**Trade-off:** The scoring approach is more nuanced — a ticket mentioning three "medium" keywords but only one "critical" keyword would be classified as "medium" instead of "critical". The first-match approach in the primary solution always picks the highest-severity match, which is the safer default for incident response (you would rather over-escalate than under-escalate). Use scoring when you want to weight the evidence rather than escalate on a single keyword.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Ticket with no matching keywords ("Everything is fine") | `classify_ticket()` returns "low" as the default, which is the correct behaviour | The final `return "low"` handles this case |
| Ticket matching keywords from multiple levels | The first-match approach returns the highest severity (critical > high > medium > low) because we iterate in priority order | The explicit `for priority in ["critical", "high", ...]` loop ensures this ordering |
| Empty line in ticket file | `process_tickets()` skips it because of the `if not stripped: continue` guard | The blank-line check is already in place |
| Multi-word keyword like "data loss" | Substring matching handles it correctly — `"data loss" in "We experienced data loss"` is True | Multi-word keywords work naturally with `in` operator |

## Key takeaways

1. **Business rules belong in data structures, not in if/elif chains.** Storing keywords in a dict makes rules configurable, testable, and eventually loadable from a database or config file. This data-driven approach is how real ticket routing systems work.
2. **Order of evaluation matters in priority systems.** Checking critical before low ensures the highest matching priority wins. This "first match wins" pattern appears in firewall rules, CSS specificity, and URL routing.
3. **This project connects to real incident management systems.** PagerDuty, Jira Service Management, and Zendesk all route tickets by keyword analysis and rules. The same pattern scales from a simple script to enterprise help desk software.
