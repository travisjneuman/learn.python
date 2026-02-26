# Level 8 Mini Capstone — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) | [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. This capstone integrates the entire Level 8: KPI dashboards, response profiling, SLA monitoring, fault injection, and graceful degradation. You are building a mini observability platform that monitors simulated services, detects degradation, generates alerts, and produces a unified health report. If you have completed projects 01-14, every subsystem should feel familiar. The challenge is composing them into one coherent platform.

## Thinking Process

Real observability platforms like Datadog, Grafana, and New Relic all solve the same fundamental problem: given N services producing M metrics each, how do you turn that firehose of data into a clear picture of system health? The answer has three parts: collect metrics, evaluate health, and alert when something is wrong.

Your platform monitors five simulated services, each with a different performance profile. The "api-gateway" is fast and reliable. The "payment-service" is slower with higher error rates. The "notification-svc" is the most problematic — high error rates and occasional downtime. By simulating traffic to all five services simultaneously, you produce realistic metric distributions that your platform must aggregate and evaluate.

The architectural pattern here is the Facade. The `ObservabilityPlatform` class provides one unified interface that hides the complexity of metrics collection, health evaluation, and alert generation. Callers just say `record_request()` and `evaluate_alerts()` — they do not need to understand how percentiles are computed or how health thresholds work. This encapsulation is what makes the platform composable: you could add log aggregation or distributed tracing as new subsystems without changing the public interface.

## Step 1: Define the Service Health Model

**What to do:** Create a `ServiceHealth` enum with HEALTHY, DEGRADED, CRITICAL, and DOWN. Create a `ServiceMetrics` dataclass that stores latency samples, error/success counts, and uptime checks, with computed properties for error rate, availability, percentiles, and health status.

**Why:** The `ServiceMetrics` class is the richest data model in this project. Storing raw latency samples (instead of pre-computed averages) lets you compute any statistic after the fact. The `health()` method encodes the operational rules: availability below 95% means DOWN, error rate above 10% or p99 above 1000ms means CRITICAL, and so on.

```python
class ServiceHealth(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    DOWN = "down"

@dataclass
class ServiceMetrics:
    name: str
    latency_ms: list[float] = field(default_factory=list)
    error_count: int = 0
    success_count: int = 0
    uptime_checks: int = 0
    uptime_passes: int = 0

    @property
    def error_rate(self) -> float:
        if self.request_count == 0:
            return 0.0
        return self.error_count / self.request_count

    def health(self) -> ServiceHealth:
        if self.availability < 95:
            return ServiceHealth.DOWN
        if self.error_rate > 0.10 or self.p99_latency > 1000:
            return ServiceHealth.CRITICAL
        if self.error_rate > 0.05 or self.p99_latency > 500:
            return ServiceHealth.DEGRADED
        return ServiceHealth.HEALTHY
```

**Predict:** A service has 100 requests with 6 errors (6% error rate) and p99 latency of 400ms. Is it HEALTHY or DEGRADED? Check both conditions in the `health()` method.

## Step 2: Create the Alert and Report Types

**What to do:** Create an `Alert` dataclass with service name, severity, message, and timestamp. Create a `PlatformReport` dataclass that holds all service metrics, all alerts, and an overall health assessment.

**Why:** Alerts are the system's way of telling operators "something needs attention." The `PlatformReport` is the single-pane-of-glass output: one JSON document that shows every service's health, every triggered alert, and a summary of how many services are in each state. The `to_dict()` methods handle serialization.

```python
@dataclass
class Alert:
    service: str
    severity: str       # "warning", "critical", "page"
    message: str
    timestamp: float = field(default_factory=time.time)

@dataclass
class PlatformReport:
    services: list[ServiceMetrics]
    alerts: list[Alert]
    overall_health: ServiceHealth

    def to_dict(self) -> dict:
        return {
            "overall_health": self.overall_health.value,
            "service_count": len(self.services),
            "alert_count": len(self.alerts),
            "services": [s.to_dict() for s in self.services],
            "alerts": [a.to_dict() for a in self.alerts[:20]],
            "summary": {
                "healthy": sum(1 for s in self.services if s.health() == ServiceHealth.HEALTHY),
                "degraded": sum(1 for s in self.services if s.health() == ServiceHealth.DEGRADED),
                # ... critical, down
            },
        }
```

