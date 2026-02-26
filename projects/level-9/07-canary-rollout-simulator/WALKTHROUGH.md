# Canary Rollout Simulator — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. This project simulates a deployment pattern used by Kubernetes, Argo Rollouts, and AWS CodeDeploy. Spend at least 30 minutes attempting it independently.

## Thinking Process

Imagine you have a web service handling 10,000 requests per minute. You have a new version ready to deploy. Deploying to 100% of traffic at once means if there is a bug, all 10,000 requests per minute hit it simultaneously. A canary deployment instead routes 1% of traffic to the new version first. If that 1% shows elevated error rates or latency, you roll back before 99% of users ever see the problem.

The code models this as a **state machine**. The rollout starts at `NOT_STARTED`, progresses through `CANARY` (small percentage) and `PROGRESSIVE` (larger percentages), and ends at either `COMPLETED` (metrics stayed healthy) or `ROLLED_BACK` (metrics degraded). Each stage has a traffic percentage and an error threshold -- the maximum acceptable difference between canary and baseline error rates.

The key design decision is **deterministic simulation via seeded randomness**. By passing a `random.Random(seed)` instance, the same seed always produces the same canary metrics, making the simulation reproducible for testing. This is the same technique used in game development, scientific computing, and fuzz testing.

## Step 1: Define the Domain Types

**What to do:** Create enums for rollout phases, dataclasses for rollout stages and metric snapshots, and a result dataclass for the final outcome.

**Why:** The `RolloutPhase` enum defines every possible state the deployment can be in. `RolloutStage` captures the configuration for each progressive step. `MetricSnapshot` records what was observed during each stage. These types are the vocabulary of the simulator -- they make the code self-documenting.

```python
class RolloutPhase(Enum):
    NOT_STARTED = "not_started"
    CANARY = "canary"
    PROGRESSIVE = "progressive"
    FULL = "full"
    ROLLED_BACK = "rolled_back"
    COMPLETED = "completed"


@dataclass
class RolloutStage:
    name: str
    traffic_pct: float       # % of traffic going to canary
    duration_steps: int      # number of evaluation steps
    error_threshold: float   # max allowed error rate delta vs baseline


@dataclass
class MetricSnapshot:
    stage_name: str
    canary_error_rate: float
    baseline_error_rate: float
    canary_latency_ms: float
    baseline_latency_ms: float
    traffic_pct: float

    @property
    def error_rate_delta(self) -> float:
        return self.canary_error_rate - self.baseline_error_rate
```

Two details to notice:

- **`error_threshold` is a delta, not an absolute rate.** A baseline error rate of 1% is normal. The question is whether the canary's error rate is significantly _higher_ than the baseline. A delta of 0.02 means "tolerate up to 2 percentage points more errors than baseline."
- **`MetricSnapshot` uses properties** to compute derived values (`error_rate_delta`, `latency_delta_ms`). The raw metrics are stored; the comparisons are computed on demand.

**Predict:** If the baseline error rate is 0.01 (1%) and the canary error rate is 0.025 (2.5%), what is the `error_rate_delta`? Would a threshold of 0.02 trigger a rollback?

## Step 2: Define the Default Rollout Strategy

**What to do:** Write a `default_stages()` function that returns the standard five-stage canary rollout: 1% -> 5% -> 25% -> 50% -> 100%.

**Why:** Progressive traffic increases are the core safety mechanism. At 1%, a bug affects 1 in 100 users. If metrics look good, you increase to 5%, then 25%, and so on. Each stage has a tighter error threshold as traffic increases -- you tolerate more variance at 1% (small sample size) than at 50% (statistically significant).

```python
def default_stages() -> list[RolloutStage]:
    return [
        RolloutStage("canary-1pct",        1,   5, 0.02),
        RolloutStage("canary-5pct",        5,   5, 0.015),
        RolloutStage("progressive-25pct",  25,  5, 0.01),
        RolloutStage("progressive-50pct",  50,  5, 0.01),
        RolloutStage("full-100pct",        100, 3, 0.005),
    ]
```

Notice the thresholds get stricter as traffic increases: 0.02 at 1%, 0.015 at 5%, 0.01 at 25-50%, 0.005 at 100%. This reflects the reality that at higher traffic percentages, you have more data and tighter confidence, so smaller deviations are more meaningful.

**Predict:** Why does the last stage (100%) have only 3 evaluation steps while the others have 5? What would happen if you set all thresholds to 0.0?

## Step 3: Build the Canary Rollout Engine

**What to do:** Create the `CanaryRollout` class with an `execute()` method that simulates the full rollout, checking metrics at each stage and either promoting or rolling back.

**Why:** This is the state machine. The `execute()` method iterates through stages, generates simulated metrics at each one, and compares them against thresholds. If any stage exceeds its error or latency threshold, the rollout immediately stops and enters the `ROLLED_BACK` state. Otherwise, it progresses to `COMPLETED`.

