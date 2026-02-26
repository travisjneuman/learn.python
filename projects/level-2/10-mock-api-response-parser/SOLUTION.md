# Mock API Response Parser — Annotated Solution

> **STOP!** Try solving this yourself first. Use the [project README](./README.md) before reading the solution.

---

## Complete Solution

```python
"""Mock API Response Parser — complete annotated solution."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_response(raw_json: str) -> dict:
    """Parse a raw JSON string into a Python dict."""
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        # WHY: Returning a result dict instead of re-raising lets the caller
        # handle parse errors uniformly. The raw_preview helps debugging
        # by showing the first 100 chars of the malformed input.
        return {
            "success": False,
            "error": f"Invalid JSON: {exc}",
            "raw_preview": raw_json[:100],
        }

    # WHY: API responses should be JSON objects (dicts). A bare array or
    # string at the root is unusual and likely means the file format is wrong.
    if not isinstance(data, dict):
        return {
            "success": False,
            "error": f"Expected JSON object, got {type(data).__name__}",
        }

    return {"success": True, "data": data}


def validate_response(response: dict, required_fields: list[str]) -> dict:
    """Validate that a parsed API response has all required fields."""
    if not isinstance(response, dict):
        return {"valid": False, "error": "Response is not a dict"}

    # WHY: List comprehensions with membership checks cleanly partition
    # fields into found and missing. This is more readable than a loop
    # with two append branches.
    found = [f for f in required_fields if f in response]
    missing = [f for f in required_fields if f not in response]

    return {
        "valid": len(missing) == 0,
        "found_fields": found,
        "missing_fields": missing,
        # WHY: extra_fields shows what the API returned that we did not ask for.
        # Set difference (response keys minus required fields) finds them efficiently.
        "extra_fields": sorted(set(response.keys()) - set(required_fields)),
    }


def extract_items(response: dict, items_key: str = "data") -> list[dict]:
    """Extract a list of items from a nested response structure.

    Many APIs return: {"status": 200, "data": [{"id": 1}, ...]}
    This safely navigates to that nested list.
    """
    items = response.get(items_key)

    if items is None:
        return []

    if isinstance(items, list):
        return items

    # WHY: Sometimes the API returns a single object instead of an array
    # when there is only one result. Wrapping it in a list normalises the
    # return type so callers always get a list.
    if isinstance(items, dict):
        return [items]

    return []


def summarise_items(items: list[dict], group_field: str | None = None) -> dict:
    """Summarise extracted items with counts and optional grouping."""
    if not items:
        return {"count": 0, "fields": [], "groups": {}}

    # WHY: Collecting all unique field names across all items reveals the
    # schema. Different items may have different fields (sparse data).
    all_fields: set[str] = set()
    for item in items:
        all_fields.update(item.keys())

    summary: dict = {
        "count": len(items),
        "fields": sorted(all_fields),
    }

    if group_field:
        # WHY: Counting items per group value (like SQL GROUP BY + COUNT)
        # reveals the distribution of data. dict.get with default 0
        # handles the accumulation without needing defaultdict.
        groups: dict[str, int] = {}
        for item in items:
            key = str(item.get(group_field, "UNKNOWN"))
            groups[key] = groups.get(key, 0) + 1
        # WHY: Sort by count descending so the most common groups appear first.
        summary["groups"] = dict(
            sorted(groups.items(), key=lambda pair: pair[1], reverse=True)
        )

    return summary


def check_status(response: dict) -> dict:
    """Check the HTTP status code in an API response."""
    # WHY: APIs use different key names for status codes. Checking multiple
    # common names ("status", "status_code", "code") makes this function
    # work with more APIs without configuration.
    status = response.get("status", response.get("status_code", response.get("code")))

    if status is None:
        return {"category": "unknown", "message": "No status code found"}

    try:
        status = int(status)
    except (ValueError, TypeError):
        return {"category": "invalid", "message": f"Invalid status: {status}"}

    # WHY: HTTP status codes follow a standard range convention.
    # 2xx = success, 3xx = redirect, 4xx = client error, 5xx = server error.
    # Categorising by range is more useful than checking exact codes.
    if 200 <= status < 300:
        category = "success"
    elif 300 <= status < 400:
        category = "redirect"
    elif 400 <= status < 500:
        category = "client_error"
    elif 500 <= status < 600:
        category = "server_error"
    else:
        category = "unknown"

    return {"status": status, "category": category}


def process_api_file(path: Path) -> list[dict]:
    """Process a file containing one or more JSON API responses."""
    if not path.exists():
        raise FileNotFoundError(f"API response file not found: {path}")

    raw = path.read_text(encoding="utf-8").strip()
    results: list[dict] = []

    parsed = parse_response(raw)

    if parsed["success"]:
        data = parsed["data"]
        if isinstance(data, list):
            # WHY: Support files containing a JSON array of responses.
            # Each response is processed independently.
            for idx, resp in enumerate(data):
                if isinstance(resp, dict):
                    results.append(_process_single(resp, idx))
        else:
            results.append(_process_single(data, 0))
    else:
        results.append(parsed)

    return results


def _process_single(response: dict, index: int) -> dict:
    """Process a single API response dict into a summary."""
    # WHY: Leading underscore signals this is a private helper, not part
    # of the public API. It orchestrates the three analysis steps.
    status = check_status(response)
    items = extract_items(response)
    summary = summarise_items(items)

    return {
        "index": index,
        "status": status,
        "item_count": summary["count"],
        "fields": summary["fields"],
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Mock API response parser")
    parser.add_argument("input", help="Path to JSON API response file")
    parser.add_argument(
        "--validate", nargs="+", help="Required fields to validate",
    )
    parser.add_argument(
        "--extract", default="data", help="Key containing items to extract",
    )
    parser.add_argument(
        "--group", default=None, help="Field to group extracted items by",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point: parse API response file and display results."""
    args = parse_args()
    path = Path(args.input)
    raw = path.read_text(encoding="utf-8")
    parsed = parse_response(raw)

    if not parsed["success"]:
        print(f"Parse error: {parsed['error']}")
        return

    response = parsed["data"]

    if args.validate:
        validation = validate_response(response, args.validate)
        print(json.dumps(validation, indent=2))
        return

    items = extract_items(response, args.extract)
    summary = summarise_items(items, group_field=args.group)
    status = check_status(response)

    print(f"Status: {status}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
```

