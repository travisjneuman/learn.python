# Level 7 Mini Capstone — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) | [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. This capstone combines all Level 7 concepts into one pipeline: multi-source adapters, caching with deduplication, contract validation, freshness checking, cross-source reconciliation, feature flags, and observability metrics. If you have completed projects 01-14 in this level, every individual piece should be familiar. The challenge is orchestrating them into a coherent pipeline with configurable stages.

## Thinking Process

Think of this project as building a data integration hub — the kind of system that sits at the center of a company and pulls data from multiple upstream APIs, cleans it, validates it, checks for staleness, and reconciles it across sources. Each source speaks a different dialect, some data is cached from previous runs, and you need to be able to toggle individual stages on and off for debugging.

The pipeline has five stages, each addressing a specific concern. Adaptation normalizes source-specific formats into a common shape. Caching deduplicates records so the same data is not processed twice. Validation ensures every record has the required fields. Freshness checking flags stale data. Reconciliation compares records across sources to find discrepancies. Feature flags let you disable any stage without modifying code.

The most important architectural insight is that these stages form a pipeline where each stage's output feeds into the next. The adapt stage produces normalized records. The cache stage deduplicates them. The validate stage filters out invalid ones. Each stage shrinks or transforms the record list before passing it on. Understanding this flow — and what happens when you disable a stage in the middle — is what this capstone tests.

## Step 1: Build the Source Adapters

**What to do:** Write an `adapt_source()` function that normalizes raw records from different source types (like "alpha" and "beta") into a common shape with `id`, `value`, and `source` fields. Each source type uses different field names.

**Why:** This is the same Adapter pattern from project 01, but now it handles multiple sources in a single function using branching logic. The `source` field preserves provenance so you know where each record originated, which matters for the reconciliation stage later.

```python
def adapt_source(source_type: str, raw: list[dict]) -> list[dict]:
    out = []
    for rec in raw:
        if source_type == "alpha":
            out.append({"id": rec.get("uid"), "value": rec.get("data"), "source": "alpha"})
        elif source_type == "beta":
            out.append({"id": rec.get("identifier"), "value": rec.get("payload"), "source": "beta"})
        else:
            out.append({**rec, "source": source_type})  # passthrough
    return out
```

**Predict:** What does the `else` branch do with an unknown source type? Why is a passthrough safer than raising an error here?

## Step 2: Implement the Cache Layer

**What to do:** Create a `SimpleCache` class with `get()`, `put()`, and a `stats` property that tracks hits and misses. The cache uses an MD5 hash of each record as its key.

**Why:** In a pipeline that runs repeatedly, you do not want to reprocess records you have already seen. The cache deduplicates by content: if two records have identical fields, they produce the same hash and the second one is skipped. Tracking hits and misses gives you visibility into how effective the cache is.

```python
class SimpleCache:
    def __init__(self) -> None:
        self._store: dict[str, dict] = {}
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> dict | None:
        if key in self._store:
            self.hits += 1
            return self._store[key]
        self.misses += 1
        return None

    def put(self, key: str, value: dict) -> None:
        self._store[key] = value

    @property
    def stats(self) -> dict:
        total = self.hits + self.misses
        return {"hits": self.hits, "misses": self.misses,
                "hit_rate": round(self.hits / total, 4) if total else 0.0}
```

**Predict:** If you process 10 records and 3 of them are duplicates, what will `hits`, `misses`, and `hit_rate` be? (Think: 7 unique records = 7 misses, 3 duplicates = 3 hits.)

## Step 3: Add Contract Validation and Freshness Checking

**What to do:** Write `validate_contract()` that checks if a record has all required fields (returning a list of missing ones) and `check_freshness()` that compares a timestamp against a maximum age to determine if data is "fresh" or "stale".

**Why:** Contract validation ensures you only pass well-formed records downstream. Without it, a missing `id` field could cause a `KeyError` crash three stages later, far from the actual problem. Freshness checking catches stale data that might have been cached too long or sourced from a lagging API.

```python
def validate_contract(record: dict, required: list[str]) -> list[str]:
    """Return list of missing required fields."""
    return [f for f in required if f not in record or record[f] is None]

def check_freshness(last_updated: float, max_age: float, now: float) -> str:
    age = now - last_updated
    if age > max_age:
        return "stale"
    return "fresh"
```

**Predict:** Why does `validate_contract()` also check `record[f] is None` in addition to `f not in record`? What kind of data source would produce a record where a field exists but is `None`?

## Step 4: Build the Reconciliation Function

**What to do:** Write `reconcile_sources()` that groups records by a key field across sources, then compares values to find matches, mismatches, and single-source-only records.

**Why:** When you pull the same data from two different sources, they should agree. If Source A says order #123 costs $50 and Source B says it costs $55, you have a discrepancy that needs investigation. Reconciliation automates this comparison.

