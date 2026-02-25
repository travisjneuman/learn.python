"""Tests for Incident Postmortem Generator.

Covers: impact scoring, completeness validation, section generation,
quality assessment, and action item tracking.
"""

from __future__ import annotations

import pytest

from project import (
    ActionItem,
    ActionPriority,
    ActionStatus,
    ImpactSummary,
    IncidentData,
    IncidentSeverity,
    PostmortemGenerator,
    TimelineEntry,
    assess_quality,
)


# --- Fixtures -----------------------------------------------------------

@pytest.fixture
def generator() -> PostmortemGenerator:
    return PostmortemGenerator()


@pytest.fixture
def full_incident() -> IncidentData:
    return IncidentData(
        incident_id="INC-001",
        title="API outage",
        severity=IncidentSeverity.SEV1,
        date="2024-01-15",
        summary="Total API failure for 2 hours.",
        root_cause="Memory leak in request handler.",
        trigger="Traffic spike after product launch.",
        impact=ImpactSummary(
            affected_users=50000,
            affected_services=["api", "web", "mobile"],
            duration_minutes=120,
            revenue_impact_usd=200000,
            data_loss=True,
        ),
        timeline=[
            TimelineEntry("10:00", "Alerts fire", "PagerDuty"),
            TimelineEntry("10:05", "On-call responds", "alice"),
            TimelineEntry("10:30", "Root cause found", "alice"),
            TimelineEntry("11:00", "Fix deployed", "bob"),
        ],
        contributing_factors=["No memory limits", "Missing circuit breaker"],
        what_went_well=["Fast escalation"],
        what_went_poorly=["Slow detection"],
    )


@pytest.fixture
def minimal_incident() -> IncidentData:
    return IncidentData(
        incident_id="INC-002",
        title="Minor CSS bug",
        severity=IncidentSeverity.SEV4,
        date="2024-02-01",
        summary="Button color wrong.",
        root_cause="",
        trigger="",
        impact=ImpactSummary(),
    )


# --- Impact scoring -----------------------------------------------------

class TestImpactScoring:
    @pytest.mark.parametrize("users,min_score", [
        (50, 0),
        (500, 10),
        (5000, 20),
        (50000, 30),
    ])
    def test_user_impact_scaling(self, users: int, min_score: float) -> None:
        impact = ImpactSummary(affected_users=users)
        assert impact.severity_score >= min_score

    def test_maximum_severity(self) -> None:
        impact = ImpactSummary(
            affected_users=100000,
            affected_services=["a", "b", "c", "d", "e"],
            duration_minutes=300,
            revenue_impact_usd=500000,
            data_loss=True,
        )
        assert impact.severity_score == 100

    def test_zero_impact(self) -> None:
        impact = ImpactSummary()
        assert impact.severity_score == 0

    def test_data_loss_adds_points(self) -> None:
        without = ImpactSummary(affected_users=100)
        with_loss = ImpactSummary(affected_users=100, data_loss=True)
        assert with_loss.severity_score > without.severity_score


# --- Completeness validation -------------------------------------------

class TestValidation:
    def test_full_incident_no_missing(self, generator: PostmortemGenerator,
                                       full_incident: IncidentData) -> None:
        missing = generator.validate_completeness(full_incident)
        assert len(missing) == 0

    def test_minimal_incident_has_missing(self, generator: PostmortemGenerator,
                                           minimal_incident: IncidentData) -> None:
        missing = generator.validate_completeness(minimal_incident)
        assert "root_cause" in missing
        assert "trigger" in missing
        assert "timeline" in missing


# --- Section generation -------------------------------------------------

class TestSections:
    def test_all_sections_present(self, generator: PostmortemGenerator,
                                   full_incident: IncidentData) -> None:
        postmortem = generator.generate(full_incident)
        expected = {"summary", "impact", "timeline", "root_cause", "lessons"}
        assert set(postmortem.sections.keys()) == expected

    def test_summary_contains_title(self, generator: PostmortemGenerator,
                                     full_incident: IncidentData) -> None:
        postmortem = generator.generate(full_incident)
        assert full_incident.title in postmortem.sections["summary"]

    def test_impact_contains_user_count(self, generator: PostmortemGenerator,
                                         full_incident: IncidentData) -> None:
        postmortem = generator.generate(full_incident)
        assert "50,000" in postmortem.sections["impact"]

    def test_timeline_entries_rendered(self, generator: PostmortemGenerator,
                                       full_incident: IncidentData) -> None:
        postmortem = generator.generate(full_incident)
        assert "Alerts fire" in postmortem.sections["timeline"]
        assert "10:00" in postmortem.sections["timeline"]


# --- Quality assessment -------------------------------------------------

class TestQuality:
    def test_full_incident_high_quality(self, full_incident: IncidentData) -> None:
        actions = [ActionItem("A1", "Fix", "alice", ActionPriority.HIGH)]
        score = assess_quality(full_incident, actions)
        assert score >= 80

    def test_minimal_incident_low_quality(self, minimal_incident: IncidentData) -> None:
        score = assess_quality(minimal_incident, [])
        assert score < 30

    def test_actions_without_owners_lower_score(self, full_incident: IncidentData) -> None:
        with_owner = [ActionItem("A1", "Fix", "alice", ActionPriority.HIGH)]
        without_owner = [ActionItem("A1", "Fix", "", ActionPriority.HIGH)]
        score_with = assess_quality(full_incident, with_owner)
        score_without = assess_quality(full_incident, without_owner)
        assert score_with > score_without


# --- Serialization ------------------------------------------------------

class TestSerialization:
    def test_to_dict_structure(self, generator: PostmortemGenerator,
                                full_incident: IncidentData) -> None:
        actions = [ActionItem("A1", "Fix leak", "alice", ActionPriority.CRITICAL)]
        postmortem = generator.generate(full_incident, actions)
        d = postmortem.to_dict()
        assert d["incident_id"] == "INC-001"
        assert d["severity"] == "sev1"
        assert len(d["action_items"]) == 1
        assert "quality_score" in d
