# Solution: Level 8 / Project 08 - Fault Injection Harness

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try the [Walkthrough](./WALKTHROUGH.md) first -- it guides
> your thinking without giving away the answer.
>
> [Back to project README](./README.md)

---

## Complete solution

```python
"""Fault Injection Harness -- inject failures for resilience testing."""

from __future__ import annotations

import argparse
import json
import random
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Generator

class FaultType(Enum):
    EXCEPTION = "exception"
    DELAY = "delay"
    CORRUPTION = "corruption"
    TIMEOUT = "timeout"

# WHY probability-based injection? -- Real failures are stochastic. A 30%
# rate tests intermittent recovery, not just total outages. This is the
# Netflix Chaos Monkey approach: inject realistic failure rates.
@dataclass
class FaultConfig:
    name: str
    fault_type: FaultType
    probability: float
    target_function: str = "*"
    delay_seconds: float = 1.0
    exception_class: str = "RuntimeError"
    exception_message: str = "Injected fault"
    enabled: bool = True

    def __post_init__(self) -> None:
        if not 0.0 <= self.probability <= 1.0:
            raise ValueError(f"Probability must be 0.0-1.0, got {self.probability}")

@dataclass
class FaultEvent:
    fault_name: str
    fault_type: FaultType
    target: str
    timestamp: float = field(default_factory=time.monotonic)
    details: str = ""

@dataclass
class HarnessStats:
    calls_intercepted: int = 0
    faults_triggered: int = 0
    faults_skipped: int = 0
    events: list[FaultEvent] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "calls_intercepted": self.calls_intercepted,
            "faults_triggered": self.faults_triggered,
            "faults_skipped": self.faults_skipped,
            "trigger_rate": round(self.faults_triggered / self.calls_intercepted * 100, 1)
                           if self.calls_intercepted > 0 else 0.0,
            "events": [{"fault": e.fault_name, "type": e.fault_type.value,
                         "target": e.target} for e in self.events],
        }

class FaultInjector:
    """Centralized fault engine: add/remove rules, inject via decorator
    or context manager, track all triggered faults in one place."""

    def __init__(self, seed: int | None = None) -> None:
        self._rules: list[FaultConfig] = []
        self._stats = HarnessStats()
        # WHY seeded RNG? -- Same seed = same faults = deterministic tests.
        self._rng = random.Random(seed)
        self._active = True

    @property
    def stats(self) -> HarnessStats:
        return self._stats

    def add_rule(self, config: FaultConfig) -> None:
        self._rules.append(config)

    def remove_rule(self, name: str) -> bool:
        before = len(self._rules)
        self._rules = [r for r in self._rules if r.name != name]
        return len(self._rules) < before

    def enable(self) -> None:
        self._active = True

    def disable(self) -> None:
        self._active = False

    def _matching_rules(self, func_name: str) -> list[FaultConfig]:
        return [r for r in self._rules
                if r.enabled and (r.target_function == "*" or r.target_function == func_name)]

    def _should_trigger(self, probability: float) -> bool:
        return self._rng.random() < probability

    def _apply_fault(self, rule: FaultConfig, func_name: str) -> None:
        self._stats.events.append(FaultEvent(
            fault_name=rule.name, fault_type=rule.fault_type, target=func_name))
        self._stats.faults_triggered += 1
        if rule.fault_type == FaultType.EXCEPTION:
            raise RuntimeError(f"[FAULT:{rule.name}] {rule.exception_message}")
        elif rule.fault_type == FaultType.DELAY:
            time.sleep(rule.delay_seconds)
        elif rule.fault_type == FaultType.TIMEOUT:
            time.sleep(rule.delay_seconds)
            raise TimeoutError(f"[FAULT:{rule.name}] Operation timed out")

    def check_and_inject(self, func_name: str) -> None:
        if not self._active:
            return
        self._stats.calls_intercepted += 1
        for rule in self._matching_rules(func_name):
            if self._should_trigger(rule.probability):
                self._apply_fault(rule, func_name)
                return
        self._stats.faults_skipped += 1

    def inject(self, func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            self.check_and_inject(func.__name__)
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        wrapper.__wrapped__ = func
        return wrapper

    @contextmanager
    def scope(self, rules: list[FaultConfig]) -> Generator[None, None, None]:
        # WHY try/finally? -- Rules must be cleaned up even if the block
        # raises, preventing rule leakage into subsequent tests.
        for rule in rules:
            self.add_rule(rule)
        try:
            yield
        finally:
            for rule in rules:
                self.remove_rule(rule.name)

# WHY check bool before int? -- In Python, bool is a subclass of int.
# isinstance(True, int) is True. Without the bool check first,
# True becomes -1 instead of False.
def corrupt_data(data: dict[str, Any], corruption_rate: float = 0.3,
                 rng: random.Random | None = None) -> dict[str, Any]:
    if rng is None:
        rng = random.Random()
    corrupted = dict(data)
    for key in list(corrupted.keys()):
        if rng.random() < corruption_rate:
            value = corrupted[key]
            if isinstance(value, bool):
                corrupted[key] = not value
            elif isinstance(value, str):
                corrupted[key] = value[::-1]
            elif isinstance(value, (int, float)):
                corrupted[key] = -value
            elif value is None:
                corrupted[key] = "CORRUPTED"
    return corrupted

def run_demo() -> dict[str, Any]:
    injector = FaultInjector(seed=42)
    injector.add_rule(FaultConfig(name="api-error", fault_type=FaultType.EXCEPTION,
                                  probability=0.3, target_function="call_api",
                                  exception_message="Service unavailable"))
    injector.add_rule(FaultConfig(name="db-delay", fault_type=FaultType.DELAY,
                                  probability=0.2, target_function="query_db",
                                  delay_seconds=0.01))

    @injector.inject
    def call_api(endpoint: str) -> dict:
        return {"status": 200, "endpoint": endpoint}

    @injector.inject
    def query_db(query: str) -> list:
        return [{"id": 1, "data": query}]

    results: list[dict[str, Any]] = []
    for i in range(20):
        try:
            call_api(f"/endpoint/{i}")
            results.append({"call": i, "type": "api", "success": True})
        except RuntimeError:
            results.append({"call": i, "type": "api", "success": False})
        try:
            query_db(f"SELECT * FROM t WHERE id={i}")
            results.append({"call": i, "type": "db", "success": True})
        except (RuntimeError, TimeoutError):
            results.append({"call": i, "type": "db", "success": False})

    original = {"name": "Alice", "score": 95, "active": True}
    corrupted = corrupt_data(original, corruption_rate=0.5, rng=random.Random(42))
    return {"stats": injector.stats.to_dict(), "results_sample": results[:10],
            "corruption_demo": {"original": original, "corrupted": corrupted}}

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Fault injection harness")
    parser.add_argument("--seed", type=int, default=42)
    parser.parse_args(argv)
    print(json.dumps(run_demo(), indent=2))

if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Seeded RNG for reproducibility | Same seed = same faults = deterministic debugging | System random -- realistic but non-reproducible |
| Decorator + context manager APIs | Decorator for permanent injection; context manager for scoped test blocks | Decorator only -- loses temporary scoped injection |
| `bool` checked before `int` in corruption | Python's `bool` subclasses `int`; wrong order corrupts `True` to `-1` | Type dispatch dict -- cleaner but more code for a helper |
| `__post_init__` probability validation | Catches config bugs at creation time, not at injection time | Silent clamping -- hides the error instead of surfacing it |

## Alternative approaches

### Approach B: Middleware-based fault injection for web apps

```python
class FaultMiddleware:
    """Inject faults at the HTTP layer. Every request passes through,
    and the injector decides based on route, headers, or user ID."""
    def __init__(self, app, injector: FaultInjector):
        self.app = app
        self.injector = injector

    def __call__(self, request):
        self.injector.check_and_inject(request.path)
        return self.app(request)
```

**Trade-off:** Middleware injection is more realistic for web services (faults at the network boundary) but only works for HTTP-based systems. The decorator approach works for any callable, making it more versatile for unit-level chaos testing.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Probability > 1.0 in FaultConfig | `__post_init__` raises ValueError immediately -- correct behaviour | Validation catches this; without it, faults fire every time |
| Exception inside `scope()` block | Rules must still be removed to avoid polluting future tests | `try/finally` ensures cleanup even on exception |
| Not catching injected exceptions | Unhandled RuntimeError crashes the program | Always wrap fault-injected calls in try/except |
