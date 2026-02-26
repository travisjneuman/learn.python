# Enterprise Python Blueprint — Step-by-Step Walkthrough

[<- Back to Project README](./README.md) · [Solution](./SOLUTION.md)

## Before You Start

Read the [project README](./README.md) first. Try to solve it on your own before following this guide. This project builds a code generator using the Strategy and Registry patterns -- the same approach that tools like Cookiecutter, `create-react-app`, and Yeoman use internally. Spend at least 30 minutes attempting it independently.

## Thinking Process

Every new microservice in an organization should start from the same baseline: consistent logging format, config schema, test harness, and CI pipeline. Without this, each team invents their own conventions, creating "snowflake services" that drift from organizational standards and become hard to operate at scale. This project solves that by generating scaffolding from code.

The architecture uses two patterns working together. The **Strategy pattern** defines a `FileGenerator` protocol -- any class with `name()` and `generate()` methods qualifies. Each generator produces files for one concern (logging, config, testing, CI). The **Registry pattern** collects generators and orchestrates them: "run every registered generator against this project spec and assemble the output." Adding a new generator (e.g., Dockerfile, CODEOWNERS) requires writing one class and one `registry.register()` call -- nothing else changes.

The third key concept is **immutable specification**. The `ProjectSpec` dataclass uses `frozen=True`, which means once you define a project's name, tier, and owners, nothing can change it during generation. This prevents subtle bugs where one generator modifies the spec and corrupts downstream generators.

## Step 1: Define the Domain Types

**What to do:** Create a `ComplianceTier` enum (BASIC, STANDARD, STRICT), a frozen `ProjectSpec` dataclass, and a `GeneratedFile` dataclass.

**Why:** The compliance tier controls how strict the generated output is. BASIC projects get debug mode and simple logging. STRICT projects get security scans, compliance checks, and vault-based secrets. The frozen spec prevents accidental mutation.

```python
class ComplianceTier(Enum):
    BASIC = auto()
    STANDARD = auto()
    STRICT = auto()


@dataclass(frozen=True)
class ProjectSpec:
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
    relative_path: str
    content: str
    executable: bool = False
```

Three details to notice:

- **`frozen=True` makes the dataclass immutable.** Any attempt to do `spec.name = "new-name"` raises `FrozenInstanceError`. This is a contract enforced by Python itself.
- **`__post_init__` validates at construction time.** Invalid project names are rejected before any generation happens, preventing invalid state from propagating through the system.
- **The validation allows hyphens, underscores, and alphanumeric characters.** `"billing-svc"` is valid. `"bad name!"` is not.

**Predict:** What happens if you try `ProjectSpec(name="my service", language="python", tier=ComplianceTier.BASIC)`? What about `"my-service"`?

## Step 2: Build the Strategy Interface and Generators

**What to do:** Define the `FileGenerator` protocol and implement four concrete generators: `LoggingGenerator`, `ConfigGenerator`, `TestHarnessGenerator`, and `CIGenerator`.

**Why:** The Protocol class defines the contract: any generator must have `name() -> str` and `generate(spec) -> list[GeneratedFile]`. Concrete generators implement this contract for different concerns. The compliance tier influences each generator differently -- the logging generator changes log level, the CI generator adds security scan steps, the config generator switches secrets backend.

```python
class FileGenerator(Protocol):
    def name(self) -> str: ...
    def generate(self, spec: ProjectSpec) -> list[GeneratedFile]: ...


class LoggingGenerator:
    def name(self) -> str:
        return "logging"

    def generate(self, spec: ProjectSpec) -> list[GeneratedFile]:
        log_level = "DEBUG" if spec.tier == ComplianceTier.STRICT else "INFO"
        config = {
            "version": 1,
            "root": {"level": log_level, "handlers": ["console"]},
            # ... formatters, handlers ...
        }
        return [GeneratedFile("logging_config.json", json.dumps(config, indent=2))]


class CIGenerator:
    def name(self) -> str:
        return "ci"

    def generate(self, spec: ProjectSpec) -> list[GeneratedFile]:
        steps = ["checkout", "setup-python", "install-deps", "lint", "test"]
        if spec.tier == ComplianceTier.STRICT:
            steps.extend(["security-scan", "compliance-check"])
        pipeline = {"name": f"CI — {spec.name}", "jobs": {"build": {"steps": steps}}}
        return [GeneratedFile(".github/workflows/ci.yml", json.dumps(pipeline, indent=2))]
```

The Protocol class is Python's structural typing. `LoggingGenerator` never explicitly says "I implement FileGenerator" -- it just has the right methods. This is duck typing made explicit. Any class with `name()` and `generate()` can be used as a generator, regardless of its inheritance hierarchy.

**Predict:** The `CIGenerator` adds "security-scan" and "compliance-check" only for STRICT tier. If you add a new tier called `PARANOID`, what would you need to change?

## Step 3: Build the Generator Registry

