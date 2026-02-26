# API Query Adapter — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) | [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. The goal is to take data from multiple APIs that each use different field names and shapes, and normalize everything into one unified format. If you can write a function that takes a dictionary with one set of keys and returns a dataclass with a standard set of fields, you have the core idea.

## Thinking Process

Imagine you work at a company that buys products from three different suppliers. Supplier A sends invoices with fields called `item_id`, `item_name`, and `price`. Supplier B uses `id`, `label`, and `cost`. Supplier C uses `sku`, `title`, and `amount`. They all mean the same thing — an identifier, a name, and a price — but every system uses different words for them.

Your accounting team does not want to learn three different formats. They want one spreadsheet with columns `id`, `name`, and `value`. The Adapter pattern solves this: you write a small translator for each supplier that maps their unique field names to your standard format. Downstream code only deals with the standard format and never needs to know which supplier the data came from.

The architecture has three layers. At the bottom, mock data simulates what each API would return. In the middle, adapter functions translate each API's format into `UnifiedRecord` dataclasses. At the top, a registry maps source names to adapters so you can add new sources without changing the core logic. This separation of concerns means adding a new API requires writing one adapter function and one registry entry — nothing else changes.

## Step 1: Define the Unified Schema

**What to do:** Create a `UnifiedRecord` dataclass with fields that represent the common shape all API responses will be normalized into: `id`, `name`, `value`, `source`, and `timestamp`.

**Why:** This is the contract between your adapters and your downstream code. No matter which API the data came from, it will always have exactly these five fields. Dataclasses give you type safety (your IDE will catch typos) and a clean `__repr__` for debugging.

```python
from dataclasses import dataclass

@dataclass
class UnifiedRecord:
    id: str
    name: str
    value: float
    source: str
    timestamp: str
```

**Predict:** Why include a `source` field if the whole point is to unify the data? When would you need to know which API a record originally came from?

## Step 2: Create Mock API Data

**What to do:** Define three mock datasets that simulate what each API would return. Each uses completely different field names for the same concepts.

**Why:** Using mock data lets you build and test the entire adapter system without making real network calls. This is standard practice: get the logic right with controlled data first, then swap in real API calls later.

```python
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
```

**Predict:** What field names does API A use for "identifier" and "price"? What about API C? Notice how every API uses different names for the same concept.

## Step 3: Write Individual Adapter Functions

**What to do:** Write one adapter function per API. Each takes a list of raw dictionaries and returns a list of `UnifiedRecord` instances, mapping source-specific field names to the unified fields.

**Why:** Each adapter is small and focused: it knows the quirks of exactly one API. When API A changes its field names, you only modify `adapt_api_a()`. Nothing else in your system needs to change.

```python
def adapt_api_a(raw: list[dict]) -> list[UnifiedRecord]:
    results = []
    for r in raw:
        results.append(UnifiedRecord(
            id=r["item_id"],       # API A calls it "item_id"
            name=r["item_name"],   # API A calls it "item_name"
            value=r["price"],      # API A calls it "price"
            source="api_a",
            timestamp=r["ts"],     # API A calls it "ts"
        ))
    return results

def adapt_api_b(raw: list[dict]) -> list[UnifiedRecord]:
    results = []
    for r in raw:
        results.append(UnifiedRecord(
            id=r["id"], name=r["label"],
            value=r["cost"], source="api_b", timestamp=r["created"],
        ))
    return results
```

**Predict:** If API A adds a new field called `"category"` that you do not care about, does `adapt_api_a()` need to change? What if API A renames `"price"` to `"unit_price"`?

## Step 4: Build the Adapter Registry

**What to do:** Create a dictionary that maps source names to their adapter functions. Write a `adapt_response()` function that looks up the correct adapter by name and calls it.

**Why:** The registry is the Adapter pattern's dispatch mechanism. Instead of writing `if source == "api_a": ...` chains, you store the mapping in a dictionary. Adding a new API is a one-line change: add a new entry to the dictionary. This is the Open/Closed Principle in action — open for extension, closed for modification.

