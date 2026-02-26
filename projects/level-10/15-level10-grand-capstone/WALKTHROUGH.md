# Level 10 Grand Capstone: Enterprise Platform — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. This is the grand capstone of the entire core curriculum -- it integrates patterns from all 14 prior Level 10 projects into a unified platform. Spend at least 60 minutes attempting it independently. If you have completed the earlier Level 10 projects, you will recognize each subsystem.

## Thinking Process

This capstone answers a deceptively simple question: "Is this service ready for production?" The answer requires checking five dimensions: Do the policies allow it? Is the service operationally ready? Does the architecture fit our constraints? Does the change pass the risk gate? And who is the tenant? Each dimension is a separate subsystem with its own rules, but the platform must produce one coherent report.

The architecture is a **Facade over five Protocol-based subsystems**. The `EnterprisePlatform` class does not implement policy checking, readiness evaluation, or fitness testing itself. It delegates to specialized classes (`RequiredFieldPolicy`, `ReadinessChecker`, `ArchitectureFitness`, `ChangeGate`) and aggregates their results into a `PlatformReport`. This is dependency injection without a framework -- each subsystem is passed into the platform at construction time and can be swapped, extended, or tested independently.

The unifying concept is the **universal `CheckResult` type**. Every subsystem produces `CheckResult` objects with the same structure: subsystem name, check ID, pass/fail/warn status, severity, and message. This common language lets the platform aggregate results from different domains into a single dashboard without translating between subsystem-specific result types. This is composition at scale.

## Step 1: Define the Shared Domain Types

**What to do:** Create `Severity` and `Status` enums, and a frozen `CheckResult` dataclass that all subsystems share.

**Why:** A universal result type is what makes the facade possible. Without it, the platform would need to understand the internal types of every subsystem. With `CheckResult`, the platform just counts passes, fails, and warnings -- regardless of whether they came from policy, readiness, architecture, or change gate checks.

```python
class Severity(Enum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class Status(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"


@dataclass(frozen=True)
class CheckResult:
    subsystem: str      # Which subsystem produced this result
    check_id: str       # Unique identifier for the check
    status: Status      # Pass, fail, or warn
    severity: Severity  # How serious is a failure
    message: str        # Human-readable explanation
```

The `frozen=True` makes results immutable. Once a subsystem produces a result, nothing can change it -- not the platform, not another subsystem, not a reporting layer. This guarantees audit integrity.

**Predict:** Why does `CheckResult` include both `status` (pass/fail/warn) and `severity` (info/warning/error/critical)? Can a check pass with CRITICAL severity?

## Step 2: Build the Tenant Manager

**What to do:** Create a `Tenant` dataclass and `TenantManager` class for multi-tenant registration and lookup.

**Why:** Enterprise platforms serve multiple tenants (customers, teams, business units). Each tenant has a plan level (basic, standard, enterprise) that determines what features and policies apply. The tenant manager is the identity layer -- it answers "who is making this request?"

```python
@dataclass(frozen=True)
class Tenant:
    tenant_id: str
    name: str
    plan: str  # basic, standard, enterprise


class TenantManager:
    def __init__(self) -> None:
        self._tenants: dict[str, Tenant] = {}

    def register(self, tenant: Tenant) -> None:
        self._tenants[tenant.tenant_id] = tenant

    def get(self, tenant_id: str) -> Tenant | None:
        return self._tenants.get(tenant_id)
```

The tenant manager is intentionally simple. In a real system, it would integrate with an identity provider (Auth0, Okta). Here, it demonstrates the pattern: register tenants, look them up, and pass their plan level into policy checks.

**Predict:** If two tenants are registered with plans "enterprise" and "basic", and a policy requires "standard" plan minimum, which tenant passes?

## Step 3: Build the Policy Engine

**What to do:** Define a `PolicyCheck` protocol and implement two concrete policies: `RequiredFieldPolicy` (checks for required context fields) and `PlanLevelPolicy` (checks tenant plan meets a minimum).

**Why:** Policies are the governance layer. They enforce organizational rules: "every service must have an owner," "every deployment must have a cost center," "only enterprise-plan tenants can use this feature." The Protocol interface means new policies can be added without modifying the engine.

