# Solution: Level 9 / Project 04 - Observability SLO Pack

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
"""Observability SLO Pack — define SLOs, measure SLIs, calculate error budgets."""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# --- Domain types -------------------------------------------------------

class SLIType(Enum):
    AVAILABILITY = "availability"     # % of successful requests
    LATENCY = "latency"              # % of requests under threshold
    THROUGHPUT = "throughput"         # requests/second minimum
    ERROR_RATE = "error_rate"        # inverse: % of errors below threshold


# WHY good_count / total_count instead of a raw percentage? -- SRE best
# practice tracks good events vs total events. This lets you combine SLIs
# across time windows by simply summing counts, which you can't do with
# pre-computed percentages (averaging percentages is statistically wrong
# when sample sizes differ). The error budget = SLO target - actual SLI.
@dataclass
class SLI:
    """Service Level Indicator — a measurable metric."""
    name: str
    sli_type: SLIType
    good_count: int = 0
    total_count: int = 0

    @property
    def value(self) -> float:
        """Current SLI value as a percentage (0-100)."""
        if self.total_count == 0:
            return 100.0
        return (self.good_count / self.total_count) * 100


@dataclass
class SLO:
    """Service Level Objective — a target for an SLI."""
    name: str
    sli: SLI
    target_pct: float  # e.g., 99.9
    window_days: int = 30

    @property
    def error_budget_pct(self) -> float:
        """Total allowed error as percentage of window."""
        return 100.0 - self.target_pct

    @property
    def error_budget_remaining_pct(self) -> float:
        """How much error budget is left."""
        current = self.sli.value
        budget = self.error_budget_pct
        consumed = max(0, self.target_pct - current)
        return max(0, budget - consumed)

    @property
    def in_compliance(self) -> bool:
        return self.sli.value >= self.target_pct

    # WHY burn rate instead of just "in breach or not"? -- A binary check
    # tells you the current state, but burn rate tells you the velocity.
    # A burn rate of 10x means you'll exhaust the monthly error budget in
    # 3 days. Google SRE uses multi-window burn-rate alerts to balance
    # sensitivity (catch real issues) with specificity (avoid false alarms).
    @property
    def burn_rate(self) -> float:
        """Rate of error budget consumption (1.0 = normal, >1 = burning fast)."""
        budget = self.error_budget_pct
        if budget <= 0:
            return 0.0
        consumed = max(0, self.error_budget_pct - self.error_budget_remaining_pct)
        return consumed / budget


@dataclass
class BurnRateAlert:
    """Alert triggered when error budget burns too quickly."""
    slo_name: str
    burn_rate: float
    severity: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "slo": self.slo_name,
            "burn_rate": round(self.burn_rate, 2),
            "severity": self.severity,
            "message": self.message,
        }


# --- SLO Pack (management layer) ---------------------------------------

class SLOPack:
    """Manages a collection of SLOs with monitoring and alerting."""

    def __init__(self) -> None:
        self._slos: dict[str, SLO] = {}

    def add_slo(self, slo: SLO) -> None:
        self._slos[slo.name] = slo

    def get_slo(self, name: str) -> SLO | None:
        return self._slos.get(name)

    def record_event(self, slo_name: str, good: bool) -> None:
        """Record a good or bad event for an SLO's SLI."""
        slo = self._slos.get(slo_name)
        if not slo:
            raise KeyError(f"Unknown SLO: {slo_name}")
        slo.sli.total_count += 1
        if good:
            slo.sli.good_count += 1

    def check_burn_rates(self, warn_threshold: float = 2.0,
                         critical_threshold: float = 10.0) -> list[BurnRateAlert]:
        """Check all SLOs for excessive burn rates."""
        alerts: list[BurnRateAlert] = []
        for slo in self._slos.values():
            rate = slo.burn_rate
            if rate >= critical_threshold:
                alerts.append(BurnRateAlert(
                    slo_name=slo.name, burn_rate=rate, severity="critical",
                    message=f"{slo.name}: burn rate {rate:.1f}x, budget nearly exhausted",
                ))
            elif rate >= warn_threshold:
                alerts.append(BurnRateAlert(
                    slo_name=slo.name, burn_rate=rate, severity="warning",
                    message=f"{slo.name}: burn rate {rate:.1f}x, above normal",
                ))
        return alerts

    def compliance_report(self) -> dict[str, Any]:
        """Generate a compliance report for all SLOs."""
        slos_data: list[dict[str, Any]] = []
        for slo in self._slos.values():
            slos_data.append({
                "name": slo.name,
                "sli_type": slo.sli.sli_type.value,
                "current_sli_pct": round(slo.sli.value, 4),
                "target_pct": slo.target_pct,
                "in_compliance": slo.in_compliance,
                "error_budget_total_pct": round(slo.error_budget_pct, 4),
                "error_budget_remaining_pct": round(slo.error_budget_remaining_pct, 4),
                "burn_rate": round(slo.burn_rate, 2),
            })

        in_compliance = sum(1 for s in self._slos.values() if s.in_compliance)
        return {
            "total_slos": len(self._slos),
            "in_compliance": in_compliance,
            "out_of_compliance": len(self._slos) - in_compliance,
            "slos": slos_data,
        }


