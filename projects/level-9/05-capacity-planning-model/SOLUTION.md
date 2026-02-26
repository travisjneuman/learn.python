# Solution: Level 9 / Project 05 - Capacity Planning Model

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first -- it guides
> your thinking without giving away the answer.
>
> [Back to project README](./README.md)

---

## Complete solution

```python
"""Capacity Planning Model — model capacity needs based on growth projections."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


# --- Domain types -------------------------------------------------------

class GrowthModel(Enum):
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    STEP = "step"


class ResourceType(Enum):
    COMPUTE = "compute"
    STORAGE = "storage"
    BANDWIDTH = "bandwidth"
    MEMORY = "memory"


# WHY configurable growth models? -- Different resources grow differently.
# Storage tends to grow linearly (constant data ingest rate). User traffic
# grows exponentially during viral growth. Infrastructure scales in steps
# (you add servers in whole units). Using the wrong model leads to either
# premature over-provisioning (wasted cost) or capacity shortfalls (outages).
@dataclass
class ResourceProfile:
    """Current and maximum capacity for a resource."""
    resource_type: ResourceType
    current_usage: float
    max_capacity: float
    unit: str = ""
    growth_model: GrowthModel = GrowthModel.LINEAR
    growth_rate: float = 0.0  # per-month growth (absolute for linear, % for exponential)

    @property
    def utilization_pct(self) -> float:
        if self.max_capacity <= 0:
            return 100.0
        return (self.current_usage / self.max_capacity) * 100

    @property
    def headroom(self) -> float:
        return self.max_capacity - self.current_usage


@dataclass
class CapacityForecast:
    """Projected usage for a resource at a future month."""
    resource_type: ResourceType
    month: int
    projected_usage: float
    max_capacity: float
    utilization_pct: float
    exhaustion_risk: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "resource": self.resource_type.value,
            "month": self.month,
            "projected_usage": round(self.projected_usage, 1),
            "max_capacity": self.max_capacity,
            "utilization_pct": round(self.utilization_pct, 1),
            "exhaustion_risk": self.exhaustion_risk,
        }


@dataclass
class CapacityPlan:
    """Complete capacity plan with forecasts and recommendations."""
    forecasts: list[CapacityForecast] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "forecasts": [f.to_dict() for f in self.forecasts],
            "recommendations": self.recommendations,
            "risk_count": sum(1 for f in self.forecasts if f.exhaustion_risk),
        }


# --- Growth functions (Strategy pattern) --------------------------------

def linear_growth(current: float, rate: float, months: int) -> float:
    """Project usage assuming constant monthly growth."""
    return current + (rate * months)


def exponential_growth(current: float, rate_pct: float, months: int) -> float:
    """Project usage assuming compound monthly growth."""
    return current * ((1 + rate_pct / 100) ** months)


# WHY step growth every 3 months? -- Infrastructure often scales in discrete
# units (you can't add half a server). Step growth models this reality:
# capacity increases happen in batches during planned scaling events,
# not continuously.
def step_growth(current: float, rate: float, months: int) -> float:
    """Project usage with step increases every 3 months."""
    steps = months // 3
    return current + (rate * steps)


GROWTH_FUNCTIONS: dict[GrowthModel, Callable[[float, float, int], float]] = {
    GrowthModel.LINEAR: linear_growth,
    GrowthModel.EXPONENTIAL: exponential_growth,
    GrowthModel.STEP: step_growth,
}


# --- Capacity planner ---------------------------------------------------

class CapacityPlanner:
    """Plans capacity needs by projecting resource growth."""

    def __init__(self, risk_threshold_pct: float = 80.0) -> None:
        self._profiles: list[ResourceProfile] = []
        self._risk_threshold = risk_threshold_pct

    def add_resource(self, profile: ResourceProfile) -> None:
        self._profiles.append(profile)

    def forecast(self, months_ahead: int = 12) -> CapacityPlan:
        """Generate capacity forecasts for all resources."""
        plan = CapacityPlan()

        for profile in self._profiles:
            grow_fn = GROWTH_FUNCTIONS[profile.growth_model]

            for month in range(1, months_ahead + 1):
                projected = grow_fn(profile.current_usage, profile.growth_rate, month)
                util_pct = (projected / profile.max_capacity * 100
                           if profile.max_capacity > 0 else 100.0)
                at_risk = util_pct >= self._risk_threshold

                plan.forecasts.append(CapacityForecast(
                    resource_type=profile.resource_type,
                    month=month,
                    projected_usage=projected,
                    max_capacity=profile.max_capacity,
                    utilization_pct=util_pct,
                    exhaustion_risk=at_risk,
                ))

                # WHY only one recommendation per resource? -- Multiple warnings
                # for the same resource create noise. The first month at risk is
                # the actionable one; subsequent months are redundant.
                if at_risk and not any(
                    r.startswith(f"[{profile.resource_type.value}]")
                    for r in plan.recommendations
                ):
                    plan.recommendations.append(
                        f"[{profile.resource_type.value}] Will reach "
                        f"{util_pct:.0f}% utilization by month {month}. "
                        f"Plan expansion before month {max(1, month - 2)}."
                    )

        return plan

    def months_until_exhaustion(self, profile: ResourceProfile) -> int | None:
        """Calculate months until a resource hits max capacity."""
        grow_fn = GROWTH_FUNCTIONS[profile.growth_model]
        for month in range(1, 120):  # max 10 years
            projected = grow_fn(profile.current_usage, profile.growth_rate, month)
            if projected >= profile.max_capacity:
                return month
        return None

    def what_if(self, profile: ResourceProfile,
                new_capacity: float) -> list[CapacityForecast]:
        """Scenario: what if we increase capacity?"""
        grow_fn = GROWTH_FUNCTIONS[profile.growth_model]
        results: list[CapacityForecast] = []
        for month in range(1, 13):
            projected = grow_fn(profile.current_usage, profile.growth_rate, month)
            util_pct = projected / new_capacity * 100 if new_capacity > 0 else 100.0
            results.append(CapacityForecast(
                resource_type=profile.resource_type,
                month=month,
                projected_usage=projected,
                max_capacity=new_capacity,
                utilization_pct=util_pct,
                exhaustion_risk=util_pct >= self._risk_threshold,
            ))
        return results


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    planner = CapacityPlanner(risk_threshold_pct=80.0)

    planner.add_resource(ResourceProfile(
        ResourceType.COMPUTE, current_usage=60, max_capacity=100,
        unit="vCPUs", growth_model=GrowthModel.LINEAR, growth_rate=3,
    ))
    planner.add_resource(ResourceProfile(
        ResourceType.STORAGE, current_usage=500, max_capacity=1000,
        unit="GB", growth_model=GrowthModel.EXPONENTIAL, growth_rate=5,
    ))
    planner.add_resource(ResourceProfile(
        ResourceType.BANDWIDTH, current_usage=200, max_capacity=500,
        unit="Mbps", growth_model=GrowthModel.STEP, growth_rate=50,
    ))

    plan = planner.forecast(months_ahead=12)
    return plan.to_dict()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capacity planning model")
    parser.add_argument("--months", type=int, default=12)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    print(json.dumps(run_demo(), indent=2))


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Strategy pattern for growth functions | Each resource type grows differently; swapping the function changes the projection without modifying the planner | Giant if/elif chain on growth model -- violates open-closed principle; adding a new model requires modifying the planner |
| 80% default risk threshold | Industry standard: 80% utilization is the point where performance degrades and lead time for expansion matters | 100% threshold -- too late; by the time you hit 100%, users are already affected |
| What-if scenario analysis | Capacity planning is about evaluating options; "what if we double storage?" answers the question CFOs actually ask | Single-plan output only -- forces re-running with different inputs instead of comparing side-by-side |
| `months_until_exhaustion` capped at 120 months | Prevents infinite loops when growth rate is zero or negative; 10 years is a reasonable planning horizon | Unbounded search -- risks infinite loop with zero growth rate |
| One recommendation per resource type | Avoids alert fatigue; the first at-risk month is the actionable signal | One recommendation per month per resource -- creates 12 warnings for the same issue |

## Alternative approaches

### Approach B: Monte Carlo capacity simulation

```python
import random

