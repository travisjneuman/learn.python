# Solution: Level 9 / Project 01 - Architecture Decision Log

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first -- it guides
> your thinking without giving away the answer.
>
> [Back to project README](./README.md)

---

## Complete solution

```python
"""Architecture Decision Log — create and manage Architecture Decision Records."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable


# --- Domain types -------------------------------------------------------

class ADRStatus(Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"
    REJECTED = "rejected"


# WHY capture context, decision, AND consequences? -- The context explains
# the forces that led to the decision; the consequences document trade-offs
# accepted. Without context, future engineers don't know WHY a decision was
# made and may reverse it without understanding the constraints. The
# superseded_by field creates an audit chain across evolving decisions.
@dataclass
class ADR:
    """Architecture Decision Record."""
    adr_id: int
    title: str
    status: ADRStatus
    context: str
    decision: str
    consequences: str
    created_date: str = ""
    superseded_by: int | None = None
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.adr_id,
            "title": self.title,
            "status": self.status.value,
            "context": self.context,
            "decision": self.decision,
            "consequences": self.consequences,
            "created_date": self.created_date,
            "superseded_by": self.superseded_by,
            "tags": self.tags,
        }


# --- Observer pattern for status changes --------------------------------

# WHY a type alias for the callback? -- Defining StatusChangeCallback makes
# the observer contract explicit: callbacks receive the ADR plus old and new
# status. Without this, callers pass arbitrary callables and errors surface
# at runtime rather than at definition time.
StatusChangeCallback = Callable[[ADR, ADRStatus, ADRStatus], None]


class ADRLog:
    """Manages a collection of ADRs with CRUD, search, and notifications.

    Uses the observer pattern: register callbacks that fire whenever
    an ADR's status changes, enabling audit trails and integrations.
    """

    def __init__(self) -> None:
        self._adrs: dict[int, ADR] = {}
        self._next_id = 1
        self._observers: list[StatusChangeCallback] = []
        # WHY a separate change history list? -- Observers are ephemeral
        # (they exist only while registered). The history list provides a
        # persistent audit trail that survives observer lifecycle changes.
        self._change_history: list[dict[str, Any]] = []

    @property
    def count(self) -> int:
        return len(self._adrs)

    def on_status_change(self, callback: StatusChangeCallback) -> None:
        """Register an observer for status changes."""
        self._observers.append(callback)

    def create(
        self,
        title: str,
        context: str,
        decision: str,
        consequences: str,
        tags: list[str] | None = None,
    ) -> ADR:
        """Create a new ADR in PROPOSED status."""
        adr = ADR(
            adr_id=self._next_id,
            title=title,
            status=ADRStatus.PROPOSED,
            context=context,
            decision=decision,
            consequences=consequences,
            created_date=datetime.now().isoformat()[:10],
            tags=tags or [],
        )
        self._adrs[adr.adr_id] = adr
        self._next_id += 1
        return adr

    def get(self, adr_id: int) -> ADR | None:
        return self._adrs.get(adr_id)

    def update_status(self, adr_id: int, new_status: ADRStatus) -> ADR:
        """Change an ADR's status, notifying observers."""
        adr = self._adrs.get(adr_id)
        if adr is None:
            raise KeyError(f"ADR {adr_id} not found")
        old_status = adr.status
        adr.status = new_status

        change = {
            "adr_id": adr_id,
            "from": old_status.value,
            "to": new_status.value,
            "title": adr.title,
        }
        self._change_history.append(change)

        # WHY notify after recording history? -- If an observer raises an
        # exception, the history still captures the change. Observers are
        # fire-and-forget; the core state machine should not depend on them.
        for observer in self._observers:
            observer(adr, old_status, new_status)

        return adr

    def supersede(self, old_id: int, new_id: int) -> None:
        """Mark old ADR as superseded by new ADR."""
        old_adr = self._adrs.get(old_id)
        new_adr = self._adrs.get(new_id)
        if not old_adr:
            raise KeyError(f"ADR {old_id} not found")
        if not new_adr:
            raise KeyError(f"ADR {new_id} not found")
        old_adr.superseded_by = new_id
        self.update_status(old_id, ADRStatus.SUPERSEDED)

    def search(self, query: str) -> list[ADR]:
        """Full-text search across title, context, decision, consequences."""
        q = query.lower()
        return [
            adr for adr in self._adrs.values()
            if q in adr.title.lower()
            or q in adr.context.lower()
            or q in adr.decision.lower()
            or q in adr.consequences.lower()
        ]

    def filter_by_status(self, status: ADRStatus) -> list[ADR]:
        return [a for a in self._adrs.values() if a.status == status]

    def filter_by_tag(self, tag: str) -> list[ADR]:
        return [a for a in self._adrs.values() if tag in a.tags]

    def all(self) -> list[ADR]:
        return sorted(self._adrs.values(), key=lambda a: a.adr_id)

    def change_history(self) -> list[dict[str, Any]]:
        return list(self._change_history)

    def summary(self) -> dict[str, Any]:
        """Generate a summary of all ADRs by status."""
        by_status: dict[str, int] = {}
        for adr in self._adrs.values():
            by_status[adr.status.value] = by_status.get(adr.status.value, 0) + 1
        return {
            "total": self.count,
            "by_status": by_status,
            "recent": [a.to_dict() for a in self.all()[-5:]],
        }


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    """Demonstrate ADR lifecycle management."""
    log = ADRLog()
    notifications: list[str] = []
    log.on_status_change(
        lambda adr, old, new: notifications.append(
            f"ADR-{adr.adr_id} '{adr.title}': {old.value} -> {new.value}"
        )
    )

    adr1 = log.create(
        title="Use PostgreSQL for primary data store",
        context="We need a relational database for transactional data.",
        decision="Use PostgreSQL 15 with connection pooling via PgBouncer.",
        consequences="Team needs PostgreSQL expertise. Migrations via Alembic.",
        tags=["database", "infrastructure"],
    )
    adr2 = log.create(
        title="REST over GraphQL for public API",
        context="We need a stable public API. Team has REST experience.",
        decision="Use REST with OpenAPI spec. Reserve GraphQL for internal use.",
        consequences="Simpler tooling. May need BFF layer for mobile clients.",
        tags=["api", "architecture"],
    )
    adr3 = log.create(
        title="Migrate to GraphQL for public API",
        context="Mobile clients require flexible queries. BFF layer too complex.",
        decision="Adopt GraphQL with schema stitching for public API v2.",
        consequences="Need GraphQL training. REST API maintained for v1 compat.",
        tags=["api", "architecture"],
    )

    log.update_status(adr1.adr_id, ADRStatus.ACCEPTED)
    log.update_status(adr2.adr_id, ADRStatus.ACCEPTED)
    log.update_status(adr3.adr_id, ADRStatus.ACCEPTED)
    log.supersede(adr2.adr_id, adr3.adr_id)

    return {
        "summary": log.summary(),
        "search_results": [a.to_dict() for a in log.search("graphql")],
        "notifications": notifications,
        "history": log.change_history(),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Architecture Decision Log manager")
    parser.add_argument("--demo", action="store_true", default=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    print(json.dumps(run_demo(), indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Observer pattern for status changes | Decouples notification logic from core ADR state management; new integrations (Slack, email, audit log) register as observers without modifying ADRLog | Direct notification calls inside `update_status` -- tightly couples ADRLog to specific notification channels |
| Supersede chain via `superseded_by` field | Creates a linked list of decisions over time; you can trace why ADR-002 was replaced by ADR-003 | Deleting old ADRs -- loses the historical context that led to the current decision |
| Full-text search across all text fields | Engineers searching for "graphql" want to find every ADR that mentions it, whether in context, decision, or consequences | Searching only title -- misses ADRs where the keyword appears in the reasoning |
| Auto-incrementing IDs with `_next_id` | Guarantees unique IDs without external dependency; simple for in-memory use | UUIDs -- more robust for distributed systems but harder to reference in conversation ("ADR-3" vs "ADR-a7f3b2c1") |
| Change history as a separate persistent list | Survives observer lifecycle; provides a permanent audit trail even if observers are added/removed | Relying solely on observers for audit -- loses history when no observer is registered |

## Alternative approaches

### Approach B: Event-sourced ADR log

```python
class ADREvent:
    """Instead of mutating ADR state directly, record events and
    derive current state by replaying them."""
    def __init__(self, event_type: str, adr_id: int, data: dict):
        self.event_type = event_type  # "created", "status_changed", "superseded"
        self.adr_id = adr_id
        self.data = data
        self.timestamp = datetime.now().isoformat()

class EventSourcedADRLog:
    def __init__(self):
        self._events: list[ADREvent] = []

    def apply(self, event: ADREvent):
        self._events.append(event)

    def current_state(self, adr_id: int) -> dict:
        """Replay all events for this ADR to build current state."""
        state = {}
        for e in self._events:
            if e.adr_id == adr_id:
                state.update(e.data)
        return state
```

**Trade-off:** Event sourcing gives you a complete history of every change (not just status transitions), enabling temporal queries like "what did ADR-2 look like before it was superseded?" The tradeoff is added complexity: you must replay events to get current state, and event schemas need versioning as the domain evolves. Use direct mutation for simple systems, event sourcing when full audit trails and temporal queries are business requirements.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Superseding a non-existent ADR | `KeyError` raised because `_adrs.get(old_id)` returns `None` | Guard with explicit existence check and clear error message |
| Observer raises an exception during notification | Status change is recorded in history but remaining observers are not notified | Wrap each observer call in try/except, or use an event queue to decouple notification timing |
| Searching with empty string | Every ADR matches because `"" in any_string` is always `True` | Validate query is non-empty before searching, or return empty list for blank queries |
