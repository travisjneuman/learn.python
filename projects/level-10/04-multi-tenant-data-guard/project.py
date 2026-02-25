"""Multi-Tenant Data Guard — Data isolation and access control for multi-tenant systems.

Architecture: Implements row-level security through a TenantContext that flows
through every data operation. Uses the Proxy pattern: a TenantAwareStore wraps
a raw data store and injects tenant filtering on every read/write. An AccessPolicy
layer adds role-based permissions on top of tenant isolation.

Design rationale: In SaaS systems, tenant data leakage is a catastrophic failure.
By making tenant context mandatory at the data-access layer — not optional
middleware — the system makes cross-tenant access structurally impossible rather
than relying on developers remembering to filter.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, TypeVar

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

class Role(Enum):
    VIEWER = auto()
    EDITOR = auto()
    ADMIN = auto()
    SUPER_ADMIN = auto()  # Cross-tenant access


class Permission(Enum):
    READ = auto()
    WRITE = auto()
    DELETE = auto()
    ADMIN = auto()


# Role -> permissions mapping
ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.VIEWER: {Permission.READ},
    Role.EDITOR: {Permission.READ, Permission.WRITE},
    Role.ADMIN: {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN},
    Role.SUPER_ADMIN: {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN},
}


@dataclass(frozen=True)
class TenantContext:
    """Immutable context that identifies the current tenant and user."""
    tenant_id: str
    user_id: str
    role: Role

    def has_permission(self, perm: Permission) -> bool:
        return perm in ROLE_PERMISSIONS.get(self.role, set())

    @property
    def is_super_admin(self) -> bool:
        return self.role == Role.SUPER_ADMIN


class TenantViolationError(Exception):
    """Raised when a cross-tenant data access is attempted."""


class PermissionDeniedError(Exception):
    """Raised when the user lacks required permission."""


# ---------------------------------------------------------------------------
# In-memory data store (simulates database)
# ---------------------------------------------------------------------------

@dataclass
class Record:
    """A single data record tagged with its owning tenant."""
    id: str
    tenant_id: str
    data: dict[str, Any]


class DataStore:
    """Raw in-memory store — no access control. Should never be used directly."""

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


# ---------------------------------------------------------------------------
# Tenant-aware proxy (Proxy pattern)
# ---------------------------------------------------------------------------

class TenantAwareStore:
    """Proxy that enforces tenant isolation and role-based access control.

    Every operation requires a TenantContext. The proxy ensures:
    1. Reads only return records belonging to the caller's tenant
    2. Writes tag records with the caller's tenant
    3. Deletes only affect the caller's tenant
    4. Super-admins can bypass tenant filtering (audit use cases)
    """

    def __init__(self, store: DataStore) -> None:
        self._store = store
        self._audit_log: list[dict[str, str]] = []

    def _audit(self, ctx: TenantContext, action: str, target: str) -> None:
        self._audit_log.append({
            "tenant_id": ctx.tenant_id,
            "user_id": ctx.user_id,
            "action": action,
            "target": target,
        })

    @property
    def audit_log(self) -> list[dict[str, str]]:
        return list(self._audit_log)

    def _require_permission(self, ctx: TenantContext, perm: Permission) -> None:
        if not ctx.has_permission(perm):
            raise PermissionDeniedError(
                f"User '{ctx.user_id}' (role={ctx.role.name}) lacks {perm.name} permission"
            )

    def _check_tenant(self, ctx: TenantContext, record: Record) -> None:
        if not ctx.is_super_admin and record.tenant_id != ctx.tenant_id:
            raise TenantViolationError(
                f"Tenant '{ctx.tenant_id}' cannot access record owned by '{record.tenant_id}'"
            )

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


# ---------------------------------------------------------------------------
# Convenience factory
# ---------------------------------------------------------------------------

def create_guarded_store() -> TenantAwareStore:
    """Create a fresh tenant-aware store for use."""
    return TenantAwareStore(DataStore())


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

def main() -> None:
    store = create_guarded_store()

    # Simulate two tenants inserting data
    acme = TenantContext("acme", "alice", Role.EDITOR)
    globex = TenantContext("globex", "bob", Role.EDITOR)
    superuser = TenantContext("system", "admin", Role.SUPER_ADMIN)

    store.insert(acme, "inv-001", {"amount": 100, "status": "paid"})
    store.insert(acme, "inv-002", {"amount": 250, "status": "pending"})
    store.insert(globex, "inv-003", {"amount": 500, "status": "paid"})

    # Acme can only see their records
    acme_records = store.list_records(acme)
    print(f"Acme sees {len(acme_records)} records")

    # Super admin sees all
    all_records = store.list_records(superuser)
    print(f"Super admin sees {len(all_records)} records")

    # Cross-tenant access blocked
    try:
        store.get(acme, "inv-003")
    except TenantViolationError as e:
        print(f"Blocked: {e}")

    print(f"\nAudit log ({len(store.audit_log)} entries):")
    for entry in store.audit_log:
        print(f"  [{entry['tenant_id']}] {entry['user_id']} -> {entry['action']} {entry['target']}")


if __name__ == "__main__":
    main()
