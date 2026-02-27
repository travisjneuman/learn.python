"""Tests for Token Rotation Simulator."""

from __future__ import annotations

import json
import time

import pytest

from project import Token, TokenManager, run


class TestTokenManager:
    def test_generate_creates_valid_token(self) -> None:
        mgr = TokenManager(ttl_seconds=3600)
        token = mgr.generate("t1")
        assert token.is_valid
        assert mgr.validate("t1")

    def test_revoke_invalidates(self) -> None:
        mgr = TokenManager()
        mgr.generate("t1")
        mgr.revoke("t1")
        assert not mgr.validate("t1")

    def test_rotate_revokes_old(self) -> None:
        mgr = TokenManager()
        old = mgr.generate("old")
        new = mgr.rotate()
        assert old.revoked
        assert new.is_valid
        assert mgr.current.token_id == new.token_id

    def test_expired_token_invalid(self) -> None:
        token = Token(token_id="t", value="v",
                      created_at=time.time() - 100,
                      expires_at=time.time() - 1)
        assert token.is_expired
        assert not token.is_valid

    @pytest.mark.parametrize("ops", [1, 3, 5])
    def test_multiple_rotations(self, ops: int) -> None:
        mgr = TokenManager()
        mgr.generate()
        for _ in range(ops):
            mgr.rotate()
        stats = mgr.stats()
        assert stats["active"] == 1
        assert stats["revoked"] >= ops

    def test_audit_log(self) -> None:
        mgr = TokenManager()
        mgr.generate("t1")
        mgr.rotate()
        assert len(mgr.audit_log) >= 3  # generate, revoke, generate, rotate


@pytest.mark.integration
def test_run_end_to_end(tmp_path) -> None:
    config = {"ttl_seconds": 3600, "operations": ["generate", "rotate"]}
    inp = tmp_path / "config.json"
    inp.write_text(json.dumps(config), encoding="utf-8")
    out = tmp_path / "out.json"
    summary = run(inp, out)
    assert summary["operations_run"] == 2
    assert summary["stats"]["active"] == 1