# --- Demo ---------------------------------------------------------------

def run_demo() -> dict[str, Any]:
    pack = SLOPack()

    pack.add_slo(SLO(
        name="api-availability",
        sli=SLI("api-success-rate", SLIType.AVAILABILITY),
        target_pct=99.9,
    ))
    pack.add_slo(SLO(
        name="api-latency",
        sli=SLI("api-fast-requests", SLIType.LATENCY),
        target_pct=95.0,
    ))

    rng = random.Random(42)
    for _ in range(10000):
        pack.record_event("api-availability", rng.random() > 0.002)
        pack.record_event("api-latency", rng.random() > 0.06)

    alerts = pack.check_burn_rates()
    report = pack.compliance_report()

    return {
        "report": report,
        "alerts": [a.to_dict() for a in alerts],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SLO/SLI management pack")
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
| Good/total event counting instead of percentages | Counts can be summed across time windows without statistical error; percentages cannot be averaged correctly when sample sizes differ | Pre-computed percentages -- simpler but produces wrong results when combining windows |
| Burn rate as a derived property | Provides velocity information ("how fast are we consuming budget?") rather than just binary breach detection | Boolean `in_breach` only -- loses the urgency signal that predicts future exhaustion |
| SLO wraps SLI with target | Clean separation: SLI measures what happens, SLO defines what should happen. Same SLI can be used with different SLO targets for different service tiers | Single class combining measurement and target -- conflates observation with policy |
| Configurable alert thresholds | Different organizations have different risk tolerances; 2x burn rate may be acceptable for some, alarming for others | Hardcoded thresholds -- forces one-size-fits-all alerting that does not match team needs |
| Default SLI value of 100% when no data | Assumes healthy until proven otherwise; avoids false alerts during startup | Default to 0% -- would fire alerts before any data arrives, creating noise |

## Alternative approaches

### Approach B: Multi-window burn rate alerts (Google SRE style)

```python
class MultiWindowBurnRateAlert:
    """Google SRE-style alerting using two time windows to balance
    sensitivity with specificity. A fast burn (short window) catches
    acute incidents; a slow burn (long window) catches gradual degradation."""
    def __init__(self, slo_target: float,
                 short_window_hours: int = 1,
                 long_window_hours: int = 6):
        self.target = slo_target
        self.short_window = short_window_hours
        self.long_window = long_window_hours

    def evaluate(self, short_window_error_rate: float,
                 long_window_error_rate: float) -> str | None:
        budget = 1 - self.target / 100
        short_burn = short_window_error_rate / budget if budget > 0 else 0
        long_burn = long_window_error_rate / budget if budget > 0 else 0
        # Both windows must fire to reduce false positives
        if short_burn > 14.4 and long_burn > 6:
            return "page"  # immediate human attention
        if short_burn > 6 and long_burn > 3:
            return "ticket"  # non-urgent but needs fix
        return None
```

**Trade-off:** Multi-window alerting dramatically reduces false positives compared to single-threshold alerts. A brief spike triggers the short window but not the long window, so no page fires. Only sustained degradation triggers both windows. The tradeoff is implementation complexity and the need for windowed metric aggregation. Use single-threshold for learning; multi-window for production SRE.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Recording events for an unregistered SLO name | `KeyError` raised by `record_event` | Validate SLO name before recording, or register SLOs before starting traffic |
| SLO target of 100% | `error_budget_pct` is 0.0, making `burn_rate` always 0.0 regardless of actual errors | Validate that target is strictly less than 100%; a 100% SLO allows zero errors, which is not realistic |
| Averaging SLI percentages across unequal time windows | Produces statistically incorrect results (Simpson's paradox) | Always aggregate by summing good_count and total_count, then dividing; never average percentages |
