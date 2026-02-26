# Solution: Level 10 / Project 04 - Multi Tenant Data Guard

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
>.

---

## Complete solution

```python
"""Multi-Tenant Data Guard -- Data isolation and access control for SaaS systems."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, TypeVar

T = TypeVar("T")


class Role(Enum):
    VIEWER = auto()
    EDITOR = auto()
    ADMIN = auto()
    SUPER_ADMIN = auto()


class Permission(Enum):
    READ = auto()
    WRITE = auto()
    DELETE = auto()
    ADMIN = auto()


# WHY declarative permission matrix? -- Defining roles as data makes the access
# model auditable at a glance. Security reviewers can verify the matrix without
# reading code. SUPER_ADMIN gets the same permissions as ADMIN but with cross-
# tenant access handled separately in TenantContext -- separation of concerns.
ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.VIEWER: {Permission.READ},
    Role.EDITOR: {Permission.READ, Permission.WRITE},
    Role.ADMIN: {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN},
    Role.SUPER_ADMIN: {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN},
}


# WHY frozen=True? -- If tenant context could be mutated mid-request, an attacker
# could escalate privileges by changing tenant_id or role after the initial check.
# Freezing prevents this at the language level.
@dataclass(frozen=True)
class TenantContext:
    tenant_id: str
    user_id: str
    role: Role

    def has_permission(self, perm: Permission) -> bool:
        return perm in ROLE_PERMISSIONS.get(self.role, set())

    @property
    def is_super_admin(self) -> bool:
        return self.role == Role.SUPER_ADMIN


class TenantViolationError(Exception):
    """Cross-tenant data access attempted."""

class PermissionDeniedError(Exception):
    """User lacks required permission."""


@dataclass
class Record:
    id: str
    tenant_id: str
    data: dict[str, Any]


class DataStore:
    """Raw in-memory store -- no access control. Should never be used directly."""
    def __init__(self) -> None:
        self._records: dict[str, Record] = {}

    def insert(self, record: Record) -> None:
        self._records[record.id] = record

    def get(self, record_id: str) -> Record | None:
        return self._records.get(record_id)

    def list_all(self) -> list[Record]:
        return list(self._records.values())

    def delete(self, record_id: str) -> bool:
        return self._records.pop(record_id, None) is not None

    @property
    def count(self) -> int:
        return len(self._records)


# WHY Proxy pattern instead of middleware? -- Middleware can be bypassed by calling
# the store directly. The Proxy wraps the store so there is no way to access data
# without going through tenant checks. This makes isolation structural, not optional.
class TenantAwareStore:
    def __init__(self, store: DataStore) -> None:
        self._store = store
        self._audit_log: list[dict[str, str]] = []

    # WHY log all access, including denied? -- Failed access attempts are security
    # signals. If someone repeatedly tries to access another tenant's data, that
    # pattern should be visible in the audit log for incident response.
    def _audit(self, ctx: TenantContext, action: str, target: str) -> None:
        self._audit_log.append({
            "tenant_id": ctx.tenant_id, "user_id": ctx.user_id,
            "action": action, "target": target,
        })

    @property
    def audit_log(self) -> list[dict[str, str]]:
        return list(self._audit_log)

    def _require_permission(self, ctx: TenantContext, perm: Permission) -> None:
        if not ctx.has_permission(perm):
            raise PermissionDeniedError(
                f"User '{ctx.user_id}' (role={ctx.role.name}) lacks {perm.name} permission")

    def _check_tenant(self, ctx: TenantContext, record: Record) -> None:
        if not ctx.is_super_admin and record.tenant_id != ctx.tenant_id:
            raise TenantViolationError(
                f"Tenant '{ctx.tenant_id}' cannot access record owned by '{record.tenant_id}'")

    # WHY auto-tag tenant_id on insert? -- The caller never sets tenant_id
    # manually. The proxy injects it from the context, preventing a developer
    # from accidentally (or maliciously) writing data under another tenant.
    def insert(self, ctx: TenantContext, record_id: str, data: dict[str, Any]) -> Record:
        self._require_permission(ctx, Permission.WRITE)
        record = Record(id=record_id, tenant_id=ctx.tenant_id, data=data)
        self._store.insert(record)
        self._audit(ctx, "INSERT", record_id)
        return record

    def get(self, ctx: TenantContext, record_id: str) -> Record | None:
        self._require_permission(ctx, Permission.READ)
        record = self._store.get(record_id)
        if record is None:
            return None
        self._check_tenant(ctx, record)
        self._audit(ctx, "READ", record_id)
        return record

    # WHY filter in list_records instead of raising? -- Listing should return
    # only the caller's records, not raise on every foreign record. Super admins
    # see everything for audit purposes.
    def list_records(self, ctx: TenantContext) -> list[Record]:
        self._require_permission(ctx, Permission.READ)
        all_records = self._store.list_all()
        if ctx.is_super_admin:
            self._audit(ctx, "LIST_ALL", f"{len(all_records)} records")
            return all_records
        filtered = [r for r in all_records if r.tenant_id == ctx.tenant_id]
        self._audit(ctx, "LIST", f"{len(filtered)} records")
        return filtered

    def delete(self, ctx: TenantContext, record_id: str) -> bool:
        self._require_permission(ctx, Permission.DELETE)
        record = self._store.get(record_id)
        if record is None:
            return False
        self._check_tenant(ctx, record)
        result = self._store.delete(record_id)
        self._audit(ctx, "DELETE", record_id)
        return result


def create_guarded_store() -> TenantAwareStore:
    return TenantAwareStore(DataStore())


def main() -> None:
    store = create_guarded_store()
    acme = TenantContext("acme", "alice", Role.EDITOR)
    globex = TenantContext("globex", "bob", Role.EDITOR)
    superuser = TenantContext("system", "admin", Role.SUPER_ADMIN)

    store.insert(acme, "inv-001", {"amount": 100, "status": "paid"})
    store.insert(acme, "inv-002", {"amount": 250, "status": "pending"})
    store.insert(globex, "inv-003", {"amount": 500, "status": "paid"})

    print(f"Acme sees {len(store.list_records(acme))} records")
    print(f"Super admin sees {len(store.list_records(superuser))} records")

    try:
        store.get(acme, "inv-003")
    except TenantViolationError as e:
        print(f"Blocked: {e}")

    print(f"\nAudit log ({len(store.audit_log)} entries):")
    for entry in store.audit_log:
        print(f"  [{entry['tenant_id']}] {entry['user_id']} -> {entry['action']} {entry['target']}")


if __name__ == "__main__":
    main()
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Proxy pattern wrapping DataStore | Makes tenant isolation structural -- impossible to bypass since there is no public access to the raw store | Middleware filtering -- can be accidentally skipped by calling the store directly |
| Frozen TenantContext | Prevents privilege escalation by mutating tenant_id or role mid-request | Mutable context with validation on each use -- more error-prone |
| Auto-tagging tenant_id on insert | Eliminates a class of bugs where developers manually set the wrong tenant | Manual tenant_id parameter -- opens the door to cross-tenant writes |
| Audit log records both successes and denials | Failed access attempts are security signals for incident detection | Log only successes -- misses attack patterns |
| SUPER_ADMIN cross-tenant at context level, not permission level | Keeps permission matrix simple; cross-tenant access is a separate concern | Add a CROSS_TENANT permission -- mixes two orthogonal concepts |

## Alternative approaches

### Approach B: SQL WHERE clause injection for database-backed stores

```python
class SQLTenantStore:
    def __init__(self, connection, ctx: TenantContext):
        self._conn = connection
        self._ctx = ctx

    def list_records(self) -> list[dict]:
        # WHY always inject WHERE? -- This is the "mandatory filter" pattern.
        # Every query goes through this method, so tenant isolation is guaranteed.
        query = "SELECT * FROM records WHERE tenant_id = ?"
        return self._conn.execute(query, (self._ctx.tenant_id,)).fetchall()
```

**Trade-off:** SQL-level filtering scales better than in-memory filtering for large datasets since the database handles the filtering. However, it requires trust in the ORM/query layer. The in-memory proxy is better for learning the isolation concept; the SQL approach is better for production.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| VIEWER attempts an insert | `PermissionDeniedError` raised before any data operation | Check role permissions in the API layer before calling the store |
| Accessing a record owned by another tenant | `TenantViolationError` with descriptive message | Use `list_records` (filtered) instead of `get` (individual) when possible |
| Audit log grows unbounded in long-running processes | Memory leak as entries accumulate | Add a max-size ring buffer or flush to persistent storage periodically |
