"""Tests for Fill-In Challenge #5 — Basic Class."""

from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import pytest

_spec = spec_from_file_location("ex05", Path(__file__).parent.parent / "05_basic_class.py")
_mod = module_from_spec(_spec)
_spec.loader.exec_module(_mod)

BankAccount = _mod.BankAccount


class TestBankAccountInit:
    def test_default_balance(self):
        acc = BankAccount("Alice")
        assert acc.owner == "Alice"
        assert acc.balance == 0.0

    def test_custom_balance(self):
        acc = BankAccount("Bob", 100.0)
        assert acc.balance == 100.0


class TestBankAccountStr:
    def test_str(self):
        acc = BankAccount("Alice", 150.0)
        assert str(acc) == "BankAccount(Alice, $150.00)"

    def test_str_zero(self):
        acc = BankAccount("Bob")
        assert str(acc) == "BankAccount(Bob, $0.00)"


class TestDeposit:
    def test_basic(self):
        acc = BankAccount("Alice")
        result = acc.deposit(50.0)
        assert result == 50.0
        assert acc.balance == 50.0

    def test_negative_raises(self):
        acc = BankAccount("Alice")
        with pytest.raises(ValueError):
            acc.deposit(-10)

    def test_zero_raises(self):
        acc = BankAccount("Alice")
        with pytest.raises(ValueError):
            acc.deposit(0)


class TestWithdraw:
    def test_basic(self):
        acc = BankAccount("Alice", 100.0)
        result = acc.withdraw(30.0)
        assert result == 70.0

    def test_overdraft_raises(self):
        acc = BankAccount("Alice", 10.0)
        with pytest.raises(ValueError):
            acc.withdraw(20.0)

    def test_negative_raises(self):
        acc = BankAccount("Alice", 100.0)
        with pytest.raises(ValueError):
            acc.withdraw(-5)


class TestTransfer:
    def test_basic(self):
        a = BankAccount("Alice", 100.0)
        b = BankAccount("Bob", 50.0)
        result = a.transfer(b, 30.0)
        assert result == (70.0, 80.0)
        assert a.balance == 70.0
        assert b.balance == 80.0

    def test_insufficient_raises(self):
        a = BankAccount("Alice", 10.0)
        b = BankAccount("Bob")
        with pytest.raises(ValueError):
            a.transfer(b, 20.0)
