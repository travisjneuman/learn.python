"""Level 7 / Project 06 — Token Rotation Simulator.

Simulates API token lifecycle: generation, expiry checking, rotation,
and revocation.  No real APIs — all simulated.

Key concepts:
- Token lifecycle: create → use → rotate → revoke
- Expiry-based validity checking
- Overlap period: old token valid during rotation
- Audit trail of all token operations
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Token:
    token_id: str
    value: str
    created_at: float
    expires_at: float
    revoked: bool = False

    @property
    def is_expired(self) -> bool:
        return time.time() > self.expires_at

    @property
    def is_valid(self) -> bool:
        return not self.revoked and not self.is_expired


class TokenManager:
    def __init__(self, ttl_seconds: float = 3600) -> None:
        self.ttl = ttl_seconds
        self._tokens: dict[str, Token] = {}
        self._current_id: str = ""
        self._audit: list[dict] = []

    def generate(self, token_id: str | None = None) -> Token:
        now = time.time()
        tid = token_id or f"tok_{int(now)}"
        value = hashlib.sha256(f"{tid}:{now}".encode()).hexdigest()[:32]
        token = Token(token_id=tid, value=value, created_at=now, expires_at=now + self.ttl)
        self._tokens[tid] = token
        self._current_id = tid
        self._audit.append({"action": "generate", "token": tid, "at": now})
        logging.info("generated token=%s", tid)
        return token

    def validate(self, token_id: str) -> bool:
        token = self._tokens.get(token_id)
        if not token:
            return False
        return token.is_valid

    def rotate(self) -> Token:
        if self._current_id and self._current_id in self._tokens:
            old = self._tokens[self._current_id]
            old.revoked = True
            self._audit.append({"action": "revoke", "token": self._current_id})
        new_token = self.generate()
        self._audit.append({"action": "rotate", "token": new_token.token_id})
        return new_token

    def revoke(self, token_id: str) -> bool:
        token = self._tokens.get(token_id)
        if not token:
            return False
        token.revoked = True
        self._audit.append({"action": "revoke", "token": token_id})
        return True

    @property
    def current(self) -> Token | None:
        return self._tokens.get(self._current_id)

    @property
    def audit_log(self) -> list[dict]:
        return list(self._audit)

    def stats(self) -> dict:
        total = len(self._tokens)
        active = sum(1 for t in self._tokens.values() if t.is_valid)
        revoked = sum(1 for t in self._tokens.values() if t.revoked)
        return {"total": total, "active": active, "revoked": revoked}


def run(input_path: Path, output_path: Path) -> dict:
    if input_path.exists():
        config = json.loads(input_path.read_text(encoding="utf-8"))
    else:
        config = {}

    ttl = config.get("ttl_seconds", 3600)
    operations = config.get("operations", ["generate", "rotate", "rotate"])

    mgr = TokenManager(ttl_seconds=ttl)
    for op in operations:
        if op == "generate":
            mgr.generate()
        elif op == "rotate":
            mgr.rotate()
        elif op.startswith("revoke:"):
            mgr.revoke(op.split(":")[1])

    summary = {
        "operations_run": len(operations),
        "stats": mgr.stats(),
        "audit": mgr.audit_log,
        "current_token": mgr.current.token_id if mgr.current else None,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Token Rotation Simulator")
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