**What to do:** Create a `GeneratorRegistry` class that stores generators and has a `generate_blueprint()` method that runs all generators and assembles the output into a `Blueprint`.

**Why:** The registry is the composition layer. It decouples "which generators exist" from "how they are run." Adding a new generator is one line: `registry.register(MyNewGenerator())`. The registry also auto-generates a `MANIFEST.json` that records which generator produced each file.

```python
class GeneratorRegistry:
    def __init__(self) -> None:
        self._generators: list[FileGenerator] = []

    def register(self, gen: FileGenerator) -> None:
        self._generators.append(gen)

    def generate_blueprint(self, spec: ProjectSpec) -> Blueprint:
        all_files: list[GeneratedFile] = []
        manifest_entries: list[dict[str, str]] = []
        for gen in self._generators:
            files = gen.generate(spec)
            all_files.extend(files)
            for f in files:
                manifest_entries.append({
                    "generator": gen.name(),
                    "path": f.relative_path,
                })
        # Always add manifest
        manifest = GeneratedFile(
            "MANIFEST.json",
            json.dumps({"project": spec.name, "files": manifest_entries}, indent=2),
        )
        all_files.append(manifest)
        return Blueprint(spec=spec, files=all_files)
```

The `MANIFEST.json` is generated last because it needs to know about all other generated files. It serves as a receipt: "this blueprint produced these 6 files, and here is which generator created each one." This traceability is important when something goes wrong -- you can see exactly which generator produced a problematic file.

**Predict:** With the four default generators, how many files does a STANDARD blueprint produce? How many does a STRICT blueprint produce?

## Step 4: Build the Blueprint and Persistence

**What to do:** Create a `Blueprint` dataclass that holds the spec and generated files, with a `write_to()` method that persists all files under a root directory.

**Why:** The blueprint is the complete output of the generation process. Separating "generate" from "write" enables testing without touching the filesystem -- tests can inspect `blueprint.files` and `blueprint.paths` without creating actual files.

```python
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

    def write_to(self, root: Path) -> int:
        written = 0
        for gf in self.files:
            target = root / gf.relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(gf.content, encoding="utf-8")
            written += 1
        return written
```

`target.parent.mkdir(parents=True, exist_ok=True)` handles nested paths like `config/settings.json` and `.github/workflows/ci.yml`. Without `parents=True`, creating `config/settings.json` would fail if the `config/` directory does not exist.

**Predict:** If `write_to()` is called twice with the same root directory, what happens to existing files? Is this idempotent?

## Step 5: Wire Up the High-Level API and CLI

**What to do:** Write `build_default_registry()` that pre-loads the four standard generators, `generate_project()` as the public API, and `main()` as the CLI entry point.

**Why:** The layered API provides three levels of control. The CLI is for operators who want to generate a project from the terminal. The `generate_project()` function is for scripts and automation. The registry is for developers who want to customize which generators run.

```python
def build_default_registry() -> GeneratorRegistry:
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
```

`ComplianceTier[tier.upper()]` converts a string like `"standard"` into the enum `ComplianceTier.STANDARD`. If the string does not match any enum member, Python raises `KeyError` -- which is useful but not user-friendly (the "Fix it" section asks you to improve this).

**Predict:** What happens if you call `generate_project("svc", tier="nonexistent")`? What exception do you get?

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Modifying `ProjectSpec` during generation | Forgetting that `frozen=True` prevents mutation | Read from the spec; never try to set attributes on it |
| Using `type: ignore` to bypass Protocol | Generator missing `name()` or `generate()` method | Implement both methods; Protocol checks them structurally |
| Hardcoding file paths with `\` on Windows | Using string concatenation instead of `Path` | Always use `Path` objects and `/` for `relative_path` strings |
| Manifest includes itself | Generating manifest before collecting all files | Generate manifest last, after all other generators have run |
| Invalid tier string causes raw `KeyError` | `ComplianceTier["bad"]` raises unhelpful `KeyError` | Catch `KeyError` and raise a descriptive `ValueError` instead |

## Testing Your Solution

```bash
pytest -v
```

Expected output:
```text
~14 passed
```

Test from the command line:

```bash
python project.py my-service --tier standard --owners alice bob
```

You should see a list of generated files. Add `--output-dir ./output` to actually write them to disk and inspect the contents.

## What You Learned

- **The Strategy pattern** enables open/closed design: the system is open for extension (add new generators) but closed for modification (existing generators and the registry do not change). This is how you build systems that grow without becoming fragile.
- **The Registry pattern** decouples discovery from execution. Generators are registered at startup; the registry orchestrates them at generation time. This separation makes it easy to build different generator sets for different teams or compliance requirements.
- **Immutable specifications** (`frozen=True`) prevent a class of mutation bugs. When a spec is passed through multiple generators, none of them can accidentally change it, eliminating subtle data corruption that would be hard to debug.
