"""Tests for Capacity Planning Model.

Covers: growth models, forecast generation, exhaustion detection, and what-if scenarios.
"""

from __future__ import annotations

import pytest

from project import (
    CapacityPlanner,
    GrowthModel,
    ResourceProfile,
    ResourceType,
    exponential_growth,
    linear_growth,
    step_growth,
)


# --- Growth functions ---------------------------------------------------

class TestGrowthFunctions:
    @pytest.mark.parametrize("current,rate,months,expected", [
        (100, 10, 1, 110),
        (100, 10, 6, 160),
        (0, 5, 3, 15),
    ])
    def test_linear_growth(self, current, rate, months, expected) -> None:
        assert linear_growth(current, rate, months) == expected

    def test_exponential_growth(self) -> None:
        result = exponential_growth(100, 10, 1)  # 10% monthly
        assert result == pytest.approx(110.0)

    @pytest.mark.parametrize("months,expected_steps", [
        (1, 0),
        (3, 1),
        (6, 2),
        (12, 4),
    ])
    def test_step_growth(self, months, expected_steps) -> None:
        result = step_growth(100, 50, months)
        assert result == 100 + (50 * expected_steps)


# --- ResourceProfile ---------------------------------------------------

class TestResourceProfile:
    def test_utilization_pct(self) -> None:
        p = ResourceProfile(ResourceType.COMPUTE, current_usage=75, max_capacity=100)
        assert p.utilization_pct == 75.0

    def test_headroom(self) -> None:
        p = ResourceProfile(ResourceType.STORAGE, current_usage=300, max_capacity=1000)
        assert p.headroom == 700


# --- CapacityPlanner ----------------------------------------------------

class TestCapacityPlanner:
    def test_forecast_generates_entries(self) -> None:
        planner = CapacityPlanner()
        planner.add_resource(ResourceProfile(
            ResourceType.COMPUTE, current_usage=50, max_capacity=100,
            growth_model=GrowthModel.LINEAR, growth_rate=5,
        ))
        plan = planner.forecast(months_ahead=6)
        compute_forecasts = [f for f in plan.forecasts if f.resource_type == ResourceType.COMPUTE]
        assert len(compute_forecasts) == 6

    def test_risk_detection(self) -> None:
        planner = CapacityPlanner(risk_threshold_pct=80.0)
        planner.add_resource(ResourceProfile(
            ResourceType.COMPUTE, current_usage=70, max_capacity=100,
            growth_model=GrowthModel.LINEAR, growth_rate=5,
        ))
        plan = planner.forecast(months_ahead=6)
        risky = [f for f in plan.forecasts if f.exhaustion_risk]
        assert len(risky) > 0

    def test_months_until_exhaustion(self) -> None:
        planner = CapacityPlanner()
        profile = ResourceProfile(
            ResourceType.COMPUTE, current_usage=80, max_capacity=100,
            growth_model=GrowthModel.LINEAR, growth_rate=5,
        )
        months = planner.months_until_exhaustion(profile)
        assert months is not None
        assert months == 4  # 80 + 5*4 = 100

    def test_what_if_increased_capacity(self) -> None:
        planner = CapacityPlanner(risk_threshold_pct=80.0)
        profile = ResourceProfile(
            ResourceType.COMPUTE, current_usage=70, max_capacity=100,
            growth_model=GrowthModel.LINEAR, growth_rate=5,
        )
        forecasts = planner.what_if(profile, new_capacity=200)
        # With doubled capacity, should be much less risky
        risky = [f for f in forecasts if f.exhaustion_risk]
        assert len(risky) == 0

    def test_recommendations_generated(self) -> None:
        planner = CapacityPlanner(risk_threshold_pct=50.0)
        planner.add_resource(ResourceProfile(
            ResourceType.STORAGE, current_usage=40, max_capacity=100,
            growth_model=GrowthModel.LINEAR, growth_rate=10,
        ))
        plan = planner.forecast(months_ahead=6)
        assert len(plan.recommendations) > 0
