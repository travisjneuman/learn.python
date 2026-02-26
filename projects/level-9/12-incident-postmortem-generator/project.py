"""Incident Postmortem Generator — produce structured postmortems from incident data.

Design rationale:
    Blameless postmortems are essential for learning from failures. This
    project takes raw incident data (timeline, impact, actions) and
    generates a structured postmortem document with severity classification,
    root cause analysis prompts, and action item tracking.

Concepts practised:
    - builder pattern for document assembly
    - template method for report sections
    - dataclasses with rich domain logic
    - enum-based classification
    - string formatting and report generation
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


# --- Domain types -------------------------------------------------------

class IncidentSeverity(Enum):
    SEV1 = "sev1"
    SEV2 = "sev2"
    SEV3 = "sev3"
    SEV4 = "sev4"


# WHY track action items with priority AND status? -- Postmortems without
# tracked action items are theater. The priority ensures critical fixes
# (prevent recurrence) are addressed before nice-to-haves. The status
# tracks completion — blameless postmortem culture requires following
# through on commitments, and the status field makes that visible.
class ActionPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ActionStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class TimelineEntry:
    """A single event in the incident timeline."""
    timestamp: str  # ISO format string
    description: str
    actor: str = ""

    def to_dict(self) -> dict[str, str]:
        return {"timestamp": self.timestamp, "description": self.description, "actor": self.actor}


@dataclass
class ActionItem:
    """A follow-up action from the postmortem."""
    action_id: str
    description: str
    owner: str
    priority: ActionPriority
    status: ActionStatus = ActionStatus.OPEN
    due_date: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.action_id,
            "description": self.description,
            "owner": self.owner,
            "priority": self.priority.value,
            "status": self.status.value,
            "due_date": self.due_date,
        }


@dataclass
class ImpactSummary:
    """Quantified impact of the incident."""
    affected_users: int = 0
    affected_services: list[str] = field(default_factory=list)
    duration_minutes: float = 0
    revenue_impact_usd: float = 0
    data_loss: bool = False

    @property
    def severity_score(self) -> float:
        """Compute a numeric severity score (0-100) from impact metrics."""
        score = 0.0
        # User impact: up to 30 points
        if self.affected_users > 10000:
            score += 30
        elif self.affected_users > 1000:
            score += 20
        elif self.affected_users > 100:
            score += 10
        # Duration: up to 25 points
        if self.duration_minutes > 240:
            score += 25
        elif self.duration_minutes > 60:
            score += 15
        elif self.duration_minutes > 15:
            score += 5
        # Service breadth: up to 20 points
        score += min(20, len(self.affected_services) * 5)
        # Revenue: up to 15 points
        if self.revenue_impact_usd > 100000:
            score += 15
        elif self.revenue_impact_usd > 10000:
            score += 10
        elif self.revenue_impact_usd > 0:
            score += 5
        # Data loss: 10 points
        if self.data_loss:
            score += 10
        return min(100, score)

    def to_dict(self) -> dict[str, Any]:
        return {
            "affected_users": self.affected_users,
            "affected_services": self.affected_services,
            "duration_minutes": self.duration_minutes,
            "revenue_impact_usd": self.revenue_impact_usd,
            "data_loss": self.data_loss,
            "severity_score": self.severity_score,
        }


@dataclass
class IncidentData:
    """Raw incident data used to generate a postmortem."""
    incident_id: str
    title: str
    severity: IncidentSeverity
    date: str
    summary: str
    root_cause: str
    trigger: str
    impact: ImpactSummary
    timeline: list[TimelineEntry] = field(default_factory=list)
    contributing_factors: list[str] = field(default_factory=list)
    what_went_well: list[str] = field(default_factory=list)
    what_went_poorly: list[str] = field(default_factory=list)


# --- Postmortem generation ----------------------------------------------

@dataclass
class Postmortem:
    """A structured postmortem document."""
    incident_id: str
    title: str
    severity: IncidentSeverity
    date: str
    sections: dict[str, str] = field(default_factory=dict)
    action_items: list[ActionItem] = field(default_factory=list)
    quality_score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "incident_id": self.incident_id,
            "title": self.title,
            "severity": self.severity.value,
            "date": self.date,
            "sections": self.sections,
            "action_items": [a.to_dict() for a in self.action_items],
            "quality_score": round(self.quality_score, 1),
        }


def _build_summary_section(data: IncidentData) -> str:
    return (
        f"Incident: {data.title}\n"
        f"Severity: {data.severity.value.upper()}\n"
        f"Date: {data.date}\n\n"
        f"{data.summary}"
    )


def _build_impact_section(data: IncidentData) -> str:
    imp = data.impact
    lines = [
        f"Affected Users: {imp.affected_users:,}",
        f"Affected Services: {', '.join(imp.affected_services) or 'None'}",
        f"Duration: {imp.duration_minutes} minutes",
        f"Revenue Impact: ${imp.revenue_impact_usd:,.2f}",
        f"Data Loss: {'Yes' if imp.data_loss else 'No'}",
        f"Severity Score: {imp.severity_score}/100",
    ]
    return "\n".join(lines)


def _build_timeline_section(data: IncidentData) -> str:
    if not data.timeline:
        return "No timeline entries recorded."
    lines = []
    for entry in data.timeline:
        actor = f" [{entry.actor}]" if entry.actor else ""
        lines.append(f"  {entry.timestamp}{actor}: {entry.description}")
    return "\n".join(lines)


def _build_root_cause_section(data: IncidentData) -> str:
    parts = [f"Root Cause: {data.root_cause}", f"Trigger: {data.trigger}"]
    if data.contributing_factors:
        parts.append("\nContributing Factors:")
        for f in data.contributing_factors:
            parts.append(f"  - {f}")
    return "\n".join(parts)


def _build_lessons_section(data: IncidentData) -> str:
    parts: list[str] = []
    if data.what_went_well:
        parts.append("What Went Well:")
        for item in data.what_went_well:
            parts.append(f"  + {item}")
    if data.what_went_poorly:
        parts.append("\nWhat Went Poorly:")
        for item in data.what_went_poorly:
            parts.append(f"  - {item}")
    return "\n".join(parts) if parts else "No lessons recorded."


def assess_quality(data: IncidentData, action_items: list[ActionItem]) -> float:
    """Score postmortem completeness (0-100)."""
    score = 0.0
    if data.root_cause:
        score += 20
    if data.trigger:
        score += 10
    if len(data.timeline) >= 3:
        score += 15
    elif data.timeline:
        score += 5
    if data.contributing_factors:
        score += 10
    if data.what_went_well:
        score += 10
    if data.what_went_poorly:
        score += 10
    if action_items:
        score += 15
    # Bonus for having owners on all actions
    if action_items and all(a.owner for a in action_items):
        score += 10
    return min(100, score)


class PostmortemGenerator:
    """Generates structured postmortem documents from incident data."""

    def __init__(self) -> None:
        self._section_builders: dict[str, Any] = {
            "summary": _build_summary_section,
            "impact": _build_impact_section,
            "timeline": _build_timeline_section,
            "root_cause": _build_root_cause_section,
            "lessons": _build_lessons_section,
        }

    def generate(self, data: IncidentData, action_items: list[ActionItem] | None = None) -> Postmortem:
        """Build a complete postmortem from incident data."""
        actions = action_items or []
        sections = {
            name: builder(data)
            for name, builder in self._section_builders.items()
        }
        quality = assess_quality(data, actions)
        return Postmortem(
            incident_id=data.incident_id,
            title=data.title,
            severity=data.severity,
            date=data.date,
            sections=sections,
            action_items=actions,
            quality_score=quality,
        )

    def validate_completeness(self, data: IncidentData) -> list[str]:
        """Return list of missing fields that should be filled."""
        missing: list[str] = []
        if not data.root_cause:
            missing.append("root_cause")
        if not data.trigger:
            missing.append("trigger")
        if not data.timeline:
            missing.append("timeline")
        if not data.summary:
            missing.append("summary")
        if not data.what_went_well:
            missing.append("what_went_well")
        if not data.what_went_poorly:
            missing.append("what_went_poorly")
        return missing


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    gen = PostmortemGenerator()

    data = IncidentData(
        incident_id="INC-2024-042",
        title="Database connection pool exhaustion",
        severity=IncidentSeverity.SEV2,
        date="2024-03-15",
        summary="Connection pool exhaustion caused API errors for 45 minutes.",
        root_cause="Connection leak in retry logic — connections not returned on error path.",
        trigger="Traffic spike from marketing campaign.",
        impact=ImpactSummary(
            affected_users=5000,
            affected_services=["api", "web-app"],
            duration_minutes=45,
            revenue_impact_usd=15000,
        ),
        timeline=[
            TimelineEntry("09:15", "Alerts fire for elevated 5xx rate", "PagerDuty"),
            TimelineEntry("09:18", "On-call engineer acknowledges", "alice"),
            TimelineEntry("09:30", "Root cause identified", "alice"),
            TimelineEntry("09:45", "Hotfix deployed", "bob"),
            TimelineEntry("10:00", "All clear confirmed", "alice"),
        ],
        contributing_factors=["No connection pool monitoring", "Missing circuit breaker"],
        what_went_well=["Fast detection", "Clear escalation path"],
        what_went_poorly=["No runbook for pool exhaustion", "Slow initial diagnosis"],
    )

    actions = [
        ActionItem("A1", "Add connection pool metrics", "alice", ActionPriority.HIGH),
        ActionItem("A2", "Implement circuit breaker", "bob", ActionPriority.CRITICAL),
        ActionItem("A3", "Write runbook for pool issues", "carol", ActionPriority.MEDIUM),
    ]

    postmortem = gen.generate(data, actions)
    return postmortem.to_dict()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Incident postmortem generator")
    parser.add_argument("--demo", action="store_true", default=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    print(json.dumps(run_demo(), indent=2))


if __name__ == "__main__":
    main()
