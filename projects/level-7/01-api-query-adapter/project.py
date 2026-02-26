"""Level 7 / Project 01 — API Query Adapter.

Adapts different API response formats into a unified schema.
Uses simulated API responses (no network calls) to teach
normalization patterns.

Key concepts:
- Adapter pattern: one interface, multiple implementations
- Schema normalization: different sources → same output shape
- Error handling for missing/unexpected fields
- Dataclasses for typed response containers
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

# ---------------------------------------------------------------------------
# Unified schema
# ---------------------------------------------------------------------------


@dataclass
class UnifiedRecord:
    """The common shape that all API responses are normalized into."""

    id: str
    name: str
    value: float
    source: str
    timestamp: str


# ---------------------------------------------------------------------------
# Simulated API responses (mock data)
# ---------------------------------------------------------------------------

MOCK_API_A = [
    {"item_id": "A-001", "item_name": "Widget", "price": 9.99, "ts": "2025-01-15T08:00:00"},
    {"item_id": "A-002", "item_name": "Gadget", "price": 24.99, "ts": "2025-01-15T09:00:00"},
]

MOCK_API_B = [
    {"id": "B-001", "label": "Bolt Pack", "cost": 3.49, "created": "2025-01-15T10:00:00"},
    {"id": "B-002", "label": "Nut Set", "cost": 2.99, "created": "2025-01-15T11:00:00"},
]

MOCK_API_C = [
    {"sku": "C-001", "title": "Spring", "amount": 1.50, "date": "2025-01-15T12:00:00"},
]


# ---------------------------------------------------------------------------
# Adapters
# ---------------------------------------------------------------------------


def adapt_api_a(raw: list[dict]) -> list[UnifiedRecord]:
    """Adapter for API A: uses item_id, item_name, price, ts."""
    results = []
    for r in raw:
        results.append(UnifiedRecord(
            id=r["item_id"], name=r["item_name"],
            value=r["price"], source="api_a", timestamp=r["ts"],
        ))
    return results


def adapt_api_b(raw: list[dict]) -> list[UnifiedRecord]:
    """Adapter for API B: uses id, label, cost, created."""
    results = []
    for r in raw:
        results.append(UnifiedRecord(
            id=r["id"], name=r["label"],
            value=r["cost"], source="api_b", timestamp=r["created"],
        ))
    return results


def adapt_api_c(raw: list[dict]) -> list[UnifiedRecord]:
    """Adapter for API C: uses sku, title, amount, date."""
    results = []
    for r in raw:
        results.append(UnifiedRecord(
            id=r["sku"], name=r["title"],
            value=r["amount"], source="api_c", timestamp=r["date"],
        ))
    return results


# ---------------------------------------------------------------------------
# Adapter registry
# ---------------------------------------------------------------------------

ADAPTERS: dict[str, Callable[..., Any]] = {
    "api_a": adapt_api_a,
    "api_b": adapt_api_b,
    "api_c": adapt_api_c,
}


def adapt_response(source: str, raw: list[dict]) -> list[UnifiedRecord]:
    """Route raw data to the correct adapter by source name."""
    adapter = ADAPTERS.get(source)
    if adapter is None:
        raise ValueError(f"No adapter for source '{source}'. Available: {list(ADAPTERS.keys())}")
    return adapter(raw)


# ---------------------------------------------------------------------------
# Query engine
# ---------------------------------------------------------------------------


def query_all_sources(
    sources: dict[str, list[dict]] | None = None,
) -> list[UnifiedRecord]:
    """Query all configured sources and merge into unified records."""
    if sources is None:
        sources = {"api_a": MOCK_API_A, "api_b": MOCK_API_B, "api_c": MOCK_API_C}

    all_records: list[UnifiedRecord] = []
    for source_name, raw_data in sources.items():
        try:
            records = adapt_response(source_name, raw_data)
            all_records.extend(records)
            logging.info("adapted source=%s records=%d", source_name, len(records))
        except (KeyError, ValueError) as exc:
            logging.warning("skip source=%s error=%s", source_name, exc)

    return all_records


def filter_records(
    records: list[UnifiedRecord],
    min_value: float | None = None,
    source: str | None = None,
) -> list[UnifiedRecord]:
    """Filter unified records by optional criteria."""
    result = records
    if min_value is not None:
        result = [r for r in result if r.value >= min_value]
    if source is not None:
        result = [r for r in result if r.source == source]
    return result


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run(input_path: Path, output_path: Path) -> dict:
    """Load source config, adapt all APIs, write unified output."""
    if input_path.exists():
        config = json.loads(input_path.read_text(encoding="utf-8"))
        sources = config.get("sources", None)
    else:
        sources = None  # use built-in mocks

    start = time.perf_counter()
    records = query_all_sources(sources)
    elapsed_ms = round((time.perf_counter() - start) * 1000, 1)

    summary = {
        "total_records": len(records),
        "sources_queried": len(sources) if sources else 3,
        "elapsed_ms": elapsed_ms,
        "records": [
            {"id": r.id, "name": r.name, "value": r.value,
             "source": r.source, "timestamp": r.timestamp}
            for r in records
        ],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    logging.info("adapted %d records in %.1fms", len(records), elapsed_ms)
    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="API Query Adapter — normalize multiple API formats"
    )
    parser.add_argument("--input", default="data/sample_input.json")
    parser.add_argument("--output", default="data/output_summary.json")
    parser.add_argument("--run-id", default="manual-run")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    args = parse_args()
    summary = run(Path(args.input), Path(args.output))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
