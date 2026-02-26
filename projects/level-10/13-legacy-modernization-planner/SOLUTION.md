# Solution: Level 10 / Project 13 - Legacy Modernization Planner

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
>.

---

## Complete solution

```python
"""Legacy Modernization Planner -- Analyze codebase and generate modernization plans."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


# WHY five distinct strategies? -- Each component's ideal modernization path
# depends on its complexity, coupling, and business value. A high-value
# tightly-coupled system benefits from WRAP (Strangler Fig), while a low-value
# unused system should RETIRE. Encoding strategies as an enum forces explicit
# choice and prevents the common trap of "rewrite everything."
class ModernizationStrategy(Enum):
    REWRITE = auto()
    REFACTOR = auto()
    WRAP = auto()
    REPLACE = auto()
    RETIRE = auto()


class RiskLevel(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


class Phase(Enum):
    ASSESS = auto()
    WRAP = auto()
    MIGRATE = auto()
    VALIDATE = auto()
    DECOMMISSION = auto()


@dataclass
class LegacyComponent:
    name: str
    language: str
    age_years: float
    lines_of_code: int
    dependency_count: int
    test_coverage_pct: float
    monthly_incidents: float
    business_criticality: int  # 1-10 scale
    has_documentation: bool = False

    # WHY validation in __post_init__? -- A criticality of 0 or 99 is
    # meaningless and would corrupt the priority formula. Fail-fast
    # validation catches bad data at construction time rather than
    # producing mysterious scores downstream.
    def __post_init__(self) -> None:
        if not 1 <= self.business_criticality <= 10:
            raise ValueError(f"business_criticality must be 1-10, got {self.business_criticality}")


@dataclass(frozen=True)
class ModernizationScore:
    component_name: str
    urgency: float
    effort: float
    risk: float
    priority: float
    recommended_strategy: ModernizationStrategy


@dataclass
class RoadmapStep:
    phase: Phase
    component: str
    description: str
    estimated_weeks: int
    risk_level: RiskLevel


@dataclass
class ModernizationPlan:
    scores: list[ModernizationScore] = field(default_factory=list)
    roadmap: list[RoadmapStep] = field(default_factory=list)

    @property
    def total_weeks(self) -> int:
        return sum(s.estimated_weeks for s in self.roadmap)

    @property
    def component_count(self) -> int:
        return len(self.scores)

    def summary(self) -> dict[str, Any]:
        return {
            "components_analyzed": self.component_count,
            "total_estimated_weeks": self.total_weeks,
            "roadmap_steps": len(self.roadmap),
            "priorities": [
                {"component": s.component_name, "priority": round(s.priority, 1),
                 "strategy": s.recommended_strategy.name}
                for s in sorted(self.scores, key=lambda x: x.priority, reverse=True)
            ],
        }


# WHY capped sub-scores? -- Each dimension (age, incidents, coverage) is
# capped to prevent a single extreme value from dominating the total.
# An 18-year-old system is urgent, but it should not score infinity.
# Caps normalize the scale so urgency, effort, and risk are comparable.
def compute_urgency(comp: LegacyComponent) -> float:
    age_score = min(comp.age_years * 5, 30)
    incident_score = min(comp.monthly_incidents * 10, 30)
    coverage_penalty = max(0, (50 - comp.test_coverage_pct)) * 0.4
    return age_score + incident_score + coverage_penalty


def compute_effort(comp: LegacyComponent) -> float:
    size_score = min(comp.lines_of_code / 1000, 30)
    dep_score = min(comp.dependency_count * 2, 20)
    # WHY documentation penalty? -- Undocumented systems take longer to
    # modernize because engineers must reverse-engineer behavior first.
    doc_penalty = 0 if comp.has_documentation else 10
    return size_score + dep_score + doc_penalty


def compute_risk(comp: LegacyComponent) -> float:
    criticality_risk = comp.business_criticality * 3
    size_risk = min(comp.lines_of_code / 2000, 15)
    coverage_risk = max(0, (70 - comp.test_coverage_pct)) * 0.3
    return criticality_risk + size_risk + coverage_risk


# WHY threshold-based strategy selection? -- Each strategy has a different
# risk/reward profile. REFACTOR is low-risk but only works for small, simple
# systems. WRAP (Strangler Fig) is the safest path for high-risk systems.
# REWRITE is high-reward but only justified when urgency is high and effort
# is manageable.
def recommend_strategy(urgency: float, effort: float, risk: float) -> ModernizationStrategy:
    if effort < 15 and risk < 20:
        return ModernizationStrategy.REFACTOR
    if risk > 35:
        return ModernizationStrategy.WRAP
    if urgency > 40 and effort < 30:
        return ModernizationStrategy.REWRITE
    if effort > 40:
        return ModernizationStrategy.REPLACE
    return ModernizationStrategy.WRAP


# WHY priority = (urgency * criticality) / effort? -- This formula balances
# "how badly does it need fixing" against "how hard is it to fix." High
# urgency + high business value + low effort = fix first. max(effort, 1)
# prevents division by zero.
def score_component(comp: LegacyComponent) -> ModernizationScore:
    urgency = compute_urgency(comp)
    effort = compute_effort(comp)
    risk = compute_risk(comp)
    strategy = recommend_strategy(urgency, effort, risk)
    priority = (urgency * comp.business_criticality) / max(effort, 1)
    return ModernizationScore(comp.name, urgency, effort, risk, priority, strategy)


# WHY five phases per component? -- The Strangler Fig pattern requires
# ASSESS (understand the legacy), WRAP (create new interface), MIGRATE
# (redirect traffic), VALIDATE (prove correctness), DECOMMISSION (remove
# old code). Skipping any phase introduces risk.
def generate_roadmap(scores: list[ModernizationScore]) -> list[RoadmapStep]:
    sorted_scores = sorted(scores, key=lambda s: s.priority, reverse=True)
    steps: list[RoadmapStep] = []

    for sc in sorted_scores:
        risk_level = RiskLevel.LOW if sc.risk < 20 else (RiskLevel.MEDIUM if sc.risk < 35 else RiskLevel.HIGH)
        weeks_base = max(2, int(sc.effort / 5))

        steps.append(RoadmapStep(Phase.ASSESS, sc.component_name,
                                  f"Assess {sc.component_name} for {sc.recommended_strategy.name}",
                                  1, RiskLevel.LOW))
        steps.append(RoadmapStep(Phase.WRAP, sc.component_name,
                                  f"Create interface wrapper for {sc.component_name}",
                                  weeks_base, risk_level))
        steps.append(RoadmapStep(Phase.MIGRATE, sc.component_name,
                                  f"Migrate traffic to new {sc.component_name}",
                                  weeks_base * 2, risk_level))
        steps.append(RoadmapStep(Phase.VALIDATE, sc.component_name,
                                  f"Validate replacement of {sc.component_name}",
                                  1, RiskLevel.LOW))
        steps.append(RoadmapStep(Phase.DECOMMISSION, sc.component_name,
                                  f"Decommission legacy {sc.component_name}",
                                  1, RiskLevel.LOW))
    return steps


def create_plan(components: list[LegacyComponent]) -> ModernizationPlan:
    scores = [score_component(c) for c in components]
    roadmap = generate_roadmap(scores)
    return ModernizationPlan(scores=scores, roadmap=roadmap)


def main() -> None:
    components = [
        LegacyComponent("billing-monolith", "Java", 12, 80000, 25, 30, 4.0, 9, False),
        LegacyComponent("auth-service", "Python", 5, 5000, 8, 75, 1.0, 8, True),
        LegacyComponent("report-generator", "Perl", 18, 15000, 12, 10, 2.5, 4, False),
        LegacyComponent("notification-service", "Ruby", 7, 3000, 5, 60, 0.5, 5, True),
    ]
    plan = create_plan(components)
    print(json.dumps(plan.summary(), indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Multi-dimensional scoring (urgency, effort, risk) | A single score cannot capture whether a system is urgent-but-easy vs urgent-and-hard; three dimensions enable informed prioritization | Single "tech debt" score -- too coarse to guide strategy selection |
| Strangler Fig five-phase roadmap | Each phase is independently reversible; the system works at every boundary | Big-bang rewrite -- highest risk, often fails because the old system must stay running during development |
| Capped sub-scores (e.g., min(age * 5, 30)) | Prevents a single extreme dimension from dominating the total and distorting priorities | Uncapped scores -- an 18-year-old system would score 90 on age alone, overwhelming all other factors |
| Priority formula: (urgency * criticality) / effort | Balances business impact against implementation cost; high-value easy wins rise to the top | Simple urgency ranking -- ignores effort, so a massive rewrite might rank first despite being impractical |
| Strategy selection via threshold rules | Transparent, auditable decision logic; teams can explain why each strategy was chosen | Machine learning model -- opaque, requires training data, harder to override |

## Alternative approaches

### Approach B: Branch-by-abstraction with feature flags

```python
@dataclass
class AbstractionLayer:
    component: str
    interface_name: str
    legacy_impl: str
    new_impl: str
    flag_name: str    # feature flag controlling traffic split

    def traffic_split(self, pct_new: int) -> dict[str, int]:
        """Gradually shift traffic from legacy to new implementation."""
        return {"legacy": 100 - pct_new, "new": pct_new}
```

**Trade-off:** Branch-by-abstraction uses feature flags to gradually route traffic from legacy to new implementations. This gives finer-grained control than Strangler Fig's all-or-nothing service replacement. However, it requires both implementations to coexist in the same codebase, which increases maintenance burden and cognitive load.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| `business_criticality` set to 0 | `ValueError` from `__post_init__` validation, which is correct behavior | Keep validation; do not allow values outside 1-10 range |
| Component with zero effort (tiny, well-documented) | `max(effort, 1)` prevents division by zero in priority calculation; priority becomes very high, which is correct -- easy wins should rank first | The `max(effort, 1)` guard is sufficient |
| All components have the same priority score | `sorted()` is stable, so they appear in original order; this may not be the best tie-breaking strategy | Add a secondary sort key (e.g., business_criticality descending) for deterministic ordering |
