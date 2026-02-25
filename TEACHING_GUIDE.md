# Teaching Guide — Using This Curriculum in a Classroom

Home: [README](./README.md)

This guide helps instructors adapt the learn.python curriculum for classroom use, whether you are running a university course, a bootcamp cohort, or a community workshop.

---

## Semester Mapping

### 16-Week University Semester

| Week | Content | Projects Assigned | Deliverable |
|------|---------|-------------------|-------------|
| 1 | Computer Literacy Primer (Doc 00), Setup (Doc 03) | Level 00: exercises 01–05 | Python installed, first script runs |
| 2 | Roadmap + Glossary (Docs 01–02), begin Foundations (Doc 04) | Level 00: exercises 06–15 | All absolute beginner exercises complete |
| 3 | Foundations continued — variables, loops, functions | Level 0: projects 01–05 | First passing test |
| 4 | Foundations continued — files, errors, collections | Level 0: projects 06–10 | File I/O project working |
| 5 | Foundations wrap-up, Level 0 capstone | Level 0: projects 11–15 | **Gate A: Setup + first test** |
| 6 | Quality & Testing (Doc 09) — pytest, ruff, black | Level 1: projects 01–08 | Tests written for own code |
| 7 | Input validation, CSV, JSON | Level 1: projects 09–15 | CSV reader handles malformed input |
| 8 | **Midterm** — practical exam (timed project) | Midterm project | Working solution under time pressure |
| 9 | Data structures, cleaning, error handling | Level 2: projects 01–08 | Data cleaning pipeline |
| 10 | Level 2 completion + Module 01 (Web Scraping) intro | Level 2: projects 09–15 | **Gate B: Resilient data tools** |
| 11 | Packages, logging, TDD | Level 3: projects 01–08 | Package with tests |
| 12 | Level 3 completion + Module 02 or 03 | Level 3: projects 09–15 | CLI tool or API client |
| 13 | Schema validation, data contracts | Level 4: projects 01–08 | Schema-validated pipeline |
| 14 | Level 4 completion, begin Level 5 | Level 4: projects 09–15 | Transformation pipeline |
| 15 | Level 5 — scheduling, monitoring, resilience | Level 5: projects 01–10 | Retry-enabled system |
| 16 | **Final project** + oral defense | Capstone selection | **Gate C or D** |

### 10-Week Bootcamp (Intensive)

| Week | Content | Pace |
|------|---------|------|
| 1 | Docs 00–04, Level 00, Level 0 (projects 01–08) | Foundations blitz |
| 2 | Level 0 (09–15), Level 1 (01–08) | Testing + validation |
| 3 | Level 1 (09–15), Level 2 (01–08) | Data structures |
| 4 | Level 2 (09–15), Level 3 (01–08) | Packages + TDD |
| 5 | Level 3 (09–15), Module 01 or 03 | **Midpoint check** |
| 6 | Level 4 (01–10) | Pipelines |
| 7 | Level 4 (11–15), Level 5 (01–08) | Operations |
| 8 | Level 5 (09–15), Module 04 or 07 | Applied skills |
| 9 | Level 6 (selected projects) | SQL + ETL |
| 10 | **Capstone week** — final project + presentations | Demo day |

### Weekend Workshop (2 Days)

Focus on Level 00 and Level 0 only. Goal: participants leave with Python installed, a working script, and a passing test.

| Session | Duration | Content |
|---------|----------|---------|
| Saturday AM | 3 hours | Setup, Computer Literacy Primer, exercises 01–08 |
| Saturday PM | 3 hours | Foundations intro, Level 0 projects 01–05 |
| Sunday AM | 3 hours | Level 0 projects 06–10, debugging practice |
| Sunday PM | 3 hours | Level 0 projects 11–15, first test, wrap-up |

---

## Fork Instructions for Teachers

### Setting Up Your Class Repository

1. **Fork** the repository on GitHub
2. Enable GitHub Discussions on your fork for student Q&A
3. Create a branch for your semester: `fall-2026`, `spring-2027`, etc.
4. Customize `CLAUDE.md` with your learner context if using AI tutoring
5. Optionally remove levels beyond your course scope to reduce student confusion

### Per-Student Setup

