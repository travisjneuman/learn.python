"""Cross-Team Handoff Kit — generate structured handoff documents for team transitions.

Design rationale:
    When ownership of a service transfers between teams, critical context
    gets lost. This project builds a handoff document generator that
    captures architecture, operational knowledge, known issues, contacts,
    and runbooks in a structured format with completeness scoring.

Concepts practised:
    - builder pattern for document assembly
    - dataclasses with validation
    - completeness scoring heuristics
    - template-based text generation
    - enum-based categorization
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# --- Domain types -------------------------------------------------------

class HandoffSection(Enum):
    OVERVIEW = "overview"
    ARCHITECTURE = "architecture"
    OPERATIONS = "operations"
    KNOWN_ISSUES = "known_issues"
    CONTACTS = "contacts"
    RUNBOOKS = "runbooks"
    DEPENDENCIES = "dependencies"
    MONITORING = "monitoring"


class IssueSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ServiceOverview:
    """High-level service description."""
    name: str
    purpose: str
    tech_stack: list[str] = field(default_factory=list)
    repo_url: str = ""
    documentation_url: str = ""


@dataclass
class ArchitectureNote:
    """Key architectural decision or component description."""
    component: str
    description: str
    rationale: str = ""
    diagram_url: str = ""


@dataclass
class KnownIssue:
    """A known issue or technical debt item."""
    title: str
    description: str
    severity: IssueSeverity
    workaround: str = ""
    ticket_url: str = ""


@dataclass
class Contact:
    """A key contact for the service."""
    name: str
    role: str
    team: str
    email: str = ""
    notes: str = ""


@dataclass
class Runbook:
    """An operational runbook."""
    title: str
    trigger: str
    steps: list[str] = field(default_factory=list)
    last_tested: str = ""

    @property
    def is_tested(self) -> bool:
        return bool(self.last_tested)


@dataclass
class Dependency:
    """An upstream or downstream service dependency."""
    service_name: str
    direction: str  # "upstream" or "downstream"
    protocol: str = ""
    criticality: str = "medium"
    notes: str = ""


@dataclass
class MonitoringConfig:
    """Monitoring and alerting configuration."""
    dashboard_url: str = ""
    alert_channels: list[str] = field(default_factory=list)
    key_metrics: list[str] = field(default_factory=list)
    slos: list[str] = field(default_factory=list)


# --- Handoff document ---------------------------------------------------

@dataclass
class HandoffDocument:
    """Complete handoff document for a service transition."""
    service: ServiceOverview
    from_team: str
    to_team: str
    date: str
    architecture: list[ArchitectureNote] = field(default_factory=list)
    known_issues: list[KnownIssue] = field(default_factory=list)
    contacts: list[Contact] = field(default_factory=list)
    runbooks: list[Runbook] = field(default_factory=list)
    dependencies: list[Dependency] = field(default_factory=list)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    notes: str = ""

    @property
    def completeness_score(self) -> float:
        """Score how complete the handoff document is (0-100)."""
        score = 0.0
        max_score = 100.0

        # Overview (20 points)
        if self.service.purpose:
            score += 10
        if self.service.tech_stack:
            score += 5
        if self.service.repo_url:
            score += 5

        # Architecture (15 points)
        if self.architecture:
            score += 10
            if any(a.rationale for a in self.architecture):
                score += 5

        # Known issues (15 points)
        if self.known_issues:
            score += 10
            if any(i.workaround for i in self.known_issues):
                score += 5

        # Contacts (10 points)
        if self.contacts:
            score += 10

        # Runbooks (15 points)
        if self.runbooks:
            score += 10
            if any(r.is_tested for r in self.runbooks):
                score += 5

        # Dependencies (10 points)
        if self.dependencies:
            score += 10

        # Monitoring (15 points)
        if self.monitoring.dashboard_url:
            score += 5
        if self.monitoring.key_metrics:
            score += 5
        if self.monitoring.slos:
            score += 5

        return min(max_score, score)

    @property
    def missing_sections(self) -> list[str]:
        """Return names of sections with no content."""
        missing: list[str] = []
        if not self.service.purpose:
            missing.append(HandoffSection.OVERVIEW.value)
        if not self.architecture:
            missing.append(HandoffSection.ARCHITECTURE.value)
        if not self.known_issues:
            missing.append(HandoffSection.KNOWN_ISSUES.value)
        if not self.contacts:
            missing.append(HandoffSection.CONTACTS.value)
        if not self.runbooks:
            missing.append(HandoffSection.RUNBOOKS.value)
        if not self.dependencies:
            missing.append(HandoffSection.DEPENDENCIES.value)
        if not self.monitoring.key_metrics:
            missing.append(HandoffSection.MONITORING.value)
        return missing

    def to_dict(self) -> dict[str, Any]:
        return {
            "service": self.service.name,
            "from_team": self.from_team,
            "to_team": self.to_team,
            "date": self.date,
            "completeness_score": round(self.completeness_score, 1),
            "missing_sections": self.missing_sections,
            "architecture_items": len(self.architecture),
            "known_issues_count": len(self.known_issues),
            "critical_issues": sum(
                1 for i in self.known_issues if i.severity == IssueSeverity.CRITICAL
            ),
            "contacts_count": len(self.contacts),
            "runbooks_count": len(self.runbooks),
            "tested_runbooks": sum(1 for r in self.runbooks if r.is_tested),
            "dependencies_count": len(self.dependencies),
        }


# --- Handoff builder ----------------------------------------------------

class HandoffBuilder:
    """Builder pattern for constructing handoff documents step by step."""

    def __init__(self, service: ServiceOverview, from_team: str, to_team: str, date: str) -> None:
        self._doc = HandoffDocument(
            service=service, from_team=from_team, to_team=to_team, date=date,
        )

    def add_architecture(self, note: ArchitectureNote) -> HandoffBuilder:
        self._doc.architecture.append(note)
        return self

    def add_known_issue(self, issue: KnownIssue) -> HandoffBuilder:
        self._doc.known_issues.append(issue)
        return self

    def add_contact(self, contact: Contact) -> HandoffBuilder:
        self._doc.contacts.append(contact)
        return self

    def add_runbook(self, runbook: Runbook) -> HandoffBuilder:
        self._doc.runbooks.append(runbook)
        return self

    def add_dependency(self, dep: Dependency) -> HandoffBuilder:
        self._doc.dependencies.append(dep)
        return self

    def set_monitoring(self, config: MonitoringConfig) -> HandoffBuilder:
        self._doc.monitoring = config
        return self

    def set_notes(self, notes: str) -> HandoffBuilder:
        self._doc.notes = notes
        return self

    def build(self) -> HandoffDocument:
        return self._doc


def generate_checklist(doc: HandoffDocument) -> list[dict[str, Any]]:
    """Generate a transition checklist from the handoff document."""
    items: list[dict[str, Any]] = []

    items.append({"task": "Review architecture documentation", "done": bool(doc.architecture)})
    items.append({"task": "Review known issues", "done": bool(doc.known_issues)})
    items.append({"task": "Meet with key contacts", "done": bool(doc.contacts)})
    items.append({"task": "Test all runbooks", "done": all(r.is_tested for r in doc.runbooks) if doc.runbooks else False})
    items.append({"task": "Verify monitoring access", "done": bool(doc.monitoring.dashboard_url)})
    items.append({"task": "Map all dependencies", "done": bool(doc.dependencies)})
    items.append({"task": "Get repository access", "done": bool(doc.service.repo_url)})

    # Add items for critical issues
    for issue in doc.known_issues:
        if issue.severity == IssueSeverity.CRITICAL:
            items.append({
                "task": f"Address critical issue: {issue.title}",
                "done": False,
            })

    return items


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    service = ServiceOverview(
        name="payment-service",
        purpose="Processes all payment transactions",
        tech_stack=["Python", "FastAPI", "PostgreSQL", "Redis"],
        repo_url="https://github.com/org/payment-service",
    )

    doc = (
        HandoffBuilder(service, "payments-team", "platform-team", "2024-03-01")
        .add_architecture(ArchitectureNote(
            "API Gateway", "FastAPI with async handlers",
            rationale="High throughput requirement",
        ))
        .add_architecture(ArchitectureNote(
            "Database", "PostgreSQL with read replicas",
        ))
        .add_known_issue(KnownIssue(
            "Memory leak under load", "RSS grows 10MB/hour under sustained load",
            IssueSeverity.HIGH, workaround="Restart pods every 12 hours",
        ))
        .add_contact(Contact("Alice", "Tech Lead", "payments-team", "alice@co.com"))
        .add_contact(Contact("Bob", "SRE", "platform-team", "bob@co.com"))
        .add_runbook(Runbook(
            "Database failover", "Primary DB unreachable",
            ["Check replication lag", "Promote replica", "Update DNS"],
            last_tested="2024-02-15",
        ))
        .add_dependency(Dependency("stripe-api", "upstream", "HTTPS", "critical"))
        .add_dependency(Dependency("notification-service", "downstream", "gRPC"))
        .set_monitoring(MonitoringConfig(
            dashboard_url="https://grafana.co/payments",
            key_metrics=["p99_latency", "error_rate", "throughput"],
            slos=["99.9% availability", "p99 < 500ms"],
        ))
        .build()
    )

    checklist = generate_checklist(doc)

    return {
        "handoff": doc.to_dict(),
        "checklist": checklist,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cross-team handoff kit")
    parser.add_argument("--demo", action="store_true", default=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    print(json.dumps(run_demo(), indent=2))


if __name__ == "__main__":
    main()
