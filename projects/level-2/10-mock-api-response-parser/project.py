"""Level 2 project: Mock API Response Parser.

Heavily commented beginner-friendly script:
- parse and validate mock API JSON responses,
- extract data from nested response structures,
- handle different HTTP status codes and error payloads.

Skills practiced: nested data structures, dict/list comprehensions,
try/except for JSON parsing, sets, enumerate, sorting with key.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_response(raw_json: str) -> dict:
    """Parse a raw JSON string into a Python dict.

    Wraps json.loads with friendly error handling for beginners.
    """
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        return {
            "success": False,
            "error": f"Invalid JSON: {exc}",
            "raw_preview": raw_json[:100],
        }

    if not isinstance(data, dict):
        return {
            "success": False,
            "error": f"Expected JSON object, got {type(data).__name__}",
        }

    return {"success": True, "data": data}


def validate_response(response: dict, required_fields: list[str]) -> dict:
    """Validate that a parsed API response has all required fields.

    Returns a validation report with found/missing field lists.
    """
    if not isinstance(response, dict):
        return {"valid": False, "error": "Response is not a dict"}

    found = [f for f in required_fields if f in response]
    missing = [f for f in required_fields if f not in response]

    return {
        "valid": len(missing) == 0,
        "found_fields": found,
        "missing_fields": missing,
        "extra_fields": sorted(set(response.keys()) - set(required_fields)),
    }


def extract_items(response: dict, items_key: str = "data") -> list[dict]:
    """Extract a list of items from a nested response.

    Many APIs return data in a structure like:
        {"status": 200, "data": [{"id": 1}, {"id": 2}]}

    This function safely navigates to that nested list.
    """
    items = response.get(items_key)

    if items is None:
        return []

    if isinstance(items, list):
        return items

    if isinstance(items, dict):
        # Sometimes "data" is a single object — wrap it in a list.
        return [items]

    return []


def summarise_items(items: list[dict], group_field: str | None = None) -> dict:
    """Summarise extracted items with counts and optional grouping.

    Uses dict comprehensions and sorting with key functions.
    """
    if not items:
        return {"count": 0, "fields": [], "groups": {}}

    # Collect all unique field names across all items.
    all_fields: set[str] = set()
    for item in items:
        all_fields.update(item.keys())

    summary: dict = {
        "count": len(items),
        "fields": sorted(all_fields),
    }

    # Optional grouping — count items per group value.
    if group_field:
        groups: dict[str, int] = {}
        for item in items:
            key = str(item.get(group_field, "UNKNOWN"))
            groups[key] = groups.get(key, 0) + 1
        # Sort by count descending.
        summary["groups"] = dict(
            sorted(groups.items(), key=lambda pair: pair[1], reverse=True)
        )

    return summary


def check_status(response: dict) -> dict:
    """Check the HTTP status code in an API response.

    Categorises the status into success, redirect, client error,
    or server error ranges.
    """
    status = response.get("status", response.get("status_code", response.get("code")))

    if status is None:
        return {"category": "unknown", "message": "No status code found"}

    try:
        status = int(status)
    except (ValueError, TypeError):
        return {"category": "invalid", "message": f"Invalid status: {status}"}

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
    """Process a file containing one or more JSON API responses.

    The file can contain:
    - A single JSON object (one response)
    - A JSON array of response objects
    - Multiple JSON objects separated by blank lines

    Returns a list of processed response summaries.
    """
    if not path.exists():
        raise FileNotFoundError(f"API response file not found: {path}")

    raw = path.read_text(encoding="utf-8").strip()
    results: list[dict] = []

    # Try parsing as a single JSON value first.
    parsed = parse_response(raw)

    if parsed["success"]:
        data = parsed["data"]
        if isinstance(data, list):
            # Array of responses.
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
        "--validate",
        nargs="+",
        help="Required fields to validate",
    )
    parser.add_argument(
        "--extract",
        default="data",
        help="Key containing items to extract",
    )
    parser.add_argument(
        "--group",
        default=None,
        help="Field to group extracted items by",
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

    # Extract and summarise items.
    items = extract_items(response, args.extract)
    summary = summarise_items(items, group_field=args.group)
    status = check_status(response)

    print(f"Status: {status}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
