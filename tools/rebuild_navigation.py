"""Rebuild complete navigation chain across the entire curriculum.

This script updates every markdown file in the learn.python curriculum
with consistent navigation links (prev/home/next) in table format.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def rel(from_file: str, to_file: str) -> str:
    """Compute relative path from one file to another."""
    from_path = (ROOT / from_file).parent
    to_path = ROOT / to_file
    try:
        return to_path.relative_to(from_path).as_posix()
    except ValueError:
        # Need to go up directories
        rel_path = Path()
        common = from_path
        ups = 0
        while True:
            try:
                remainder = to_path.relative_to(common)
                return ("../" * ups + remainder.as_posix())
            except ValueError:
                common = common.parent
                ups += 1


def home_rel(from_file: str) -> str:
    """Compute relative path to README.md from a file."""
    return rel(from_file, "README.md")


def nav_table(from_file: str, prev_file: str | None, next_file: str | None, prev_label: str = "Prev", next_label: str = "Next") -> str:
    """Generate navigation table."""
    home = home_rel(from_file)
    prev_link = f"[← {prev_label}]({rel(from_file, prev_file)})" if prev_file else ""
    next_link = f"[{next_label} →]({rel(from_file, next_file)})" if next_file else ""
    return f"\n---\n\n| {prev_link} | [Home]({home}) | {next_link} |\n|:---|:---:|---:|\n"


def strip_old_nav(content: str) -> str:
    """Remove existing navigation sections from content."""
    # Remove ## Next sections (with various formats)
    content = re.sub(
        r'\n## Next\n.*?(?=\n## |\Z)', '', content, flags=re.DOTALL
    )
    # Remove ## Prev sections
    content = re.sub(
        r'\n## Prev\n.*?(?=\n## |\Z)', '', content, flags=re.DOTALL
    )
    # Remove ## Navigation sections
    content = re.sub(
        r'\n## Navigation\n.*?(?=\n## |\Z)', '', content, flags=re.DOTALL
    )
    # Remove existing nav tables (| [← pattern)
    content = re.sub(
        r'\n---\n\n\| \[←.*?\|:---|:---:\|---:\|\n?', '', content, flags=re.DOTALL
    )
    # Also remove trailing nav tables without prev
    content = re.sub(
        r'\n---\n\n\|  \| \[Home\].*?\|:---|:---:\|---:\|\n?', '', content, flags=re.DOTALL
    )
    # Clean trailing whitespace/newlines
    content = content.rstrip('\n') + '\n'
    return content


def update_file(filepath: str, prev_file: str | None, next_file: str | None,
                prev_label: str = "Prev", next_label: str = "Next"):
    """Update a file's navigation."""
    full_path = ROOT / filepath
    if not full_path.exists():
        print(f"  SKIP (not found): {filepath}")
        return
    content = full_path.read_text(encoding='utf-8')
    content = strip_old_nav(content)
    nav = nav_table(filepath, prev_file, next_file, prev_label, next_label)
    content = content + nav
    full_path.write_text(content, encoding='utf-8')
    print(f"  OK: {filepath}")


# =============================================================================
# MASTER CHAIN - Main navigation sequence
# =============================================================================

