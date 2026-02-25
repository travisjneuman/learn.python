"""Enterprise Python Blueprint — Project template generator with enterprise standards.

Architecture: Uses the Strategy pattern for pluggable template generators and a
Registry for discovering and composing project components. Each generator produces
files for a specific concern (logging, config, testing, CI) so teams can mix and
match based on their compliance tier.

Design rationale: Real enterprise projects need consistent scaffolding across dozens
of microservices. A code-driven generator ensures every new service starts with the
same logging format, config schema, test harness, and CI pipeline — eliminating
"snowflake services" that drift from organizational standards.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Protocol, TypeVar

T = TypeVar("T", bound="FileGenerator")


# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

class ComplianceTier(Enum):
    """How strict the generated project must be."""
    BASIC = auto()
    STANDARD = auto()
    STRICT = auto()


@dataclass(frozen=True)
class ProjectSpec:
    """Immutable specification for a project to generate."""
    name: str
    language: str
    tier: ComplianceTier
    owners: list[str] = field(default_factory=list)
    description: str = ""

    def __post_init__(self) -> None:
        if not self.name.replace("-", "").replace("_", "").isalnum():
            raise ValueError(f"Invalid project name: {self.name!r}")


@dataclass
class GeneratedFile:
    """A single file produced by a generator."""
    relative_path: str
    content: str
    executable: bool = False


# ---------------------------------------------------------------------------
# Strategy pattern — pluggable file generators
# ---------------------------------------------------------------------------

class FileGenerator(Protocol):
    """Strategy interface for producing project scaffold files."""

    def name(self) -> str: ...
    def generate(self, spec: ProjectSpec) -> list[GeneratedFile]: ...


class LoggingGenerator:
    """Produces structured logging configuration."""

    def name(self) -> str:
        return "logging"

    def generate(self, spec: ProjectSpec) -> list[GeneratedFile]:
        log_level = "DEBUG" if spec.tier == ComplianceTier.STRICT else "INFO"
        config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json": {
                    "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
                    "class": "logging.Formatter",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                    "level": log_level,
                }
            },
            "root": {"level": log_level, "handlers": ["console"]},
        }
        return [GeneratedFile("logging_config.json", json.dumps(config, indent=2))]


class ConfigGenerator:
    """Produces application config skeleton with environment overrides."""

    def name(self) -> str:
        return "config"

    def generate(self, spec: ProjectSpec) -> list[GeneratedFile]:
        config = {
            "app_name": spec.name,
            "environment": "development",
            "debug": spec.tier == ComplianceTier.BASIC,
            "owners": spec.owners,
            "secrets_backend": "env" if spec.tier == ComplianceTier.BASIC else "vault",
        }
        return [GeneratedFile("config/settings.json", json.dumps(config, indent=2))]


class TestHarnessGenerator:
    """Produces pytest configuration and sample test."""

    def name(self) -> str:
        return "testing"

    def generate(self, spec: ProjectSpec) -> list[GeneratedFile]:
        files: list[GeneratedFile] = []
        ini_lines = ["[pytest]", "testpaths = tests", "addopts = -v --tb=short"]
        if spec.tier in (ComplianceTier.STANDARD, ComplianceTier.STRICT):
            ini_lines.append("  --strict-markers")
        files.append(GeneratedFile("pytest.ini", "\n".join(ini_lines)))
        sample_test = (
            f'"""Auto-generated smoke test for {spec.name}."""\n\n'
            "def test_smoke() -> None:\n"
            "    assert True\n"
        )
        files.append(GeneratedFile("tests/test_smoke.py", sample_test))
        return files


class CIGenerator:
    """Produces CI pipeline definition (GitHub Actions style)."""

    def name(self) -> str:
        return "ci"

    def generate(self, spec: ProjectSpec) -> list[GeneratedFile]:
        steps = ["checkout", "setup-python", "install-deps", "lint", "test"]
        if spec.tier == ComplianceTier.STRICT:
            steps.extend(["security-scan", "compliance-check"])
        pipeline = {
            "name": f"CI — {spec.name}",
            "on": {"push": {"branches": ["main"]}, "pull_request": {}},
            "jobs": {
                "build": {
                    "runs-on": "ubuntu-latest",
                    "steps": steps,
                }
            },
        }
        return [GeneratedFile(".github/workflows/ci.yml", json.dumps(pipeline, indent=2))]


# ---------------------------------------------------------------------------
# Generator registry — discovers and composes generators
# ---------------------------------------------------------------------------

class GeneratorRegistry:
    """Registry that collects generators and orchestrates blueprint creation."""

    def __init__(self) -> None:
        self._generators: list[FileGenerator] = []

    def register(self, gen: FileGenerator) -> None:
        self._generators.append(gen)

    @property
    def generator_names(self) -> list[str]:
        return [g.name() for g in self._generators]

    def generate_blueprint(self, spec: ProjectSpec) -> Blueprint:
        """Run every registered generator against the spec."""
        all_files: list[GeneratedFile] = []
        manifest_entries: list[dict[str, str]] = []
        for gen in self._generators:
            files = gen.generate(spec)
            all_files.extend(files)
            for f in files:
                manifest_entries.append({"generator": gen.name(), "path": f.relative_path})
        # Always add a manifest so teams know what was generated.
        manifest = GeneratedFile(
            "MANIFEST.json",
            json.dumps({"project": spec.name, "files": manifest_entries}, indent=2),
        )
        all_files.append(manifest)
        return Blueprint(spec=spec, files=all_files)


@dataclass
class Blueprint:
    """Complete output of the generation process."""
    spec: ProjectSpec
    files: list[GeneratedFile]

    @property
    def file_count(self) -> int:
        return len(self.files)

    @property
    def paths(self) -> list[str]:
        return [f.relative_path for f in self.files]

    def write_to(self, root: Path) -> int:
        """Persist all files under *root*. Returns count written."""
        written = 0
        for gf in self.files:
            target = root / gf.relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(gf.content, encoding="utf-8")
            written += 1
        return written


# ---------------------------------------------------------------------------
# Convenience factory
# ---------------------------------------------------------------------------

def build_default_registry() -> GeneratorRegistry:
    """Pre-load the standard set of enterprise generators."""
    registry = GeneratorRegistry()
    registry.register(LoggingGenerator())
    registry.register(ConfigGenerator())
    registry.register(TestHarnessGenerator())
    registry.register(CIGenerator())
    return registry


def generate_project(
    name: str,
    tier: str = "STANDARD",
    owners: list[str] | None = None,
    output_dir: Path | None = None,
) -> Blueprint:
    """High-level API: generate an enterprise blueprint and optionally write it."""
    spec = ProjectSpec(
        name=name,
        language="python",
        tier=ComplianceTier[tier.upper()],
        owners=owners or [],
    )
    registry = build_default_registry()
    blueprint = registry.generate_blueprint(spec)
    if output_dir is not None:
        blueprint.write_to(output_dir)
    return blueprint


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Enterprise Python Blueprint Generator")
    parser.add_argument("name", help="Project name (alphanumeric, hyphens, underscores)")
    parser.add_argument("--tier", choices=["basic", "standard", "strict"], default="standard")
    parser.add_argument("--owners", nargs="*", default=[])
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()

    bp = generate_project(args.name, tier=args.tier, owners=args.owners, output_dir=args.output_dir)
    print(f"Generated {bp.file_count} files for '{bp.spec.name}' (tier={bp.spec.tier.name}):")
    for path in bp.paths:
        print(f"  {path}")


if __name__ == "__main__":
    main()
