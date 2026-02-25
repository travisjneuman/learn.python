"""Tests for Service Simulator."""

import pytest

from project import (
    ServiceConfig,
    ServiceResponse,
    SimulatedService,
    retry_request,
    run_load_test,
)


@pytest.fixture
def always_succeed() -> SimulatedService:
    """Service that always returns 200."""
    return SimulatedService(ServiceConfig(
        success_rate=1.0,
        timeout_rate=0.0,
        error_rate=0.0,
        rate_limit_rate=0.0,
        seed=42,
    ))


@pytest.fixture
def always_fail() -> SimulatedService:
    """Service that always returns 500."""
    return SimulatedService(ServiceConfig(
        success_rate=0.0,
        timeout_rate=0.0,
        error_rate=1.0,
        rate_limit_rate=0.0,
        seed=42,
    ))


def test_successful_request(always_succeed: SimulatedService) -> None:
    """Service configured for 100% success should return 200."""
    response = always_succeed.request("GET", "/api/data")
    assert response.status_code == 200
    assert response.error is None


def test_error_request(always_fail: SimulatedService) -> None:
    """Service configured for 100% error should return 500."""
    response = always_fail.request("GET", "/api/data")
    assert response.status_code == 500
    assert response.error is not None


def test_response_has_latency(always_succeed: SimulatedService) -> None:
    """Every response should have positive latency."""
    response = always_succeed.request()
    assert response.latency_ms > 0


def test_seed_produces_deterministic_results() -> None:
    """Same seed should produce same sequence of responses."""
    s1 = SimulatedService(ServiceConfig(seed=123))
    s2 = SimulatedService(ServiceConfig(seed=123))
    for _ in range(10):
        r1 = s1.request()
        r2 = s2.request()
        assert r1.status_code == r2.status_code


def test_retry_succeeds(always_succeed: SimulatedService) -> None:
    """Retry on always-succeed should return 200 on first try."""
    response, attempts = retry_request(always_succeed)
    assert response.status_code == 200
    assert attempts == 1


def test_retry_exhausted(always_fail: SimulatedService) -> None:
    """Retry on always-fail should exhaust retries."""
    response, attempts = retry_request(always_fail, max_retries=3)
    assert response.status_code == 500
    assert attempts == 3


def test_run_load_test(always_succeed: SimulatedService) -> None:
    """Load test should return correct total and status counts."""
    results = run_load_test(always_succeed, 50)
    assert results["total_requests"] == 50
    assert 200 in results["by_status"]


def test_mixed_responses() -> None:
    """With default config, a large sample should have mixed statuses."""
    service = SimulatedService(ServiceConfig(seed=42))
    results = run_load_test(service, 1000)
    # With default rates, we should see multiple status codes.
    assert len(results["by_status"]) >= 2


def test_service_config_defaults() -> None:
    """Default config should have sensible values."""
    config = ServiceConfig()
    assert 0 <= config.success_rate <= 1
    assert config.min_latency_ms < config.max_latency_ms
