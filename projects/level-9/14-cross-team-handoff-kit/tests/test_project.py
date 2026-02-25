"""Tests for Cross-Team Handoff Kit.

Covers: completeness scoring, missing sections, builder pattern,
checklist generation, and serialization.
"""

from __future__ import annotations

import pytest

from project import (
    ArchitectureNote,
    Contact,
    Dependency,
    HandoffBuilder,
    HandoffDocument,
    IssueSeverity,
    KnownIssue,
    MonitoringConfig,
    Runbook,
    ServiceOverview,
    generate_checklist,
)


# --- Fixtures -----------------------------------------------------------

@pytest.fixture
def service() -> ServiceOverview:
    return ServiceOverview(
        name="api-service",
        purpose="Core API gateway",
        tech_stack=["Python", "FastAPI"],
        repo_url="https://github.com/org/api",
    )


@pytest.fixture
def full_doc(service: ServiceOverview) -> HandoffDocument:
    return (
        HandoffBuilder(service, "team-a", "team-b", "2024-01-01")
        .add_architecture(ArchitectureNote("API", "REST endpoints", rationale="simplicity"))
        .add_known_issue(KnownIssue("Bug", "desc", IssueSeverity.MEDIUM, workaround="restart"))
        .add_contact(Contact("Alice", "Lead", "team-a"))
        .add_runbook(Runbook("Deploy", "New release", ["build", "deploy"], last_tested="2024-01-01"))
        .add_dependency(Dependency("db", "upstream"))
        .set_monitoring(MonitoringConfig(
            dashboard_url="https://grafana.co/api",
            key_metrics=["latency"],
            slos=["99.9% uptime"],
        ))
        .build()
    )


@pytest.fixture
def empty_doc() -> HandoffDocument:
    service = ServiceOverview(name="empty", purpose="")
    return HandoffDocument(service=service, from_team="a", to_team="b", date="2024-01-01")


# --- Completeness scoring -----------------------------------------------

class TestCompleteness:
    def test_full_doc_high_score(self, full_doc: HandoffDocument) -> None:
        assert full_doc.completeness_score >= 90

    def test_empty_doc_low_score(self, empty_doc: HandoffDocument) -> None:
        assert empty_doc.completeness_score == 0

    def test_partial_doc_middle_score(self, service: ServiceOverview) -> None:
        doc = (
            HandoffBuilder(service, "a", "b", "2024-01-01")
            .add_contact(Contact("Alice", "Lead", "team-a"))
            .build()
        )
        score = doc.completeness_score
        assert 20 < score < 80


# --- Missing sections ---------------------------------------------------

class TestMissingSections:
    def test_full_doc_no_missing(self, full_doc: HandoffDocument) -> None:
        assert len(full_doc.missing_sections) == 0

    def test_empty_doc_all_missing(self, empty_doc: HandoffDocument) -> None:
        missing = empty_doc.missing_sections
        assert "overview" in missing
        assert "architecture" in missing
        assert "contacts" in missing
        assert "runbooks" in missing


# --- Builder pattern ----------------------------------------------------

class TestBuilder:
    def test_chaining(self, service: ServiceOverview) -> None:
        doc = (
            HandoffBuilder(service, "a", "b", "2024-01-01")
            .add_architecture(ArchitectureNote("c1", "desc"))
            .add_architecture(ArchitectureNote("c2", "desc"))
            .add_contact(Contact("Alice", "Lead", "a"))
            .build()
        )
        assert len(doc.architecture) == 2
        assert len(doc.contacts) == 1

    def test_builder_sets_metadata(self, service: ServiceOverview) -> None:
        doc = HandoffBuilder(service, "from", "to", "2024-06-01").build()
        assert doc.from_team == "from"
        assert doc.to_team == "to"
        assert doc.date == "2024-06-01"


# --- Checklist generation -----------------------------------------------

class TestChecklist:
    def test_checklist_has_items(self, full_doc: HandoffDocument) -> None:
        checklist = generate_checklist(full_doc)
        assert len(checklist) >= 7

    def test_critical_issues_in_checklist(self, service: ServiceOverview) -> None:
        doc = (
            HandoffBuilder(service, "a", "b", "2024-01-01")
            .add_known_issue(KnownIssue("Outage risk", "desc", IssueSeverity.CRITICAL))
            .build()
        )
        checklist = generate_checklist(doc)
        critical_tasks = [c for c in checklist if "critical" in c["task"].lower()]
        assert len(critical_tasks) == 1

    def test_tested_runbooks_marked_done(self, service: ServiceOverview) -> None:
        doc = (
            HandoffBuilder(service, "a", "b", "2024-01-01")
            .add_runbook(Runbook("r1", "trigger", ["step"], last_tested="2024-01-01"))
            .build()
        )
        checklist = generate_checklist(doc)
        runbook_item = next(c for c in checklist if "runbook" in c["task"].lower())
        assert runbook_item["done"] is True

    def test_untested_runbooks_not_done(self, service: ServiceOverview) -> None:
        doc = (
            HandoffBuilder(service, "a", "b", "2024-01-01")
            .add_runbook(Runbook("r1", "trigger", ["step"]))
            .build()
        )
        checklist = generate_checklist(doc)
        runbook_item = next(c for c in checklist if "runbook" in c["task"].lower())
        assert runbook_item["done"] is False


# --- Serialization ------------------------------------------------------

class TestSerialization:
    def test_to_dict_structure(self, full_doc: HandoffDocument) -> None:
        d = full_doc.to_dict()
        assert d["service"] == "api-service"
        assert "completeness_score" in d
        assert "missing_sections" in d
        assert d["contacts_count"] == 1

    @pytest.mark.parametrize("field_name", [
        "from_team", "to_team", "date", "known_issues_count",
        "runbooks_count", "dependencies_count",
    ])
    def test_required_fields(self, full_doc: HandoffDocument, field_name: str) -> None:
        d = full_doc.to_dict()
        assert field_name in d