```python
def reconcile_sources(groups: dict[str, list[dict]], key: str) -> dict:
    all_keys: dict[str, dict[str, dict]] = {}
    for source, records in groups.items():
        for rec in records:
            k = str(rec.get(key, ""))
            if k:
                all_keys.setdefault(k, {})[source] = rec

    matched, mismatched, single = 0, 0, 0
    for k, sources in all_keys.items():
        if len(sources) < 2:
            single += 1
        else:
            vals = [json.dumps(r.get("value")) for r in sources.values()]
            if len(set(vals)) == 1:
                matched += 1
            else:
                mismatched += 1
    return {"matched": matched, "mismatched": mismatched, "single_source": single}
```

**Predict:** Why use `json.dumps(r.get("value"))` to compare values instead of comparing them directly? What types of values would compare incorrectly without serialization?

## Step 5: Orchestrate the Pipeline with Feature Flags

**What to do:** Write `run_pipeline()` that reads a config dictionary and executes each stage only if its feature flag is enabled. The flags dict defaults to `True` for all stages. Track which stages ran in the `PipelineMetrics` dataclass.

**Why:** Feature flags let operators disable specific stages for debugging. If the cache stage is causing problems, disable it with `"cache": false` in the config. If freshness checking is too aggressive, turn it off. This operational flexibility is essential in production pipelines.

```python
def run_pipeline(config: dict) -> dict:
    flags = config.get("flags", {})
    metrics = PipelineMetrics()
    cache = SimpleCache()
    all_records = []

    # Stage 1: Adapt sources (only if flag is enabled)
    if flags.get("adapt", True):
        metrics.stages_run.append("adapt")
        for src_name, src_data in sources_config.items():
            adapted = adapt_source(src_name, src_data.get("records", []))
            all_records.extend(adapted)

    # Stage 2: Cache dedup
    if flags.get("cache", True):
        metrics.stages_run.append("cache")
        deduped = []
        for rec in all_records:
            key = hashlib.md5(json.dumps(rec, sort_keys=True).encode()).hexdigest()[:12]
            if not cache.get(key):
                cache.put(key, rec)
                deduped.append(rec)
        all_records = deduped

    # Stages 3-5: validate, freshness, reconcile (similar pattern)
    # ...
```

**Predict:** What happens if you disable the `adapt` flag but leave all other stages enabled? The `all_records` list starts empty — what do the cache, validate, and freshness stages do with zero records?

## Step 6: Build the Output Report

**What to do:** Assemble the final output dictionary with metrics from every stage: records in/out, cache stats, validation errors, stale records, reconciliation results, and which stages ran.

**Why:** This report is the "receipt" of the pipeline run. It tells operators at a glance what happened: how many records came in, how many survived each stage, and whether any data quality issues were found. It is also what your tests assert against.

```python
return {
    "records_in": metrics.records_in,
    "records_out": metrics.records_out,
    "stages_run": metrics.stages_run,
    "cache": cache.stats,
    "validation_errors": metrics.validation_errors,
    "stale_records": metrics.stale_records,
    "reconciliation": recon,
}
```

**Predict:** If all 5 stages run on 10 records with no errors, no duplicates, and no stale data, what should `records_in` and `records_out` both equal?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Disabling the adapt stage and expecting downstream stages to still work | Without adaptation, no records enter the pipeline | Downstream stages should handle empty input gracefully (check `if not all_records: return`) |
| Using `md5` on unsorted dict keys | Python dicts preserve insertion order, but two dicts with the same keys in different order produce different hashes | Always use `json.dumps(rec, sort_keys=True)` for deterministic hashing |
| Treating `None` values as present during contract validation | A record like `{"id": None}` technically has the `id` key | Check both `f not in record` AND `record[f] is None` |
| Running reconciliation with only one source | Reconciliation needs at least two sources to compare | Guard with `if len(grouped) >= 2` before running reconciliation |

## Testing Your Solution

```bash
pytest -q
```

You should see 2+ tests pass. The tests verify that the full pipeline produces correct metrics, that feature flags control stage execution, and that the output structure matches expectations.

## What You Learned

- **Feature flags** give operators runtime control over pipeline behavior without code changes. In production, this is how teams safely roll out changes: enable a new stage for 10% of traffic, monitor for errors, then gradually increase.
- **Multi-stage pipelines** are composed of independent stages where each stage's output feeds the next. Understanding the data flow — and what happens when a stage is removed or disabled — is essential for debugging production issues.
- **Cross-source reconciliation** catches data quality problems that no single source can detect on its own. When two authoritative sources disagree about the same record, something is wrong, and the earlier you detect it, the cheaper it is to fix.
