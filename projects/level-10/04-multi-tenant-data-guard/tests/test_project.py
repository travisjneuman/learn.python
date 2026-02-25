"""Tests for Multi-Tenant Data Guard.

Covers tenant isolation, role-based access, cross-tenant blocking,
super-admin bypass, audit logging, and permission edge cases.
"""
from __future__ import annotations

import pytest

from project import (
    Permission,
    PermissionDeniedError,
    Role,
    TenantAwareStore,
    TenantContext,
    TenantViolationError,
    create_guarded_store,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def store() -> TenantAwareStore:
    return create_guarded_store()


@pytest.fixture
def acme_editor() -> TenantContext:
    return TenantContext("acme", "alice", Role.EDITOR)


@pytest.fixture
def globex_editor() -> TenantContext:
    return TenantContext("globex", "bob", Role.EDITOR)


@pytest.fixture
def acme_viewer() -> TenantContext:
    return TenantContext("acme", "carol", Role.VIEWER)


@pytest.fixture
def super_admin() -> TenantContext:
    return TenantContext("system", "admin", Role.SUPER_ADMIN)


# ---------------------------------------------------------------------------
# Tenant isolation
# ---------------------------------------------------------------------------

class TestTenantIsolation:
    def test_tenant_sees_own_records(
        self, store: TenantAwareStore, acme_editor: TenantContext, globex_editor: TenantContext
    ) -> None:
        store.insert(acme_editor, "r1", {"val": 1})
        store.insert(globex_editor, "r2", {"val": 2})
        assert len(store.list_records(acme_editor)) == 1
        assert len(store.list_records(globex_editor)) == 1

    def test_cross_tenant_read_blocked(
        self, store: TenantAwareStore, acme_editor: TenantContext, globex_editor: TenantContext
    ) -> None:
        store.insert(globex_editor, "r1", {"secret": True})
        with pytest.raises(TenantViolationError):
            store.get(acme_editor, "r1")

    def test_cross_tenant_delete_blocked(
        self, store: TenantAwareStore, acme_editor: TenantContext, globex_editor: TenantContext
    ) -> None:
        store.insert(globex_editor, "r1", {"val": 1})
        acme_admin = TenantContext("acme", "admin", Role.ADMIN)
        with pytest.raises(TenantViolationError):
            store.delete(acme_admin, "r1")


# ---------------------------------------------------------------------------
# Role-based access
# ---------------------------------------------------------------------------

class TestRoleBasedAccess:
    def test_viewer_cannot_write(self, store: TenantAwareStore, acme_viewer: TenantContext) -> None:
        with pytest.raises(PermissionDeniedError):
            store.insert(acme_viewer, "r1", {"val": 1})

    def test_viewer_can_read(
        self, store: TenantAwareStore, acme_editor: TenantContext, acme_viewer: TenantContext
    ) -> None:
        store.insert(acme_editor, "r1", {"val": 1})
        record = store.get(acme_viewer, "r1")
        assert record is not None
        assert record.data["val"] == 1

    def test_editor_cannot_delete(self, store: TenantAwareStore, acme_editor: TenantContext) -> None:
        store.insert(acme_editor, "r1", {"val": 1})
        with pytest.raises(PermissionDeniedError):
            store.delete(acme_editor, "r1")

    @pytest.mark.parametrize("role,perm,expected", [
        (Role.VIEWER, Permission.READ, True),
        (Role.VIEWER, Permission.WRITE, False),
        (Role.EDITOR, Permission.WRITE, True),
        (Role.EDITOR, Permission.DELETE, False),
        (Role.ADMIN, Permission.DELETE, True),
    ])
    def test_permission_matrix(self, role: Role, perm: Permission, expected: bool) -> None:
        ctx = TenantContext("t1", "u1", role)
        assert ctx.has_permission(perm) == expected


# ---------------------------------------------------------------------------
# Super admin
# ---------------------------------------------------------------------------

class TestSuperAdmin:
    def test_super_admin_sees_all_tenants(
        self, store: TenantAwareStore, acme_editor: TenantContext,
        globex_editor: TenantContext, super_admin: TenantContext
    ) -> None:
        store.insert(acme_editor, "r1", {})
        store.insert(globex_editor, "r2", {})
        all_records = store.list_records(super_admin)
        assert len(all_records) == 2

    def test_super_admin_can_read_any_record(
        self, store: TenantAwareStore, acme_editor: TenantContext, super_admin: TenantContext
    ) -> None:
        store.insert(acme_editor, "r1", {"data": "secret"})
        record = store.get(super_admin, "r1")
        assert record is not None


# ---------------------------------------------------------------------------
# Audit logging
# ---------------------------------------------------------------------------

class TestAuditLog:
    def test_operations_logged(self, store: TenantAwareStore, acme_editor: TenantContext) -> None:
        store.insert(acme_editor, "r1", {"val": 1})
        store.list_records(acme_editor)
        assert len(store.audit_log) == 2
        assert store.audit_log[0]["action"] == "INSERT"
        assert store.audit_log[1]["action"] == "LIST"

    def test_audit_captures_tenant_info(self, store: TenantAwareStore, acme_editor: TenantContext) -> None:
        store.insert(acme_editor, "r1", {})
        entry = store.audit_log[0]
        assert entry["tenant_id"] == "acme"
        assert entry["user_id"] == "alice"