```python
class PolicyCheck(Protocol):
    def check_id(self) -> str: ...
    def evaluate(self, context: dict[str, Any]) -> CheckResult: ...


class RequiredFieldPolicy:
    def __init__(self, field_name: str) -> None:
        self._field = field_name

    def check_id(self) -> str:
        return f"POL-REQ-{self._field}"

    def evaluate(self, context: dict[str, Any]) -> CheckResult:
        if context.get(self._field):
            return CheckResult("policy", self.check_id(), Status.PASS,
                             Severity.INFO, f"'{self._field}' present")
        return CheckResult("policy", self.check_id(), Status.FAIL,
                         Severity.ERROR, f"'{self._field}' missing")


class PlanLevelPolicy:
    def __init__(self, min_plan: str) -> None:
        self._min = min_plan
        self._levels = {"basic": 1, "standard": 2, "enterprise": 3}

    def evaluate(self, context: dict[str, Any]) -> CheckResult:
        plan = context.get("plan", "basic")
        if self._levels.get(plan, 0) >= self._levels.get(self._min, 0):
            return CheckResult("policy", self.check_id(), Status.PASS, ...)
        return CheckResult("policy", self.check_id(), Status.FAIL, ...)
```

The `PlanLevelPolicy` uses a level mapping (`{"basic": 1, "standard": 2, "enterprise": 3}`) to compare plans numerically. This is cleaner than a chain of `if/elif` statements and makes it easy to add new plan tiers.

**Predict:** What does `RequiredFieldPolicy("owner").evaluate({"owner": ""})` return? Is an empty string considered "present"?

## Step 4: Build the Change Gate and Readiness Checker

**What to do:** Create `ChangeGate` (risk-scored approval/rejection) and `ReadinessChecker` (operational readiness evaluation).

**Why:** The change gate prevents high-risk changes from reaching production without review. The readiness checker verifies that a service has the operational prerequisites (monitoring, alerting, runbook, health check) before it is considered production-ready.

```python
class ChangeGate:
    def __init__(self, auto_approve_threshold: float = 25.0,
                 block_threshold: float = 75.0) -> None:
        self._auto_threshold = auto_approve_threshold
        self._block_threshold = block_threshold

    def evaluate(self, change: ChangeRequest) -> CheckResult:
        if change.risk_score < self._auto_threshold:
            return CheckResult("change_gate", change.change_id, Status.PASS,
                             Severity.INFO, "Auto-approved")
        if change.risk_score >= self._block_threshold:
            return CheckResult("change_gate", change.change_id, Status.FAIL,
                             Severity.CRITICAL, "Blocked — too risky")
        return CheckResult("change_gate", change.change_id, Status.WARN,
                         Severity.WARNING, "Needs review")


class ReadinessChecker:
    def evaluate(self, svc: ServiceConfig) -> list[CheckResult]:
        results: list[CheckResult] = []
        checks = [
            ("monitoring", svc.has_monitoring),
            ("alerting", svc.has_alerting),
            ("runbook", svc.has_runbook),
            ("healthcheck", svc.has_healthcheck),
        ]
        for name, present in checks:
            status = Status.PASS if present else Status.FAIL
            severity = Severity.INFO if present else Severity.ERROR
            results.append(CheckResult("readiness", f"RDY-{name}", status,
                                      severity, f"{name}: {'present' if present else 'missing'}"))
        return results
```

The change gate has three zones: auto-approve (low risk, below 25), needs review (medium risk, 25-75), and blocked (high risk, 75+). This three-tier model is used by real change management systems like ServiceNow and PagerDuty.

**Predict:** A change with risk score 50 gets "Needs review" (WARN). Does this count as a failure in the overall health score?

## Step 5: Build the Architecture Fitness Evaluator

**What to do:** Create `ArchitectureFitness` that checks service count and average dependency count against thresholds.

**Why:** Architecture fitness functions are automated checks that verify your system stays within architectural constraints. Too many services create operational overhead. Too many dependencies create coupling and cascading failure risk. These checks act as guardrails that flag architectural drift before it becomes a crisis.