MAIN_CHAIN = [
    "README.md",
    "START_HERE.md",
    "00_COMPUTER_LITERACY_PRIMER.md",
    "01_ROADMAP.md",
    "02_GLOSSARY.md",
    "03_SETUP_ALL_PLATFORMS.md",
    "concepts/what-is-a-variable.md",
    "projects/level-00-absolute-beginner/README.md",
    "04_FOUNDATIONS.md",
    "concepts/how-loops-work.md",
    "concepts/types-and-conversions.md",
    "concepts/functions-explained.md",
    "practice/flashcards/README.md",
    "practice/challenges/README.md",
    "09_QUALITY_TOOLING.md",
    "concepts/errors-and-debugging.md",
    "concepts/the-terminal-deeper.md",
    "projects/level-0/README.md",
    "concepts/collections-explained.md",
    "concepts/files-and-paths.md",
    "projects/level-1/README.md",
    "projects/level-2/README.md",
    "concepts/how-imports-work.md",
    "concepts/classes-and-objects.md",
    "concepts/decorators-explained.md",
    "concepts/virtual-environments.md",
    "05_AUTOMATION_FILES_EXCEL.md",
    "projects/level-3/README.md",
    "06_SQL.md",
    "projects/level-4/README.md",
    "projects/level-5/README.md",
    "07_MONITORING_API_INTEGRATION.md",
    "concepts/http-explained.md",
    "concepts/api-basics.md",
    "concepts/async-explained.md",
    "projects/level-6/README.md",
    "projects/level-7/README.md",
    "08_DASHBOARDS.md",
    "projects/level-8/README.md",
    "projects/level-9/README.md",
    "projects/level-10/README.md",
    "projects/elite-track/README.md",
    "projects/modules/README.md",
    "10_CAPSTONE_PROJECTS.md",
    "11_CHECKLISTS.md",
    "12_SCREENSHOT_CHECKPOINTS.md",
    "13_SAMPLE_DATABASE_SCHEMAS.md",
    "14_NAVIGATION_AND_STUDY_WORKFLOW.md",
    "15_NEXT_LEVEL_EXPANSION_PLAN.md",
    "curriculum/16_LEARNER_PROFILE_AND_PLACEMENT.md",
    "curriculum/17_ASSESSMENT_AND_RUBRICS.md",
    "curriculum/18_REMEDIATION_PLAYBOOK.md",
    "curriculum/19_MENTOR_GUIDE.md",
    "curriculum/20_CURRICULUM_CHANGELOG.md",
    "curriculum/21_FULL_STACK_MASTERY_PATH.md",
    "curriculum/22_SPECIALIZATION_TRACKS.md",
    "curriculum/23_RESOURCE_AND_CURRICULUM_MAP.md",
    "curriculum/24_MASTERY_SCORING_AND_GATES.md",
    "curriculum/25_INFINITY_MASTERY_LOOP.md",
    "curriculum/26_ZERO_TO_MASTER_PLAYBOOK.md",
    "curriculum/27_DAY_0_TO_DAY_30_BOOTSTRAP.md",
    "curriculum/28_LEVEL_0_TO_2_DEEP_GUIDE.md",
    "curriculum/29_LEVEL_3_TO_5_DEEP_GUIDE.md",
    "curriculum/30_LEVEL_6_TO_8_DEEP_GUIDE.md",
    "curriculum/31_LEVEL_9_TO_10_AND_BEYOND.md",
    "curriculum/32_DAILY_SESSION_SCRIPT.md",
    "curriculum/33_WEEKLY_REVIEW_TEMPLATE.md",
    "curriculum/34_FAILURE_RECOVERY_ATLAS.md",
    "curriculum/35_CAPSTONE_BLUEPRINTS.md",
    "curriculum/36_ELITE_ENGINEERING_TRACK.md",
    "curriculum/37_QUARTERLY_EXAMS_AND_DEFENSES.md",
    "curriculum/38_SYSTEM_DESIGN_AND_RFCS.md",
    "curriculum/39_PRODUCTION_PLATFORM_LAB.md",
    "curriculum/40_SECURITY_COMPLIANCE_HARDENING.md",
    "curriculum/41_PERFORMANCE_ENGINEERING_LAB.md",
    "curriculum/42_OPEN_SOURCE_CONTRIBUTION_LANE.md",
    "curriculum/43_PUBLIC_PROOF_OF_WORK_PORTFOLIO.md",
    "curriculum/44_SME_INTERVIEW_AND_DEBATE_BANK.md",
    "curriculum/45_MASTERY_TELEMETRY_AND_REMEDIATION.md",
    "curriculum/46_ACCESSIBILITY_AND_LEARNING_PROFILE_PLAYBOOK.md",
    "curriculum/47_DIAGNOSTIC_AND_PERSONALIZED_STUDY_ENGINE.md",
    "curriculum/48_MISCONCEPTION_AND_FAILURE_ATLAS_EXPANDED.md",
    "curriculum/49_COMPETENCY_COVERAGE_AND_GAP_CLOSURE_MATRIX.md",
    "curriculum/50_CERTIFICATION_GRADE_COMPLETION_PROTOCOL.md",
]

# =============================================================================
# INTERNAL PROJECT CHAINS
# =============================================================================

LEVEL_00_PROJECTS = [
    "01-first-steps", "02-hello-world", "03-your-first-script", "04-variables",
    "05-numbers-and-math", "06-strings-and-text", "07-user-input",
    "08-making-decisions", "09-lists", "10-for-loops", "11-while-loops",
    "12-dictionaries", "13-functions", "14-reading-files", "15-putting-it-together",
]

