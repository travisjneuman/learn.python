"""Level 2 project: Config Driven Calculator.

Heavily commented beginner-friendly script:
- load operation configs from a JSON file,
- dispatch calculations based on config definitions,
- support custom operations defined entirely in config.

Skills practiced: nested data structures, dict lookups, try/except,
JSON loading, list comprehensions, sorting with key functions.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


# Default operations when no config is provided.
DEFAULT_OPERATIONS: dict[str, dict] = {
    "add": {"symbol": "+", "description": "Addition"},
    "subtract": {"symbol": "-", "description": "Subtraction"},
    "multiply": {"symbol": "*", "description": "Multiplication"},
    "divide": {"symbol": "/", "description": "Division"},
    "power": {"symbol": "**", "description": "Exponentiation"},
    "modulo": {"symbol": "%", "description": "Modulo (remainder)"},
}


def load_config(path: Path) -> dict:
    """Load calculator configuration from a JSON file.

    The config file should have an "operations" key with operation
    definitions and an optional "settings" key.

    Falls back to DEFAULT_OPERATIONS if the file is missing or invalid.
    """
    if not path.exists():
        return {"operations": DEFAULT_OPERATIONS, "settings": {}}

    try:
        raw = path.read_text(encoding="utf-8")
        config = json.loads(raw)
    except (json.JSONDecodeError, OSError) as exc:
        # Return defaults instead of crashing on bad config.
        return {
            "operations": DEFAULT_OPERATIONS,
            "settings": {},
            "config_error": str(exc),
        }

    # Ensure required keys exist.
    config.setdefault("operations", DEFAULT_OPERATIONS)
    config.setdefault("settings", {})
    return config


def calculate(operation: str, a: float, b: float) -> dict:
    """Perform a calculation and return a result dict.

    Handles division by zero, invalid operations, and math errors.
    """
    try:
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

        # Check for infinity or NaN results.
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
    """Run a batch of calculations from a list of operation dicts.

    Each dict should have: {"operation": str, "a": number, "b": number}
    Uses enumerate to track original order.
    """
    results = []
    for idx, op in enumerate(operations_list):
        try:
            name = op["operation"]
            a = float(op.get("a", 0))
            b = float(op.get("b", 0))
            result = calculate(name, a, b)
            result["index"] = idx
            results.append(result)
        except (KeyError, ValueError, TypeError) as exc:
            results.append({
                "index": idx,
                "success": False,
                "error": f"Invalid operation spec: {exc}",
            })
    return results


def list_operations(config: dict) -> list[dict]:
    """List all available operations from config.

    Returns a sorted list of operation info dicts.
    """
    ops = config.get("operations", DEFAULT_OPERATIONS)
    # List comprehension building info dicts, sorted by operation name.
    return sorted(
        [
            {"name": name, **info}
            for name, info in ops.items()
        ],
        key=lambda op: op["name"],
    )


def calculate_chain(operations: list[tuple[str, float]], start: float = 0) -> dict:
    """Chain multiple operations together, feeding each result into the next.

    Example: start=10, [("add", 5), ("multiply", 2)] -> (10+5)*2 = 30
    """
    current = start
    steps: list[dict] = []

    for op_name, operand in operations:
        result = calculate(op_name, current, operand)
        if not result["success"]:
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
        "--config",
        default="data/sample_input.txt",
        help="Path to JSON config file",
    )
    parser.add_argument("--op", help="Operation to perform")
    parser.add_argument("--a", type=float, help="First operand")
    parser.add_argument("--b", type=float, default=0, help="Second operand")
    parser.add_argument(
        "--list", action="store_true", help="List available operations"
    )
    parser.add_argument(
        "--batch", help="Path to JSON file with batch operations"
    )
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

    # Default: show config info.
    print("Calculator config loaded. Use --list to see operations.")
    print(f"Operations available: {len(config.get('operations', {}))}")


if __name__ == "__main__":
    main()
