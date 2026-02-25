"""Platform Cost Estimator — model infrastructure costs from usage patterns.

Design rationale:
    Cloud infrastructure costs can spiral without visibility. This project
    models resource consumption (compute, storage, network, database) and
    projects monthly costs. Supports what-if analysis for capacity changes
    and cost optimization recommendations.

Concepts practised:
    - strategy pattern for pricing models
    - dataclasses with computed properties
    - tiered pricing calculations
    - what-if scenario modeling
    - cost optimization heuristics
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


# --- Domain types -------------------------------------------------------

class ResourceType(Enum):
    COMPUTE = "compute"
    STORAGE = "storage"
    NETWORK = "network"
    DATABASE = "database"


class PricingTier(Enum):
    ON_DEMAND = "on_demand"
    RESERVED = "reserved"
    SPOT = "spot"


@dataclass
class ResourceUsage:
    """Usage metrics for a single resource."""
    name: str
    resource_type: ResourceType
    quantity: float  # Units depend on type (vCPU-hours, GB, GB-transferred, etc.)
    unit: str = ""
    pricing_tier: PricingTier = PricingTier.ON_DEMAND
    tags: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class PricingRule:
    """A pricing rule: unit cost with optional volume tiers."""
    resource_type: ResourceType
    pricing_tier: PricingTier
    base_rate: float  # Cost per unit
    # Volume discount tiers: list of (threshold, rate) pairs
    volume_tiers: tuple[tuple[float, float], ...] = ()

    def calculate(self, quantity: float) -> float:
        """Calculate cost applying volume tiers if present."""
        if not self.volume_tiers:
            return quantity * self.base_rate

        total = 0.0
        remaining = quantity
        prev_threshold = 0.0

        for threshold, rate in sorted(self.volume_tiers):
            tier_quantity = min(remaining, threshold - prev_threshold)
            if tier_quantity <= 0:
                break
            total += tier_quantity * rate
            remaining -= tier_quantity
            prev_threshold = threshold

        # Any remaining quantity at base rate
        if remaining > 0:
            total += remaining * self.base_rate
        return total


@dataclass
class CostLineItem:
    """A single line item in the cost breakdown."""
    resource_name: str
    resource_type: ResourceType
    quantity: float
    unit_cost: float
    total_cost: float
    pricing_tier: PricingTier

    def to_dict(self) -> dict[str, Any]:
        return {
            "resource": self.resource_name,
            "type": self.resource_type.value,
            "quantity": self.quantity,
            "unit_cost": round(self.unit_cost, 4),
            "total_cost": round(self.total_cost, 2),
            "tier": self.pricing_tier.value,
        }


@dataclass
class CostEstimate:
    """Complete cost estimate with breakdown and recommendations."""
    line_items: list[CostLineItem] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)

    @property
    def total_monthly(self) -> float:
        return sum(item.total_cost for item in self.line_items)

    @property
    def by_type(self) -> dict[str, float]:
        totals: dict[str, float] = {}
        for item in self.line_items:
            key = item.resource_type.value
            totals[key] = totals.get(key, 0) + item.total_cost
        return totals

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_monthly": round(self.total_monthly, 2),
            "by_type": {k: round(v, 2) for k, v in self.by_type.items()},
            "line_items": [i.to_dict() for i in self.line_items],
            "recommendations": self.recommendations,
        }


# --- Cost engine --------------------------------------------------------

# Default pricing rules (simplified cloud pricing)
DEFAULT_PRICING: list[PricingRule] = [
    PricingRule(ResourceType.COMPUTE, PricingTier.ON_DEMAND, 0.05),
    PricingRule(ResourceType.COMPUTE, PricingTier.RESERVED, 0.03),
    PricingRule(ResourceType.COMPUTE, PricingTier.SPOT, 0.015),
    PricingRule(
        ResourceType.STORAGE, PricingTier.ON_DEMAND, 0.023,
        volume_tiers=((50, 0.026), (500, 0.023), (5000, 0.021)),
    ),
    PricingRule(ResourceType.NETWORK, PricingTier.ON_DEMAND, 0.09),
    PricingRule(ResourceType.DATABASE, PricingTier.ON_DEMAND, 0.10),
    PricingRule(ResourceType.DATABASE, PricingTier.RESERVED, 0.065),
]


class PlatformCostEstimator:
    """Estimates platform infrastructure costs from resource usage."""

    def __init__(self, pricing_rules: list[PricingRule] | None = None) -> None:
        self._rules: dict[tuple[ResourceType, PricingTier], PricingRule] = {}
        for rule in (pricing_rules or DEFAULT_PRICING):
            self._rules[(rule.resource_type, rule.pricing_tier)] = rule

    def estimate(self, usage: list[ResourceUsage]) -> CostEstimate:
        """Calculate costs for a list of resource usage entries."""
        items: list[CostLineItem] = []
        for resource in usage:
            rule = self._rules.get((resource.resource_type, resource.pricing_tier))
            if not rule:
                # Fall back to on-demand pricing
                rule = self._rules.get((resource.resource_type, PricingTier.ON_DEMAND))
            if not rule:
                continue

            total = rule.calculate(resource.quantity)
            unit_cost = total / resource.quantity if resource.quantity > 0 else 0
            items.append(CostLineItem(
                resource_name=resource.name,
                resource_type=resource.resource_type,
                quantity=resource.quantity,
                unit_cost=unit_cost,
                total_cost=total,
                pricing_tier=resource.pricing_tier,
            ))

        recommendations = self._generate_recommendations(items, usage)
        return CostEstimate(line_items=items, recommendations=recommendations)

    def what_if(
        self, baseline: list[ResourceUsage], modified: list[ResourceUsage],
    ) -> dict[str, Any]:
        """Compare costs between baseline and modified usage."""
        base_est = self.estimate(baseline)
        mod_est = self.estimate(modified)
        diff = mod_est.total_monthly - base_est.total_monthly
        pct = (diff / base_est.total_monthly * 100) if base_est.total_monthly > 0 else 0
        return {
            "baseline_monthly": round(base_est.total_monthly, 2),
            "modified_monthly": round(mod_est.total_monthly, 2),
            "difference": round(diff, 2),
            "change_pct": round(pct, 1),
        }

    def _generate_recommendations(
        self, items: list[CostLineItem], usage: list[ResourceUsage],
    ) -> list[str]:
        """Generate cost optimization recommendations."""
        recs: list[str] = []
        total = sum(i.total_cost for i in items)
        if total == 0:
            return recs

        # Check for on-demand compute that could be reserved
        for resource in usage:
            if (resource.resource_type == ResourceType.COMPUTE
                    and resource.pricing_tier == PricingTier.ON_DEMAND
                    and resource.quantity > 500):
                recs.append(
                    f"Consider reserved instances for '{resource.name}' "
                    f"(currently {resource.quantity} units on-demand)"
                )

        # Check if any single type dominates (> 60% of total)
        for item in items:
            if item.total_cost / total > 0.6:
                recs.append(
                    f"'{item.resource_name}' accounts for "
                    f"{item.total_cost / total * 100:.0f}% of costs — review for optimization"
                )

        # Check for high network costs
        network_cost = sum(i.total_cost for i in items if i.resource_type == ResourceType.NETWORK)
        if network_cost > total * 0.3:
            recs.append("Network costs are high — consider CDN or caching to reduce egress")

        return recs


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    estimator = PlatformCostEstimator()

    usage = [
        ResourceUsage("web-servers", ResourceType.COMPUTE, 720, "vCPU-hours"),
        ResourceUsage("api-servers", ResourceType.COMPUTE, 1440, "vCPU-hours",
                       pricing_tier=PricingTier.RESERVED),
        ResourceUsage("s3-storage", ResourceType.STORAGE, 1000, "GB"),
        ResourceUsage("cdn-egress", ResourceType.NETWORK, 500, "GB"),
        ResourceUsage("rds-primary", ResourceType.DATABASE, 720, "hours",
                       pricing_tier=PricingTier.RESERVED),
    ]

    estimate = estimator.estimate(usage)

    # What-if: move web-servers to reserved
    modified = [
        ResourceUsage("web-servers", ResourceType.COMPUTE, 720, "vCPU-hours",
                       pricing_tier=PricingTier.RESERVED),
        *usage[1:],
    ]
    comparison = estimator.what_if(usage, modified)

    return {"estimate": estimate.to_dict(), "what_if_reserved": comparison}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Platform cost estimator")
    parser.add_argument("--demo", action="store_true", default=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    print(json.dumps(run_demo(), indent=2))


if __name__ == "__main__":
    main()