**Predict:** Why does the report limit alerts to `self.alerts[:20]`? What problem could arise if a noisy service generated thousands of alerts?

## Step 3: Build the ObservabilityPlatform Facade

**What to do:** Create the `ObservabilityPlatform` class that initializes metrics for each registered service, then provides `record_request()` and `record_health_check()` methods to feed data in, and `evaluate_alerts()` and `report()` methods to get insights out.

**Why:** This is the Facade pattern in action. The platform hides all the complexity of metric aggregation, percentile computation, threshold evaluation, and alert generation behind a simple interface. External code calls `record_request("api-gateway", 42.5, True)` and the platform handles everything else internally.

```python
class ObservabilityPlatform:
    def __init__(self, service_names: list[str]) -> None:
        self._metrics = {name: ServiceMetrics(name=name) for name in service_names}
        self._alerts: list[Alert] = []

    def record_request(self, service: str, latency_ms: float, success: bool) -> None:
        metrics = self._metrics.get(service)
        if not metrics:
            return  # silently ignore unregistered services
        metrics.latency_ms.append(latency_ms)
        if success:
            metrics.success_count += 1
        else:
            metrics.error_count += 1

    def record_health_check(self, service: str, passed: bool) -> None:
        metrics = self._metrics.get(service)
        if not metrics:
            return
        metrics.uptime_checks += 1
        if passed:
            metrics.uptime_passes += 1
```

**Predict:** What happens if you call `record_request("unknown-service", 50.0, True)` for a service that was never registered? The code silently ignores it — is this a good design choice, or should it raise an error?

## Step 4: Implement Alert Evaluation

**What to do:** Write `evaluate_alerts()` that checks every service's health and generates alerts for any service that is DEGRADED, CRITICAL, or DOWN. Each alert includes the severity level and a descriptive message with specific metrics.

**Why:** Alert evaluation transforms raw metrics into actionable notifications. The severity mapping (DEGRADED -> "warning", CRITICAL -> "critical", DOWN -> "page") determines the urgency of the response. The message includes specific numbers (error rate, p99 latency, availability percentage) so the on-call engineer knows exactly what is wrong without having to dig through dashboards.

```python
def evaluate_alerts(self) -> list[Alert]:
    new_alerts = []
    for metrics in self._metrics.values():
        health = metrics.health()
        if health == ServiceHealth.CRITICAL:
            alert = Alert(
                service=metrics.name, severity="critical",
                message=f"{metrics.name}: error_rate={metrics.error_rate:.1%}, "
                        f"p99={metrics.p99_latency:.0f}ms",
            )
            new_alerts.append(alert)
            self._alerts.append(alert)
        elif health == ServiceHealth.DEGRADED:
            alert = Alert(
                service=metrics.name, severity="warning",
                message=f"{metrics.name}: degraded performance",
            )
            new_alerts.append(alert)
            self._alerts.append(alert)
        elif health == ServiceHealth.DOWN:
            alert = Alert(
                service=metrics.name, severity="page",
                message=f"{metrics.name}: service DOWN, "
                        f"availability={metrics.availability:.1f}%",
            )
            new_alerts.append(alert)
            self._alerts.append(alert)
    return new_alerts
```

**Predict:** If you call `evaluate_alerts()` twice without clearing the alerts list, what happens? Does the second call add duplicate alerts?

## Step 5: Generate the Unified Report

**What to do:** Write `report()` that collects all service metrics, determines the overall platform health (worst status wins), and returns a `PlatformReport` object.

