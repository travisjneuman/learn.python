"""Capacity Planning Model — model capacity needs based on growth projections.

Design rationale:
    Capacity planning prevents outages by projecting resource needs before
    demand exceeds supply. This project models compute, storage, and
    bandwidth growth using configurable curves and generates capacity
    forecasts with headroom recommendations.

Concepts practised:
    - growth modeling (linear, exponential, step-function)
    - strategy pattern for growth curve selection
    - dataclasses for resource profiles and forecasts
    - threshold-based alerts for capacity risks
    - what-if scenario analysis
"""

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