class MonteCarloCapacityPlanner:
    """Instead of deterministic projections, sample growth rates from
    a distribution to produce confidence intervals."""
    def __init__(self, simulations: int = 1000, seed: int = 42):
        self._runs = simulations
        self._rng = random.Random(seed)

    def forecast(self, profile: ResourceProfile, months: int) -> dict:
        results_by_month: dict[int, list[float]] = {}
        for _ in range(self._runs):
            usage = profile.current_usage
            for m in range(1, months + 1):
                # Sample growth rate with noise
                actual_rate = profile.growth_rate * self._rng.gauss(1.0, 0.2)
                usage += actual_rate
                results_by_month.setdefault(m, []).append(usage)
        return {
            m: {"p50": sorted(v)[len(v)//2], "p90": sorted(v)[int(len(v)*0.9)]}
            for m, v in results_by_month.items()
        }
```

**Trade-off:** Monte Carlo simulation accounts for growth rate uncertainty, producing confidence intervals ("90% chance storage stays under 800GB by month 6") instead of single-point estimates. This is more honest about the future but requires more computation and is harder to explain to non-technical stakeholders. Use deterministic projections for simple planning; Monte Carlo when growth rates are uncertain or stakes are high.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Exponential growth with high rate over long horizon | Projected usage overflows to astronomically large numbers | Cap projections at a reasonable multiple of max_capacity, or limit forecast horizon |
| Zero growth rate with step model | `steps = months // 3` produces steps but `rate * steps` is zero; projection never changes | Detect zero growth rate and return current usage directly |
| Max capacity of zero | `utilization_pct` would divide by zero | Guard with `if max_capacity > 0 else 100.0` to report fully utilized |