```python
class CanaryRollout:
    def __init__(
        self,
        stages: list[RolloutStage],
        latency_threshold_ms: float = 50.0,
    ) -> None:
        self._stages = stages
        self._latency_threshold = latency_threshold_ms
        self._phase = RolloutPhase.NOT_STARTED
        self._snapshots: list[MetricSnapshot] = []
        self._stages_completed = 0

    def execute(
        self,
        baseline_error_rate: float,
        baseline_latency_ms: float,
        canary_error_fn=None,
        canary_latency_fn=None,
        rng: random.Random | None = None,
    ) -> RolloutResult:
        if rng is None:
            rng = random.Random()

        self._phase = RolloutPhase.CANARY

        for i, stage in enumerate(self._stages):
            # Simulate canary metrics
            if canary_error_fn:
                canary_err = canary_error_fn(stage, rng)
            else:
                canary_err = baseline_error_rate + rng.gauss(0, 0.005)

            # ... build snapshot, check rollback conditions ...

            if snapshot.error_rate_delta > stage.error_threshold:
                self._phase = RolloutPhase.ROLLED_BACK
                return RolloutResult(phase=self._phase, ...)

        self._phase = RolloutPhase.COMPLETED
        return RolloutResult(phase=self._phase, ...)
```

Three critical design decisions:

- **`rng.gauss(0, 0.005)` simulates noise.** Real metrics fluctuate. The Gaussian distribution with mean 0 and standard deviation 0.005 means most simulated canary metrics are close to baseline, with occasional larger deviations.
- **`max(0, canary_err)` prevents negative error rates.** The Gaussian noise can produce negative values, but a negative error rate is physically impossible.
- **Callback functions (`canary_error_fn`, `canary_latency_fn`) enable testing.** Tests can inject deterministic "bad" metrics to verify that rollback triggers correctly, without relying on random chance.

**Predict:** With `rng = random.Random(42)`, will two separate calls to `execute()` produce the same result? Why is this important for testing?

## Step 4: Implement Rollback Detection

**What to do:** Add the two rollback checks inside the stage loop: one for error rate delta exceeding the threshold, one for latency delta exceeding the global latency threshold.

**Why:** These are the safety gates. In real canary deployments, the system continuously monitors metrics and automatically rolls back if degradation is detected. The error threshold is per-stage (stricter at higher traffic), while the latency threshold is global (a 50ms spike is bad regardless of traffic percentage).

```python
# Inside the stage loop:
snapshot = MetricSnapshot(
    stage_name=stage.name,
    canary_error_rate=max(0, canary_err),
    baseline_error_rate=baseline_error_rate,
    canary_latency_ms=max(0, canary_lat),
    baseline_latency_ms=baseline_latency_ms,
    traffic_pct=stage.traffic_pct,
)
self._snapshots.append(snapshot)

# Check rollback: error rate
if snapshot.error_rate_delta > stage.error_threshold:
    self._phase = RolloutPhase.ROLLED_BACK
    return RolloutResult(
        phase=self._phase,
        stages_completed=i,
        total_stages=len(self._stages),
        rollback_reason=f"Error rate delta {snapshot.error_rate_delta:.4f} "
                        f"exceeds threshold {stage.error_threshold}",
        snapshots=self._snapshots,
    )

# Check rollback: latency
if snapshot.latency_delta_ms > self._latency_threshold:
    self._phase = RolloutPhase.ROLLED_BACK
    return RolloutResult(...)
```

The `rollback_reason` string is descriptive because in production, operators need to know _why_ a rollback happened. "Error rate delta 0.0312 exceeds threshold 0.02" is actionable. "Rollback triggered" is not.

**Predict:** If both the error rate _and_ latency thresholds are exceeded on the same stage, which rollback reason gets reported? Why?

## Step 5: Wire Up the Demo and CLI

**What to do:** Create `run_demo()` that runs the simulation with seed 42 and prints the result as JSON. Add argparse for `--seed`.

**Why:** The seeded demo ensures anyone running `python project.py --demo` gets the same output, making it easy to verify the solution matches expected behavior. The JSON output is structured for both human reading and programmatic consumption.

```python
def run_demo() -> dict[str, Any]:
    stages = default_stages()
    rollout = CanaryRollout(stages, latency_threshold_ms=50)
    result = rollout.execute(
        baseline_error_rate=0.01,
        baseline_latency_ms=100,
        rng=random.Random(42),
    )
    return result.to_dict()
```

The demo uses realistic parameters: 1% baseline error rate and 100ms baseline latency. These are typical for a production web service.

**Predict:** With seed 42, does the demo rollout complete successfully or get rolled back? Run it to find out.

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Using `random.random()` instead of a seeded `Random` instance | Global random state makes tests non-deterministic | Always pass `rng=random.Random(seed)` for reproducible simulations |
| Forgetting `max(0, canary_err)` | Gaussian noise can produce negative values | Clamp simulated metrics to physical bounds |
| Error threshold as absolute rate, not delta | Confusing "2% error rate" with "2% more than baseline" | Threshold compares `canary_error_rate - baseline_error_rate` |
| Not recording snapshots before rollback | Returning early without appending the failing snapshot | Append the snapshot _before_ checking rollback conditions |
| Non-increasing traffic percentages | Defining stages as [50%, 25%, 100%] | Validate that traffic percentages strictly increase across stages |

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
python project.py --seed 42
```

You should see JSON output showing either a completed rollout with all stages passed, or a rollback with the specific reason and stage where it failed.

## What You Learned

- **Canary deployments** reduce risk by gradually routing traffic to new code and comparing metrics against the stable baseline. This is fundamentally safer than deploying to 100% at once because you detect problems before they affect most users.
- **State machines** model complex workflows with well-defined transitions. The rollout can only be in one phase at a time, and transitions follow rules (you cannot go from COMPLETED back to CANARY).
- **Deterministic simulation via seeded randomness** makes complex systems testable. By controlling the random number generator, you get reproducible results that can be asserted against in tests, while still modeling realistic metric variability.
