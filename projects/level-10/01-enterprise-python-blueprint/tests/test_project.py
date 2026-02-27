"""Tests for Enterprise Python Blueprint generator.

Covers spec validation, individual generators, registry composition,
blueprint persistence, and compliance tier variations.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from project import (
    Blueprint,
    CIGenerator,
    ComplianceTier,
    ConfigGenerator,
    GeneratorRegistry,
    LoggingGenerator,
    ProjectSpec,
    TestHarnessGenerator,
    build_default_registry,
    generate_project,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def standard_spec() -> ProjectSpec:
    return ProjectSpec(name="billing-svc", language="python", tier=ComplianceTier.STANDARD, owners=["alice"])


@pytest.fixture
def strict_spec() -> ProjectSpec:
    return ProjectSpec(name="payment-gateway", language="python", tier=ComplianceTier.STRICT, owners=["bob", "carol"])


# ---------------------------------------------------------------------------
# Spec validation
# ---------------------------------------------------------------------------

class TestProjectSpec:
    def test_valid_name_accepted(self, standard_spec: ProjectSpec) -> None:
        assert standard_spec.name == "billing-svc"

    def test_invalid_name_rejected(self) -> None:
        with pytest.raises(ValueError, match="Invalid project name"):
            ProjectSpec(name="bad name!", language="python", tier=ComplianceTier.BASIC)


# ---------------------------------------------------------------------------
# Individual generators
# ---------------------------------------------------------------------------

class TestLoggingGenerator:
    def test_strict_tier_uses_debug_level(self, strict_spec: ProjectSpec) -> None:
        files = LoggingGenerator().generate(strict_spec)
        assert len(files) == 1
        assert '"DEBUG"' in files[0].content

    def test_basic_tier_uses_info_level(self) -> None:
        spec = ProjectSpec(name="demo", language="python", tier=ComplianceTier.BASIC)
        files = LoggingGenerator().generate(spec)
        assert '"INFO"' in files[0].content


class TestConfigGenerator:
    def test_strict_tier_uses_vault_backend(self, strict_spec: ProjectSpec) -> None:
        files = ConfigGenerator().generate(strict_spec)
        assert '"vault"' in files[0].content

    def test_basic_tier_enables_debug(self) -> None:
        spec = ProjectSpec(name="demo", language="python", tier=ComplianceTier.BASIC)
        files = ConfigGenerator().generate(spec)
        assert '"debug": true' in files[0].content


class TestCIGenerator:
    @pytest.mark.parametrize("tier,expected_step", [
        (ComplianceTier.STRICT, "security-scan"),
        (ComplianceTier.STANDARD, "test"),
    ])
    def test_ci_steps_vary_by_tier(self, tier: ComplianceTier, expected_step: str) -> None:
        spec = ProjectSpec(name="svc", language="python", tier=tier)
        files = CIGenerator().generate(spec)
        assert expected_step in files[0].content


# ---------------------------------------------------------------------------
# Registry and blueprint composition
# ---------------------------------------------------------------------------

class TestGeneratorRegistry:
    def test_default_registry_has_four_generators(self) -> None:
        registry = build_default_registry()
        assert len(registry.generator_names) == 4

    def test_blueprint_includes_manifest(self, standard_spec: ProjectSpec) -> None:
        registry = build_default_registry()
        bp = registry.generate_blueprint(standard_spec)
        assert "MANIFEST.json" in bp.paths


@pytest.mark.integration
class TestBlueprintPersistence:
    def test_write_creates_all_files(self, tmp_path: Path, standard_spec: ProjectSpec) -> None:
        registry = build_default_registry()
        bp = registry.generate_blueprint(standard_spec)
        written = bp.write_to(tmp_path)
        assert written == bp.file_count
        for rel in bp.paths:
            assert (tmp_path / rel).exists()


# ---------------------------------------------------------------------------
# High-level API
# ---------------------------------------------------------------------------

class TestGenerateProject:
    def test_generate_project_returns_blueprint(self) -> None:
        bp = generate_project("my-service", tier="basic")
        assert isinstance(bp, Blueprint)
        assert bp.file_count >= 5

    def test_generate_writes_to_disk(self, tmp_path: Path) -> None:
        bp = generate_project("disk-svc", tier="standard", output_dir=tmp_path)
        assert (tmp_path / "MANIFEST.json").exists()
        assert bp.spec.tier == ComplianceTier.STANDARD
