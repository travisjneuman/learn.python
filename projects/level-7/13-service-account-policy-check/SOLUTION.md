# Solution: Level 7 / Project 13 - Service Account Policy Check

> **STOP — Try it yourself first!**
>
> You learn by building, not by reading answers. Spend at least 30 minutes
> attempting this project before looking here.
>
> - Re-read the [README](./README.md) for requirements
> - Try the [WALKTHROUGH](./WALKTHROUGH.md) for guided hints without spoilers

---

## Complete solution

```python
"""Level 7 / Project 13 — Service Account Policy Check.

Validates that service accounts conform to a security policy:
least-privilege permissions, key rotation age, and naming conventions.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import time
from dataclasses import dataclass, field
from pathlib import Path


# -- Data model ----------------------------------------------------------

@dataclass
class ServiceAccount:
    name: str
    permissions: list[str]
    key_created_at: float      # epoch seconds
    owner: str = ""


@dataclass
class PolicyRule:
    """One rule in the security policy."""
    name: str
    check: str                 # "max_permissions" | "key_age" | "naming"
    params: dict = field(default_factory=dict)


@dataclass
class Violation:
    account: str
    rule: str
    message: str


# -- Core logic ----------------------------------------------------------

# WHY an allowlist of permissions? -- Least-privilege means accounts should
# only have permissions from a known set.  Any permission not in this set is
# either a typo or a privilege escalation risk.  The set data structure gives
# O(1) membership checks.
ALLOWED_PERMISSIONS: set[str] = {
    "read", "write", "delete", "admin", "deploy",
    "logs:read", "logs:write", "metrics:read",
}


def check_max_permissions(
    account: ServiceAccount, max_count: int,
) -> Violation | None:
    """Flag accounts with too many permissions."""
    if len(account.permissions) > max_count:
        return Violation(
            account.name, "max_permissions",
            f"has {len(account.permissions)} permissions, max allowed is {max_count}",
        )
    return None


def check_key_age(
    account: ServiceAccount, max_age_days: float, now: float | None = None,
) -> Violation | None:
    """Flag accounts whose API keys have not been rotated recently."""
    now = now or time.time()
    age_days = (now - account.key_created_at) / 86400
    # WHY age check in days? -- Key rotation policies are typically
    # expressed in days (e.g. "rotate every 90 days").  Converting from
    # epoch seconds to days makes the threshold human-readable.
    if age_days > max_age_days:
        return Violation(
            account.name, "key_age",
            f"key is {age_days:.0f} days old, max allowed is {max_age_days:.0f}",
        )
    return None


def check_naming(account: ServiceAccount, pattern: str) -> Violation | None:
    """Ensure account names follow organizational naming conventions."""
    # WHY regex for naming? -- Naming conventions (e.g. "must start with
    # svc-") are naturally expressed as patterns.  re.match checks from
    # the start of the string, enforcing prefix conventions.
    if not re.match(pattern, account.name):
        return Violation(
            account.name, "naming",
            f"name '{account.name}' does not match pattern '{pattern}'",
        )
    return None


def check_unknown_permissions(account: ServiceAccount) -> list[Violation]:
    """Flag permissions not in the allowlist."""
    unknown = set(account.permissions) - ALLOWED_PERMISSIONS
    return [
        Violation(account.name, "unknown_permission", f"unknown permission: {p}")
        for p in sorted(unknown)
    ]


def run_policy_check(
    accounts: list[ServiceAccount],
    rules: list[PolicyRule],
    now: float | None = None,
) -> list[Violation]:
    """Evaluate all rules against all accounts.

    WHY nested loops (accounts x rules)? -- Every account must be checked
    against every rule.  The unknown-permissions check runs unconditionally
    because it is a baseline security requirement, not an optional policy.
    """
    violations: list[Violation] = []
    for acct in accounts:
        violations.extend(check_unknown_permissions(acct))
        for rule in rules:
            v: Violation | None = None
            if rule.check == "max_permissions":
                v = check_max_permissions(acct, rule.params.get("max", 5))
            elif rule.check == "key_age":
                v = check_key_age(acct, rule.params.get("max_days", 90), now)
            elif rule.check == "naming":
                v = check_naming(acct, rule.params.get("pattern", r"^svc-"))
            if v:
                violations.append(v)
                logging.warning("violation: %s -- %s", v.account, v.message)
    return violations


def compliance_summary(
    accounts: list[ServiceAccount], violations: list[Violation],
) -> dict:
    """Build a compliance report from violations."""
    violated_names = {v.account for v in violations}
    return {
        "total_accounts": len(accounts),
        "compliant": len(accounts) - len(violated_names),
        "non_compliant": len(violated_names),
        "total_violations": len(violations),
        "violations": [
            {"account": v.account, "rule": v.rule, "message": v.message}
            for v in violations
        ],
    }


# -- Builders ------------------------------------------------------------

def accounts_from_config(raw: list[dict]) -> list[ServiceAccount]:
    return [
        ServiceAccount(
            name=d["name"],
            permissions=d.get("permissions", []),
            key_created_at=d.get("key_created_at", time.time()),
            owner=d.get("owner", ""),
        )
        for d in raw
    ]


def rules_from_config(raw: list[dict]) -> list[PolicyRule]:
    return [
        PolicyRule(name=d["name"], check=d["check"], params=d.get("params", {}))
        for d in raw
    ]


# -- Entry points --------------------------------------------------------

def run(input_path: Path, output_path: Path) -> dict:
    config = json.loads(input_path.read_text(encoding="utf-8")) if input_path.exists() else {}

    accounts = accounts_from_config(config.get("accounts", []))
    rules = rules_from_config(config.get("rules", []))
    now = config.get("now")

    violations = run_policy_check(accounts, rules, now)
    summary = compliance_summary(accounts, violations)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Service Account Policy Check")
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
| Separate check functions per rule type | Each check is independently testable and can be reused across different policy configurations | Single monolithic `check_all()` function -- harder to test and extend |
| `ALLOWED_PERMISSIONS` as a set | O(1) membership checks; clear declaration of what is permitted | List -- O(n) lookups; works but slower for large permission sets |
| `Violation` returns `None` when check passes | Caller uses `if v:` pattern; avoids boolean flags or exception-based control flow | Return `(bool, str)` tuple -- less ergonomic; cannot be extended with fields |
| Unknown-permissions check runs unconditionally | Least-privilege is a baseline security requirement, not an optional policy rule | Make it a configurable rule like the others -- risks operators accidentally disabling it |

## Alternative approaches

### Approach B: Rule engine with pluggable check functions

```python
RULE_REGISTRY: dict[str, Callable] = {}

def rule(name: str):
    def decorator(fn):
        RULE_REGISTRY[name] = fn
        return fn
    return decorator

@rule("max_permissions")
def _check_max(acct, params):
    # ...

def run_checks(accounts, rules):
    for acct in accounts:
        for rule in rules:
            check_fn = RULE_REGISTRY[rule.check]
            check_fn(acct, rule.params)
```

**Trade-off:** A decorator-based rule registry makes adding new checks trivial (just decorate a function) and eliminates the if/elif chain. But the indirection makes the code harder to follow for learners who are still building mental models of decorators.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Naming pattern with invalid regex (e.g. `"[invalid"`) | `re.error` crashes `check_naming` | Wrap `re.match()` in try/except for `re.error`; report as a rule configuration violation |
| `key_created_at` is in the far future | Negative age_days; check passes even though the timestamp is suspicious | Clamp negative ages to zero and log a warning about the anomalous timestamp |
| Account has zero permissions | Passes `max_permissions` check (0 <= max), but an account with no permissions is likely misconfigured | Add a `min_permissions` rule or flag zero-permission accounts as suspicious |
