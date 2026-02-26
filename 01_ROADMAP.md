# 01 - Roadmap: Zero Experience -> Python SME (Automation and Dashboards)
Home: [README](./README.md)

## Who this is for
- You have zero coding, scripting, or programming experience.
- You need practical outcomes in a real operations environment.
- You learn best by doing real work, not passive studying.

## What you will build
- Reliable Python automations for files, Excel, SQL, and monitoring data.
- Repeatable ETL workflows using SQL databases as a reporting backbone.
- Monitoring API data ingestion jobs.
- Browser-based dashboards for non-technical stakeholders.

## Prerequisites
- One supported platform: Windows, macOS, Linux, Android, or iOS (desktop strongly recommended for full path).
- Permission to install Python and VS Code.
- Database credentials for your SQL database (SQLite for learning, PostgreSQL for production).
- Read-only API access to your monitoring platform to start.

## Program overview (8-10 hrs/week default)
- Phase 0 (Week 1): environment setup and first script.
- Phase 1 (Weeks 2-6): Python foundations.
- Phase 2 (Weeks 7-10): quality tooling and team-ready workflow.
- Phase 3 (Weeks 11-16): file and Excel automation.
- Phase 4 (Weeks 17-22): SQL-first ETL pipelines.
- Phase 5 (Weeks 23-28): monitoring API integration.
- Phase 6 (Weeks 29-38): dashboard delivery for browser users.
- Phase 7 (Weeks 39+): release process, governance, and handoff maturity.
- Phase 8+ (Advanced): full-stack expert path and infinite mastery loop.
- Phase 9+ (Elite): formal exams, architecture defenses, platform hardening, and world-class evidence loop.

## Step-by-step lab pack

### Phase 0 - Setup (Week 1)
Weekly outcome:
- Local Python environment works reliably.

Minimum deliverables:
- `python --version` works.
- `.venv` created and activated.
- First script runs.
- First test passes.

Done means done:
- You can repeat setup in a fresh folder without guessing.

Fail/recover guidance:
- If activation fails, use the troubleshooting section in [03_SETUP_ALL_PLATFORMS.md](./03_SETUP_ALL_PLATFORMS.md).

### Phase 1 - Foundations (Weeks 2-6)
Weekly outcomes:
- Week 2: variables, types, conditionals.
- Week 3: loops and collections.
- Week 4: functions and modular thinking.
- Week 5: file IO and paths.
- Week 6: debugging and code reading.

Minimum deliverables:
- 15 micro-scripts.
- One debugging diary file.

Done means done:
- You can explain each script out loud in plain language.

Fail/recover guidance:
- If stuck, reduce problem size and rebuild with toy data.

### Phase 2 - Quality and workflow (Weeks 7-10)
Weekly outcomes:
- toolchain setup, formatting, linting, tests, logging.

Minimum deliverables:
- reusable project template with `pyproject.toml`, tests, logging, and README.

Done means done:
- Any teammate can run your tool using documented steps.

Fail/recover guidance:
- If tooling feels heavy, keep features tiny and run checks per feature.

### Phase 3 - Files and Excel automation (Weeks 11-16)
Weekly outcomes:
- robust ingestion of multiple spreadsheets with validation.

Minimum deliverables:
- Capstone A baseline complete.

Done means done:
- malformed inputs are rejected safely with clear logs.

Fail/recover guidance:
- Start with a 2-file sample dataset and scale gradually.

### Phase 4 - SQL ETL (Weeks 17-22)
Weekly outcomes:
- clean table design and idempotent pipeline loads.

Minimum deliverables:
- staging and reporting tables + ETL job + daily summary query.

Done means done:
- rerunning ETL does not duplicate records.

Fail/recover guidance:
- freeze schema changes until test dataset passes end-to-end.

### Phase 5 - Monitoring API integration (Weeks 23-28)
Weekly outcomes:
- read-only ingestion from monitoring APIs into cache tables.

Minimum deliverables:
- one daily ingestion job from each source.

Done means done:
- data contract documented, ingestion stable, errors logged.

Fail/recover guidance:
- enforce read-only endpoints first and short polling windows.