**Why:** The report is the final output — the "single pane of glass" that shows the state of the entire platform. The overall health follows the same worst-status-wins pattern as the dashboard KPI assembler: if any service is DOWN, the platform is DOWN, regardless of how healthy the other services are.

```python
def report(self) -> PlatformReport:
    services = list(self._metrics.values())
    healths = [s.health() for s in services]

    if ServiceHealth.DOWN in healths:
        overall = ServiceHealth.DOWN
    elif ServiceHealth.CRITICAL in healths:
        overall = ServiceHealth.CRITICAL
    elif ServiceHealth.DEGRADED in healths:
        overall = ServiceHealth.DEGRADED
    else:
        overall = ServiceHealth.HEALTHY

    return PlatformReport(services=services, alerts=self._alerts, overall_health=overall)
```

**Predict:** With five services where four are HEALTHY and one is DEGRADED, what is the overall platform health? Is this the right behavior for a production platform?

## Step 6: Run the Simulation

**What to do:** Write `run_simulation()` that creates the platform, defines service profiles (latency base, error probability, down probability), and generates synthetic traffic using Gaussian-distributed latencies and probability-based errors. After generating traffic, evaluate alerts and produce the report.

**Why:** The simulation proves the entire system works together. Each service has a different profile: the payment service is slow with moderate errors, the notification service has high error rates and occasional downtime. The Gaussian distribution for latency creates realistic variation: most requests cluster around the base latency, with occasional outliers.

```python
def run_simulation(num_requests=200, seed=42):
    rng = random.Random(seed)
    service_profiles = {
        "api-gateway": {"latency_base": 50, "error_prob": 0.02, "down_prob": 0.0},
        "payment-service": {"latency_base": 200, "error_prob": 0.08, "down_prob": 0.01},
        "notification-svc": {"latency_base": 80, "error_prob": 0.15, "down_prob": 0.02},
        # ... more services
    }
    platform = ObservabilityPlatform(list(service_profiles.keys()))

    for _ in range(num_requests):
        for svc_name, profile in service_profiles.items():
            latency = max(1, rng.gauss(profile["latency_base"], profile["latency_base"] * 0.3))
            success = rng.random() > profile["error_prob"]
            platform.record_request(svc_name, latency, success)
            platform.record_health_check(svc_name, rng.random() > profile["down_prob"])

    platform.evaluate_alerts()
    return platform.report().to_dict()
```

**Predict:** The notification service has `error_prob=0.15` (15%) and `down_prob=0.02` (2%). After 200 requests, approximately how many errors would you expect? What health status will it likely have?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Computing percentiles on an empty list | A newly registered service has no latency samples | Check `if not values: return 0.0` before sorting and indexing |
| Using `random.gauss()` without `max()` clamping | Gaussian distribution can produce negative values | Always clamp: `max(1, rng.gauss(base, stddev))` |
| Not distinguishing error rate from availability | Error rate is about request failures; availability is about health check failures | Track them separately with different counters |
| Calling `evaluate_alerts()` multiple times without dedup | Each call appends new alerts even if conditions have not changed | Either clear alerts before re-evaluation, or track which services have already alerted |

## Testing Your Solution

```bash
pytest -q
```

You should see 7+ tests pass. The tests verify service metrics computation, health classification, alert generation, the full simulation, and the report structure.

## What You Learned

- **The Facade pattern** simplifies complex systems by providing a unified interface. The `ObservabilityPlatform` hides metrics aggregation, percentile math, health evaluation, and alert generation behind `record_request()` and `report()`. Callers do not need to understand the internal complexity.
- **The three pillars of observability** are metrics (numbers like latency and error rate), logs (structured event records), and traces (request paths across services). This project focuses on metrics and alerting, which are the foundation for the other two.
- **Statistical summaries at multiple percentiles** (p50, p95, p99) reveal different aspects of system behavior. p50 shows the median experience, p95 shows the near-worst case, and p99 catches extreme outliers. Production dashboards always show multiple percentiles because each tells a different story about user experience.
