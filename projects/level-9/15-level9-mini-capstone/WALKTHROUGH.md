# Level 9 Mini Capstone: Platform Engineering Toolkit — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. This capstone integrates SLOs, cost tracking, reliability scoring, and governance checks into a single platform view. It is the culmination of Level 9 concepts, so spend at least 45 minutes attempting it independently.

## Thinking Process

Real platform engineering teams do not run SLO checks, cost reports, reliability scores, and governance audits in isolation. They compose them into a unified operational view that answers one question: "How healthy is this service?" The answer requires combining signals from multiple domains -- a service might have excellent uptime but terrible cost control, or perfect governance compliance but SLO breaches.

This project uses the **Facade pattern**: a single `PlatformToolkit` class that wraps four independent subsystems (SLOs, costs, reliability, governance) behind one `generate_report()` method. Each subsystem has its own data model, scoring rules, and status vocabulary. The facade aggregates their outputs into a `PlatformReport` without flattening the domain-specific nuances.

The architectural skill being tested here is **composition over inheritance**. You are not building a god class that knows about SLOs, costs, and governance. You are building four focused data models and one thin orchestration layer. This separation means each subsystem can evolve independently -- the cost model can add new trend calculations without touching the reliability scorer.

## Step 1: Build the SLO Subsystem

**What to do:** Create `SLODefinition` with a target percentage, current percentage, and computed properties for error budget remaining and whether the SLO is met.

**Why:** SLOs (Service Level Objectives) are the quantitative contract between a service and its users. An SLO of 99.9% availability means you can afford 43 minutes of downtime per month. The error budget is the difference between 100% and the target -- it is how much room you have to break things before violating the SLO.

```python
@dataclass
class SLODefinition:
    name: str
    target: float    # e.g. 99.9 for 99.9%
    current: float = 100.0

    @property
    def budget_remaining_pct(self) -> float:
        total_budget = 100.0 - self.target   # e.g. 0.1 for 99.9% target
        if total_budget <= 0:
            return 0.0
        consumed = 100.0 - self.current
        remaining = max(0, total_budget - consumed)
        return round(remaining / total_budget * 100, 1)

    @property
    def is_met(self) -> bool:
        return self.current >= self.target
```

The error budget calculation is worth understanding step by step. For a 99.9% target: `total_budget = 0.1`. If current is 99.95%, then `consumed = 0.05`, `remaining = 0.05`, and `budget_remaining_pct = 50.0%`. Half your error budget is left.

**Predict:** If the target is 99.99% and the current is 99.8%, what is `budget_remaining_pct`? Is the SLO met?

## Step 2: Build the Cost Subsystem

**What to do:** Create `CostEntry` for monthly cost records and `CostProfile` with trend detection and over-budget checks.

**Why:** Cost is a dimension of service health that is often overlooked. A service that works perfectly but costs 3x its budget is not healthy. The trend detection (STABLE, INCREASING, SPIKING, DECREASING) provides early warning before costs become a crisis.

```python
@dataclass
class CostProfile:
    budget_monthly: float = 0.0
    entries: list[CostEntry] = field(default_factory=list)

    @property
    def trend(self) -> CostTrend:
        if len(self.entries) < 2:
            return CostTrend.STABLE
        recent = self.entries[-1].amount
        prev = self.entries[-2].amount
        if prev == 0:
            return CostTrend.STABLE
        change_pct = (recent - prev) / prev * 100
        if change_pct > 20:
            return CostTrend.SPIKING
        elif change_pct > 5:
            return CostTrend.INCREASING
        elif change_pct < -5:
            return CostTrend.DECREASING
        return CostTrend.STABLE

    @property
    def over_budget(self) -> bool:
        return self.latest_cost > self.budget_monthly > 0
```

The `over_budget` property uses a double comparison: `latest_cost > self.budget_monthly > 0`. The `> 0` guard prevents false positives when `budget_monthly` is 0 (which would mean "no budget set" rather than "zero budget").

**Predict:** If costs went from $2,800 to $3,500 in one month, what trend category is that? What is the percentage change?

## Step 3: Build the Reliability Subsystem

**What to do:** Create `ReliabilityMetrics` with uptime, MTTR (Mean Time to Recovery), incident count, and change failure rate. Compute a weighted 0-100 reliability score.

**Why:** Reliability is multidimensional. A service can have 99.99% uptime but take 2 hours to recover from incidents (bad MTTR). The weighted score combines all four dimensions into a single number that enables cross-service comparison.

```python
@dataclass
class ReliabilityMetrics:
    uptime_pct: float = 100.0
    mttr_minutes: float = 0.0
    incidents_30d: int = 0
    change_failure_rate_pct: float = 0.0

    @property
    def reliability_score(self) -> float:
        score = 0.0
        # Uptime: 40 points (heaviest weight)
        if self.uptime_pct >= 99.99:
            score += 40
        elif self.uptime_pct >= 99.9:
            score += 35
        # ... more tiers ...

        # MTTR: 25 points (lower is better)
        if self.mttr_minutes <= 5:
            score += 25
        # ... more tiers ...

        # Incidents: 20 points (fewer is better)
        # Change failure rate: 15 points
        return score
```

The weights (40-25-20-15) reflect industry priorities: uptime matters most, then recovery speed, then incident frequency, then deployment safety. These are the same DORA metrics used by Google's DevOps Research program.

**Predict:** A service has 99.95% uptime, 8-minute MTTR, 1 incident in 30 days, and 5% change failure rate. What is its reliability score? Walk through each tier.

## Step 4: Build the Governance Subsystem