### Phase 6 - Dashboard delivery (Weeks 29-38)
Weekly outcomes:
- browser-consumable dashboard with filters and exports.

Minimum deliverables:
- working dashboard with data freshness indicator.

Done means done:
- non-technical user can answer core ops questions without SQL access.

Fail/recover guidance:
- fallback to SQL-only cache mode when source APIs are slow.

### Phase 7 - Shipping and governance (Weeks 39+)
Weekly outcomes:
- release process, support runbook, handoff standards.

Minimum deliverables:
- release checklist and operational runbook.

Done means done:
- another engineer can operate and troubleshoot your tools.

Fail/recover guidance:
- capture every incident and convert it into checklist updates.

## Milestone gates
- Gate A: setup + first script + first passing test.
- Gate B: Capstone A supports safe reruns and rejects.
- Gate C: SQL ETL is idempotent and logged.
- Gate D: Monitoring API ingestion proof into database cache.
- Gate E: browser dashboard available to stakeholders.

## Project ladder mapping (practice by skill level)
- Use [`./projects`](./projects) continuously while progressing through phases.
- Suggested mapping:
  - Levels 0-2 during Phase 0-1
  - Levels 3-5 during Phase 2-3
  - Levels 6-7 during Phase 4
  - Levels 8-9 during Phase 5-6
  - Level 10 during Phase 7 and capstone hardening
- Project index:
  - [projects/README.md](./projects/README.md)

## Screenshot and checkpoint workflow
- Capture proof screenshots and reflections while learning:
  - [12_SCREENSHOT_CHECKPOINTS.md](./12_SCREENSHOT_CHECKPOINTS.md)
- Use this after each session to improve retention and speed up troubleshooting.

## If you fall behind (catch-up plan)
1. Keep only one active project at a time.
2. Finish minimum deliverables before adding features.
3. Switch to 45-minute sessions with explicit goals.
4. Use Hybrid mode until momentum returns.

## Learning-style options (Play/Build/Dissect/Teach-back)
- Play: tweak example scripts and observe behavior changes.
- Build: implement full milestone checklists exactly.
- Dissect: read unfamiliar scripts and annotate line-by-line intent.
- Teach-back: explain one concept weekly to another person or a written journal.

## Expected output
- A complete progression from beginner to production-capable Python practitioner.
- A portfolio of capstones tied to real data systems.
- A clear upgrade path to full-stack expert mastery:
  - [21_FULL_STACK_MASTERY_PATH.md](./curriculum/21_FULL_STACK_MASTERY_PATH.md)
  - [22_SPECIALIZATION_TRACKS.md](./curriculum/22_SPECIALIZATION_TRACKS.md)
  - [23_RESOURCE_AND_CURRICULUM_MAP.md](./curriculum/23_RESOURCE_AND_CURRICULUM_MAP.md)
  - [24_MASTERY_SCORING_AND_GATES.md](./curriculum/24_MASTERY_SCORING_AND_GATES.md)
  - [25_INFINITY_MASTERY_LOOP.md](./curriculum/25_INFINITY_MASTERY_LOOP.md)
- A literal, no-assumptions execution path for absolute beginners:
  - [26_ZERO_TO_MASTER_PLAYBOOK.md](./curriculum/26_ZERO_TO_MASTER_PLAYBOOK.md)
  - [27_DAY_0_TO_DAY_30_BOOTSTRAP.md](./curriculum/27_DAY_0_TO_DAY_30_BOOTSTRAP.md)
  - [28_LEVEL_0_TO_2_DEEP_GUIDE.md](./curriculum/28_LEVEL_0_TO_2_DEEP_GUIDE.md)
  - [29_LEVEL_3_TO_5_DEEP_GUIDE.md](./curriculum/29_LEVEL_3_TO_5_DEEP_GUIDE.md)
  - [30_LEVEL_6_TO_8_DEEP_GUIDE.md](./curriculum/30_LEVEL_6_TO_8_DEEP_GUIDE.md)
  - [31_LEVEL_9_TO_10_AND_BEYOND.md](./curriculum/31_LEVEL_9_TO_10_AND_BEYOND.md)
  - [32_DAILY_SESSION_SCRIPT.md](./curriculum/32_DAILY_SESSION_SCRIPT.md)
  - [33_WEEKLY_REVIEW_TEMPLATE.md](./curriculum/33_WEEKLY_REVIEW_TEMPLATE.md)
  - [34_FAILURE_RECOVERY_ATLAS.md](./curriculum/34_FAILURE_RECOVERY_ATLAS.md)
  - [35_CAPSTONE_BLUEPRINTS.md](./curriculum/35_CAPSTONE_BLUEPRINTS.md)
