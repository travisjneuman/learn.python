# Dashboard KPI Assembler — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) | [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. The goal is to aggregate metric samples from multiple sources, compute statistical summaries (mean, percentile, min, max), evaluate each KPI against thresholds to assign a traffic-light status, and detect trends. If you can group numbers by category, compute their average, and compare against a threshold, you have the foundation.

## Thinking Process

Every operations team has a dashboard — a screen that shows whether the system is healthy at a glance. Green means good, yellow means watch it, red means something is wrong. Behind that dashboard is exactly the kind of code you are building here.

The first challenge is aggregation. Metrics arrive as individual readings: "at 10:05, latency was 42ms, at 10:06 it was 38ms, at 10:07 it was 250ms." You need to summarize these into useful statistics. The mean (average) tells you the typical experience. The 95th percentile (p95) tells you the worst experience for all but the top 5% of requests. These two numbers together paint a much richer picture than either alone — a system with mean latency of 50ms but p95 of 2000ms has a serious tail latency problem.

The second challenge is threshold evaluation. Raw numbers are meaningless without context. Is 200ms good or bad? It depends on the KPI. For a homepage load time, 200ms is excellent. For a database health check, it is terrible. The `KPIDefinition` class carries the thresholds that give meaning to the numbers. The third challenge is trend detection: are things getting better or worse over time? This requires comparing the first half of the sample window to the second half.

## Step 1: Define the Domain Types

**What to do:** Create an enum `KPIStatus` with values GREEN, YELLOW, RED. Create dataclasses for `KPIDefinition` (the blueprint: name, unit, thresholds), `MetricSample` (a single reading), `KPISummary` (the aggregated result), and `Dashboard` (the top-level container).

**Why:** These types form a layered domain model. `KPIDefinition` says what to measure and what the thresholds are. `MetricSample` is a raw data point. `KPISummary` is the computed result. `Dashboard` ties them all together. Using an enum for status ensures you only ever produce one of three valid values.

```python
class KPIStatus(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"

@dataclass
class KPIDefinition:
    name: str
    unit: str
    green_threshold: float   # values <= this are green
    yellow_threshold: float  # values <= this (but > green) are yellow; above is red

    def evaluate(self, value: float) -> KPIStatus:
        if value <= self.green_threshold:
            return KPIStatus.GREEN
        if value <= self.yellow_threshold:
            return KPIStatus.YELLOW
        return KPIStatus.RED
```

**Predict:** If a KPI has `green_threshold=100` and `yellow_threshold=200`, what status does a value of 100 get? What about 101? What about 201?

## Step 2: Write the Statistical Helpers

**What to do:** Write a `percentile()` function that computes the nth percentile using the nearest-rank method, and a `compute_trend()` function that splits values into first-half and second-half, compares their means, and classifies the change as improving, stable, or degrading.

**Why:** These are the mathematical tools that turn raw samples into actionable insights. The p95 value answers "what latency do 95% of requests experience?" which is more useful than the mean for catching tail latency issues. Trend detection answers "is this getting better or worse?" which tells operators whether to act now or just monitor.

```python
def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    sorted_v = sorted(values)
    rank = math.ceil(pct / 100.0 * len(sorted_v)) - 1
    return sorted_v[max(0, rank)]

def compute_trend(values: list[float]) -> str:
    if len(values) < 4:
        return "stable"
    mid = len(values) // 2
    first_mean = sum(values[:mid]) / mid
    second_mean = sum(values[mid:]) / (len(values) - mid)
    if first_mean == 0:
        return "stable"
    change_pct = (second_mean - first_mean) / abs(first_mean) * 100
    if change_pct < -10:
        return "improving"
    if change_pct > 10:
        return "degrading"
    return "stable"
```

**Predict:** Why does `compute_trend()` require at least 4 values before computing a trend? What would happen with only 2 values split into halves of 1 each?

## Step 3: Load and Parse Input Data

**What to do:** Write `load_kpi_definitions()` and `load_metric_samples()` that parse raw dictionaries from JSON into typed dataclass instances.

**Why:** Parsing happens once at the boundary between external data (JSON) and internal logic. After this step, everything works with typed objects, which means your IDE can autocomplete field names, catch typos, and your code is self-documenting.

```python
def load_kpi_definitions(raw: list[dict]) -> list[KPIDefinition]:
    return [
        KPIDefinition(
            name=d["name"], unit=d.get("unit", ""),
            green_threshold=float(d["green_threshold"]),
            yellow_threshold=float(d["yellow_threshold"]),
        )
        for d in raw
    ]

def load_metric_samples(raw: list[dict]) -> list[MetricSample]:
    return [
        MetricSample(
            source=s["source"], kpi_name=s["kpi_name"],
            timestamp=s.get("timestamp", ""), value=float(s["value"]),
        )
        for s in raw
    ]
```

**Predict:** Why call `float(d["green_threshold"])` instead of just using `d["green_threshold"]` directly? What could go wrong if the JSON contains the string `"100"` instead of the number `100`?

## Step 4: Aggregate a Single KPI

**What to do:** Write `aggregate_kpi()` that filters all samples for a specific KPI name, computes the statistics (mean, p95, min, max), evaluates the status against thresholds, and detects the trend.

