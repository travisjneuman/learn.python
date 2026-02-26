# Fault Injection Harness — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) | [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. The goal is to build a configurable fault injection framework that can introduce exceptions, delays, and data corruption into function calls, controlled by probability. If you can write a decorator that sometimes raises an exception before calling the wrapped function, you have the core idea.

## Thinking Process

Most bugs hide in error-handling code. The happy path gets tested every day by normal usage. But the code that runs when the database is down, when the API returns garbage, or when a network timeout strikes? That code might run once a year in production — and when it does, it is the most critical moment possible. Chaos engineering flips this by deliberately injecting failures so your error-handling paths get exercised regularly.

The design has three layers. At the bottom, `FaultConfig` dataclasses define what kind of fault to inject, how often (probability), and which functions to target. In the middle, the `FaultInjector` engine checks rules on every intercepted call and decides whether to trigger a fault based on the configured probability. At the top, two entry points let you apply injection: the `@inject` decorator for permanent wrapping, and the `scope()` context manager for temporary rules during testing.

The probability-based approach is what makes this realistic rather than just a test tool. Setting probability to 0.3 means roughly 30% of calls will fail, simulating the kind of intermittent failures that are hardest to debug in production. A deterministic "fail every time" mode would be too simple — real failures are stochastic, and your code needs to handle them gracefully.

## Step 1: Define the Domain Types

**What to do:** Create a `FaultType` enum with EXCEPTION, DELAY, CORRUPTION, and TIMEOUT. Create a `FaultConfig` dataclass with fields for name, fault type, probability (0.0 to 1.0), target function, and type-specific settings. Add `__post_init__` validation to ensure probability is valid. Create `FaultEvent` and `HarnessStats` dataclasses for tracking what happened.

**Why:** The enum constrains fault types to known values — you cannot accidentally specify "exeption" (typo). The `FaultConfig` dataclass is the rule definition: it says "when function X is called, inject fault type Y with probability Z." Validation in `__post_init__` catches configuration errors at creation time rather than at runtime.

```python
class FaultType(Enum):
    EXCEPTION = "exception"
    DELAY = "delay"
    CORRUPTION = "corruption"
    TIMEOUT = "timeout"

@dataclass
class FaultConfig:
    name: str
    fault_type: FaultType
    probability: float  # 0.0 to 1.0
    target_function: str = "*"  # "*" matches all functions
    delay_seconds: float = 1.0
    exception_class: str = "RuntimeError"
    exception_message: str = "Injected fault"
    enabled: bool = True

    def __post_init__(self) -> None:
        if not 0.0 <= self.probability <= 1.0:
            raise ValueError(f"Probability must be 0.0-1.0, got {self.probability}")
```

**Predict:** What happens if you create `FaultConfig(name="test", fault_type=FaultType.DELAY, probability=1.5)`? At what point does the error occur — when you construct the object, or when you use it?

## Step 2: Build the FaultInjector Engine

**What to do:** Create the `FaultInjector` class with a list of rules, a stats tracker, and a seeded `random.Random` instance. Add methods to `add_rule()`, `remove_rule()`, `enable()`, and `disable()` the injector globally.

**Why:** The seeded RNG is crucial for reproducibility. In testing, you need deterministic behavior: seed 42 should always trigger the same faults on the same calls. In production chaos experiments, you want randomness. The `_active` flag provides a global kill switch.

```python
class FaultInjector:
    def __init__(self, seed: int | None = None) -> None:
        self._rules: list[FaultConfig] = []
        self._stats = HarnessStats()
        self._rng = random.Random(seed)
        self._active = True

    def add_rule(self, config: FaultConfig) -> None:
        self._rules.append(config)

    def remove_rule(self, name: str) -> bool:
        before = len(self._rules)
        self._rules = [r for r in self._rules if r.name != name]
        return len(self._rules) < before
```

**Predict:** Why use `random.Random(seed)` (an instance) instead of calling `random.seed(seed)` and using the module-level functions? What problem could the module-level approach cause if multiple parts of your code use random numbers?

## Step 3: Implement the Injection Logic

**What to do:** Write `_matching_rules()` to find rules that apply to a given function name, `_should_trigger()` to decide based on probability, and `_apply_fault()` to execute the fault (raise an exception, sleep for a delay, or both for timeouts).

**Why:** This is the decision engine. On every intercepted call, it finds matching rules, rolls the dice for each one, and applies the first triggered fault. The matching logic supports both wildcard (`"*"`) and specific function names, giving you fine-grained control.

```python
def _matching_rules(self, func_name: str) -> list[FaultConfig]:
    return [
        r for r in self._rules
        if r.enabled and (r.target_function == "*" or r.target_function == func_name)
    ]

def _should_trigger(self, probability: float) -> bool:
    return self._rng.random() < probability

def _apply_fault(self, rule: FaultConfig, func_name: str) -> None:
    event = FaultEvent(fault_name=rule.name, fault_type=rule.fault_type, target=func_name)
    self._stats.events.append(event)
    self._stats.faults_triggered += 1

    if rule.fault_type == FaultType.EXCEPTION:
        raise RuntimeError(f"[FAULT:{rule.name}] {rule.exception_message}")
    elif rule.fault_type == FaultType.DELAY:
        time.sleep(rule.delay_seconds)
    elif rule.fault_type == FaultType.TIMEOUT:
        time.sleep(rule.delay_seconds)
        raise TimeoutError(f"[FAULT:{rule.name}] Operation timed out")
```