**What to do:** Write `run_governance_checks()` that evaluates a service against five operational policies: runbook, monitoring, ownership, documentation, and incident response.

**Why:** Governance ensures services meet organizational standards. A service without a runbook cannot be operated reliably during incidents. A service without an owner has no one accountable for its health. These checks enforce baseline operational maturity.

```python
def run_governance_checks(
    service_name: str,
    has_runbook: bool = False,
    has_monitoring: bool = False,
    has_owner: bool = False,
    has_documentation: bool = False,
    has_incident_response: bool = False,
) -> list[GovernanceCheck]:
    checks: list[GovernanceCheck] = []
    checks.append(GovernanceCheck(
        "runbook", has_runbook,
        "" if has_runbook else f"{service_name} missing operational runbook",
    ))
    # ... remaining checks ...
    return checks
```

The function returns a list of `GovernanceCheck` objects (each with a name, pass/fail boolean, and failure message) rather than a single pass/fail verdict. This granularity matters because "3 of 5 governance checks failed" is actionable ("which 3?"), while "governance: FAIL" is not.

**Predict:** If a service passes runbook, monitoring, and ownership but fails documentation and incident response, what `GovernanceStatus` does it get?

## Step 5: Compose Everything with the Platform Facade

**What to do:** Create `PlatformService` that holds all subsystem data, and `PlatformToolkit` that registers services and generates a unified `PlatformReport`.

**Why:** The facade is where composition happens. Each `PlatformService` contains SLOs, costs, reliability, and governance data. The service's `health` property aggregates issues across all subsystems into a single `HealthStatus` (HEALTHY, DEGRADED, CRITICAL). The `PlatformToolkit` aggregates across all services into a fleet-wide report.

```python
@dataclass
class PlatformService:
    name: str
    team: str
    slos: list[SLODefinition] = field(default_factory=list)
    cost: CostProfile = field(default_factory=CostProfile)
    reliability: ReliabilityMetrics = field(default_factory=ReliabilityMetrics)
    governance_checks: list[GovernanceCheck] = field(default_factory=list)

    @property
    def health(self) -> HealthStatus:
        issues = 0
        if any(not slo.is_met for slo in self.slos):
            issues += 2
        if self.reliability.reliability_score < 50:
            issues += 2
        elif self.reliability.reliability_score < 70:
            issues += 1
        # ... governance and cost checks ...

        if issues >= 4:
            return HealthStatus.CRITICAL
        elif issues >= 2:
            return HealthStatus.DEGRADED
        return HealthStatus.HEALTHY
```

The issue-counting approach is a simple but effective scoring heuristic. SLO breaches and low reliability are weighted more heavily (2 points each) because they directly impact users. Governance failures and cost overruns add 1 point each because they are organizational concerns, not user-facing outages.

**Predict:** A service has an SLO breach (2 issues), reliability score of 60 (1 issue), and passes all governance checks (0 issues). What health status does it get?

## Step 6: Generate the Report and Run the Demo

**What to do:** Write `generate_report()` that aggregates all registered services into a `PlatformReport`, and `run_demo()` that creates two services (one healthy, one degraded) and prints the report.

**Why:** The report is the deliverable. It answers "how is the platform doing?" with numbers: how many services are healthy, how many SLOs are breached, total monthly cost, and average reliability score. The per-service details let operators drill into the specific service that needs attention.

```python
class PlatformToolkit:
    def generate_report(self) -> PlatformReport:
        services = list(self._services.values())
        if not services:
            return PlatformReport(0, 0, 0, 0, 0, 0, 0, 0.0, 0.0)

        # Count health statuses
        health_counts = {s: 0 for s in HealthStatus}
        for svc in services:
            health_counts[svc.health] += 1

        # Aggregate metrics
        avg_reliability = sum(
            svc.reliability.reliability_score for svc in services
        ) / len(services)
        # ...
```

The empty-services guard (`if not services`) is important -- without it, the `/ len(services)` division would crash with `ZeroDivisionError`. Defensive programming at the boundary prevents cascading failures.

**Predict:** If you add a third service with `HealthStatus.CRITICAL`, how does the report's breakdown change?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Dividing by zero in `generate_report()` | No services registered | Guard with `if not services: return empty report` |
| `budget_monthly=0` causes false `over_budget` | Treating "no budget set" as "zero budget" | Use `self.budget_monthly > 0` guard in the property |
| Single `HealthStatus` for all failure types | Collapsing distinct domains into one status | Keep separate enums per domain; compose in the health property |
| Modifying subsystem data in the facade | Facade mutating service objects during report generation | Keep `generate_report()` read-only; only aggregate, never modify |
| Forgetting `field(default_factory=...)` | Dataclass mutable default trap | Always use factory for lists, dicts, and mutable defaults |

## Testing Your Solution

```bash
pytest -q
```

Expected output:
```text
7 passed
```

Test from the command line:

```bash
python project.py --demo
```

You should see JSON output with `total_services`, health counts, SLO breach count, cost totals, reliability scores, and per-service detail rows.

## What You Learned

- **The Facade pattern** simplifies complex multi-subsystem interactions by providing one unified API. Callers do not need to understand the internals of SLOs, costs, reliability, and governance -- they just call `generate_report()` and get a complete picture.
- **Composition over inheritance** keeps subsystems independent. The cost model does not know about SLOs, the governance checker does not know about reliability. Each can evolve, be tested, and be reasoned about in isolation. The facade is the only place they meet.
- **Multi-dimensional health scoring** reflects reality: a service is not simply "up" or "down." It has SLO compliance, cost efficiency, operational reliability, and governance maturity. Platform engineering is about seeing all dimensions simultaneously and prioritizing the most urgent problems.