**Why:** This is the core transformation: from a list of raw samples to a single summary with meaning. The function filters by KPI name first, then computes everything on the filtered subset. This means you can have thousands of samples across many KPIs and each one gets its own independent summary.

```python
def aggregate_kpi(definition: KPIDefinition, samples: list[MetricSample]) -> KPISummary:
    values = [s.value for s in samples if s.kpi_name == definition.name]
    if not values:
        return KPISummary(
            name=definition.name, unit=definition.unit,
            sample_count=0, mean=0.0, p95=0.0,
            minimum=0.0, maximum=0.0,
            status=KPIStatus.GREEN, trend="stable",
        )
    mean_val = sum(values) / len(values)
    return KPISummary(
        name=definition.name, unit=definition.unit,
        sample_count=len(values),
        mean=round(mean_val, 2),
        p95=round(percentile(values, 95), 2),
        minimum=round(min(values), 2),
        maximum=round(max(values), 2),
        status=definition.evaluate(mean_val),
        trend=compute_trend(values),
    )
```

**Predict:** The status is evaluated on the `mean_val`. Could a KPI be GREEN by mean but still have dangerously high individual readings? When would you want to evaluate status on p95 instead?

## Step 5: Assemble the Dashboard

**What to do:** Write `assemble_dashboard()` that iterates over all KPI definitions, aggregates each one, counts the status colors, and determines the overall health. The overall health is "critical" if any KPI is red, "warning" if any is yellow, and "healthy" otherwise.

**Why:** The dashboard provides the single-pane-of-glass view that operators need. The overall health follows the "worst status wins" pattern: if even one KPI is red, the entire dashboard is critical. This ensures red KPIs cannot hide behind a sea of green ones.

```python
def assemble_dashboard(title, definitions, samples) -> Dashboard:
    dashboard = Dashboard(title=title)
    for defn in definitions:
        summary = aggregate_kpi(defn, samples)
        dashboard.kpis.append(summary)
        if summary.status == KPIStatus.RED:
            dashboard.red_count += 1
        elif summary.status == KPIStatus.YELLOW:
            dashboard.yellow_count += 1
        else:
            dashboard.green_count += 1

    if dashboard.red_count > 0:
        dashboard.overall_health = "critical"
    elif dashboard.yellow_count > 0:
        dashboard.overall_health = "warning"
    else:
        dashboard.overall_health = "healthy"
    return dashboard
```

**Predict:** If you have 10 KPIs, 9 are green, and 1 is yellow, what is the overall health? Would an operator want to be paged for this situation, or just notified?

## Step 6: Serialize and Output

**What to do:** Write `dashboard_to_dict()` that converts the `Dashboard` dataclass into a plain dictionary suitable for JSON serialization. Wire up the CLI to load input, assemble the dashboard, and write the output.

**Why:** Dataclasses are great for internal logic, but JSON output requires plain dicts. The serialization function handles the conversion, including turning enums into their string values. This separation means you can change the internal representation without affecting the output format.

```python
def dashboard_to_dict(dashboard: Dashboard) -> dict:
    return {
        "title": dashboard.title,
        "overall_health": dashboard.overall_health,
        "counts": {"red": dashboard.red_count, "yellow": dashboard.yellow_count, "green": dashboard.green_count},
        "kpis": [
            {"name": k.name, "unit": k.unit, "sample_count": k.sample_count,
             "mean": k.mean, "p95": k.p95, "min": k.minimum, "max": k.maximum,
             "status": k.status.value, "trend": k.trend}
            for k in dashboard.kpis
        ],
    }
```

**Predict:** Why does the serialization use `k.status.value` (the string "green") instead of `k.status` (the enum `KPIStatus.GREEN`)? What error would you get if you tried to JSON-serialize an enum directly?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Evaluating status on a single sample instead of the aggregate | It seems more precise, but individual readings are noisy | Evaluate on the mean (or p95) to smooth out outliers |
| Not handling empty sample lists | Edge case when a KPI has no matching samples | Return a default KPISummary with zeros and GREEN status |
| Treating trend detection as reliable with few data points | With 2-3 samples, "trend" is just noise | Require a minimum of 4 samples before computing trends |
| Serializing enums directly to JSON | `json.dumps()` does not know how to serialize `Enum` objects | Always use `.value` to get the string representation |

## Testing Your Solution

```bash
pytest -q
```

You should see 7+ tests pass. The tests verify threshold evaluation, statistical computations, trend detection, the full assembly pipeline, and JSON serialization.

## What You Learned

- **Percentile-based metrics** (especially p95 and p99) reveal performance problems that averages hide. A mean latency of 50ms with a p95 of 2000ms means 5% of your users are having a terrible experience, but the average looks fine.
- **Threshold-driven alerting** with traffic-light status turns raw numbers into actionable signals. The key design decision is where to set the thresholds and which statistic to evaluate against (mean vs. p95 vs. max).
- **Trend detection** answers the question "is this getting worse?" which is often more useful than "is this bad right now?" A KPI that is currently green but degrading rapidly deserves attention before it turns yellow.
