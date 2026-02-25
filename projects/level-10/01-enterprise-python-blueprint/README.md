# Level 10 / Project 01 - Enterprise Python Blueprint
Home: [README](../../../README.md)

## Focus
- Strategy pattern for pluggable code generators
- Registry pattern for component discovery and composition
- Compliance tiers that change generated output
- Enterprise project scaffolding automation

## Why this project exists
Every new microservice in an organization should start from the same standards — logging format, config schema, test harness, CI pipeline. This project builds a code-driven blueprint generator so teams get consistent scaffolding automatically, eliminating "snowflake services" that drift from organizational norms.

## Run (copy/paste)
```bash
cd <repo-root>/projects/level-10/01-enterprise-python-blueprint
python project.py my-service --tier standard --owners alice bob
pytest -v
```

## Expected terminal output
```text
Generated 6 files for 'my-service' (tier=STANDARD):
  logging_config.json
  config/settings.json
  pytest.ini
  tests/test_smoke.py
  .github/workflows/ci.yml
  MANIFEST.json
```

## Expected artifacts
- Blueprint files written to `--output-dir` (if provided)
- MANIFEST.json listing every generated file and its source generator
- Passing tests (`pytest -v` shows ~14 passed)

## Alter it (required)
1. Add a new generator (e.g., `DockerfileGenerator`) that produces a `Dockerfile` — register it in `build_default_registry` and verify the manifest grows by one entry.
2. Make the `STRICT` tier require a `CODEOWNERS` file — add a generator that only emits output for strict-tier specs.
3. Re-run tests after each change to ensure nothing regresses.

## Break it (required)
1. Pass a project name containing spaces or special characters — observe the `ValueError`.
2. Remove a generator from the registry and watch downstream tests that expect its output fail.
3. Change `ComplianceTier` enum values and see how `generate_project("x", tier="nonexistent")` raises `KeyError`.

## Fix it (required)
1. Add input sanitization that auto-slugifies project names instead of rejecting them.
2. Make the registry validate that at least one generator is registered before generating.
3. Add a friendly error message for unknown tier strings instead of a raw `KeyError`.

## Explain it (teach-back)
1. Why does the Strategy pattern (FileGenerator protocol) make this system extensible without modifying existing code?
2. How does the compliance tier influence each generator differently?
3. What is the purpose of the MANIFEST.json and why is it generated last?
4. How would you adapt this blueprint system to generate projects in languages other than Python?

## Mastery check
You can move on when you can:
- add a new generator and register it without modifying any existing generator,
- explain how the Protocol class enables duck-typed strategy dispatch,
- write a test for a custom generator using the existing fixtures,
- describe why immutable `ProjectSpec` prevents accidental mutation during generation.

---

## Related Concepts

- [Api Basics](../../../concepts/api-basics.md)
- [Async Explained](../../../concepts/async-explained.md)
- [Errors and Debugging](../../../concepts/errors-and-debugging.md)
- [Functions Explained](../../../concepts/functions-explained.md)
- [Quiz: Api Basics](../../../concepts/quizzes/api-basics-quiz.py)

---

| [← Prev](../README.md) | [Home](../../../README.md) | [Next →](../02-autonomous-run-orchestrator/README.md) |
|:---|:---:|---:|
