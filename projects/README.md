# Projects Ladder (Level 0 -> Level 10)
Home: [README](../README.md)

This ladder contains 11 levels with 15 projects per level.
Each level now has unique project themes aligned to that skill stage.

## Levels
- [level-0](./level-0/README.md)
- [level-1](./level-1/README.md)
- [level-2](./level-2/README.md)
- [level-3](./level-3/README.md)
- [level-4](./level-4/README.md)
- [level-5](./level-5/README.md)
- [level-6](./level-6/README.md)
- [level-7](./level-7/README.md)
- [level-8](./level-8/README.md)
- [level-9](./level-9/README.md)
- [level-10](./level-10/README.md)

## Elite extension
- [elite-track](./elite-track/README.md)

## How to use
1. Pick your current level.
2. Run each starter project once.
3. For at least 3 projects, complete alter/break/fix/explain.
4. Promote one project into a mini-capstone extension.

`<repo-root>` in project commands means the folder containing `/README.md` in this repository.

## Required per-project flow
For every project README, follow this order:
1. `Run (copy/paste)`
2. `Expected terminal output`
3. `Alter it (required)`
4. `Break it (required)`
5. `Fix it (required)`
6. `Explain it (teach-back)`
7. `Mastery check`

## Next
Start with [level-0](./level-0/README.md).

## Smoke check runner
- Script: `./run_smoke_checks.sh`
- Quick check (1 project per level): `./run_smoke_checks.sh`
- Full check (all projects): `./run_smoke_checks.sh --full`
- Elite track quick check: `./run_elite_smoke_checks.sh`
- Elite track full check: `./run_elite_smoke_checks.sh --full`
- Level index contract check: `../tools/check_level_index_contract.sh`
- README contract check: `../tools/check_project_readme_contract.sh`
- Python comment/docstring contract check: `../tools/check_project_python_comment_contract.sh`