## Design Decisions

| Decision | Why |
|----------|-----|
| Structured result dicts from `parse_response` | Returning `{"success": True/False, ...}` instead of raising exceptions mirrors how real API responses work. The caller checks `success` and handles errors uniformly. |
| Multiple status code key names | Real APIs are inconsistent — some use `"status"`, others use `"status_code"` or `"code"`. Checking all three makes the parser work with more APIs without configuration. |
| `extract_items` wraps single objects in a list | Normalising the return type to always be a list means callers never need to check `isinstance` before iterating. This is the "robustness principle" — be liberal in what you accept. |
| Set operations for field discovery | `set.update()` and set difference (`-`) are the natural tools for collecting unique fields and finding extras. They run in O(1) per operation, making them efficient for large responses. |
| `_process_single` as a private helper | The underscore prefix convention signals "internal use only." This keeps the public API clean (`process_api_file`) while extracting reusable logic into a helper. |

## Alternative Approaches

### Using `jsonschema` for validation

```python
from jsonschema import validate, ValidationError

schema = {
    "type": "object",
    "required": ["status", "data"],
    "properties": {
        "status": {"type": "integer"},
        "data": {"type": "array"},
    }
}

try:
    validate(instance=response, schema=schema)
except ValidationError as e:
    print(f"Invalid: {e.message}")
```

The `jsonschema` library provides comprehensive JSON Schema validation, including type checks, nested structures, and pattern matching. The manual approach in this project teaches the fundamentals of field-by-field validation. For production APIs, use `jsonschema` or Pydantic.

### Using `dataclasses` or Pydantic models

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class ApiResponse:
    status: int
    data: list
    message: Optional[str] = None
```

Typed models catch structural problems at parse time and provide IDE autocompletion. This project uses plain dicts because they are the natural representation of JSON and do not require understanding classes yet.

## Common Pitfalls

1. **Assuming the `data` key always contains a list** — Some APIs return `"data": {"user": {...}}` (a single object) or even `"data": "OK"` (a string). Always check the type before iterating, or use `extract_items` which handles this safely.

2. **Trusting the status code alone** — A response with `"status": 200` can still contain an error in the body (e.g., `"data": [], "error": "No results"`). Always validate the response body in addition to checking the status code.

3. **Forgetting to handle non-dict JSON roots** — A file containing `[1, 2, 3]` is valid JSON but not a valid API response object. Without the `isinstance(data, dict)` check in `parse_response`, the code would crash when trying to access `.get()` on a list.
