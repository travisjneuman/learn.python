# Solution: Level 9 / Project 13 - Platform Cost Estimator

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first -- it guides
> your thinking without giving away the answer.
>
> [Back to project README](./README.md)

---

## Complete solution

```python
"""Platform Cost Estimator — model infrastructure costs from usage patterns."""

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


# WHY model pricing tiers? -- The same cloud resource costs dramatically
# different amounts based on commitment: on-demand (full price, no commitment),
# reserved (30-70% discount, 1-3 year commitment), and spot (60-90% discount,
# can be interrupted). Cost optimization means choosing the right tier for
# each workload's reliability requirements.
class PricingTier(Enum):
    ON_DEMAND = "on_demand"
    RESERVED = "reserved"
    SPOT = "spot"


@dataclass
class ResourceUsage:
    """Usage metrics for a single resource."""
    name: str
    resource_type: ResourceType
    quantity: float
    unit: str = ""
    pricing_tier: PricingTier = PricingTier.ON_DEMAND
    tags: dict[str, str] = field(default_factory=dict)


# WHY frozen PricingRule? -- Pricing rules are reference data that should
# not be mutated during cost calculation. Freezing them prevents accidental
# side effects when multiple resources share the same pricing rule.
@dataclass(frozen=True)
class PricingRule:
    """A pricing rule: unit cost with optional volume tiers."""
    resource_type: ResourceType
    pricing_tier: PricingTier
    base_rate: float
    volume_tiers: tuple[tuple[float, float], ...] = ()

    # WHY tiered pricing? -- Cloud providers charge less per unit at higher
    # volumes. S3 charges $0.026/GB for the first 50TB, $0.023 for the next
    # 450TB, and $0.021 above 500TB. Implementing this correctly can save
    # thousands on cost estimates.
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

        for resource in usage:
            if (resource.resource_type == ResourceType.COMPUTE
                    and resource.pricing_tier == PricingTier.ON_DEMAND
                    and resource.quantity > 500):
                recs.append(
                    f"Consider reserved instances for '{resource.name}' "
                    f"(currently {resource.quantity} units on-demand)"
                )

        for item in items:
            if item.total_cost / total > 0.6:
                recs.append(
                    f"'{item.resource_name}' accounts for "
                    f"{item.total_cost / total * 100:.0f}% of costs — review for optimization"
                )

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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Volume-tiered pricing with sorted thresholds | Mirrors real cloud pricing (S3, EC2 data transfer) where unit cost decreases at higher volumes | Flat rate only -- oversimplifies; real cloud bills have significant tiered discounts |
| Fallback to on-demand pricing when tier not found | A resource using SPOT pricing for a type that only has ON_DEMAND rules still gets costed, rather than silently dropped | Skip unmatched resources -- silently underestimates the bill |
| What-if scenario comparison | Answers "how much would we save by switching to reserved?" -- the most common FinOps question | Single estimate only -- forces manual comparison of two separate runs |
| Heuristic-based recommendations | Automatically flags common cost optimization opportunities (reserved instances, dominant resources, high network costs) | No recommendations -- produces a bill without actionable insights |
| Frozen PricingRule dataclass | Pricing rules are reference data shared across many calculations; immutability prevents accidental side effects | Mutable rules -- risk of a calculation accidentally modifying shared pricing data |

## Alternative approaches

### Approach B: Tag-based cost allocation

```python
class CostAllocator:
    """Allocate costs to teams and projects based on resource tags.
    Enables showback/chargeback reporting where each team sees
    their share of infrastructure costs."""
    def allocate(self, estimate: CostEstimate,
                 usage: list[ResourceUsage]) -> dict[str, float]:
        by_team: dict[str, float] = {}
        for item, resource in zip(estimate.line_items, usage):
            team = resource.tags.get("team", "unallocated")
            by_team[team] = by_team.get(team, 0) + item.total_cost
        return by_team
```

**Trade-off:** Tag-based cost allocation enables showback (informational) or chargeback (billing) to individual teams, creating cost accountability. This is how mature FinOps organizations operate -- each team sees their infrastructure spend. The tradeoff is that it requires consistent tagging across all resources, which is an organizational discipline challenge. Use total-cost estimates for initial visibility; tag-based allocation when you need per-team accountability.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Resource quantity of zero | `unit_cost = total / resource.quantity` would divide by zero | Guard with `if resource.quantity > 0 else 0` |
| No pricing rule for a resource type/tier combination | Resource is silently skipped; total estimate is understated | Log a warning when no rule is found, or raise an error for unrecognized resource types |
| Volume tiers not sorted by threshold | `calculate` processes tiers in wrong order, producing incorrect costs | Sort tiers by threshold inside `calculate` with `sorted(self.volume_tiers)` |
