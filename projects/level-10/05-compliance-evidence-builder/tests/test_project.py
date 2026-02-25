"""Tests for Compliance Evidence Builder.

Covers evidence collection, control assessment, report generation,
hash integrity, and collector composition.
"""
from __future__ import annotations

import pytest

from project import (
    AccessControlCollector,
    CompliancePackage,
    ControlDefinition,
    ControlStatus,
    EncryptionCheckCollector,
    Evidence,
    EvidenceType,
    TestResultCollector,
    build_demo_package,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def soc2_controls() -> list[ControlDefinition]:
    return [
        ControlDefinition("CC6.1", "SOC2", "Logical Access", "Restrict access"),
        ControlDefinition("CC6.7", "SOC2", "Encryption", "Encrypt data"),
        ControlDefinition("CC7.1", "SOC2", "Monitoring", "Detect anomalies"),
    ]


@pytest.fixture
def package(soc2_controls: list[ControlDefinition]) -> CompliancePackage:
    return CompliancePackage("SOC2-test", soc2_controls)


# ---------------------------------------------------------------------------
# Evidence basics
# ---------------------------------------------------------------------------

class TestEvidence:
    def test_content_hash_deterministic(self) -> None:
        ev = Evidence("EV-1", EvidenceType.CONFIGURATION, ("CC1",), "test", "content-a")
        assert ev.content_hash == ev.content_hash

    def test_different_content_different_hash(self) -> None:
        ev1 = Evidence("EV-1", EvidenceType.CONFIGURATION, ("CC1",), "test", "content-a")
        ev2 = Evidence("EV-2", EvidenceType.CONFIGURATION, ("CC1",), "test", "content-b")
        assert ev1.content_hash != ev2.content_hash


# ---------------------------------------------------------------------------
# Individual collectors
# ---------------------------------------------------------------------------

class TestEncryptionCollector:
    def test_collects_one_evidence(self) -> None:
        collector = EncryptionCheckCollector({"encryption_at_rest": True, "algorithm": "AES-256"})
        items = collector.collect()
        assert len(items) == 1
        assert "AES-256" in items[0].content

    def test_maps_to_correct_controls(self) -> None:
        collector = EncryptionCheckCollector({"encryption_at_rest": True})
        items = collector.collect()
        assert "CC6.1" in items[0].control_ids
        assert "CC6.7" in items[0].control_ids


class TestAccessControlCollector:
    def test_produces_one_evidence_per_policy(self) -> None:
        policies = [{"name": "p1"}, {"name": "p2"}, {"name": "p3"}]
        items = AccessControlCollector(policies).collect()
        assert len(items) == 3

    def test_empty_policies_produce_no_evidence(self) -> None:
        items = AccessControlCollector([]).collect()
        assert len(items) == 0


class TestTestResultCollector:
    def test_summarizes_pass_count(self) -> None:
        results = [{"name": "t1", "passed": True}, {"name": "t2", "passed": False}]
        items = TestResultCollector(results).collect()
        assert "1/2" in items[0].description


# ---------------------------------------------------------------------------
# Package and assessment
# ---------------------------------------------------------------------------

class TestCompliancePackage:
    def test_collect_all_returns_count(self, package: CompliancePackage) -> None:
        package.register_collector(EncryptionCheckCollector({"encryption_at_rest": True}))
        count = package.collect_all()
        assert count == 1
        assert package.evidence_count == 1

    def test_control_with_multiple_evidence_is_satisfied(self, package: CompliancePackage) -> None:
        package.register_collector(EncryptionCheckCollector({"encryption_at_rest": True}))
        package.register_collector(AccessControlCollector([{"name": "p1"}]))
        package.collect_all()
        assessments = package.assess_controls()
        cc61 = next(a for a in assessments if a.control.control_id == "CC6.1")
        assert cc61.status == ControlStatus.SATISFIED

    def test_unassessed_control_detected(self, package: CompliancePackage) -> None:
        package.collect_all()  # No collectors registered
        assessments = package.assess_controls()
        assert all(a.status == ControlStatus.NOT_ASSESSED for a in assessments)

    def test_report_structure(self, package: CompliancePackage) -> None:
        package.register_collector(EncryptionCheckCollector({"encryption_at_rest": True}))
        package.collect_all()
        report = package.generate_report()
        assert report["framework"] == "SOC2-test"
        assert "total_controls" in report
        assert "status_summary" in report
        assert len(report["controls"]) == 3


class TestDemoPackage:
    def test_demo_runs_without_error(self) -> None:
        pkg = build_demo_package()
        pkg.collect_all()
        report = pkg.generate_report()
        assert report["total_evidence"] > 0
        assert report["total_controls"] == 5
