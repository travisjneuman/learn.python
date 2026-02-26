"""Level 7 / Project 09 — Contract Version Checker.

Validates that upstream API responses conform to a declared schema
contract.  Detects missing fields, type mismatches, and unexpected
extra fields — all without making real API calls.

Key concepts:
- Schema contracts as simple dicts  {field: expected_type_name}
- Semantic versioning comparison (major.minor.patch)
- Breaking vs non-breaking change detection
- Contract validation against sample payloads
"""

from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path


# -- Data model ----------------------------------------------------------

@dataclass
class ContractField:
    """One field in a schema contract."""
    name: str
    type_name: str        # "str", "int", "float", "bool", "list", "dict"
    required: bool = True


# WHY versioned schema contracts? -- When an upstream API changes its
# response shape, downstream consumers break. By declaring a versioned
# contract, you can detect breaking changes (major bump) vs safe additions
# (minor bump) before they reach production pipelines.
@dataclass
class Contract:
    """A versioned schema contract."""
    version: str          # e.g. "2.1.0"
    fields: list[ContractField] = field(default_factory=list)


@dataclass
class ValidationResult:
    """Outcome of validating one payload against a contract."""
    valid: bool
    missing: list[str] = field(default_factory=list)
    type_errors: list[str] = field(default_factory=list)
    extra_fields: list[str] = field(default_factory=list)


# -- Version helpers -----------------------------------------------------

def parse_version(v: str) -> tuple[int, int, int]:
    parts = v.split(".")
    return int(parts[0]), int(parts[1]), int(parts[2])


def is_breaking(old: str, new: str) -> bool:
    """Major bump or field removal counts as breaking."""
    o = parse_version(old)
    n = parse_version(new)
    return n[0] > o[0]


def diff_contracts(old: Contract, new: Contract) -> dict:
    """Compare two contract versions."""
    old_names = {f.name for f in old.fields}
    new_names = {f.name for f in new.fields}
    added = sorted(new_names - old_names)
    removed = sorted(old_names - new_names)
    breaking = is_breaking(old.version, new.version) or len(removed) > 0
    return {
        "old_version": old.version,
        "new_version": new.version,
        "added": added,
        "removed": removed,
        "breaking": breaking,
    }


# -- Validation ----------------------------------------------------------

TYPE_MAP: dict[str, type] = {
    "str": str, "int": int, "float": float,
    "bool": bool, "list": list, "dict": dict,
}


def validate_payload(payload: dict, contract: Contract) -> ValidationResult:
    """Check a single payload against a contract."""
    missing, type_errors = [], []
    contract_names = set()

    for cf in contract.fields:
        contract_names.add(cf.name)
        if cf.name not in payload:
            if cf.required:
                missing.append(cf.name)
            continue
        expected = TYPE_MAP.get(cf.type_name)
        if expected and not isinstance(payload[cf.name], expected):
            type_errors.append(
                f"{cf.name}: expected {cf.type_name}, got {type(payload[cf.name]).__name__}"
            )

    extra = sorted(set(payload.keys()) - contract_names)
    valid = len(missing) == 0 and len(type_errors) == 0
    return ValidationResult(valid=valid, missing=missing,
                            type_errors=type_errors, extra_fields=extra)


def validate_batch(
    payloads: list[dict], contract: Contract,
) -> dict:
    """Validate many payloads, return aggregate stats."""
    results = [validate_payload(p, contract) for p in payloads]
    valid_count = sum(1 for r in results if r.valid)
    return {
        "total": len(payloads),
        "valid": valid_count,
        "invalid": len(payloads) - valid_count,
        "issues": [
            {"missing": r.missing, "type_errors": r.type_errors, "extra": r.extra_fields}
            for r in results if not r.valid
        ],
    }


# -- Builders ------------------------------------------------------------

def contract_from_dict(d: dict) -> Contract:
    fields = [
        ContractField(
            name=f["name"],
            type_name=f["type"],
            required=f.get("required", True),
        )
        for f in d.get("fields", [])
    ]
    return Contract(version=d["version"], fields=fields)


# -- Entry points --------------------------------------------------------

def run(input_path: Path, output_path: Path) -> dict:
    config = json.loads(input_path.read_text(encoding="utf-8")) if input_path.exists() else {}

    contract = contract_from_dict(config.get("contract", {"version": "1.0.0"}))
    payloads = config.get("payloads", [])
    old_contract_raw = config.get("old_contract")

    summary = validate_batch(payloads, contract)
    summary["contract_version"] = contract.version

    if old_contract_raw:
        old_contract = contract_from_dict(old_contract_raw)
        summary["diff"] = diff_contracts(old_contract, contract)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Contract Version Checker")
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