```python
ADAPTERS: dict[str, Callable] = {
    "api_a": adapt_api_a,
    "api_b": adapt_api_b,
    "api_c": adapt_api_c,
}

def adapt_response(source: str, raw: list[dict]) -> list[UnifiedRecord]:
    adapter = ADAPTERS.get(source)
    if adapter is None:
        raise ValueError(f"No adapter for source '{source}'. Available: {list(ADAPTERS.keys())}")
    return adapter(raw)
```

**Predict:** What happens if you call `adapt_response("api_d", data)` when there is no adapter for `"api_d"`? Why is raising a clear error better than returning an empty list?

## Step 5: Query All Sources and Merge Results

**What to do:** Write `query_all_sources()` that iterates over all configured sources, adapts each one, and merges the results into a single list of `UnifiedRecord` objects. Add `filter_records()` for optional filtering by minimum value or source.

**Why:** The merge step is where the adapter pattern pays off. Downstream code receives one flat list of identically-shaped records. It does not matter whether the data came from 2 sources or 20 — the interface is the same.

```python
def query_all_sources(sources=None) -> list[UnifiedRecord]:
    if sources is None:
        sources = {"api_a": MOCK_API_A, "api_b": MOCK_API_B, "api_c": MOCK_API_C}

    all_records = []
    for source_name, raw_data in sources.items():
        try:
            records = adapt_response(source_name, raw_data)
            all_records.extend(records)
        except (KeyError, ValueError) as exc:
            logging.warning("skip source=%s error=%s", source_name, exc)
    return all_records
```

**Predict:** Why does the code catch `KeyError` and `ValueError` and log a warning instead of crashing? In a production system with 10 sources, should one bad source take down the entire pipeline?

## Step 6: Wire Up the Orchestrator and CLI

**What to do:** Write `run()` that loads optional source configuration from a JSON file (falling back to mocks), adapts all sources, measures elapsed time, and writes the unified results to a JSON output file.

**Why:** The orchestrator ties the layers together and produces a tangible output you can inspect. The elapsed time measurement is a bonus: it shows how fast the adaptation runs, which is useful for performance profiling when you scale to real API calls.

```python
def run(input_path: Path, output_path: Path) -> dict:
    if input_path.exists():
        config = json.loads(input_path.read_text())
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
        "records": [{"id": r.id, "name": r.name, "value": r.value,
                     "source": r.source, "timestamp": r.timestamp} for r in records],
    }
    output_path.write_text(json.dumps(summary, indent=2))
    return summary
```

**Predict:** With the three mock APIs (2 + 2 + 1 records), what should `total_records` be in the output?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Hard-coding field mappings in the query function instead of adapters | It seems simpler to put everything in one place | Keep mappings in adapter functions so each source's logic is isolated |
| Forgetting to handle missing fields in raw data | Mock data is always clean, but real APIs can return partial responses | Use `.get("field", default)` or add explicit `KeyError` handling in adapters |
| Using `if/elif` chains instead of a registry dictionary | It works for 2-3 sources but becomes unmanageable at scale | The dictionary registry makes adding sources trivial and avoids long conditionals |
| Not including `source` in the unified record | You lose traceability — you cannot tell which API a record came from | Always include provenance so you can debug data quality issues per source |

## Testing Your Solution

```bash
pytest -q
```

You should see 2+ tests pass. The tests verify that each adapter correctly maps source-specific fields to the unified schema and that the full query-all-sources pipeline produces the expected number of records.

## What You Learned

- **The Adapter pattern** solves the problem of integrating multiple systems with incompatible interfaces. You write one small translator per source, and all downstream code works with a single unified shape. This is one of the most commonly used design patterns in real-world software.
- **Registry-based dispatch** (using a dictionary of functions) is cleaner than `if/elif` chains for routing to different handlers. It follows the Open/Closed Principle: you can add new sources without modifying existing code.
- **Separating data ingestion from data processing** means your processing logic never needs to know about API-specific quirks. This separation becomes critical as you add more sources over time.
