"""Compliance Evidence Builder — Collect and package compliance evidence from system checks.

Architecture: Uses the Observer pattern where compliance checks publish evidence
items to a central collector. Each check is an independent EvidenceCollector that
produces typed Evidence artifacts. A CompliancePackage aggregates evidence,
computes coverage against a control framework, and generates an audit-ready report.

Design rationale: Compliance audits (SOC2, ISO 27001, PCI-DSS) require demonstrable
proof that controls are active. By automating evidence collection into a structured
package, teams can produce audit artifacts on demand instead of scrambling before
an audit. The observer model lets new checks be added without modifying the core.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Protocol


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

class ControlStatus(Enum):
    SATISFIED = auto()
    PARTIAL = auto()
    NOT_MET = auto()
    NOT_ASSESSED = auto()


class EvidenceType(Enum):
    CONFIGURATION = "configuration"
    LOG_SAMPLE = "log_sample"
    POLICY_DOC = "policy_document"
    TEST_RESULT = "test_result"
    SCREENSHOT = "screenshot"


# WHY tuple for control_ids instead of list? -- One evidence artifact can
# satisfy multiple compliance controls (e.g. encryption config satisfies
# both "data at rest" and "data in transit" controls). Using a tuple (not list)
# keeps Evidence immutable (frozen=True) — critical because evidence must
# not change after collection for audit integrity.
@dataclass(frozen=True)
class Evidence:
    """A single piece of compliance evidence."""
    evidence_id: str
    evidence_type: EvidenceType
    control_ids: tuple[str, ...]
    description: str
    content: str
    collected_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def content_hash(self) -> str:
        return hashlib.sha256(self.content.encode()).hexdigest()[:16]


@dataclass(frozen=True)
class ControlDefinition:
    """A compliance control from a framework (e.g., SOC2 CC6.1)."""
    control_id: str
    framework: str
    title: str
    description: str


@dataclass
class ControlAssessment:
    """Assessment of a single control based on collected evidence."""
    control: ControlDefinition
    status: ControlStatus
    evidence_ids: list[str] = field(default_factory=list)
    notes: str = ""


# ---------------------------------------------------------------------------
# Observer pattern — evidence collectors publish to a package
# ---------------------------------------------------------------------------

class EvidenceCollector(Protocol):
    """Observer interface: each collector gathers evidence for specific controls."""
    def collector_name(self) -> str: ...
    def collect(self) -> list[Evidence]: ...


class EncryptionCheckCollector:
    """Checks that encryption-at-rest is configured."""

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config

    def collector_name(self) -> str:
        return "encryption-check"

    def collect(self) -> list[Evidence]:
        encrypted = self._config.get("encryption_at_rest", False)
        content = json.dumps({"encryption_at_rest": encrypted, "algorithm": self._config.get("algorithm", "none")})
        return [Evidence(
            evidence_id="EV-ENC-001",
            evidence_type=EvidenceType.CONFIGURATION,
            control_ids=("CC6.1", "CC6.7"),
            description="Encryption at rest configuration status",
            content=content,
        )]


class AccessControlCollector:
    """Checks that access control policies exist."""

    def __init__(self, policies: list[dict[str, Any]]) -> None:
        self._policies = policies

    def collector_name(self) -> str:
        return "access-control"

    def collect(self) -> list[Evidence]:
        evidence: list[Evidence] = []
        for i, policy in enumerate(self._policies):
            evidence.append(Evidence(
                evidence_id=f"EV-ACL-{i+1:03d}",
                evidence_type=EvidenceType.POLICY_DOC,
                control_ids=("CC6.1", "CC6.3"),
                description=f"Access control policy: {policy.get('name', 'unnamed')}",
                content=json.dumps(policy),
            ))
        return evidence


class TestResultCollector:
    """Packages test execution results as compliance evidence."""

    def __init__(self, test_results: list[dict[str, Any]]) -> None:
        self._results = test_results

    def collector_name(self) -> str:
        return "test-results"

    def collect(self) -> list[Evidence]:
        passed = sum(1 for t in self._results if t.get("passed"))
        total = len(self._results)
        return [Evidence(
            evidence_id="EV-TEST-001",
            evidence_type=EvidenceType.TEST_RESULT,
            control_ids=("CC7.1", "CC7.2"),
            description=f"Automated test results: {passed}/{total} passed",
            content=json.dumps({"total": total, "passed": passed, "results": self._results}),
        )]


# ---------------------------------------------------------------------------
# Compliance package — aggregates evidence and assesses controls
# ---------------------------------------------------------------------------

class CompliancePackage:
    """Aggregates evidence from multiple collectors and assesses control coverage."""

    def __init__(self, framework_name: str, controls: list[ControlDefinition]) -> None:
        self.framework_name = framework_name
        self._controls = {c.control_id: c for c in controls}
        self._evidence: list[Evidence] = []
        self._collectors: list[EvidenceCollector] = []

    def register_collector(self, collector: EvidenceCollector) -> None:
        self._collectors.append(collector)

    def collect_all(self) -> int:
        """Run all registered collectors and gather evidence. Returns count."""
        total = 0
        for collector in self._collectors:
            items = collector.collect()
            self._evidence.extend(items)
            total += len(items)
        return total

    @property
    def evidence_count(self) -> int:
        return len(self._evidence)

    @property
    def all_evidence(self) -> list[Evidence]:
        return list(self._evidence)

    def assess_controls(self) -> list[ControlAssessment]:
        """Map evidence to controls and determine coverage status."""
        evidence_map: dict[str, list[str]] = {}
        for ev in self._evidence:
            for cid in ev.control_ids:
                evidence_map.setdefault(cid, []).append(ev.evidence_id)

        assessments: list[ControlAssessment] = []
        for cid, control in self._controls.items():
            ev_ids = evidence_map.get(cid, [])
            if len(ev_ids) >= 2:
                status = ControlStatus.SATISFIED
            elif len(ev_ids) == 1:
                status = ControlStatus.PARTIAL
            else:
                status = ControlStatus.NOT_ASSESSED
            assessments.append(ControlAssessment(control, status, ev_ids))
        return assessments

    def generate_report(self) -> dict[str, Any]:
        """Produce an audit-ready compliance report."""
        assessments = self.assess_controls()
        status_counts = {s.name: 0 for s in ControlStatus}
        for a in assessments:
            status_counts[a.status.name] += 1

        return {
            "framework": self.framework_name,
            "total_controls": len(self._controls),
            "total_evidence": len(self._evidence),
            "status_summary": status_counts,
            "controls": [
                {
                    "control_id": a.control.control_id,
                    "title": a.control.title,
                    "status": a.status.name,
                    "evidence_count": len(a.evidence_ids),
                }
                for a in assessments
            ],
        }


# ---------------------------------------------------------------------------
# Demo: SOC2 mini-framework
# ---------------------------------------------------------------------------

SOC2_CONTROLS = [
    ControlDefinition("CC6.1", "SOC2", "Logical Access", "Restrict logical access to information assets"),
    ControlDefinition("CC6.3", "SOC2", "Role-Based Access", "Manage access based on roles and responsibilities"),
    ControlDefinition("CC6.7", "SOC2", "Data Encryption", "Encrypt data to protect confidentiality"),
    ControlDefinition("CC7.1", "SOC2", "Detection Monitoring", "Detect anomalies and security events"),
    ControlDefinition("CC7.2", "SOC2", "Incident Response", "Respond to identified security incidents"),
]


def build_demo_package() -> CompliancePackage:
    pkg = CompliancePackage("SOC2-mini", SOC2_CONTROLS)
    pkg.register_collector(EncryptionCheckCollector({"encryption_at_rest": True, "algorithm": "AES-256"}))
    pkg.register_collector(AccessControlCollector([
        {"name": "admin-policy", "mfa_required": True},
        {"name": "developer-policy", "mfa_required": False},
    ]))
    pkg.register_collector(TestResultCollector([
        {"name": "auth-test", "passed": True},
        {"name": "encryption-test", "passed": True},
        {"name": "access-test", "passed": False},
    ]))
    return pkg


def main() -> None:
    pkg = build_demo_package()
    collected = pkg.collect_all()
    print(f"Collected {collected} evidence items")

    report = pkg.generate_report()
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
