"""Legacy Modernization Planner — Analyze codebase and generate modernization plans.

Architecture: Uses a scoring model to evaluate legacy components across multiple
dimensions (age, complexity, dependency count, test coverage, incident rate).
Components are ranked by modernization priority. The planner generates a phased
roadmap using the Strangler Fig pattern — incrementally replacing legacy pieces
rather than doing a risky "big bang" rewrite.

Design rationale: Legacy systems are the backbone of most enterprises. Rewriting
everything at once is risky and expensive. The Strangler Fig pattern wraps legacy
functionality in new interfaces, redirects traffic incrementally, and decommissions
old code only after the replacement is proven — minimizing risk at each step.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

class ModernizationStrategy(Enum):
    REWRITE = auto()       # Full rewrite (highest risk, highest reward)
    REFACTOR = auto()      # Incremental improvement in place
    WRAP = auto()          # Strangler fig — wrap with new interface
    REPLACE = auto()       # Replace with off-the-shelf solution
    RETIRE = auto()        # Decommission entirely


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
    """Description of a legacy system component."""
    name: str
    language: str
    age_years: float
    lines_of_code: int
    dependency_count: int
    test_coverage_pct: float
    monthly_incidents: float
    business_criticality: int  # 1-10 scale
    has_documentation: bool = False

    def __post_init__(self) -> None:
        if not 1 <= self.business_criticality <= 10:
            raise ValueError(f"business_criticality must be 1-10, got {self.business_criticality}")


@dataclass(frozen=True)
class ModernizationScore:
    """Computed priority score for modernizing a component."""
    component_name: str
    urgency: float        # How urgently it needs modernization
    effort: float         # Estimated effort (higher = more work)
    risk: float           # Risk of modernization failure
    priority: float       # Combined score (urgency * business_criticality / effort)
    recommended_strategy: ModernizationStrategy


@dataclass
class RoadmapStep:
    """A single step in the modernization roadmap."""
    phase: Phase
    component: str
    description: str
    estimated_weeks: int
    risk_level: RiskLevel


@dataclass
class ModernizationPlan:
    """Complete modernization roadmap."""
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


# ---------------------------------------------------------------------------
# Scoring engine
# ---------------------------------------------------------------------------

def compute_urgency(comp: LegacyComponent) -> float:
    """Higher score = needs modernization more urgently."""
    age_score = min(comp.age_years * 5, 30)
    incident_score = min(comp.monthly_incidents * 10, 30)
    coverage_penalty = max(0, (50 - comp.test_coverage_pct)) * 0.4
    return age_score + incident_score + coverage_penalty


def compute_effort(comp: LegacyComponent) -> float:
    """Higher score = more effort to modernize."""
    size_score = min(comp.lines_of_code / 1000, 30)
    dep_score = min(comp.dependency_count * 2, 20)
    doc_penalty = 0 if comp.has_documentation else 10
    return size_score + dep_score + doc_penalty


def compute_risk(comp: LegacyComponent) -> float:
    """Higher score = riskier to modernize."""
    criticality_risk = comp.business_criticality * 3
    size_risk = min(comp.lines_of_code / 2000, 15)
    coverage_risk = max(0, (70 - comp.test_coverage_pct)) * 0.3
    return criticality_risk + size_risk + coverage_risk


def recommend_strategy(urgency: float, effort: float, risk: float) -> ModernizationStrategy:
    """Select modernization strategy based on scores."""
    if effort < 15 and risk < 20:
        return ModernizationStrategy.REFACTOR
    if risk > 35:
        return ModernizationStrategy.WRAP
    if urgency > 40 and effort < 30:
        return ModernizationStrategy.REWRITE
    if effort > 40:
        return ModernizationStrategy.REPLACE
    return ModernizationStrategy.WRAP


def score_component(comp: LegacyComponent) -> ModernizationScore:
    """Compute full modernization score for a component."""
    urgency = compute_urgency(comp)
    effort = compute_effort(comp)
    risk = compute_risk(comp)
    strategy = recommend_strategy(urgency, effort, risk)
    priority = (urgency * comp.business_criticality) / max(effort, 1)
    return ModernizationScore(comp.name, urgency, effort, risk, priority, strategy)


# ---------------------------------------------------------------------------
# Roadmap generator
# ---------------------------------------------------------------------------

def generate_roadmap(scores: list[ModernizationScore]) -> list[RoadmapStep]:
    """Generate a phased roadmap from scored components."""
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


# ---------------------------------------------------------------------------
# Planner (high-level API)
# ---------------------------------------------------------------------------

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
