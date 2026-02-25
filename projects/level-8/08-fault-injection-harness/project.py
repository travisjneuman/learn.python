"""Fault Injection Harness — inject failures for resilience testing.

Design rationale:
    Netflix's Chaos Monkey proved that injecting failures proactively
    builds more resilient systems. This project creates a configurable
    fault injection framework that can introduce exceptions, delays,
    and data corruption — teaching how to test error-handling paths
    that rarely execute in normal operation.

Concepts practised:
    - decorator-based fault injection
    - configurable fault types (exception, delay, corruption)
    - probability-based triggering
    - dataclasses for fault configuration
    - context manager for scoped fault injection
"""

from __future__ import annotations

import argparse
import json
import random
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Generator


# --- Domain types -------------------------------------------------------

class FaultType(Enum):
    """Types of faults that can be injected."""
    EXCEPTION = "exception"
    DELAY = "delay"
    CORRUPTION = "corruption"
    TIMEOUT = "timeout"


@dataclass
class FaultConfig:
    """Configuration for a single fault injection rule."""
    name: str
    fault_type: FaultType
    probability: float  # 0.0 to 1.0
    target_function: str = "*"  # "*" matches all
    delay_seconds: float = 1.0  # for DELAY type
    exception_class: str = "RuntimeError"
    exception_message: str = "Injected fault"
    enabled: bool = True

    def __post_init__(self) -> None:
        if not 0.0 <= self.probability <= 1.0:
            raise ValueError(f"Probability must be 0.0-1.0, got {self.probability}")


@dataclass
class FaultEvent:
    """Record of a fault that was triggered."""
    fault_name: str
    fault_type: FaultType
    target: str
    timestamp: float = field(default_factory=time.monotonic)
    details: str = ""


@dataclass
class HarnessStats:
    """Statistics from a fault injection session."""
    calls_intercepted: int = 0
    faults_triggered: int = 0
    faults_skipped: int = 0
    events: list[FaultEvent] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "calls_intercepted": self.calls_intercepted,
            "faults_triggered": self.faults_triggered,
            "faults_skipped": self.faults_skipped,
            "trigger_rate": round(
                self.faults_triggered / self.calls_intercepted * 100, 1
            ) if self.calls_intercepted > 0 else 0.0,
            "events": [
                {"fault": e.fault_name, "type": e.fault_type.value, "target": e.target}
                for e in self.events
            ],
        }


# --- Fault injection engine ---------------------------------------------

class FaultInjector:
    """Configurable fault injection engine.

    Add fault rules, then use the `inject` decorator or `scope` context
    manager to apply faults to function calls.
    """

    def __init__(self, seed: int | None = None) -> None:
        self._rules: list[FaultConfig] = []
        self._stats = HarnessStats()
        self._rng = random.Random(seed)
        self._active = True

    @property
    def stats(self) -> HarnessStats:
        return self._stats

    def add_rule(self, config: FaultConfig) -> None:
        """Register a fault injection rule."""
        self._rules.append(config)

    def remove_rule(self, name: str) -> bool:
        """Remove a rule by name. Returns True if found."""
        before = len(self._rules)
        self._rules = [r for r in self._rules if r.name != name]
        return len(self._rules) < before

    def enable(self) -> None:
        self._active = True

    def disable(self) -> None:
        self._active = False

    def _matching_rules(self, func_name: str) -> list[FaultConfig]:
        """Find all enabled rules that match a function name."""
        return [
            r for r in self._rules
            if r.enabled and (r.target_function == "*" or r.target_function == func_name)
        ]

    def _should_trigger(self, probability: float) -> bool:
        """Decide whether to trigger based on probability."""
        return self._rng.random() < probability

    def _apply_fault(self, rule: FaultConfig, func_name: str) -> None:
        """Apply the specified fault type."""
        event = FaultEvent(
            fault_name=rule.name,
            fault_type=rule.fault_type,
            target=func_name,
        )
        self._stats.events.append(event)
        self._stats.faults_triggered += 1

        if rule.fault_type == FaultType.EXCEPTION:
            raise RuntimeError(f"[FAULT:{rule.name}] {rule.exception_message}")
        elif rule.fault_type == FaultType.DELAY:
            time.sleep(rule.delay_seconds)
        elif rule.fault_type == FaultType.TIMEOUT:
            time.sleep(rule.delay_seconds)
            raise TimeoutError(f"[FAULT:{rule.name}] Operation timed out")

    def check_and_inject(self, func_name: str) -> None:
        """Check rules and potentially inject a fault before a call."""
        if not self._active:
            return
        self._stats.calls_intercepted += 1
        rules = self._matching_rules(func_name)
        for rule in rules:
            if self._should_trigger(rule.probability):
                self._apply_fault(rule, func_name)
                return
        self._stats.faults_skipped += 1

    def inject(self, func: Callable) -> Callable:
        """Decorator that applies fault injection to a function."""
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            self.check_and_inject(func.__name__)
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        wrapper.__wrapped__ = func  # type: ignore[attr-defined]
        return wrapper

    @contextmanager
    def scope(self, rules: list[FaultConfig]) -> Generator[None, None, None]:
        """Temporarily add rules for the duration of a context."""
        for rule in rules:
            self.add_rule(rule)
        try:
            yield
        finally:
            for rule in rules:
                self.remove_rule(rule.name)