```python
class ArchitectureFitness:
    def __init__(self, max_services: int = 20,
                 max_avg_deps: float = 3.0) -> None:
        self._max_svc = max_services
        self._max_deps = max_avg_deps

    def evaluate(self, service_count: int, avg_deps: float) -> list[CheckResult]:
        results: list[CheckResult] = []
        svc_ok = service_count <= self._max_svc
        results.append(CheckResult("architecture", "ARCH-svc-count",
                                   Status.PASS if svc_ok else Status.WARN,
                                   Severity.WARNING,
                                   f"{service_count} services (max {self._max_svc})"))
        dep_ok = avg_deps <= self._max_deps
        results.append(CheckResult("architecture", "ARCH-avg-deps",
                                   Status.PASS if dep_ok else Status.WARN,
                                   Severity.WARNING,
                                   f"Avg deps {avg_deps:.1f} (max {self._max_deps})"))
        return results
```

Fitness functions use WARN rather than FAIL for threshold violations. Exceeding the service count is a smell, not a showstopper. The distinction matters for the overall health score: failures make the platform "UNHEALTHY," warnings make it "AT_RISK."

**Predict:** With 25 services and average 2.0 dependencies, which fitness check passes and which warns?

## Step 6: Compose the Platform Facade

**What to do:** Build the `PlatformReport` (aggregated results with health scoring) and `EnterprisePlatform` (facade that wires all subsystems together).

**Why:** This is the culmination. The `full_assessment()` method runs all subsystem checks in sequence, collects every `CheckResult`, and produces a unified report. The report computes a health score (`passed / total * 100`) and an overall status (HEALTHY / AT_RISK / UNHEALTHY) from the aggregated results.

```python
class EnterprisePlatform:
    def __init__(self) -> None:
        self.tenant_manager = TenantManager()
        self.policies: list[PolicyCheck] = []
        self.change_gate = ChangeGate()
        self.readiness = ReadinessChecker()
        self.fitness = ArchitectureFitness()

    def full_assessment(
        self,
        tenant_context: dict[str, Any],
        service: ServiceConfig,
        change: ChangeRequest | None = None,
        service_count: int = 5,
        avg_deps: float = 2.0,
    ) -> PlatformReport:
        report = PlatformReport()

        # Run each subsystem and collect results
        for policy in self.policies:
            report.results.append(policy.evaluate(tenant_context))
        report.results.extend(self.readiness.evaluate(service))
        report.results.extend(self.fitness.evaluate(service_count, avg_deps))
        if change:
            report.results.append(self.change_gate.evaluate(change))

        return report
```

The facade is thin by design. It does not implement any business logic -- it delegates to subsystems and aggregates results. This means you can add a sixth subsystem (e.g., compliance evidence collection) by adding three lines: store the subsystem, call its evaluate method, and extend the results. No existing code changes.

**Predict:** In the demo, the assessment runs with all context fields present, a fully ready service, and a medium-risk change. How many total check results are produced? (Count: 3 policies + 4 readiness + 2 architecture + 1 change gate = 10.)

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Health score divides by zero | No checks in report | Guard with `if not self.results: return 0.0` |
| Empty context causes all policy failures | Passing `{}` without required fields | Document required context fields; test with empty context |
| Conflating WARN with FAIL in overall status | Not distinguishing "needs attention" from "broken" | UNHEALTHY requires at least one FAIL; AT_RISK requires only WARN |
| Subsystem results are mutable | Using regular dataclass for CheckResult | Use `frozen=True` to prevent post-creation modification |
| Adding a subsystem requires modifying PlatformReport | Hardcoding subsystem names in the report | Group by `result.subsystem` dynamically, not by hardcoded keys |

## Testing Your Solution

```bash
pytest -v
```

Expected output:
```text
passed
```

Test from the command line:

```bash
python project.py
```

You should see JSON output with `overall` status, `health_score`, `total_checks`, `passed`/`failed`/`warnings` counts, and a `subsystems` object grouping results by subsystem name.

## What You Learned

- **The Facade pattern** lets you build a coherent platform from independent subsystems. Each subsystem (policy, readiness, architecture, change gate) is focused and testable in isolation. The facade is the only place they meet, and it is intentionally thin -- just delegation and aggregation.
- **Protocol-based interfaces** enable loose coupling without inheritance. `PolicyCheck` is a Protocol: any class with `check_id()` and `evaluate()` methods qualifies. This means adding a new policy type does not require inheriting from a base class or modifying a registry -- just implement the two methods.
- **Universal result types** (`CheckResult`) are the key to composition at scale. When every subsystem speaks the same language, the platform can aggregate, count, filter, and display results without subsystem-specific logic. This is how real enterprise platforms (AWS Well-Architected, Google SRE dashboards) unify heterogeneous checks into a single view.
