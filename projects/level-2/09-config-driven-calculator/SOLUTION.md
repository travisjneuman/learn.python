# Config Driven Calculator — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Config Driven Calculator — complete annotated solution."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


# WHY: Default operations ensure the calculator works even without a config file.
# This is the "sensible defaults" pattern — the tool is useful out of the box,
# but customizable when needed.
DEFAULT_OPERATIONS: dict[str, dict] = {
    "add": {"symbol": "+", "description": "Addition"},
    "subtract": {"symbol": "-", "description": "Subtraction"},
    "multiply": {"symbol": "*", "description": "Multiplication"},
    "divide": {"symbol": "/", "description": "Division"},
    "power": {"symbol": "**", "description": "Exponentiation"},
    "modulo": {"symbol": "%", "description": "Modulo (remainder)"},
}


def load_config(path: Path) -> dict:
    """Load calculator configuration from a JSON file."""
    if not path.exists():
        # WHY: Returning defaults instead of crashing means the calculator
        # works without a config file. This is defensive programming.
        return {"operations": DEFAULT_OPERATIONS, "settings": {}}

    try:
        raw = path.read_text(encoding="utf-8")
        config = json.loads(raw)
    except (json.JSONDecodeError, OSError) as exc:
        # WHY: Bad config should not crash the program. Return defaults
        # plus an error message so the user knows their config was ignored.
        return {
            "operations": DEFAULT_OPERATIONS,
            "settings": {},
            "config_error": str(exc),
        }

    # WHY: setdefault fills in missing keys without overwriting existing ones.
    # This means a config file only needs to specify what it wants to change.
    config.setdefault("operations", DEFAULT_OPERATIONS)
    config.setdefault("settings", {})
    return config


def calculate(operation: str, a: float, b: float) -> dict:
    """Perform a calculation and return a result dict."""
    try:
        # WHY: The if/elif chain dispatches to the correct operation.
        # This is a simple form of the Strategy pattern — the operation
        # name selects the behavior at runtime.
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                return {"success": False, "error": "Division by zero"}
            result = a / b
        elif operation == "power":
            result = a ** b
        elif operation == "modulo":
            if b == 0:
                return {"success": False, "error": "Modulo by zero"}
            result = a % b
        elif operation == "sqrt":
            if a < 0:
                return {"success": False, "error": "Cannot sqrt negative number"}
            result = math.sqrt(a)
        else:
            return {"success": False, "error": f"Unknown operation: {operation}"}

        # WHY: Check for infinity/NaN after calculation. Operations like
        # 10**1000 can produce infinity, and 0.0/0.0 produces NaN. These
        # are technically valid floats but usually indicate a problem.
        if math.isinf(result) or math.isnan(result):
            return {"success": False, "error": "Result is infinity or NaN"}

        return {
            "success": True,
            "operation": operation,
            "a": a,
            "b": b,
            "result": round(result, 10),
        }

    except (OverflowError, ValueError) as exc:
        return {"success": False, "error": str(exc)}


def batch_calculate(operations_list: list[dict]) -> list[dict]:
    """Run a batch of calculations from a list of operation dicts."""
    results = []
    for idx, op in enumerate(operations_list):
        try:
            name = op["operation"]
            # WHY: .get with default 0 makes the second operand optional,
            # which is needed for unary operations like sqrt.
            a = float(op.get("a", 0))
            b = float(op.get("b", 0))
            result = calculate(name, a, b)
            result["index"] = idx
            results.append(result)
        except (KeyError, ValueError, TypeError) as exc:
            # WHY: Wrapping each operation in try/except means one bad entry
            # does not abort the entire batch.
            results.append({
                "index": idx,
                "success": False,
                "error": f"Invalid operation spec: {exc}",
            })
    return results


def list_operations(config: dict) -> list[dict]:
    """List all available operations from config, sorted by name."""
    ops = config.get("operations", DEFAULT_OPERATIONS)
    # WHY: Using {**info} to unpack the operation metadata and adding "name"
    # creates a flat, self-contained info dict for each operation.
    return sorted(
        [{"name": name, **info} for name, info in ops.items()],
        key=lambda op: op["name"],
    )