LEVEL_PROJECTS = {
    0: [
        "01-terminal-hello-lab", "02-calculator-basics", "03-temperature-converter",
        "04-yes-no-questionnaire", "05-number-classifier", "06-word-counter-basic",
        "07-first-file-reader", "08-string-cleaner-starter", "09-daily-checklist-writer",
        "10-duplicate-line-finder", "11-simple-menu-loop", "12-contact-card-builder",
        "13-alarm-message-generator", "14-line-length-summarizer", "15-level0-mini-toolkit",
    ],
    1: [
        "01-input-validator-lab", "02-password-strength-checker", "03-unit-price-calculator",
        "04-log-line-parser", "05-csv-first-reader", "06-simple-gradebook-engine",
        "07-date-difference-helper", "08-path-exists-checker", "09-json-settings-loader",
        "10-ticket-priority-router", "11-command-dispatcher", "12-file-extension-counter",
        "13-batch-rename-simulator", "14-basic-expense-tracker", "15-level1-mini-automation",
    ],
    2: [
        "01-dictionary-lookup-service", "02-nested-data-flattener", "03-data-cleaning-pipeline",
        "04-error-safe-divider", "05-text-report-generator", "06-records-deduplicator",
        "07-list-search-benchmark", "08-mini-inventory-engine", "09-config-driven-calculator",
        "10-mock-api-response-parser", "11-retry-loop-practice", "12-csv-to-json-converter",
        "13-validation-rule-engine", "14-anomaly-flagger", "15-level2-mini-capstone",
    ],
    3: [
        "01-package-layout-starter", "02-cli-arguments-workbench", "03-logging-baseline-tool",
        "04-test-driven-normalizer", "05-refactor-monolith-drill", "06-structured-error-handler",
        "07-batch-file-auditor", "08-template-driven-reporter", "09-reusable-utils-library",
        "10-dependency-boundary-lab", "11-project-config-bootstrap", "12-parser-with-fixtures",
        "13-quality-gate-runner", "14-service-simulator", "15-level3-mini-capstone",
    ],
    4: [
        "01-schema-validator-engine", "02-excel-input-health-check", "03-robust-csv-ingestor",
        "04-data-contract-enforcer", "05-path-safe-file-mover", "06-backup-rotation-tool",
        "07-duplicate-record-investigator", "08-malformed-row-quarantine",
        "09-transformation-pipeline-v1", "10-run-manifest-generator", "11-audit-log-enhancer",
        "12-checkpoint-recovery-tool", "13-reconciliation-reporter", "14-configurable-batch-runner",
        "15-level4-mini-capstone",
    ],
    5: [
        "01-schedule-ready-script", "02-alert-threshold-monitor", "03-multi-file-etl-runner",
        "04-config-layer-priority", "05-plugin-style-transformer", "06-metrics-summary-engine",
        "07-resilient-json-loader", "08-cross-file-joiner", "09-template-report-renderer",
        "10-api-polling-simulator", "11-retry-backoff-runner", "12-fail-safe-exporter",
        "13-operational-run-logger", "14-change-detection-tool", "15-level5-mini-capstone",
    ],
    6: [
        "01-sql-connection-simulator", "02-staging-table-loader", "03-idempotency-key-builder",
        "04-upsert-strategy-lab", "05-transaction-rollback-drill", "06-query-performance-checker",
        "07-sql-summary-publisher", "08-data-lineage-capture", "09-incremental-load-simulator",
        "10-table-drift-detector", "11-dead-letter-row-handler", "12-etl-health-dashboard-feed",
        "13-batch-window-controller", "14-sql-runbook-generator", "15-level6-mini-capstone",
    ],
    7: [
        "01-api-query-adapter", "02-monitoring-api-adapter", "03-unified-cache-writer",
        "04-source-field-mapper", "05-polling-cadence-manager", "06-token-rotation-simulator",
        "07-stale-data-detector", "08-ingestion-observability-kit", "09-contract-version-checker",
        "10-multi-source-reconciler", "11-pipeline-feature-flags", "12-incident-mode-switch",
        "13-service-account-policy-check", "14-cache-backfill-runner", "15-level7-mini-capstone",
    ],
    8: [
        "01-dashboard-kpi-assembler", "02-query-cache-layer", "03-pagination-stress-lab",
        "04-filter-state-manager", "05-export-governance-check", "06-response-time-profiler",
        "07-concurrency-queue-simulator", "08-fault-injection-harness",
        "09-graceful-degradation-engine", "10-dependency-timeout-matrix",
        "11-synthetic-monitor-runner", "12-release-readiness-evaluator", "13-sla-breach-detector",
        "14-user-journey-tracer", "15-level8-mini-capstone",
    ],
    9: [
        "01-architecture-decision-log", "02-domain-boundary-enforcer",
        "03-event-driven-pipeline-lab", "04-observability-slo-pack", "05-capacity-planning-model",
        "06-reliability-scorecard", "07-canary-rollout-simulator", "08-change-impact-analyzer",
        "09-security-baseline-auditor", "10-data-governance-enforcer",
        "11-recovery-time-estimator", "12-incident-postmortem-generator",
        "13-platform-cost-estimator", "14-cross-team-handoff-kit", "15-level9-mini-capstone",
    ],
    10: [
        "01-enterprise-python-blueprint", "02-autonomous-run-orchestrator",
        "03-policy-as-code-validator", "04-multi-tenant-data-guard",
        "05-compliance-evidence-builder", "06-resilience-chaos-workbench",
        "07-high-risk-change-gate", "08-zero-downtime-migration-lab",
        "09-strategic-architecture-review", "10-executive-metrics-publisher",
        "11-production-readiness-director", "12-onboarding-accelerator-system",
        "13-legacy-modernization-planner", "14-sme-mentorship-toolkit",
        "15-level10-grand-capstone",
    ],
}

