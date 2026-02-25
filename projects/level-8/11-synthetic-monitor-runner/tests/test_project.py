"""Tests for Synthetic Monitor Runner.

Covers: check types, runner execution, reporting, tag filtering, and history.
"""

from __future__ import annotations

import pytest

from project import (
    CheckResult,
    CheckStatus,
    SyntheticMonitorRunner,
    custom_check,
    http_check,
    threshold_check,
)


# --- Fixtures -----------------------------------------------------------

@pytest.fixture
def runner() -> SyntheticMonitorRunner:
    return SyntheticMonitorRunner()


# --- Check factories ----------------------------------------------------

class TestCheckFactories:
    def test_http_check_passes(self) -> None:
        check = http_check("test-http", "https://example.com/health")
        result = check.check_fn()
        assert result.status == CheckStatus.PASS
        assert "http" in check.tags

    @pytest.mark.parametrize("value,warn,fail,expected_status", [
        (50.0, 70.0, 90.0, CheckStatus.PASS),
        (75.0, 70.0, 90.0, CheckStatus.WARN),
        (95.0, 70.0, 90.0, CheckStatus.FAIL),
    ])
    def test_threshold_check(
        self, value: float, warn: float, fail: float, expected_status: CheckStatus,
    ) -> None:
        check = threshold_check("metric", lambda: value, warn, fail)
        result = check.check_fn()
        assert result.status == expected_status

    def test_custom_check_pass(self) -> None:
        check = custom_check("ok", lambda: True)
        result = check.check_fn()
        assert result.status == CheckStatus.PASS

    def test_custom_check_fail(self) -> None:
        check = custom_check("bad", lambda: False)
        result = check.check_fn()
        assert result.status == CheckStatus.FAIL

    def test_custom_check_exception(self) -> None:
        def boom() -> bool:
            raise RuntimeError("explosion")
        check = custom_check("boom", boom)
        result = check.check_fn()
        assert result.status == CheckStatus.FAIL
        assert "explosion" in result.message


# --- Runner execution ---------------------------------------------------

class TestRunner:
    def test_run_all_returns_report(self, runner: SyntheticMonitorRunner) -> None:
        runner.add_check(custom_check("c1", lambda: True))
        runner.add_check(custom_check("c2", lambda: True))
        report = runner.run_all()
        assert report.total_checks == 2
        assert report.passed == 2
        assert report.overall_healthy is True

    def test_critical_failure_unhealthy(self, runner: SyntheticMonitorRunner) -> None:
        check = custom_check("fail", lambda: False)
        check.critical = True
        runner.add_check(check)
        report = runner.run_all()
        assert report.overall_healthy is False

    def test_non_critical_failure_still_healthy(self, runner: SyntheticMonitorRunner) -> None:
        check = custom_check("soft-fail", lambda: False)
        check.critical = False
        runner.add_check(check)
        runner.add_check(custom_check("ok", lambda: True))
        report = runner.run_all()
        assert report.overall_healthy is True


# --- Tag filtering ------------------------------------------------------

class TestTagFiltering:
    def test_run_by_tag(self, runner: SyntheticMonitorRunner) -> None:
        runner.add_check(http_check("h1", "http://a.com"))
        runner.add_check(custom_check("c1", lambda: True))
        report = runner.run_by_tag("http")
        assert report.total_checks == 1


# --- History ------------------------------------------------------------

class TestHistory:
    def test_history_accumulates(self, runner: SyntheticMonitorRunner) -> None:
        runner.add_check(custom_check("c", lambda: True))
        runner.run_all()
        runner.run_all()
        assert len(runner.history) == 2

    def test_report_serialization(self, runner: SyntheticMonitorRunner) -> None:
        runner.add_check(custom_check("c", lambda: True))
        report = runner.run_all()
        d = report.to_dict()
        assert "total_checks" in d
        assert "checks" in d
        assert len(d["checks"]) == 1
