# Solution: Level 10 / Project 05 - Compliance Evidence Builder

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
> [Walkthrough](./WALKTHROUGH.md) for guided hints.

---

## Complete solution

```python
"""Compliance Evidence Builder -- Collect and package compliance evidence from system checks."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Protocol


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


# WHY tuple for control_ids? -- One evidence item can satisfy multiple controls
# (e.g., encryption config covers both "data at rest" and "data in transit").
# A tuple keeps Evidence immutable (frozen=True) since lists are mutable and
# would break the frozen contract. Immutability is essential for audit integrity.
@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    evidence_type: EvidenceType
    control_ids: tuple[str, ...]
    description: str
    content: str
    collected_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    # WHY content_hash? -- Auditors need proof that evidence was not tampered
    # with since collection. The SHA-256 hash serves as a fingerprint.
    @property
    def content_hash(self) -> str:
        return hashlib.sha256(self.content.encode()).hexdigest()[:16]


@dataclass(frozen=True)
class ControlDefinition:
    control_id: str
    framework: str
    title: str
    description: str


@dataclass
class ControlAssessment:
    control: ControlDefinition
    status: ControlStatus
    evidence_ids: list[str] = field(default_factory=list)
    notes: str = ""


# WHY Protocol? -- Each collector is independent (Observer pattern). New checks
# can be added without modifying the CompliancePackage.
class EvidenceCollector(Protocol):
    def collector_name(self) -> str: ...
    def collect(self) -> list[Evidence]: ...


class EncryptionCheckCollector:
    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config

    def collector_name(self) -> str:
        return "encryption-check"

    def collect(self) -> list[Evidence]:
        encrypted = self._config.get("encryption_at_rest", False)
        content = json.dumps({"encryption_at_rest": encrypted,
                               "algorithm": self._config.get("algorithm", "none")})
        return [Evidence("EV-ENC-001", EvidenceType.CONFIGURATION,
                         ("CC6.1", "CC6.7"),
                         "Encryption at rest configuration status", content)]


class AccessControlCollector:
    def __init__(self, policies: list[dict[str, Any]]) -> None:
        self._policies = policies

    def collector_name(self) -> str:
        return "access-control"

    def collect(self) -> list[Evidence]:
        return [
            Evidence(f"EV-ACL-{i+1:03d}", EvidenceType.POLICY_DOC,
                     ("CC6.1", "CC6.3"),
                     f"Access control policy: {p.get('name', 'unnamed')}",
                     json.dumps(p))
            for i, p in enumerate(self._policies)
        ]


class TestResultCollector:
    def __init__(self, test_results: list[dict[str, Any]]) -> None:
        self._results = test_results

    def collector_name(self) -> str:
        return "test-results"

    def collect(self) -> list[Evidence]:
        passed = sum(1 for t in self._results if t.get("passed"))
        total = len(self._results)
        return [Evidence("EV-TEST-001", EvidenceType.TEST_RESULT,
                         ("CC7.1", "CC7.2"),
                         f"Automated test results: {passed}/{total} passed",
                         json.dumps({"total": total, "passed": passed, "results": self._results}))]


class CompliancePackage:
    def __init__(self, framework_name: str, controls: list[ControlDefinition]) -> None:
        self.framework_name = framework_name
        self._controls = {c.control_id: c for c in controls}
        self._evidence: list[Evidence] = []
        self._collectors: list[EvidenceCollector] = []

    def register_collector(self, collector: EvidenceCollector) -> None:
        self._collectors.append(collector)

    def collect_all(self) -> int:
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

    # WHY 2+ evidence = SATISFIED, 1 = PARTIAL? -- Compliance frameworks require
    # corroborating evidence. A single piece only partially satisfies a control.
    # Two or more independent pieces provide the confidence auditors need.
    def assess_controls(self) -> list[ControlAssessment]:
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
                {"control_id": a.control.control_id, "title": a.control.title,
                 "status": a.status.name, "evidence_count": len(a.evidence_ids)}
                for a in assessments
            ],
        }


SOC2_CONTROLS = [
    ControlDefinition("CC6.1", "SOC2", "Logical Access", "Restrict logical access"),
    ControlDefinition("CC6.3", "SOC2", "Role-Based Access", "Manage access based on roles"),
    ControlDefinition("CC6.7", "SOC2", "Data Encryption", "Encrypt data for confidentiality"),
    ControlDefinition("CC7.1", "SOC2", "Detection Monitoring", "Detect security events"),
    ControlDefinition("CC7.2", "SOC2", "Incident Response", "Respond to incidents"),
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
    print(json.dumps(pkg.generate_report(), indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Observer pattern for evidence collectors | Each collector is independent; new checks added without modifying the core | Single monolithic collection function -- hard to extend and test |
| Content hashing with SHA-256 | Tamper-evidence for audit trails; content change invalidates the hash | No integrity verification -- auditors must trust evidence blindly |
| Tuple for control_ids (not list) | Keeps Evidence frozen-compatible; required for immutability | List with defensive copy -- adds overhead and still allows accidental mutation |
| 2+ evidence threshold for SATISFIED | Mirrors real audit requirements for corroborating evidence | Any evidence = satisfied -- insufficient for serious compliance frameworks |

## Alternative approaches

### Approach B: Evidence graph with dependency tracking

```python
@dataclass
class EvidenceGraph:
    _links: dict[str, set[str]] = field(default_factory=dict)

    def link(self, ev_a: str, ev_b: str) -> None:
        self._links.setdefault(ev_a, set()).add(ev_b)
        self._links.setdefault(ev_b, set()).add(ev_a)

    def corroboration_score(self, evidence_id: str) -> int:
        return len(self._links.get(evidence_id, set()))
```

**Trade-off:** An evidence graph captures relationships between items (e.g., "the encryption test corroborates the encryption config"). This produces richer audit narratives but adds complexity. The flat list approach is simpler and sufficient for most frameworks.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Calling `collect_all()` twice | Evidence list doubles because items are appended each time | Make `collect_all` idempotent by clearing `_evidence` first, or track collected state |
| Collector returns evidence for non-existent control ID | Evidence is collected but does not affect any assessment | Validate control_ids against registered controls during collection |
| Empty content string | `content_hash` produces a valid hash of the empty string, which looks like real evidence | Add validation that content is non-empty at Evidence construction time |