# --- Corruption helper --------------------------------------------------

def corrupt_data(data: dict[str, Any], corruption_rate: float = 0.3,
                 rng: random.Random | None = None) -> dict[str, Any]:
    """Randomly corrupt fields in a data dictionary.

    Used to test data validation and error handling downstream.
    """
    if rng is None:
        rng = random.Random()
    corrupted = dict(data)
    for key in list(corrupted.keys()):
        if rng.random() < corruption_rate:
            value = corrupted[key]
            if isinstance(value, bool):
                corrupted[key] = not value  # Check bool before int (bool is subclass of int)
            elif isinstance(value, str):
                corrupted[key] = value[::-1]  # reverse string
            elif isinstance(value, (int, float)):
                corrupted[key] = -value  # negate number
            elif value is None:
                corrupted[key] = "CORRUPTED"
    return corrupted


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    """Demonstrate fault injection with various fault types."""
    injector = FaultInjector(seed=42)

    # Configure fault rules
    injector.add_rule(FaultConfig(
        name="api-error", fault_type=FaultType.EXCEPTION,
        probability=0.3, target_function="call_api",
        exception_message="Service unavailable",
    ))
    injector.add_rule(FaultConfig(
        name="db-delay", fault_type=FaultType.DELAY,
        probability=0.2, target_function="query_db",
        delay_seconds=0.01,
    ))

    @injector.inject
    def call_api(endpoint: str) -> dict:
        return {"status": 200, "endpoint": endpoint}

    @injector.inject
    def query_db(query: str) -> list:
        return [{"id": 1, "data": query}]

    results: list[dict[str, Any]] = []
    for i in range(20):
        try:
            r = call_api(f"/endpoint/{i}")
            results.append({"call": i, "type": "api", "success": True})
        except RuntimeError:
            results.append({"call": i, "type": "api", "success": False})

        try:
            query_db(f"SELECT * FROM t WHERE id={i}")
            results.append({"call": i, "type": "db", "success": True})
        except (RuntimeError, TimeoutError):
            results.append({"call": i, "type": "db", "success": False})

    # Demo corruption
    original = {"name": "Alice", "score": 95, "active": True}
    corrupted = corrupt_data(original, corruption_rate=0.5, rng=random.Random(42))

    return {
        "stats": injector.stats.to_dict(),
        "results_sample": results[:10],
        "corruption_demo": {"original": original, "corrupted": corrupted},
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fault injection harness")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    parse_args(argv)
    output = run_demo()
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
