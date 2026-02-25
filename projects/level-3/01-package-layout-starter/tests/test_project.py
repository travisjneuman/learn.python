"""Tests for Package Layout Starter.

Uses pytest fixtures for temporary package structures.
"""

from pathlib import Path

import pytest

from project import (
    PackageInfo,
    generate_init_py,
    scan_module,
    scan_package,
    validate_package,
)


@pytest.fixture
def sample_package(tmp_path: Path) -> Path:
    """Create a minimal Python package structure."""
    pkg = tmp_path / "mypackage"
    pkg.mkdir()
    (pkg / "__init__.py").write_text('"""My package."""\n', encoding="utf-8")
    (pkg / "utils.py").write_text(
        "def helper():\n    return 42\n\nclass Tool:\n    pass\n",
        encoding="utf-8",
    )
    (pkg / "core.py").write_text(
        "import json\nfrom pathlib import Path\n\ndef run():\n    pass\n",
        encoding="utf-8",
    )
    return pkg


def test_scan_package(sample_package: Path) -> None:
    """Scanning should detect modules and __init__.py."""
    info = scan_package(sample_package)
    assert info.name == "mypackage"
    assert "utils" in info.modules
    assert "core" in info.modules


def test_scan_package_missing(tmp_path: Path) -> None:
    """Missing directory should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        scan_package(tmp_path / "nope")


def test_scan_module(sample_package: Path) -> None:
    """Module scanning should detect functions and classes."""
    info = scan_module(sample_package / "utils.py")
    assert "helper" in info.functions
    assert "Tool" in info.classes


def test_package_info_dataclass() -> None:
    """PackageInfo should be a proper dataclass."""
    info = PackageInfo(name="test", version="1.0.0", modules=["a", "b"])
    d = info.to_dict()
    assert d["name"] == "test"
    assert d["version"] == "1.0.0"


def test_generate_init_py() -> None:
    """Generated __init__.py should have __version__ and __all__."""
    info = PackageInfo(name="pkg", modules=["core", "utils"])
    content = generate_init_py(info)
    assert "__version__" in content
    assert "__all__" in content
    assert '"core"' in content


def test_validate_package_valid(sample_package: Path) -> None:
    """A properly structured package should have no errors."""
    issues = validate_package(sample_package)
    errors = [i for i in issues if i["severity"] == "error"]
    assert len(errors) == 0


def test_validate_package_no_init(tmp_path: Path) -> None:
    """A directory without __init__.py should report an error."""
    pkg = tmp_path / "bad_pkg"
    pkg.mkdir()
    (pkg / "module.py").write_text("x = 1\n", encoding="utf-8")
    issues = validate_package(pkg)
    assert any("__init__.py" in i["message"] for i in issues)
