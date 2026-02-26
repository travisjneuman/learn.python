# Solution: Level 10 / Project 07 - High Risk Change Gate

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
> [Walkthrough](./WALKTHROUGH.md) for guided hints.

---

## Complete solution

```python
"""High-Risk Change Gate -- Approval gates for production changes with risk scoring."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Protocol


class RiskLevel(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

    # WHY numeric thresholds (25/50/75)? -- Subjective labels like "risky" are
    # inconsistent across teams. A numeric score from measurable factors produces
    # repeatable decisions. The thresholds map scores to human-readable levels
    # that determine which approval gates apply.
    @classmethod
    def from_score(cls, score: float) -> RiskLevel:
        if score < 25: return cls.LOW
        if score < 50: return cls.MEDIUM
        if score < 75: return cls.HIGH
        return cls.CRITICAL


class GateDecision(Enum):
    APPROVED = "approved"
    NEEDS_REVIEW = "needs_review"
    BLOCKED = "blocked"


# WHY frozen=True? -- A ChangeRequest is a snapshot of a proposed change.
# If it could be mutated during evaluation, the risk score might not match
# the actual change, creating a security hole.
@dataclass(frozen=True)
class ChangeRequest:
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
    factor_name: str
    score: float
    max_score: float
    reason: str


@dataclass
class GateResult:
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
            "factors": [{"name": a.factor_name, "score": round(a.score, 1),
                         "reason": a.reason} for a in self.assessments],
        }


# WHY Protocol for RiskFactor? -- Each factor (blast radius, schema changes,
# auth changes, size, timing) has unique scoring logic. The Protocol lets
# teams add custom factors without modifying the gate.
class RiskFactor(Protocol):
    def name(self) -> str: ...
    def assess(self, change: ChangeRequest) -> RiskAssessment: ...


class BlastRadiusFactor:
    def name(self) -> str: return "blast_radius"
    # WHY cap at 30? -- Prevents blast radius from dominating the total score.
    # Even a change touching 100 services should not auto-block without other factors.
    def assess(self, change: ChangeRequest) -> RiskAssessment:
        count = len(change.affected_services)
        score = min(count * 10.0, 30.0)
        return RiskAssessment(self.name(), score, 30.0, f"{count} service(s) affected")


class SchemaChangeFactor:
    def name(self) -> str: return "schema_change"
    def assess(self, change: ChangeRequest) -> RiskAssessment:
        score = 25.0 if change.changes_schema else 0.0
        return RiskAssessment(self.name(), score, 25.0,
                              "Schema migration included" if change.changes_schema else "No schema changes")


class AuthChangeFactor:
    def name(self) -> str: return "auth_change"
    def assess(self, change: ChangeRequest) -> RiskAssessment:
        score = 20.0 if change.changes_auth else 0.0
        return RiskAssessment(self.name(), score, 20.0,
                              "Auth system modified" if change.changes_auth else "No auth changes")


class ChangeSizeFactor:
    def name(self) -> str: return "change_size"
    def assess(self, change: ChangeRequest) -> RiskAssessment:
        if change.lines_changed < 50: return RiskAssessment(self.name(), 5.0, 20.0, "Small change")
        if change.lines_changed < 200: return RiskAssessment(self.name(), 10.0, 20.0, "Medium change")
        if change.lines_changed < 500: return RiskAssessment(self.name(), 15.0, 20.0, "Large change")
        return RiskAssessment(self.name(), 20.0, 20.0, "Very large change")


class DeployWindowFactor:
    def name(self) -> str: return "deploy_window"
    def assess(self, change: ChangeRequest) -> RiskAssessment:
        scores = {"off_peak": 0.0, "weekend": 2.0, "business_hours": 10.0}
        score = scores.get(change.deploy_window, 10.0)
        return RiskAssessment(self.name(), score, 10.0, f"Deploy during {change.deploy_window}")


class RollbackFactor:
    def name(self) -> str: return "rollback"
    # WHY negative score? -- Rollbacks reduce risk because they undo a known-bad
    # state. The negative score offsets other factors. max(0, total) in the gate
    # prevents the total from going below zero.
    def assess(self, change: ChangeRequest) -> RiskAssessment:
        score = -15.0 if change.is_rollback else 0.0
        return RiskAssessment(self.name(), score, 0.0,
                              "Rollback reduces risk" if change.is_rollback else "Not a rollback")


class ChangeGate:
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
        # WHY floor at 0? -- Negative total scores from rollback offsets should
        # not produce "negative risk." Risk is always non-negative.
        total_score = max(0.0, total_score)
        risk_level = RiskLevel.from_score(total_score)
        decision, approvers, cooldown = self._apply_policy(risk_level)
        return GateResult(change.change_id, total_score, risk_level, decision,
                          assessments, approvers, cooldown)

    # WHY escalating gates? -- Review effort should scale with blast radius.
    # A typo fix auto-approves. A schema migration to three services needs
    # 2 reviewers and a 4-hour cooldown before deploy.
    @staticmethod
    def _apply_policy(risk: RiskLevel) -> tuple[GateDecision, int, int]:
        if risk == RiskLevel.LOW: return GateDecision.APPROVED, 0, 0
        if risk == RiskLevel.MEDIUM: return GateDecision.NEEDS_REVIEW, 1, 0
        if risk == RiskLevel.HIGH: return GateDecision.NEEDS_REVIEW, 2, 4
        return GateDecision.BLOCKED, 3, 24


def build_default_gate() -> ChangeGate:
    gate = ChangeGate()
    for f in [BlastRadiusFactor(), SchemaChangeFactor(), AuthChangeFactor(),
              ChangeSizeFactor(), DeployWindowFactor(), RollbackFactor()]:
        gate.register_factor(f)
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Weighted scoring pipeline with pluggable factors | Produces repeatable, explainable risk decisions from measurable inputs | Manual risk labels -- subjective and inconsistent across teams |
| Negative score for RollbackFactor | Rollbacks reduce risk, so they should offset other factors | Separate "risk reducer" mechanism -- adds complexity without benefit |
| Escalating approval gates (0/1/2/3 reviewers) | Review effort scales with blast radius rather than treating all changes equally | Binary approve/reject -- too rigid for real-world deployment workflows |
| Frozen ChangeRequest | Prevents mutation during evaluation, ensuring the scored change matches the deployed change | Mutable with defensive copies -- more error-prone |
| Score floor at zero | Risk is never negative; prevents confusing results from multiple rollback offsets | Allow negative scores -- creates meaningless "negative risk" values |

## Alternative approaches

### Approach B: Machine-learning-based risk prediction

```python
# Instead of hand-crafted factors, train a model on historical change data:
# features = [service_count, lines_changed, schema_flag, auth_flag, ...]
# label = 1 if change caused an incident, 0 otherwise
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()
model.fit(historical_features, historical_labels)
risk_probability = model.predict_proba(new_change_features)[0][1]
```

**Trade-off:** ML-based scoring adapts to your organization's specific risk patterns and can discover non-obvious correlations. However, it requires historical incident data, is harder to explain to stakeholders, and can produce surprising decisions. Hand-crafted factors are more transparent and auditable.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| No factors registered, then evaluate called | Total score is 0, everything auto-approves regardless of risk | Require at least one factor before `evaluate` can be called |
| Rollback flag on a clearly risky change | Rollback offset can reduce a CRITICAL change to HIGH or even MEDIUM | Add a minimum score floor per factor so rollback alone cannot overcome critical risk signals |
| Unknown deploy_window string | Falls through to default 10.0 score (business_hours equivalent) | Validate deploy_window against known values at ChangeRequest construction time |
