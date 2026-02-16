# 15 - Next-Level Expansion Plan (Decision Locked)
Home: [README](./README.md)

This document converts your answers into an implementation-ready expansion plan.

## Decision lock (from your answers)
1. Audience: both internal and external learners.
2. Language: English only.
3. Delivery format: documentation-first curriculum with linked external resources only.
4. Assessment model (recommended): weighted scoring with minimum floor per competency.
5. Certification: both informal badges and internal non-accredited certification track.
6. Mentoring model: self-paced by default, mentor-assisted optional.
7. Accessibility (recommended): baseline now, full accessibility program phased in quarterly.
8. Progress tracking: manual, docs-based progress logs and checkpoint notes (no app required).
9. Update cadence: quarterly.
10. Governance owner: Travis J Neuman.
11. CI automation (recommended): yes, enabled.
12. Data policy: both anonymized real examples and mock data.
13. SME definition: best-in-class practical standard (operational + engineering + teaching).
14. Maintenance budget (recommended): 2 hours/week + 1 quarterly deep review.
15. Priority: all levels are priority; execution will be parallelized with quality gates.

## Recommendations you asked for

### Assessment strictness recommendation
Use weighted scoring with pass floors.
- Why: pass/fail hides weak areas; weighted scoring exposes where support is needed.
- Model:
  - Practical execution: 35%
  - Debugging and failure recovery: 20%
  - Engineering quality (tests, logging, structure): 20%
  - Communication/teach-back: 15%
  - Operational thinking (runbooks, risk controls): 10%
- Pass criteria:
  - Overall score >= 80/100
  - No core domain below 70

### Accessibility recommendation
Implement in two waves.
- Wave 1 (now): practical baseline
  - plain-language alternatives,
  - keyboard-first navigation guidance,
  - high-contrast/readability checks,
  - consistent heading hierarchy,
  - no image-only critical instructions.
- Wave 2 (quarterly roadmap): full program
  - optional external captioned resources linked in curriculum,
  - alternate format packs (printable/offline),
  - explicit reading-level tracks.

### CI recommendation
Enable CI now with:
- markdown relative-link integrity checks,
- project smoke checks,
- quick checks on push/PR,
- full smoke on quarterly schedule + manual trigger.

### Maintenance recommendation
- Weekly: 2 hours
  - 60 min content fixes,
  - 30 min link/quality maintenance,
  - 30 min progress-log review and curriculum tuning notes.
- Quarterly: 6-hour hardening sprint
  - rubric updates,
  - remediation updates,
  - full smoke + curriculum release notes.

### Mentoring recommendation
- Keep self-paced as the default workflow.
- Add optional mentor check-ins as needed (recommended cadence: 30-45 minutes biweekly when active help is needed).
- Do not require mentors to complete the plan.

## SME standard (operational definition)
A learner is "SME-ready" when they can reliably:
1. Design and ship idempotent automations with safe reruns.
2. Build and maintain SQL reporting pipelines with quality controls.
3. Integrate Orion and DPA data into stable cache/reporting layers.
4. Deliver browser-usable dashboards for non-technical stakeholders.
5. Diagnose, recover, and explain failures clearly.
6. Mentor others using clear reasoning and reproducible examples.

## Next-level architecture
1. Personalization engine
- learner profile intake,
- placement scoring,
- pace recommendations.

2. Multi-lane learning delivery
- Explain lane,
- Show lane,
- Do lane,
- Teach lane.

3. Scored competency system
- entry checks,
- level exit checks,
- capstone readiness score,
- badge/certification map.

4. Remediation and acceleration tracks
- failure-pattern-based recovery paths,
- optional challenge packs.

5. Mentor operations
- mentor runbooks,
- review scripts,
- escalation triggers.

6. Content governance and release operations
- versioned curriculum updates,
- owner approvals,
- quarterly release notes.

## Execution roadmap

### Quarter 1
- Complete docs 16-20 in full.
- Roll out CI checks and maintenance workflow.
- Add profile intake and placement recommendations.
- Add scoring rubrics and certification track definitions.

### Quarter 2
- Add remediation packs and mentor guide workflows.
- Add enterprise simulation packs (Orion/DPA/SQL failure drills).
- Expand linked external resources by skill level and topic.

### Quarter 3
- Expand accessibility (readability variants and alternate format packs).
- Expand manual progress analytics templates (no app dependency).
- Add advanced challenge packs for levels 8-10.

### Quarter 4
- Full curriculum hardening and quality audit.
- Publish annual versioned curriculum release.

## Success metrics
- Day-1 completion rate.
- Level progression rate.
- Time-to-first-working-project.
- Failure recovery time.
- Capstone pass rates by competency area.
- Mentor intervention frequency.

## Non-goals (explicit)
- No requirement to build a learning web app.
- No requirement to host or transcribe video content in this repo.
- No requirement to collect automated personal telemetry data.

## Risks and controls
- Risk: content overload.
  - Control: dual path (quick path + deep path).
- Risk: quality drift.
  - Control: CI + quarterly release process.
- Risk: uneven level quality.
  - Control: same quality gates for levels 0-10.

## Primary Sources
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)
- [GitHub Actions docs](https://docs.github.com/en/actions)

## Optional Resources
- [Real Python](https://realpython.com/tutorials/python/)
- [Pro Git Book](https://git-scm.com/book/en/v2.html)

## Next
Go to [16_LEARNER_PROFILE_AND_PLACEMENT.md](./16_LEARNER_PROFILE_AND_PLACEMENT.md).
