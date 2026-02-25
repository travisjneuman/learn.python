"""Architecture Decision Log — create and manage Architecture Decision Records.

Design rationale:
    ADRs capture the context, decision, and consequences of significant
    architecture choices. This project builds a structured ADR system
    with status tracking, linking, and search — teaching documentation
    as a first-class engineering practice.

Concepts practised:
    - dataclasses for structured documents
    - enum for ADR lifecycle states
    - observer pattern for status change notifications
    - full-text search over structured records
    - JSON persistence and querying
"""

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
