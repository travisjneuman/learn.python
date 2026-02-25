"""Level 7 / Project 15 — Level 7 Mini-Capstone.

Ties together all Level 7 concepts into a unified API integration
pipeline: fetch from multiple sources via adapters, cache results,
validate contracts, check freshness, reconcile, and produce a
combined report — all with feature flags and observability.

Key concepts:
- Adapter pattern for multi-source ingestion
- Caching layer with hit/miss tracking
- Contract validation on incoming payloads
- Freshness checking and reconciliation
- Feature flags to toggle pipeline stages
- Structured observability (logs + metrics)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path


# -- Adapters ------------------------------------------------------------

def adapt_source(source_type: str, raw: list[dict]) -> list[dict]:
    """Normalise raw records from different source formats."""
    out: list[dict] = []
    for rec in raw:
        if source_type == "alpha":
            out.append({"id": rec.get("uid"), "value": rec.get("data"),
                         "source": "alpha"})
        elif source_type == "beta":
            out.append({"id": rec.get("identifier"), "value": rec.get("payload"),
                         "source": "beta"})
        else:
            out.append({**rec, "source": source_type})
    return out


# -- Cache ---------------------------------------------------------------

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


# -- Contract validation -------------------------------------------------

def validate_contract(record: dict, required: list[str]) -> list[str]:
    """Return list of missing required fields."""
    return [f for f in required if f not in record or record[f] is None]


# -- Freshness -----------------------------------------------------------

def check_freshness(last_updated: float, max_age: float, now: float) -> str:
    age = now - last_updated
    if age > max_age:
        return "stale"
    return "fresh"


# -- Reconciliation ------------------------------------------------------

def reconcile_sources(groups: dict[str, list[dict]], key: str) -> dict:
    """Compare records across sources by key, return match/mismatch counts."""
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


# -- Observability -------------------------------------------------------

@dataclass
class PipelineMetrics:
    records_in: int = 0
    records_out: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    validation_errors: int = 0
    stale_records: int = 0
    stages_run: list[str] = field(default_factory=list)


# -- Pipeline orchestrator -----------------------------------------------

def run_pipeline(config: dict) -> dict:
    """Execute the full Level 7 capstone pipeline."""
    flags = config.get("flags", {})
    sources_config = config.get("sources", {})
    required_fields = config.get("required_fields", ["id", "value"])
    max_age = config.get("max_age_seconds", 600)
    now = config.get("now", time.time())

    metrics = PipelineMetrics()
    cache = SimpleCache()
    all_records: list[dict] = []
    grouped: dict[str, list[dict]] = {}

    # Stage 1: Adapt sources
    if flags.get("adapt", True):
        metrics.stages_run.append("adapt")
        for src_name, src_data in sources_config.items():
            adapted = adapt_source(src_name, src_data.get("records", []))
            metrics.records_in += len(adapted)
            all_records.extend(adapted)
            grouped[src_name] = adapted
            logging.info("adapted %d records from %s", len(adapted), src_name)

    # Stage 2: Cache dedup
    if flags.get("cache", True):
        metrics.stages_run.append("cache")
        deduped: list[dict] = []
        for rec in all_records:
            key = hashlib.md5(json.dumps(rec, sort_keys=True).encode()).hexdigest()[:12]
            cached = cache.get(key)
            if cached:
                continue
            cache.put(key, rec)
            deduped.append(rec)
        all_records = deduped
        metrics.cache_hits = cache.hits
        metrics.cache_misses = cache.misses

    # Stage 3: Contract validation
    if flags.get("validate", True):
        metrics.stages_run.append("validate")
        valid: list[dict] = []
        for rec in all_records:
            missing = validate_contract(rec, required_fields)
            if missing:
                metrics.validation_errors += 1
                logging.warning("contract violation: %s missing %s", rec.get("id"), missing)
            else:
                valid.append(rec)
        all_records = valid

    # Stage 4: Freshness check
    if flags.get("freshness", True):
        metrics.stages_run.append("freshness")
        for rec in all_records:
            ts = rec.get("timestamp", now)
            status = check_freshness(ts, max_age, now)
            rec["freshness"] = status
            if status == "stale":
                metrics.stale_records += 1

    # Stage 5: Reconciliation
    recon = {}
    if flags.get("reconcile", True) and len(grouped) >= 2:
        metrics.stages_run.append("reconcile")
        recon = reconcile_sources(grouped, "id")

    metrics.records_out = len(all_records)

    return {
        "records_in": metrics.records_in,
        "records_out": metrics.records_out,
        "stages_run": metrics.stages_run,
        "cache": cache.stats,
        "validation_errors": metrics.validation_errors,
        "stale_records": metrics.stale_records,
        "reconciliation": recon,
    }


# -- Entry points --------------------------------------------------------

def run(input_path: Path, output_path: Path) -> dict:
    config = json.loads(input_path.read_text(encoding="utf-8")) if input_path.exists() else {}
    summary = run_pipeline(config)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Level 7 Mini-Capstone Pipeline")
    parser.add_argument("--input", default="data/sample_input.json")
    parser.add_argument("--output", default="data/output_summary.json")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    args = parse_args()
    summary = run(Path(args.input), Path(args.output))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
