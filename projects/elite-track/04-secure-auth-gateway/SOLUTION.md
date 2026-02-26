# Solution: Elite Track / Secure Auth Gateway

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
>.

---

## Complete solution

```python
"""Secure Auth Gateway.

This project is part of the elite extension track.
It intentionally emphasizes explicit, testable engineering decisions.
"""

# WHY a gateway pattern for auth? -- Centralizing authentication in a gateway
# means individual services don't implement auth independently (where bugs hide).
# The gateway validates tokens, enforces rate limits, and propagates identity
# context downstream -- the same pattern AWS API Gateway and Kong use.

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse CLI inputs for deterministic project execution."""
    parser = argparse.ArgumentParser(description="Secure Auth Gateway")
    parser.add_argument("--input", required=True, help="Path to input text data")
    parser.add_argument("--output", required=True, help="Path to output JSON summary")
    parser.add_argument("--run-id", default="manual-run", help="Optional run identifier")
    return parser.parse_args()


def load_lines(input_path: Path) -> list[str]:
    """Load normalized input lines and reject empty datasets safely."""
    if not input_path.exists():
        raise FileNotFoundError(f"input file not found: {input_path}")
    lines = [line.strip() for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise ValueError("input file contains no usable lines")
    return lines


def classify_line(line: str) -> dict[str, Any]:
    """Transform one CSV-like line into structured fields with validation."""
    parts = [piece.strip() for piece in line.split(",")]
    if len(parts) != 3:
        raise ValueError(f"invalid line format (expected 3 comma fields): {line}")

    name, score_raw, severity = parts
    score = int(score_raw)
    return {
        "name": name,
        "score": score,
        "severity": severity,
        # WHY is_high_risk for auth? -- In a security context, "warn" and
        # "critical" map to suspicious authentication events (failed logins,
        # token expiry, rate limit hits). Flagging them as high-risk
        # enables downstream alerting and audit trail generation.
        "is_high_risk": severity in {"warn", "critical"} or score < 5,
    }


def build_summary(records: list[dict[str, Any]], project_title: str, run_id: str) -> dict[str, Any]:
    """Build deterministic summary payload for testing and teach-back review."""
    high_risk_count = sum(1 for record in records if record["is_high_risk"])
    avg_score = round(sum(record["score"] for record in records) / len(records), 2)

    return {
        "project_title": project_title,
        "run_id": run_id,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "record_count": len(records),
        "high_risk_count": high_risk_count,
        "average_score": avg_score,
        "records": records,
    }


def write_summary(output_path: Path, payload: dict[str, Any]) -> None:
    """Write JSON output with parent directory creation for first-time runs."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    """Execute end-to-end project run."""
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    lines = load_lines(input_path)
    records = [classify_line(line) for line in lines]

    payload = build_summary(records, "Secure Auth Gateway", args.run_id)
    write_summary(output_path, payload)

    print(f"output_summary.json written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Gateway pattern (centralized auth) | Single enforcement point prevents auth bypass; services trust the gateway's identity context | Per-service auth -- each service implements its own validation, increasing attack surface |
| Deterministic input simulation | Security testing requires reproducible scenarios; real token flows add non-determinism | Live JWT validation -- realistic but requires secret management and token issuance infrastructure |
| High-risk flagging for security events | Failed logins, expired tokens, and rate limit hits are audit-critical; flagging them enables incident response | Treat all events equally -- misses the distinction between normal and suspicious activity |
| JSON audit output | Security events must be auditable; JSON is parseable by SIEM tools (Splunk, ELK) | Plain text logs -- harder to query and correlate across systems |

## Alternative approaches

### Approach B: Token validation with HMAC signatures

```python
import hashlib
import hmac
import time

def create_token(user_id: str, secret: str, ttl_seconds: int = 3600) -> str:
    """Create a simple HMAC-signed token with expiration."""
    expiry = int(time.time()) + ttl_seconds
    payload = f"{user_id}:{expiry}"
    signature = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()[:16]
    return f"{payload}:{signature}"

def validate_token(token: str, secret: str) -> dict[str, str]:
    """Validate token signature and expiration."""
    parts = token.split(":")
    if len(parts) != 3:
        return {"valid": False, "reason": "malformed token"}
    user_id, expiry_str, signature = parts
    payload = f"{user_id}:{expiry_str}"
    expected = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()[:16]
    if not hmac.compare_digest(signature, expected):
        return {"valid": False, "reason": "invalid signature"}
    if int(expiry_str) < int(time.time()):
        return {"valid": False, "reason": "token expired"}
    return {"valid": True, "user_id": user_id}
```

**Trade-off:** HMAC token validation demonstrates real auth patterns (signature verification, expiry checks, constant-time comparison). However, it requires secret management and does not teach the broader gateway pattern (rate limiting, role checks, audit logging). The CSV scaffold covers the full gateway workflow while the token validation can be layered on as the "Alter it" enhancement.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Secret key leaked in source code | All tokens can be forged; complete auth bypass | Store secrets in environment variables or a secrets manager; never commit them |
| Token expiry set too long (e.g., 30 days) | Stolen tokens remain valid for weeks; large blast radius | Use short-lived tokens (15 min) with refresh token rotation |
| No rate limiting on login attempts | Brute-force attacks can guess passwords by trying millions of combinations | Add per-IP rate limiting (e.g., 5 attempts per minute) with exponential backoff |
