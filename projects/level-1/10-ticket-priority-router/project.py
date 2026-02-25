"""Level 1 project: Ticket Priority Router.

Route support tickets to priority queues based on keywords.
Tickets containing urgent words go to high priority, etc.

Concepts: keyword matching, dictionaries, string search, business rules.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


# Keywords that indicate each priority level.
PRIORITY_KEYWORDS = {
    "critical": ["down", "outage", "crash", "data loss", "security breach"],
    "high": ["error", "broken", "failing", "urgent", "blocked"],
    "medium": ["slow", "degraded", "intermittent", "bug", "issue"],
    "low": ["question", "request", "enhancement", "feature", "how to"],
}


def classify_ticket(text: str) -> str:
    """Determine the priority of a ticket based on keywords.

    WHY check critical first? -- Priority keywords overlap.  By checking
    the highest priority first, a ticket mentioning 'crash' gets
    classified as critical even if it also mentions 'slow'.
    """
    lower_text = text.lower()

    for priority in ["critical", "high", "medium", "low"]:
        for keyword in PRIORITY_KEYWORDS[priority]:
            if keyword in lower_text:
                return priority

    return "low"  # Default priority if no keywords match.


def route_ticket(ticket_id: int, text: str) -> dict:
    """Build a routed ticket record."""
    priority = classify_ticket(text)
    return {
        "id": ticket_id,
        "text": text.strip(),
        "priority": priority,
    }


def process_tickets(lines: list[str]) -> list[dict]:
    """Process a list of ticket descriptions."""
    tickets = []
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped:
            continue
        tickets.append(route_ticket(i, stripped))
    return tickets


def group_by_priority(tickets: list[dict]) -> dict[str, list[dict]]:
    """Group tickets into priority queues.

    WHY group? -- Operations teams work through tickets by priority.
    Grouping makes it easy to see the most urgent items first.
    """
    groups = {"critical": [], "high": [], "medium": [], "low": []}
    for ticket in tickets:
        groups[ticket["priority"]].append(ticket)
    return groups


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ticket Priority Router")
    parser.add_argument("--input", default="data/sample_input.txt")
    parser.add_argument("--output", default="data/output.json")
    return parser.parse_args()


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
            print(f"    #{t['id']}: {t['text'][:60]}")
        print()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps({"tickets": tickets, "queues": {k: len(v) for k, v in groups.items()}}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