- A world-class elite extension path:
  - [36_ELITE_ENGINEERING_TRACK.md](./curriculum/36_ELITE_ENGINEERING_TRACK.md)
  - [37_QUARTERLY_EXAMS_AND_DEFENSES.md](./curriculum/37_QUARTERLY_EXAMS_AND_DEFENSES.md)
  - [38_SYSTEM_DESIGN_AND_RFCS.md](./curriculum/38_SYSTEM_DESIGN_AND_RFCS.md)
  - [39_PRODUCTION_PLATFORM_LAB.md](./curriculum/39_PRODUCTION_PLATFORM_LAB.md)
  - [40_SECURITY_COMPLIANCE_HARDENING.md](./curriculum/40_SECURITY_COMPLIANCE_HARDENING.md)
  - [41_PERFORMANCE_ENGINEERING_LAB.md](./curriculum/41_PERFORMANCE_ENGINEERING_LAB.md)
  - [42_OPEN_SOURCE_CONTRIBUTION_LANE.md](./curriculum/42_OPEN_SOURCE_CONTRIBUTION_LANE.md)
  - [43_PUBLIC_PROOF_OF_WORK_PORTFOLIO.md](./curriculum/43_PUBLIC_PROOF_OF_WORK_PORTFOLIO.md)
  - [44_SME_INTERVIEW_AND_DEBATE_BANK.md](./curriculum/44_SME_INTERVIEW_AND_DEBATE_BANK.md)
  - [45_MASTERY_TELEMETRY_AND_REMEDIATION.md](./curriculum/45_MASTERY_TELEMETRY_AND_REMEDIATION.md)
- A universal learner-adaptive completion path:
  - [46_ACCESSIBILITY_AND_LEARNING_PROFILE_PLAYBOOK.md](./curriculum/46_ACCESSIBILITY_AND_LEARNING_PROFILE_PLAYBOOK.md)
  - [47_DIAGNOSTIC_AND_PERSONALIZED_STUDY_ENGINE.md](./curriculum/47_DIAGNOSTIC_AND_PERSONALIZED_STUDY_ENGINE.md)
  - [48_MISCONCEPTION_AND_FAILURE_ATLAS_EXPANDED.md](./curriculum/48_MISCONCEPTION_AND_FAILURE_ATLAS_EXPANDED.md)
  - [49_COMPETENCY_COVERAGE_AND_GAP_CLOSURE_MATRIX.md](./curriculum/49_COMPETENCY_COVERAGE_AND_GAP_CLOSURE_MATRIX.md)
  - [50_CERTIFICATION_GRADE_COMPLETION_PROTOCOL.md](./curriculum/50_CERTIFICATION_GRADE_COMPLETION_PROTOCOL.md)
- Elite systems projects for advanced practice:
  - [projects/elite-track/README.md](./projects/elite-track/README.md)

## Break/fix drills
- Break path assumptions by renaming input folders.
- Break schema assumptions by removing required columns.
- Break API assumptions by forcing timeout values.

## Troubleshooting
- If learning stalls: reduce scope, keep daily continuity, and ship smaller increments.
- If project complexity spikes: return to the previous gate and stabilize.

## Mastery check
You are ready to advance when you can:
- describe your current phase deliverable in one sentence,
- run it end-to-end,
- explain where it fails and how to recover.

## Primary Sources
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Automate the Boring Stuff](https://automatetheboringstuff.com/3e/)
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html)

## Optional Resources
- [Exercism Python](https://exercism.org/tracks/python)
- [Real Python](https://realpython.com/tutorials/python/)

## Next

[Next: 02_GLOSSARY.md →](./02_GLOSSARY.md)
