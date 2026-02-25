"""Tests for Observability SLO Pack.

Covers: SLI calculation, SLO compliance, error budgets, burn rates, and reporting.
"""

from __future__ import annotations

import pytest

from project import SLI, SLIType, SLO, SLOPack


# --- SLI ----------------------------------------------------------------

class TestSLI:
    def test_value_with_no_events(self) -> None:
        sli = SLI("test", SLIType.AVAILABILITY)
        assert sli.value == 100.0

    @pytest.mark.parametrize("good,total,expected", [
        (999, 1000, 99.9),
        (950, 1000, 95.0),
        (0, 100, 0.0),
        (100, 100, 100.0),
    ])
    def test_value_calculation(self, good: int, total: int, expected: float) -> None:
        sli = SLI("test", SLIType.AVAILABILITY, good_count=good, total_count=total)
        assert sli.value == pytest.approx(expected)


# --- SLO ----------------------------------------------------------------

class TestSLO:
    def test_in_compliance_when_above_target(self) -> None:
        sli = SLI("s", SLIType.AVAILABILITY, good_count=999, total_count=1000)
        slo = SLO("test", sli, target_pct=99.0)
        assert slo.in_compliance is True

    def test_out_of_compliance_when_below_target(self) -> None:
        sli = SLI("s", SLIType.AVAILABILITY, good_count=980, total_count=1000)
        slo = SLO("test", sli, target_pct=99.0)
        assert slo.in_compliance is False

    def test_error_budget_pct(self) -> None:
        sli = SLI("s", SLIType.AVAILABILITY)
        slo = SLO("test", sli, target_pct=99.9)
        assert slo.error_budget_pct == pytest.approx(0.1)

    def test_burn_rate_normal(self) -> None:
        sli = SLI("s", SLIType.AVAILABILITY, good_count=999, total_count=1000)
        slo = SLO("test", sli, target_pct=99.9)
        assert slo.burn_rate >= 0


# --- SLOPack ------------------------------------------------------------

class TestSLOPack:
    def test_add_and_record(self) -> None:
        pack = SLOPack()
        pack.add_slo(SLO("avail", SLI("s", SLIType.AVAILABILITY), target_pct=99.0))
        pack.record_event("avail", True)
        pack.record_event("avail", False)
        slo = pack.get_slo("avail")
        assert slo is not None
        assert slo.sli.total_count == 2

    def test_record_unknown_slo_raises(self) -> None:
        pack = SLOPack()
        with pytest.raises(KeyError, match="Unknown SLO"):
            pack.record_event("nonexistent", True)

    def test_compliance_report_structure(self) -> None:
        pack = SLOPack()
        pack.add_slo(SLO("avail", SLI("s", SLIType.AVAILABILITY), target_pct=99.0))
        for _ in range(100):
            pack.record_event("avail", True)
        report = pack.compliance_report()
        assert "total_slos" in report
        assert "slos" in report
        assert report["in_compliance"] == 1

    def test_burn_rate_alerting(self) -> None:
        pack = SLOPack()
        pack.add_slo(SLO("bad", SLI("s", SLIType.AVAILABILITY), target_pct=99.9))
        # Record mostly failures to exhaust budget — burn rate = consumed/total_budget
        # With 100 failures the SLI is 0%, budget is 0.1%, consumed is 99.9% which
        # exceeds the budget entirely, so burn_rate = 1.0. Use a lower threshold.
        for _ in range(100):
            pack.record_event("bad", False)
        alerts = pack.check_burn_rates(warn_threshold=0.5, critical_threshold=0.9)
        assert len(alerts) > 0
        assert alerts[0].severity == "critical"