ELITE_PROJECTS = [
    "01-algorithms-complexity-lab", "02-concurrent-job-system",
    "03-distributed-cache-simulator", "04-secure-auth-gateway",
    "05-performance-profiler-workbench", "06-event-driven-architecture-lab",
    "07-observability-slo-platform", "08-policy-compliance-engine",
    "09-open-source-maintainer-simulator", "10-staff-engineer-capstone",
]


def main():
    # =================================================================
    # 1. MAIN CHAIN
    # =================================================================
    print("=== MAIN CHAIN ===")
    for i, filepath in enumerate(MAIN_CHAIN):
        prev_file = MAIN_CHAIN[i - 1] if i > 0 else MAIN_CHAIN[-1]  # wrap around
        next_file = MAIN_CHAIN[i + 1] if i < len(MAIN_CHAIN) - 1 else MAIN_CHAIN[0]  # wrap around
        update_file(filepath, prev_file, next_file)

    # =================================================================
    # 2. LEVEL-00 INTERNAL CHAIN (TRY_THIS.md files)
    # =================================================================
    print("\n=== LEVEL-00 INTERNAL CHAIN ===")
    level_readme = "projects/level-00-absolute-beginner/README.md"
    for i, proj in enumerate(LEVEL_00_PROJECTS):
        filepath = f"projects/level-00-absolute-beginner/{proj}/TRY_THIS.md"
        if i == 0:
            prev_f = level_readme
        else:
            prev_f = f"projects/level-00-absolute-beginner/{LEVEL_00_PROJECTS[i-1]}/TRY_THIS.md"
        if i == len(LEVEL_00_PROJECTS) - 1:
            next_f = level_readme
        else:
            next_f = f"projects/level-00-absolute-beginner/{LEVEL_00_PROJECTS[i+1]}/TRY_THIS.md"
        update_file(filepath, prev_f, next_f)

    # =================================================================
    # 3. LEVEL 0-10 INTERNAL CHAINS (README.md files)
    # =================================================================
    for level_num, projects in LEVEL_PROJECTS.items():
        print(f"\n=== LEVEL-{level_num} INTERNAL CHAIN ===")
        level_readme = f"projects/level-{level_num}/README.md"
        for i, proj in enumerate(projects):
            filepath = f"projects/level-{level_num}/{proj}/README.md"
            if i == 0:
                prev_f = level_readme
            else:
                prev_f = f"projects/level-{level_num}/{projects[i-1]}/README.md"
            if i == len(projects) - 1:
                next_f = level_readme
            else:
                next_f = f"projects/level-{level_num}/{projects[i+1]}/README.md"
            update_file(filepath, prev_f, next_f)

    # =================================================================
    # 4. ELITE TRACK INTERNAL CHAIN
    # =================================================================
    print("\n=== ELITE TRACK INTERNAL CHAIN ===")
    elite_readme = "projects/elite-track/README.md"
    for i, proj in enumerate(ELITE_PROJECTS):
        filepath = f"projects/elite-track/{proj}/README.md"
        if i == 0:
            prev_f = elite_readme
        else:
            prev_f = f"projects/elite-track/{ELITE_PROJECTS[i-1]}/README.md"
        if i == len(ELITE_PROJECTS) - 1:
            next_f = elite_readme
        else:
            next_f = f"projects/elite-track/{ELITE_PROJECTS[i+1]}/README.md"
        update_file(filepath, prev_f, next_f)

    print("\n=== DONE ===")
    print(f"Main chain: {len(MAIN_CHAIN)} files")
    print(f"Level-00: {len(LEVEL_00_PROJECTS)} projects")
    for k, v in LEVEL_PROJECTS.items():
        print(f"Level-{k}: {len(v)} projects")
    print(f"Elite: {len(ELITE_PROJECTS)} projects")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Rebuild complete navigation chain across the entire curriculum. "
        "Updates every markdown file with consistent prev/home/next navigation links.",
    )
    parser.parse_args()
    main()
