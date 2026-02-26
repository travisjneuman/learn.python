"""High-Risk Change Gate — Approval gates for high-risk changes with risk scoring.

Architecture: Uses a scoring pipeline where each RiskFactor contributes a weighted
score. A ChangeRequest is evaluated against all registered factors, producing an
aggregate risk level. The gate then applies approval rules: low-risk changes auto-
approve, medium-risk require one reviewer, high-risk require multiple reviewers
and a cooldown window.

Design rationale: Production incidents often stem from changes that were deployed
without proportionate review. By quantifying risk and enforcing gates, teams
shift from "all changes treated equally" to "review effort scales with blast radius."
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Protocol


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

class RiskLevel(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

    # WHY quantify risk as a numeric score? -- "This change is risky" is
    # subjective. A weighted score (0-100) from measurable factors (blast
    # radius, service tier, time of day, change frequency) produces repeatable
    # decisions. The thresholds (25/50/75) map scores to human-readable levels
    # that determine which approval gates apply.
    @classmethod
    def from_score(cls, score: float) -> RiskLevel:
        if score < 25:
            return cls.LOW
        if score < 50:
            return cls.MEDIUM
        if score < 75:
            return cls.HIGH
        return cls.CRITICAL


class GateDecision(Enum):
    APPROVED = "approved"
    NEEDS_REVIEW = "needs_review"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class ChangeRequest:
    """Immutable description of a proposed change."""
    change_id: str
    title: str
    author: str
    affected_services: list[str] = field(default_factory=list)
    changes_schema: bool = False
    changes_auth: bool = False
    lines_changed: int = 0
    is_rollback: bool = False
    deploy_window: str = "business_hours"


@dataclass
class RiskAssessment:
    """Result of evaluating a single risk factor."""
    factor_name: str
    score: float
    max_score: float
    reason: str


@dataclass
class GateResult:
    """Final decision from the change gate."""
    change_id: str
    total_score: float
    risk_level: RiskLevel
    decision: GateDecision
    assessments: list[RiskAssessment] = field(default_factory=list)
    required_approvers: int = 0
    cooldown_hours: int = 0

    def summary(self) -> dict[str, Any]:
        return {
            "change_id": self.change_id,
            "total_score": round(self.total_score, 1),
            "risk_level": self.risk_level.name,
            "decision": self.decision.value,
            "required_approvers": self.required_approvers,
            "cooldown_hours": self.cooldown_hours,
            "factors": [
                {"name": a.factor_name, "score": round(a.score, 1), "reason": a.reason}
                for a in self.assessments
            ],
        }


# ---------------------------------------------------------------------------
# Risk factors (Strategy pattern)
# ---------------------------------------------------------------------------

class RiskFactor(Protocol):
    """Strategy interface for computing a risk score contribution."""
    def name(self) -> str: ...
    def assess(self, change: ChangeRequest) -> RiskAssessment: ...


class BlastRadiusFactor:
    """Scores based on number of affected services."""
    def name(self) -> str:
        return "blast_radius"

    def assess(self, change: ChangeRequest) -> RiskAssessment:
        count = len(change.affected_services)
        score = min(count * 10.0, 30.0)
        return RiskAssessment(self.name(), score, 30.0, f"{count} service(s) affected")


class SchemaChangeFactor:
    """High score if the change modifies database schema."""
    def name(self) -> str:
        return "schema_change"

    def assess(self, change: ChangeRequest) -> RiskAssessment:
        score = 25.0 if change.changes_schema else 0.0
        reason = "Schema migration included" if change.changes_schema else "No schema changes"
        return RiskAssessment(self.name(), score, 25.0, reason)


class AuthChangeFactor:
    """Elevated score for authentication/authorization changes."""
    def name(self) -> str:
        return "auth_change"

    def assess(self, change: ChangeRequest) -> RiskAssessment:
        score = 20.0 if change.changes_auth else 0.0
        reason = "Auth system modified" if change.changes_auth else "No auth changes"
        return RiskAssessment(self.name(), score, 20.0, reason)


class ChangeSizeFactor:
    """Larger diffs carry more risk of hidden issues."""
    def name(self) -> str:
        return "change_size"

    def assess(self, change: ChangeRequest) -> RiskAssessment:
        if change.lines_changed < 50:
            return RiskAssessment(self.name(), 5.0, 20.0, "Small change")
        if change.lines_changed < 200:
            return RiskAssessment(self.name(), 10.0, 20.0, "Medium change")
        if change.lines_changed < 500:
            return RiskAssessment(self.name(), 15.0, 20.0, "Large change")
        return RiskAssessment(self.name(), 20.0, 20.0, "Very large change")


class DeployWindowFactor:
    """Off-peak deployments are lower risk due to reduced traffic."""
    def name(self) -> str:
        return "deploy_window"

    def assess(self, change: ChangeRequest) -> RiskAssessment:
        scores = {"off_peak": 0.0, "weekend": 2.0, "business_hours": 10.0}
        score = scores.get(change.deploy_window, 10.0)
        return RiskAssessment(self.name(), score, 10.0, f"Deploy during {change.deploy_window}")


class RollbackFactor:
    """Rollbacks reduce risk — they undo a known-bad state."""
    def name(self) -> str:
        return "rollback"

    def assess(self, change: ChangeRequest) -> RiskAssessment:
        score = -15.0 if change.is_rollback else 0.0
        reason = "Rollback reduces risk" if change.is_rollback else "Not a rollback"
        return RiskAssessment(self.name(), score, 0.0, reason)


# ---------------------------------------------------------------------------
# Change gate engine
# ---------------------------------------------------------------------------

class ChangeGate:
    """Evaluates change requests and produces gate decisions."""

    def __init__(self) -> None:
        self._factors: list[RiskFactor] = []

    def register_factor(self, factor: RiskFactor) -> None:
        self._factors.append(factor)

    @property
    def factor_count(self) -> int:
        return len(self._factors)

    def evaluate(self, change: ChangeRequest) -> GateResult:
        assessments: list[RiskAssessment] = []
        total_score = 0.0
        for factor in self._factors:
            assessment = factor.assess(change)
            assessments.append(assessment)
            total_score += assessment.score

        total_score = max(0.0, total_score)
        risk_level = RiskLevel.from_score(total_score)
        decision, approvers, cooldown = self._apply_policy(risk_level)

        return GateResult(
            change_id=change.change_id,
            total_score=total_score,
            risk_level=risk_level,
            decision=decision,
            assessments=assessments,
            required_approvers=approvers,
            cooldown_hours=cooldown,
        )

    @staticmethod
    def _apply_policy(risk: RiskLevel) -> tuple[GateDecision, int, int]:
        if risk == RiskLevel.LOW:
            return GateDecision.APPROVED, 0, 0
        if risk == RiskLevel.MEDIUM:
            return GateDecision.NEEDS_REVIEW, 1, 0
        if risk == RiskLevel.HIGH:
            return GateDecision.NEEDS_REVIEW, 2, 4
        return GateDecision.BLOCKED, 3, 24


def build_default_gate() -> ChangeGate:
    gate = ChangeGate()
    gate.register_factor(BlastRadiusFactor())
    gate.register_factor(SchemaChangeFactor())
    gate.register_factor(AuthChangeFactor())
    gate.register_factor(ChangeSizeFactor())
    gate.register_factor(DeployWindowFactor())
    gate.register_factor(RollbackFactor())
    return gate


def main() -> None:
    gate = build_default_gate()
    changes = [
        ChangeRequest("CHG-001", "Fix typo in docs", "alice", ["docs-site"], lines_changed=5),
        ChangeRequest("CHG-002", "Add user roles", "bob", ["auth-svc", "api-gw"],
                       changes_auth=True, lines_changed=350),
        ChangeRequest("CHG-003", "Migrate billing schema", "carol",
                       ["billing", "payment", "reporting"],
                       changes_schema=True, lines_changed=200),
    ]
    for change in changes:
        result = gate.evaluate(change)
        print(json.dumps(result.summary(), indent=2))
        print()


if __name__ == "__main__":
    main()
