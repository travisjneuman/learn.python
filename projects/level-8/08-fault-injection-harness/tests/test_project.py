"""Tests for Fault Injection Harness.

Covers: fault config, injection engine, decorator, corruption, and scoped rules.
"""

from __future__ import annotations

import pytest

from project import (
    FaultConfig,
    FaultInjector,
    FaultType,
    corrupt_data,
)
import random


# --- FaultConfig validation ---------------------------------------------

class TestFaultConfig:
    def test_valid_config(self) -> None:
        config = FaultConfig(name="test", fault_type=FaultType.EXCEPTION, probability=0.5)
        assert config.probability == 0.5

    @pytest.mark.parametrize("prob", [-0.1, 1.1, 2.0])
    def test_invalid_probability_raises(self, prob: float) -> None:
        with pytest.raises(ValueError, match="Probability"):
            FaultConfig(name="bad", fault_type=FaultType.EXCEPTION, probability=prob)


# --- FaultInjector ------------------------------------------------------

class TestFaultInjector:
    def test_exception_injection(self) -> None:
        injector = FaultInjector(seed=0)
        injector.add_rule(FaultConfig(
            name="always-fail", fault_type=FaultType.EXCEPTION,
            probability=1.0, target_function="target_fn",
        ))

        with pytest.raises(RuntimeError, match="FAULT:always-fail"):
            injector.check_and_inject("target_fn")
        assert injector.stats.faults_triggered == 1

    def test_delay_injection(self) -> None:
        injector = FaultInjector(seed=0)
        injector.add_rule(FaultConfig(
            name="slow", fault_type=FaultType.DELAY,
            probability=1.0, delay_seconds=0.01,
        ))
        # Should not raise, just delay
        injector.check_and_inject("any_fn")
        assert injector.stats.faults_triggered == 1

    def test_disabled_injector_skips(self) -> None:
        injector = FaultInjector(seed=0)
        injector.add_rule(FaultConfig(
            name="fail", fault_type=FaultType.EXCEPTION, probability=1.0,
        ))
        injector.disable()
        # Should not raise
        injector.check_and_inject("fn")
        assert injector.stats.calls_intercepted == 0

    def test_probability_zero_never_triggers(self) -> None:
        injector = FaultInjector(seed=0)
        injector.add_rule(FaultConfig(
            name="never", fault_type=FaultType.EXCEPTION, probability=0.0,
        ))
        for _ in range(100):
            injector.check_and_inject("fn")
        assert injector.stats.faults_triggered == 0


# --- Decorator ----------------------------------------------------------

class TestInjectDecorator:
    def test_decorated_function_can_fail(self) -> None:
        injector = FaultInjector(seed=0)
        injector.add_rule(FaultConfig(
            name="err", fault_type=FaultType.EXCEPTION,
            probability=1.0, target_function="my_func",
        ))

        @injector.inject
        def my_func() -> str:
            return "ok"

        with pytest.raises(RuntimeError):
            my_func()

    def test_decorated_function_succeeds_when_no_fault(self) -> None:
        injector = FaultInjector(seed=0)
        # No rules added

        @injector.inject
        def my_func() -> str:
            return "ok"

        assert my_func() == "ok"


# --- Scoped rules -------------------------------------------------------

class TestScopedRules:
    def test_rules_removed_after_scope(self) -> None:
        injector = FaultInjector(seed=0)
        temp_rule = FaultConfig(
            name="temp", fault_type=FaultType.DELAY,
            probability=1.0, delay_seconds=0.001,
        )
        with injector.scope([temp_rule]):
            injector.check_and_inject("fn")
            assert injector.stats.faults_triggered == 1

        # Rule should be gone now — verify by checking matching
        assert len(injector._matching_rules("fn")) == 0


# --- Data corruption ----------------------------------------------------

class TestCorruptData:
    def test_corruption_modifies_data(self) -> None:
        original = {"name": "Alice", "score": 95, "active": True}
        corrupted = corrupt_data(original, corruption_rate=1.0, rng=random.Random(42))
        # At least one field should differ
        assert corrupted != original

    def test_zero_rate_preserves_data(self) -> None:
        original = {"name": "Alice", "score": 95}
        result = corrupt_data(original, corruption_rate=0.0)
        assert result == original

    @pytest.mark.parametrize("value,expected_type", [
        ("hello", str),
        (42, int),
        (True, bool),
    ])
    def test_corruption_preserves_types(self, value, expected_type) -> None:
        result = corrupt_data({"k": value}, corruption_rate=1.0, rng=random.Random(0))
        assert isinstance(result["k"], expected_type)