**Predict:** If a function has two matching rules — one with probability 0.5 and one with probability 1.0 — and the first one does not trigger, will the second one always trigger? Look at the `check_and_inject` method to verify.

## Step 4: Create the Decorator and Context Manager

**What to do:** Write an `inject()` method that returns a decorator wrapping any function with fault injection. Write a `scope()` context manager that temporarily adds rules for the duration of a `with` block, then removes them automatically.

**Why:** The decorator is for permanent injection on functions you always want to test (like API calls). The context manager is for temporary injection during specific test scenarios. The `scope()` uses `try/finally` to guarantee cleanup even if an exception occurs inside the block.

```python
def inject(self, func: Callable) -> Callable:
    """Decorator that applies fault injection to a function."""
    def wrapper(*args, **kwargs):
        self.check_and_inject(func.__name__)
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
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
```

**Predict:** Why does the `scope()` context manager put `self.remove_rule()` inside a `finally` block? What would happen if a fault triggered an exception inside the `with` block and there was no `finally`?

## Step 5: Write the Data Corruption Helper

**What to do:** Write `corrupt_data()` that takes a dictionary and randomly mutates its values: reverse strings, negate numbers, flip booleans.

**Why:** Data corruption tests whether your validation and error-handling code catches bad data. The corruption is deterministic when you pass a seeded RNG, making tests reproducible. The `isinstance(value, bool)` check before `isinstance(value, (int, float))` is critical because in Python, `bool` is a subclass of `int`.

```python
def corrupt_data(data: dict, corruption_rate: float = 0.3, rng=None) -> dict:
    if rng is None:
        rng = random.Random()
    corrupted = dict(data)
    for key in list(corrupted.keys()):
        if rng.random() < corruption_rate:
            value = corrupted[key]
            if isinstance(value, bool):
                corrupted[key] = not value
            elif isinstance(value, str):
                corrupted[key] = value[::-1]  # reverse
            elif isinstance(value, (int, float)):
                corrupted[key] = -value  # negate
            elif value is None:
                corrupted[key] = "CORRUPTED"
    return corrupted
```

**Predict:** Why must `isinstance(value, bool)` come BEFORE `isinstance(value, (int, float))`? What would happen if you checked `int` first? (Hint: try `isinstance(True, int)` in a Python shell.)

## Step 6: Run the Demo

**What to do:** Write `run_demo()` that creates an injector with seed 42, adds fault rules for API errors (30% probability) and database delays (20% probability), decorates two functions, calls them in a loop, and reports the stats. Include a corruption demo.

**Why:** The demo shows the full system working end-to-end. With seed 42, the same calls trigger the same faults every time, so you can predict and verify the output. The loop of 20 iterations per function gives enough calls to see the probability distribution emerge.

```python
def run_demo() -> dict:
    injector = FaultInjector(seed=42)

    injector.add_rule(FaultConfig(
        name="api-error", fault_type=FaultType.EXCEPTION,
        probability=0.3, target_function="call_api",
    ))
    injector.add_rule(FaultConfig(
        name="db-delay", fault_type=FaultType.DELAY,
        probability=0.2, target_function="query_db", delay_seconds=0.01,
    ))

    @injector.inject
    def call_api(endpoint: str) -> dict:
        return {"status": 200, "endpoint": endpoint}

    @injector.inject
    def query_db(query: str) -> list:
        return [{"id": 1, "data": query}]

    results = []
    for i in range(20):
        try:
            call_api(f"/endpoint/{i}")
            results.append({"call": i, "type": "api", "success": True})
        except RuntimeError:
            results.append({"call": i, "type": "api", "success": False})
    # ... similar loop for query_db
```

**Predict:** With 20 API calls at 30% fault probability and 20 DB calls at 20% probability, roughly how many faults would you expect in total? (Expected: about 6 API faults + 4 DB faults = 10 total, though randomness means actual counts will vary.)

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Checking `isinstance(value, int)` before `isinstance(value, bool)` | It seems logical to check the more general type first | In Python, `bool` is a subclass of `int`, so `True` passes the `int` check. Always check `bool` first |
| Not using `try/finally` in the scope context manager | The cleanup code is only needed "on the way out" | Without `finally`, rules leak if an exception occurs inside the `with` block |
| Using `random.random()` (module-level) instead of `self._rng.random()` | Force of habit from simpler scripts | Module-level random state is global and shared. Instance-level RNG is isolated and seedable |
| Not preserving function metadata in the decorator | The wrapper function replaces `__name__`, `__doc__`, etc. | Use `functools.wraps(func)` or manually copy `__name__` as the code does |

## Testing Your Solution

```bash
pytest -q
```

You should see 7+ tests pass. The tests verify fault configuration validation, probability-based triggering, decorator behavior, scope cleanup, corruption logic, and the full demo output.

## What You Learned

- **Chaos engineering** is the practice of deliberately injecting failures to find weaknesses before they cause real outages. Netflix's Chaos Monkey randomly terminates production instances; your harness does the same at the function level.
- **Probability-based injection** creates realistic failure scenarios. Real systems do not fail 100% of the time — they fail intermittently, which is harder to handle and debug. Testing at 30% failure rate reveals whether your retry logic, circuit breakers, and fallbacks actually work.
- **Decorators and context managers** are powerful composition tools. The `@inject` decorator permanently wraps a function with fault injection. The `scope()` context manager temporarily adds rules and guarantees cleanup. Together, they provide both permanent and temporary injection without modifying the target functions.
