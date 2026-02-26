# Solution: Level 7 / Project 06 - Token Rotation Simulator

> **STOP — Try it yourself first!**
>
> You learn by building, not by reading answers. Spend at least 30 minutes
> attempting this project before looking here.
>
> - Re-read the [README](./README.md) for requirements
> 
---

## Complete solution

```python
"""Level 7 / Project 06 — Token Rotation Simulator.

Simulates API token lifecycle: generation, expiry checking, rotation,
and revocation.  No real APIs — all simulated.
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

    # WHY properties instead of methods? -- Properties read like attributes
    # (token.is_expired) which matches how you think about state.  The
    # computation is cheap enough that re-evaluating on each access is fine.
    @property
    def is_expired(self) -> bool:
        return time.time() > self.expires_at

    @property
    def is_valid(self) -> bool:
        # WHY both checks? -- A token can be invalid for two independent
        # reasons: time-based expiry OR explicit revocation.  Both must pass.
        return not self.revoked and not self.is_expired


# WHY a TokenManager class? -- Token lifecycle (generate -> validate ->
# rotate -> revoke) requires mutable state: the set of active tokens,
# the current token, and an audit trail.  Encapsulating this in a class
# keeps the state machine coherent and prevents callers from bypassing
# the lifecycle (e.g. using a revoked token).
class TokenManager:
    def __init__(self, ttl_seconds: float = 3600) -> None:
        self.ttl = ttl_seconds
        self._tokens: dict[str, Token] = {}
        self._current_id: str = ""
        # WHY an audit trail? -- Security compliance requires knowing who
        # created/rotated/revoked which token and when.  The audit list is
        # append-only so historical entries cannot be altered.
        self._audit: list[dict] = []

    def generate(self, token_id: str | None = None) -> Token:
        now = time.time()
        tid = token_id or f"tok_{int(now)}"
        # WHY SHA-256 of id+timestamp? -- Produces a unique, unpredictable
        # token value.  In production you would use secrets.token_hex(), but
        # deterministic hashing makes tests reproducible.
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
        """Revoke current token and generate a new one."""
        # WHY revoke-then-generate? -- The old token must be invalidated
        # before the new one is active to prevent both tokens being valid
        # simultaneously (unless a grace period is explicitly configured).
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
        # WHY return a copy? -- Prevents external code from mutating the
        # audit trail, preserving its append-only integrity.
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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Token stored in a dict keyed by `token_id` | O(1) lookup for validation; supports multiple active tokens during grace periods | List of tokens -- simpler but O(n) validation lookups |
| `is_valid` checks both `revoked` and `is_expired` | A token can be invalid for two independent reasons; both must be checked | Separate `is_revoked()` / `is_expired()` calls in every consumer -- error-prone duplication |
| Append-only audit trail | Security compliance requires immutable history; returning a copy prevents external mutation | Database-backed audit log -- better for production but overkill for simulation |
| `rotate()` calls `generate()` internally | Ensures consistent state: new token is always created through the same path as manual generation | Inline token creation in `rotate()` -- duplicates generation logic |

## Alternative approaches

### Approach B: Token with grace period overlap

```python
def rotate_with_grace(self, grace_seconds: float = 300) -> Token:
    """Old token stays valid for grace_seconds after rotation."""
    if self._current_id in self._tokens:
        old = self._tokens[self._current_id]
        old.expires_at = time.time() + grace_seconds  # extend, don't revoke yet
    return self.generate()
```

**Trade-off:** Grace periods prevent service disruptions during rotation -- clients using the old token have time to switch. But they also mean two valid tokens exist simultaneously, which is a larger attack surface if one is compromised.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| `rotate()` called with no existing token | Works fine (generates first token) but the revoke audit entry is skipped | Check `self._current_id` before revoking, as the code already does |
| `ttl_seconds` set to 0 | Tokens expire instantly; `is_valid` returns False immediately after creation | Validate `ttl_seconds > 0` in the constructor |
| `time.time()` called in tests | Tests become non-deterministic because real clock moves | Inject a `now` parameter or mock `time.time` in tests |
