# Solution: Level 9 / Project 14 - Cross Team Handoff Kit

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
"""Cross-Team Handoff Kit — generate structured handoff documents for team transitions."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# --- Domain types -------------------------------------------------------

# WHY enumerate handoff sections? -- Each section represents a category of
# institutional knowledge that gets lost during team transitions. Making them
# explicit ensures completeness — the scoring system can check that every
# section has content, flagging gaps before the handoff happens rather than
# discovering missing knowledge during a 2 AM incident.
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

    # WHY a completeness score? -- Handoffs with missing sections lead to
    # 2 AM incidents where the new team has no runbook and no contacts.
    # A numeric score makes gaps visible before the transition, enabling
    # the outgoing team to fill them. Treat scores below 80 as blockers.
    @property
    def completeness_score(self) -> float:
        """Score how complete the handoff document is (0-100)."""
        score = 0.0
        max_score = 100.0

        if self.service.purpose:
            score += 10
        if self.service.tech_stack:
            score += 5
        if self.service.repo_url:
            score += 5

        if self.architecture:
            score += 10
            if any(a.rationale for a in self.architecture):
                score += 5

        if self.known_issues:
            score += 10
            if any(i.workaround for i in self.known_issues):
                score += 5

        if self.contacts:
            score += 10

        if self.runbooks:
            score += 10
            if any(r.is_tested for r in self.runbooks):
                score += 5

        if self.dependencies:
            score += 10

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

# WHY the builder pattern? -- Handoff documents have many optional sections.
# A constructor with 10+ parameters is hard to read and easy to misuse.
# The builder provides method chaining (.add_contact().add_runbook()...build())
# that reads like a natural description of the document's contents.
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Builder pattern with method chaining | Handoff documents have many optional sections; builder provides readable fluent API for construction | Constructor with 10+ parameters -- hard to read, easy to pass arguments in wrong order |
| Completeness scoring with section weights | Surfaces gaps before the handoff happens; a score below 80 means critical knowledge is missing | Boolean complete/incomplete -- loses granularity; a document missing only monitoring is more complete than one missing everything |
| Tested runbook tracking via `last_tested` | An untested runbook is a liability; tracking the test date incentivizes regular runbook exercises | No testing metadata -- teams discover broken runbooks during real incidents |
| Auto-generated checklist from document content | Ensures the receiving team has a concrete list of tasks; tasks auto-mark as done based on document completeness | Manual checklist -- disconnected from the actual document; quickly becomes out of date |
| Critical issues added to checklist automatically | Critical known issues must be addressed during transition; auto-adding them ensures nothing is missed | Only listing issues in the document -- issues may not be acted on during the handoff |

## Alternative approaches

### Approach B: Interactive handoff wizard

```python
class HandoffWizard:
    """Step-by-step interactive handoff that prompts for each section,
    showing completeness progress as sections are filled."""
    def __init__(self):
        self._builder = None
        self._current_section = 0
        self._sections = list(HandoffSection)

    def start(self, service, from_team, to_team, date):
        self._builder = HandoffBuilder(
            ServiceOverview(name=service, purpose=""), from_team, to_team, date
        )
        return self._prompt_next()

    def _prompt_next(self) -> dict:
        if self._current_section >= len(self._sections):
            return {"status": "complete", "document": self._builder.build().to_dict()}
        section = self._sections[self._current_section]
        return {
            "status": "in_progress",
            "current_section": section.value,
            "progress_pct": self._current_section / len(self._sections) * 100,
            "prompt": f"Please provide information for: {section.value}",
        }
```

**Trade-off:** An interactive wizard guides users through each section, preventing them from skipping critical information. It shows progress ("60% complete, 3 sections remaining") and prompts for missing data. The tradeoff is that it requires a UI or CLI interaction model, making it harder to use in batch/automated contexts. Use the builder pattern for programmatic use; the wizard pattern for human-driven handoff processes.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Empty known_issues list | Completeness score drops by 15 points; "known_issues" appears in missing_sections | Even if there are no issues, document this explicitly ("No known issues as of [date]") |
| Runbook with no steps | `is_tested` check passes if `last_tested` is set, but an empty steps list is useless | Validate that runbooks have at least one step before accepting them |
| Builder reused after `build()` | Subsequent modifications to the builder mutate the already-built document (shared reference) | Either clone the document in `build()` or document that the builder is single-use |