def calculate_chain(operations: list[tuple[str, float]], start: float = 0) -> dict:
    """Chain operations together, feeding each result into the next.

    Example: start=10, [("add", 5), ("multiply", 2)] -> (10+5)*2 = 30
    """
    current = start
    steps: list[dict] = []

    for op_name, operand in operations:
        result = calculate(op_name, current, operand)
        if not result["success"]:
            # WHY: Stop the chain on first failure. The remaining steps
            # would use a bad value and produce meaningless results.
            return {
                "success": False,
                "error": f"Chain failed at step: {result['error']}",
                "steps": steps,
            }
        steps.append({
            "operation": op_name,
            "input": current,
            "operand": operand,
            "output": result["result"],
        })
        current = result["result"]

    return {"success": True, "final": current, "steps": steps}


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Config-driven calculator")
    parser.add_argument(
        "--config", default="data/sample_input.txt",
        help="Path to JSON config file",
    )
    parser.add_argument("--op", help="Operation to perform")
    parser.add_argument("--a", type=float, help="First operand")
    parser.add_argument("--b", type=float, default=0, help="Second operand")
    parser.add_argument("--list", action="store_true", help="List available operations")
    parser.add_argument("--batch", help="Path to JSON file with batch operations")
    return parser.parse_args()


def main() -> None:
    """Entry point: load config, run calculation or list operations."""
    args = parse_args()
    config = load_config(Path(args.config))

    if args.list:
        ops = list_operations(config)
        print("Available operations:")
        for op in ops:
            print(f"  {op['name']}: {op.get('description', 'No description')}")
        return

    if args.batch:
        batch_path = Path(args.batch)
        batch_data = json.loads(batch_path.read_text(encoding="utf-8"))
        results = batch_calculate(batch_data)
        print(json.dumps(results, indent=2))
        return

    if args.op and args.a is not None:
        result = calculate(args.op, args.a, args.b)
        print(json.dumps(result, indent=2))
        return

    print("Calculator config loaded. Use --list to see operations.")
    print(f"Operations available: {len(config.get('operations', {}))}")


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Config-driven operations | Adding a new operation (like `sqrt`) requires editing only the config and one `elif` branch, not restructuring the whole program. This separates "what operations exist" (data) from "how to compute them" (code). |
| `setdefault` for config merging | Fills in missing keys without overwriting user-provided values. A config file that only defines `"settings"` still gets all default operations. |
| Fallback to defaults on bad config | A corrupted or missing config file should degrade gracefully (use defaults) rather than crash. The `config_error` key in the return dict lets callers detect and log the problem. |
| Operation chaining | Chaining builds complex calculations from simple primitives. `(10 + 5) * 2` is two operations chained. This is how spreadsheet formulas and data transformation pipelines work. |
| `math.isinf` / `math.isnan` checks | Floating-point edge cases like `10**1000` (overflow to infinity) or `0.0/0.0` (NaN) are valid Python but usually indicate errors. Catching them prevents silent garbage propagation. |

## Alternative Approaches

### Using a dict of functions instead of if/elif

```python
OPERATIONS = {
    "add": lambda a, b: a + b,
    "subtract": lambda a, b: a - b,
    "multiply": lambda a, b: a * b,
    "divide": lambda a, b: a / b if b != 0 else None,
}

def calculate_dispatch(operation, a, b):
    func = OPERATIONS.get(operation)
    if func is None:
        return {"success": False, "error": f"Unknown: {operation}"}
    result = func(a, b)
    return {"success": True, "result": result}
```

A dispatch dict is cleaner than if/elif chains and makes adding operations trivial (just add a key). The if/elif approach in this project is more explicit about error handling (division by zero, modulo by zero), which is better for learning.

### Using `ast.literal_eval` for safe expression parsing

For more complex config-driven calculations, `ast.literal_eval` can safely parse Python literals without the security risks of dynamic code execution. However, it cannot evaluate expressions — only literal values. For actual expression evaluation, use a purpose-built parser library, never unchecked dynamic execution.

## Common Pitfalls

1. **Missing "operations" key in config** — Without `setdefault`, a config file like `{"settings": {"precision": 4}}` would crash when the code tries to access `config["operations"]`. Always provide defaults for optional config keys.

2. **`2 ** 1000` does not overflow in Python** — Unlike C or Java, Python integers have arbitrary precision. `2 ** 1000` produces a very large integer, not an error. But `float(2 ** 1000)` raises `OverflowError` because floats have limited range. The `except OverflowError` clause catches this.

3. **Non-numeric CLI arguments** — If `--a` receives a string like "abc", `argparse` catches it because `type=float` is specified. But in batch mode, the JSON values are not validated by argparse, so the `try/except` in `batch_calculate` is essential.
