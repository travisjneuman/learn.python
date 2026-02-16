# 11 — Checklists (Runbooks you will actually use)

## A) New project checklist (copy/paste)
- [ ] Create folder from template
- [ ] Create `.venv` and activate it citeturn0search5
- [ ] Install dependencies with pip citeturn0search9
- [ ] Add `pyproject.toml` config citeturn2search1
- [ ] Add Ruff + Black citeturn0search2
- [ ] Add pytest and at least 3 tests citeturn2search2
- [ ] Add logging to file
- [ ] Add README “how to run”
- [ ] Git init + first commit

## B) Automation safety checklist
- [ ] Explicit input/output paths
- [ ] Never overwrite outputs without versioning
- [ ] Handle malformed input (skip + log)
- [ ] Timeouts on network calls
- [ ] Retries for transient failures
- [ ] Idempotency for DB loads

## C) Dashboard checklist
- [ ] Fast startup (cache heavy queries)
- [ ] Filters are obvious
- [ ] Export available (CSV/XLSX)
- [ ] Auth story documented (even if “local only”)
- [ ] Error messages are actionable

## D) Release/shipping checklist (CI/CD concepts)
CI/CD is automated build/test/release/deploy. citeturn1search3turn1search10

Even without formal CI/CD, you simulate it locally:
- [ ] `ruff check .`
- [ ] `black .`
- [ ] `pytest`
- [ ] run end-to-end once on a sample dataset
- [ ] produce a versioned release artifact (zip) with README

## E) What PyPI is (and why you care)
PyPI is the public repository for Python packages. citeturn2search0
Your org may block direct PyPI installs; if so, you will use an internal mirror/index.

---

If you want, the next iteration of these docs can include:
- a complete project template folder
- example `pyproject.toml`
- example CLI scaffold (Typer)
- example logging config
- sample Excel files + expected outputs