```bash
# Students fork YOUR fork (not the upstream repo)
git clone https://github.com/YOUR_ORG/learn.python.git
cd learn.python
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### Collecting Assignments

Option A — **Pull Requests:** Students submit projects as PRs to your fork. Review inline.

Option B — **Branch per student:** Each student works on their own branch. You review branches.

Option C — **Separate repos:** Students clone the curriculum, work locally, push to their own GitHub. You review by visiting their repos.

Recommendation: Option A for small classes (under 20), Option C for larger classes.

---

## Assessment Materials

### Grading Rubrics by Level

#### Level 00 — Absolute Beginner (Pass/Fail)

| Criterion | Pass | Fail |
|-----------|------|------|
| Script runs without errors | Yes | No |
| Output matches expected | Yes | No |
| Code was written by student (not copied) | Evidence of iteration | Exact match to solution |

#### Levels 0–2 — Foundations (4-Point Scale)

| Points | Criterion |
|--------|-----------|
| 4 | All tests pass, code is clean, edge cases handled, notes.md filled in |
| 3 | All tests pass, code works but could be cleaner |
| 2 | Most tests pass, student attempted all parts |
| 1 | Partial attempt, some tests pass |
| 0 | Not submitted or clearly copied |

#### Levels 3–5 — Intermediate (4-Point Scale + Code Review)

| Points | Criterion |
|--------|-----------|
| 4 | Tests pass, follows package conventions, logging present, TDD evidence |
| 3 | Tests pass, mostly follows conventions |
| 2 | Functional but conventions not followed |
| 1 | Partial, some functionality works |

Add 1 bonus point for: meaningful git history (multiple commits showing iteration).

#### Levels 6–10 — Advanced (Rubric + Oral Defense)

| Component | Weight | Criteria |
|-----------|--------|----------|
| Code quality | 30% | Tests pass, types used, error handling, documentation |
| Architecture | 30% | Clear separation of concerns, appropriate patterns |
| Oral defense | 25% | Can explain design decisions, tradeoffs, failure modes |
| Documentation | 15% | README, notes.md, architecture decisions recorded |

### Grading Alter/Break/Fix/Explain Exercises

Many projects include TRY_THIS.md or notes.md prompts that ask students to alter, break, fix, or explain code. Grade these on understanding, not correctness:

| Exercise Type | What to Look For |
|---------------|------------------|
| **Alter** | Did the student change the right thing? Does their modification work? |
| **Break** | Did the student identify a real failure mode? Can they explain why it breaks? |
| **Fix** | Did the student diagnose the root cause, not just suppress the symptom? |
| **Explain** | Can the student describe what the code does in their own words? |

Award full credit for thoughtful wrong answers that show reasoning. Deduct for correct answers that show no understanding (copied from AI without comprehension).

---

## Suggested Assignment Structure

### Weekly Cadence

| Day | Activity |
|-----|----------|
| Monday | Introduce concept (lecture or guided reading of concept doc) |
| Tuesday | In-class coding: first 2–3 projects from the level |
| Wednesday | Quiz on the concept (use the built-in quizzes) |
| Thursday | Independent project work (remaining projects) |
| Friday | Code review session — students present one project to a partner |

### Project Submission Checklist (Give to Students)

Before submitting a project, verify:

- [ ] `python -m pytest tests/` passes
- [ ] `ruff check .` has no errors
- [ ] `notes.md` has your observations (what you learned, what was hard)
- [ ] Code has meaningful variable names (not `x`, `y`, `z`)
- [ ] You can explain every line of your code

### Capstone Projects

At the end of each major section, assign a capstone that combines skills:

| After Level | Capstone Suggestion | Duration |
|-------------|---------------------|----------|
| 2 | Build a CSV data cleaner that handles 3 types of malformed input | 1 week |
| 5 | Build a monitoring tool that polls an API and logs anomalies | 2 weeks |
| 7 | Build an ETL pipeline with caching, retry, and observability | 2 weeks |
| 10 | Production-grade system with tests, docs, Docker, and deployment | 3 weeks |

---

## Classroom Tips

### For Students With No Tech Background

The Level 00 exercises assume zero knowledge. Let students spend a full week here if needed. Rushing past this level creates compounding confusion later.

### For Mixed-Skill Classes

- Advanced students: assign expansion modules as bonus work
- Struggling students: pair with advanced students for code review sessions
- Everyone benefits from explaining code out loud — make this a regular activity

### Common Student Mistakes

| Mistake | How to Address |
|---------|----------------|
| Copying code without understanding | Require oral explanations of submitted code |
| Skipping tests | Make test passage a hard requirement for submission |
| Not reading error messages | First week: practice reading tracebacks as a class exercise |
| Fear of breaking things | Explicitly assign "break this code" exercises |
| Trying to memorize syntax | Emphasize that looking things up is normal and expected |

### Using AI Tools in Your Classroom

This curriculum includes AI tutoring guidelines (see CLAUDE.md). If you allow AI tools:

1. Set clear boundaries: AI can explain concepts, not write solutions
2. Require students to explain AI-suggested code in their own words
3. Use the "predict before running" technique: ask students what code will do before executing
4. Grade understanding, not just output

If you prohibit AI tools, the curriculum works equally well — every concept is explained in the docs, and the project READMEs provide sufficient guidance.

---

## Support

Questions about using this curriculum in a classroom? Open an issue on GitHub with the `teaching` label.

---

| [← README](./README.md) | [Home](./README.md) | [Portfolio Guide →](./PORTFOLIO_GUIDE.md) |
|:---|:---:|---:|
