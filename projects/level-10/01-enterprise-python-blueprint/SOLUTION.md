# Solution: Level 10 / Project 01 - Enterprise Python Blueprint

> **STOP** -- Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> Check the [README](./README.md) for requirements and the
> [Walkthrough](./WALKTHROUGH.md) for guided hints.

---

## Complete solution

```python
"""Enterprise Python Blueprint -- Project template generator with enterprise standards."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Protocol, TypeVar

T = TypeVar("T", bound="FileGenerator")


# WHY Enum for compliance tiers? -- Using an Enum instead of raw strings prevents
# typos like "standarrd" from silently producing wrong output. The Enum also makes
# the set of valid tiers discoverable via IDE autocomplete.
class ComplianceTier(Enum):
    BASIC = auto()
    STANDARD = auto()
    STRICT = auto()


# WHY frozen=True? -- The spec is a contract between the caller and all generators.
# If a generator could mutate the spec mid-generation, downstream generators would
# receive corrupted input. Freezing the dataclass enforces this at the language level.
@dataclass(frozen=True)
class ProjectSpec:
    name: str
    language: str
    tier: ComplianceTier
    owners: list[str] = field(default_factory=list)
    description: str = ""

    # WHY validate in __post_init__? -- Catching invalid project names at construction
    # time means no invalid ProjectSpec can ever exist. This is the "make illegal
    # states unrepresentable" principle.
    def __post_init__(self) -> None:
        if not self.name.replace("-", "").replace("_", "").isalnum():
            raise ValueError(f"Invalid project name: {self.name!r}")


@dataclass
class GeneratedFile:
    relative_path: str
    content: str
    executable: bool = False


# WHY a Protocol instead of ABC? -- Protocol enables structural subtyping (duck typing
# with type-checker support). Any class with name() and generate() methods satisfies
# the interface -- no inheritance required. This keeps generators decoupled from the
# framework and lets third-party generators plug in without importing anything.
class FileGenerator(Protocol):
    def name(self) -> str: ...
    def generate(self, spec: ProjectSpec) -> list[GeneratedFile]: ...


class LoggingGenerator:
    def name(self) -> str:
        return "logging"

    # WHY tier-dependent log level? -- STRICT tier needs DEBUG-level logging for
    # audit trails. BASIC/STANDARD use INFO to avoid noisy logs in development.
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
    def name(self) -> str:
        return "config"

    # WHY secrets_backend varies by tier? -- BASIC projects use env vars (simple).
    # STANDARD and STRICT use Vault (secure). This enforces security posture at
    # the scaffolding level rather than leaving it to individual developers.
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
    def name(self) -> str:
        return "testing"

    def generate(self, spec: ProjectSpec) -> list[GeneratedFile]:
        files: list[GeneratedFile] = []
        ini_lines = ["[pytest]", "testpaths = tests", "addopts = -v --tb=short"]
        # WHY --strict-markers for non-BASIC? -- Strict markers prevent typos in
        # pytest marker names from silently passing. BASIC skips this for simplicity.
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
    def name(self) -> str:
        return "ci"

    # WHY extra steps for STRICT? -- STRICT-tier services handle sensitive data
    # and need security scanning and compliance checks before every merge.
    def generate(self, spec: ProjectSpec) -> list[GeneratedFile]:
        steps = ["checkout", "setup-python", "install-deps", "lint", "test"]
        if spec.tier == ComplianceTier.STRICT:
            steps.extend(["security-scan", "compliance-check"])
        pipeline = {
            "name": f"CI — {spec.name}",
            "on": {"push": {"branches": ["main"]}, "pull_request": {}},
            "jobs": {"build": {"runs-on": "ubuntu-latest", "steps": steps}},
        }
        return [GeneratedFile(".github/workflows/ci.yml", json.dumps(pipeline, indent=2))]


class GeneratorRegistry:
    """Registry that collects generators and orchestrates blueprint creation."""

    def __init__(self) -> None:
        self._generators: list[FileGenerator] = []

    def register(self, gen: FileGenerator) -> None:
        self._generators.append(gen)

    @property
    def generator_names(self) -> list[str]:
        return [g.name() for g in self._generators]

    # WHY manifest generated last? -- The manifest records what was generated.
    # It must be created after all generators run so it accurately reflects
    # the complete file list.
    def generate_blueprint(self, spec: ProjectSpec) -> Blueprint:
        all_files: list[GeneratedFile] = []
        manifest_entries: list[dict[str, str]] = []
        for gen in self._generators:
            files = gen.generate(spec)
            all_files.extend(files)
            for f in files:
                manifest_entries.append({"generator": gen.name(), "path": f.relative_path})
        manifest = GeneratedFile(
            "MANIFEST.json",
            json.dumps({"project": spec.name, "files": manifest_entries}, indent=2),
        )
        all_files.append(manifest)
        return Blueprint(spec=spec, files=all_files)


@dataclass
class Blueprint:
    spec: ProjectSpec
    files: list[GeneratedFile]

    @property
    def file_count(self) -> int:
        return len(self.files)

    @property
    def paths(self) -> list[str]:
        return [f.relative_path for f in self.files]

    # WHY mkdir(parents=True)? -- The generator creates nested paths like
    # "config/settings.json". Parent directories must be created automatically.
    def write_to(self, root: Path) -> int:
        written = 0
        for gf in self.files:
            target = root / gf.relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(gf.content, encoding="utf-8")
            written += 1
        return written


# WHY a factory function? -- build_default_registry encapsulates the "which
# generators are standard." Callers get a fully configured registry without
# knowing the individual generator classes. Adding a new generator means
# changing one function, not every call site.
def build_default_registry() -> GeneratorRegistry:
    registry = GeneratorRegistry()
    registry.register(LoggingGenerator())
    registry.register(ConfigGenerator())
    registry.register(TestHarnessGenerator())
    registry.register(CIGenerator())
    return registry


# WHY tier as string in the public API? -- CLI users pass strings. Converting
# to ComplianceTier[tier.upper()] inside this function keeps the boundary clean:
# callers work with strings, internals work with type-safe enums.
def generate_project(
    name: str,
    tier: str = "STANDARD",
    owners: list[str] | None = None,
    output_dir: Path | None = None,
) -> Blueprint:
    spec = ProjectSpec(
        name=name, language="python",
        tier=ComplianceTier[tier.upper()], owners=owners or [],
    )
    registry = build_default_registry()
    blueprint = registry.generate_blueprint(spec)
    if output_dir is not None:
        blueprint.write_to(output_dir)
    return blueprint


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
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Protocol-based FileGenerator interface | Enables duck-typed extensibility -- new generators work without inheriting from a base class | Abstract base class (ABC) -- forces inheritance coupling |
| Frozen ProjectSpec dataclass | Prevents generators from accidentally mutating the shared spec during generation | Mutable dataclass with defensive copies -- more error-prone, less explicit |
| MANIFEST.json generated last | Accurately reflects all generated files since it is built after all generators run | Generate manifest first and update it -- requires two passes |
| Factory function for default registry | Centralizes "which generators are standard" in one place, easy to extend | Hard-coded list in generate_project -- mixes orchestration with configuration |
| Enum for ComplianceTier | Type-safe, IDE-discoverable, prevents string typos like "standarrd" | Raw string constants -- no validation at assignment time |

## Alternative approaches

### Approach B: Template-file-based generation (Jinja2)

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates/"))

def generate_from_template(spec: ProjectSpec) -> list[GeneratedFile]:
    files = []
    for template_name in env.list_templates():
        rendered = env.get_template(template_name).render(spec=spec)
        files.append(GeneratedFile(template_name, rendered))
    return files
```

**Trade-off:** Jinja2 templates are more readable for non-Python content (YAML, Dockerfiles) and let non-engineers edit templates. However, they lose type safety, IDE support, and testability that Python generators provide. Use templates for large projects with many file types; use code generators when compliance logic is complex.

## Common pitfalls

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Project name with spaces: `"my service"` | `ValueError` raised in `__post_init__` | Sanitize input with a slugify function before constructing ProjectSpec |
| Unknown tier string: `"enterprise"` | `KeyError` from `ComplianceTier[tier.upper()]` | Wrap in try/except and show valid choices |
| No generators registered | Blueprint has only a MANIFEST with empty files list | Add a guard in `generate_blueprint` requiring at least one generator |
