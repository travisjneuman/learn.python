"""Tests for Platform Cost Estimator.

Covers: pricing rules, volume tiers, cost estimation, what-if analysis,
and optimization recommendations.
"""

from __future__ import annotations

import pytest

from project import (
    CostEstimate,
    PlatformCostEstimator,
    PricingRule,
    PricingTier,
    ResourceType,
    ResourceUsage,
)


# --- Fixtures -----------------------------------------------------------

@pytest.fixture
def estimator() -> PlatformCostEstimator:
    return PlatformCostEstimator()


@pytest.fixture
def simple_estimator() -> PlatformCostEstimator:
    rules = [
        PricingRule(ResourceType.COMPUTE, PricingTier.ON_DEMAND, 0.10),
        PricingRule(ResourceType.COMPUTE, PricingTier.RESERVED, 0.06),
        PricingRule(ResourceType.STORAGE, PricingTier.ON_DEMAND, 0.02),
    ]
    return PlatformCostEstimator(pricing_rules=rules)


# --- Pricing rules ------------------------------------------------------

class TestPricingRules:
    def test_flat_rate(self) -> None:
        rule = PricingRule(ResourceType.COMPUTE, PricingTier.ON_DEMAND, 0.10)
        assert rule.calculate(100) == pytest.approx(10.0)

    def test_volume_tiers(self) -> None:
        rule = PricingRule(
            ResourceType.STORAGE, PricingTier.ON_DEMAND, 0.01,
            volume_tiers=((100, 0.05), (500, 0.03)),
        )
        # First 100 at 0.05, next 50 at 0.03
        cost = rule.calculate(150)
        expected = 100 * 0.05 + 50 * 0.03
        assert cost == pytest.approx(expected)

    def test_volume_tiers_beyond_all_tiers(self) -> None:
        rule = PricingRule(
            ResourceType.STORAGE, PricingTier.ON_DEMAND, 0.01,
            volume_tiers=((100, 0.05),),
        )
        # First 100 at 0.05, remaining 200 at base 0.01
        cost = rule.calculate(300)
        expected = 100 * 0.05 + 200 * 0.01
        assert cost == pytest.approx(expected)

    def test_zero_quantity(self) -> None:
        rule = PricingRule(ResourceType.COMPUTE, PricingTier.ON_DEMAND, 0.10)
        assert rule.calculate(0) == 0.0


# --- Cost estimation ----------------------------------------------------

class TestEstimation:
    def test_single_resource(self, simple_estimator: PlatformCostEstimator) -> None:
        usage = [ResourceUsage("srv", ResourceType.COMPUTE, 100)]
        est = simple_estimator.estimate(usage)
        assert est.total_monthly == pytest.approx(10.0)

    def test_reserved_cheaper_than_on_demand(self, simple_estimator: PlatformCostEstimator) -> None:
        on_demand = [ResourceUsage("srv", ResourceType.COMPUTE, 100, pricing_tier=PricingTier.ON_DEMAND)]
        reserved = [ResourceUsage("srv", ResourceType.COMPUTE, 100, pricing_tier=PricingTier.RESERVED)]
        od_est = simple_estimator.estimate(on_demand)
        rv_est = simple_estimator.estimate(reserved)
        assert rv_est.total_monthly < od_est.total_monthly

    def test_multiple_resources(self, simple_estimator: PlatformCostEstimator) -> None:
        usage = [
            ResourceUsage("compute", ResourceType.COMPUTE, 100),
            ResourceUsage("storage", ResourceType.STORAGE, 200),
        ]
        est = simple_estimator.estimate(usage)
        assert est.total_monthly == pytest.approx(100 * 0.10 + 200 * 0.02)

    def test_by_type_breakdown(self, simple_estimator: PlatformCostEstimator) -> None:
        usage = [
            ResourceUsage("a", ResourceType.COMPUTE, 50),
            ResourceUsage("b", ResourceType.STORAGE, 100),
        ]
        est = simple_estimator.estimate(usage)
        assert "compute" in est.by_type
        assert "storage" in est.by_type

    def test_unknown_tier_falls_back(self, simple_estimator: PlatformCostEstimator) -> None:
        usage = [ResourceUsage("srv", ResourceType.COMPUTE, 100, pricing_tier=PricingTier.SPOT)]
        est = simple_estimator.estimate(usage)
        # Falls back to on-demand pricing
        assert est.total_monthly == pytest.approx(10.0)


# --- What-if analysis ---------------------------------------------------

class TestWhatIf:
    def test_cost_reduction(self, estimator: PlatformCostEstimator) -> None:
        baseline = [ResourceUsage("srv", ResourceType.COMPUTE, 720)]
        modified = [ResourceUsage("srv", ResourceType.COMPUTE, 720, pricing_tier=PricingTier.RESERVED)]
        result = estimator.what_if(baseline, modified)
        assert result["difference"] < 0
        assert result["change_pct"] < 0

    def test_same_usage_no_change(self, estimator: PlatformCostEstimator) -> None:
        usage = [ResourceUsage("srv", ResourceType.COMPUTE, 100)]
        result = estimator.what_if(usage, usage)
        assert result["difference"] == 0


# --- Recommendations ---------------------------------------------------

class TestRecommendations:
    def test_high_on_demand_compute(self, estimator: PlatformCostEstimator) -> None:
        usage = [ResourceUsage("big-server", ResourceType.COMPUTE, 1000)]
        est = estimator.estimate(usage)
        assert any("reserved" in r.lower() for r in est.recommendations)

    def test_no_recommendations_for_small_usage(self, estimator: PlatformCostEstimator) -> None:
        usage = [ResourceUsage("tiny", ResourceType.COMPUTE, 10)]
        est = estimator.estimate(usage)
        reserved_recs = [r for r in est.recommendations if "reserved" in r.lower()]
        assert len(reserved_recs) == 0


# --- Serialization ------------------------------------------------------

class TestSerialization:
    def test_to_dict_keys(self, estimator: PlatformCostEstimator) -> None:
        usage = [ResourceUsage("srv", ResourceType.COMPUTE, 100)]
        d = estimator.estimate(usage).to_dict()
        assert "total_monthly" in d
        assert "by_type" in d
        assert "line_items" in d
        assert "recommendations" in d
