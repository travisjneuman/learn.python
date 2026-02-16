#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

expected_files=(
  "README.md"
  "01_ROADMAP.md"
  "02_GLOSSARY.md"
  "03_SETUP_ALL_PLATFORMS.md"
  "04_FOUNDATIONS.md"
  "05_AUTOMATION_FILES_EXCEL.md"
  "06_SQL.md"
  "07_SOLARWINDS_ORION.md"
  "08_DASHBOARDS.md"
  "09_QUALITY_TOOLING.md"
  "10_CAPSTONE_PROJECTS.md"
  "11_CHECKLISTS.md"
  "12_SCREENSHOT_CHECKPOINTS.md"
  "13_ENTERPRISE_SAMPLE_SCHEMAS.md"
  "14_NAVIGATION_AND_STUDY_WORKFLOW.md"
  "15_NEXT_LEVEL_EXPANSION_PLAN.md"
  "16_LEARNER_PROFILE_AND_PLACEMENT.md"
  "17_ASSESSMENT_AND_RUBRICS.md"
  "18_REMEDIATION_PLAYBOOK.md"
  "19_MENTOR_GUIDE.md"
  "20_CURRICULUM_CHANGELOG.md"
  "21_FULL_STACK_MASTERY_PATH.md"
  "22_SPECIALIZATION_TRACKS.md"
  "23_RESOURCE_AND_CURRICULUM_MAP.md"
  "24_MASTERY_SCORING_AND_GATES.md"
  "25_INFINITY_MASTERY_LOOP.md"
  "26_ZERO_TO_MASTER_PLAYBOOK.md"
  "27_DAY_0_TO_DAY_30_BOOTSTRAP.md"
  "28_LEVEL_0_TO_2_DEEP_GUIDE.md"
  "29_LEVEL_3_TO_5_DEEP_GUIDE.md"
  "30_LEVEL_6_TO_8_DEEP_GUIDE.md"
  "31_LEVEL_9_TO_10_AND_BEYOND.md"
  "32_DAILY_SESSION_SCRIPT.md"
  "33_WEEKLY_REVIEW_TEMPLATE.md"
  "34_FAILURE_RECOVERY_ATLAS.md"
  "35_CAPSTONE_BLUEPRINTS.md"
  "36_ELITE_ENGINEERING_TRACK.md"
  "37_QUARTERLY_EXAMS_AND_DEFENSES.md"
  "38_SYSTEM_DESIGN_AND_RFCS.md"
  "39_PRODUCTION_PLATFORM_LAB.md"
  "40_SECURITY_COMPLIANCE_HARDENING.md"
  "41_PERFORMANCE_ENGINEERING_LAB.md"
  "42_OPEN_SOURCE_CONTRIBUTION_LANE.md"
  "43_PUBLIC_PROOF_OF_WORK_PORTFOLIO.md"
  "44_SME_INTERVIEW_AND_DEBATE_BANK.md"
  "45_MASTERY_TELEMETRY_AND_REMEDIATION.md"
  "46_ACCESSIBILITY_AND_LEARNING_PROFILE_PLAYBOOK.md"
  "47_DIAGNOSTIC_AND_PERSONALIZED_STUDY_ENGINE.md"
  "48_MISCONCEPTION_AND_FAILURE_ATLAS_EXPANDED.md"
  "49_COMPETENCY_COVERAGE_AND_GAP_CLOSURE_MATRIX.md"
  "50_CERTIFICATION_GRADE_COMPLETION_PROTOCOL.md"
)

fail=0

expected_next() {
  case "$1" in
    README.md) echo "01_ROADMAP.md" ;;
    01_ROADMAP.md) echo "02_GLOSSARY.md" ;;
    02_GLOSSARY.md) echo "03_SETUP_ALL_PLATFORMS.md" ;;
    03_SETUP_ALL_PLATFORMS.md) echo "04_FOUNDATIONS.md" ;;
    04_FOUNDATIONS.md) echo "09_QUALITY_TOOLING.md" ;;
    09_QUALITY_TOOLING.md) echo "05_AUTOMATION_FILES_EXCEL.md" ;;
    05_AUTOMATION_FILES_EXCEL.md) echo "06_SQL.md" ;;
    06_SQL.md) echo "07_SOLARWINDS_ORION.md" ;;
    07_SOLARWINDS_ORION.md) echo "08_DASHBOARDS.md" ;;
    08_DASHBOARDS.md) echo "10_CAPSTONE_PROJECTS.md" ;;
    10_CAPSTONE_PROJECTS.md) echo "11_CHECKLISTS.md" ;;
    11_CHECKLISTS.md) echo "12_SCREENSHOT_CHECKPOINTS.md" ;;
    12_SCREENSHOT_CHECKPOINTS.md) echo "13_ENTERPRISE_SAMPLE_SCHEMAS.md" ;;
    13_ENTERPRISE_SAMPLE_SCHEMAS.md) echo "14_NAVIGATION_AND_STUDY_WORKFLOW.md" ;;
    14_NAVIGATION_AND_STUDY_WORKFLOW.md) echo "15_NEXT_LEVEL_EXPANSION_PLAN.md" ;;
    15_NEXT_LEVEL_EXPANSION_PLAN.md) echo "16_LEARNER_PROFILE_AND_PLACEMENT.md" ;;
    16_LEARNER_PROFILE_AND_PLACEMENT.md) echo "17_ASSESSMENT_AND_RUBRICS.md" ;;
    17_ASSESSMENT_AND_RUBRICS.md) echo "18_REMEDIATION_PLAYBOOK.md" ;;
    18_REMEDIATION_PLAYBOOK.md) echo "19_MENTOR_GUIDE.md" ;;
    19_MENTOR_GUIDE.md) echo "20_CURRICULUM_CHANGELOG.md" ;;
    20_CURRICULUM_CHANGELOG.md) echo "21_FULL_STACK_MASTERY_PATH.md" ;;
    21_FULL_STACK_MASTERY_PATH.md) echo "22_SPECIALIZATION_TRACKS.md" ;;
    22_SPECIALIZATION_TRACKS.md) echo "23_RESOURCE_AND_CURRICULUM_MAP.md" ;;
    23_RESOURCE_AND_CURRICULUM_MAP.md) echo "24_MASTERY_SCORING_AND_GATES.md" ;;
    24_MASTERY_SCORING_AND_GATES.md) echo "25_INFINITY_MASTERY_LOOP.md" ;;
    25_INFINITY_MASTERY_LOOP.md) echo "26_ZERO_TO_MASTER_PLAYBOOK.md" ;;
    26_ZERO_TO_MASTER_PLAYBOOK.md) echo "27_DAY_0_TO_DAY_30_BOOTSTRAP.md" ;;
    27_DAY_0_TO_DAY_30_BOOTSTRAP.md) echo "28_LEVEL_0_TO_2_DEEP_GUIDE.md" ;;
    28_LEVEL_0_TO_2_DEEP_GUIDE.md) echo "29_LEVEL_3_TO_5_DEEP_GUIDE.md" ;;
    29_LEVEL_3_TO_5_DEEP_GUIDE.md) echo "30_LEVEL_6_TO_8_DEEP_GUIDE.md" ;;
    30_LEVEL_6_TO_8_DEEP_GUIDE.md) echo "31_LEVEL_9_TO_10_AND_BEYOND.md" ;;
    31_LEVEL_9_TO_10_AND_BEYOND.md) echo "32_DAILY_SESSION_SCRIPT.md" ;;
    32_DAILY_SESSION_SCRIPT.md) echo "33_WEEKLY_REVIEW_TEMPLATE.md" ;;
    33_WEEKLY_REVIEW_TEMPLATE.md) echo "34_FAILURE_RECOVERY_ATLAS.md" ;;
    34_FAILURE_RECOVERY_ATLAS.md) echo "35_CAPSTONE_BLUEPRINTS.md" ;;
    35_CAPSTONE_BLUEPRINTS.md) echo "36_ELITE_ENGINEERING_TRACK.md" ;;
    36_ELITE_ENGINEERING_TRACK.md) echo "37_QUARTERLY_EXAMS_AND_DEFENSES.md" ;;
    37_QUARTERLY_EXAMS_AND_DEFENSES.md) echo "38_SYSTEM_DESIGN_AND_RFCS.md" ;;
    38_SYSTEM_DESIGN_AND_RFCS.md) echo "39_PRODUCTION_PLATFORM_LAB.md" ;;
    39_PRODUCTION_PLATFORM_LAB.md) echo "40_SECURITY_COMPLIANCE_HARDENING.md" ;;
    40_SECURITY_COMPLIANCE_HARDENING.md) echo "41_PERFORMANCE_ENGINEERING_LAB.md" ;;
    41_PERFORMANCE_ENGINEERING_LAB.md) echo "42_OPEN_SOURCE_CONTRIBUTION_LANE.md" ;;
    42_OPEN_SOURCE_CONTRIBUTION_LANE.md) echo "43_PUBLIC_PROOF_OF_WORK_PORTFOLIO.md" ;;
    43_PUBLIC_PROOF_OF_WORK_PORTFOLIO.md) echo "44_SME_INTERVIEW_AND_DEBATE_BANK.md" ;;
    44_SME_INTERVIEW_AND_DEBATE_BANK.md) echo "45_MASTERY_TELEMETRY_AND_REMEDIATION.md" ;;
    45_MASTERY_TELEMETRY_AND_REMEDIATION.md) echo "46_ACCESSIBILITY_AND_LEARNING_PROFILE_PLAYBOOK.md" ;;
    46_ACCESSIBILITY_AND_LEARNING_PROFILE_PLAYBOOK.md) echo "47_DIAGNOSTIC_AND_PERSONALIZED_STUDY_ENGINE.md" ;;
    47_DIAGNOSTIC_AND_PERSONALIZED_STUDY_ENGINE.md) echo "48_MISCONCEPTION_AND_FAILURE_ATLAS_EXPANDED.md" ;;
    48_MISCONCEPTION_AND_FAILURE_ATLAS_EXPANDED.md) echo "49_COMPETENCY_COVERAGE_AND_GAP_CLOSURE_MATRIX.md" ;;
    49_COMPETENCY_COVERAGE_AND_GAP_CLOSURE_MATRIX.md) echo "50_CERTIFICATION_GRADE_COMPLETION_PROTOCOL.md" ;;
    50_CERTIFICATION_GRADE_COMPLETION_PROTOCOL.md) echo "README.md" ;;
    *) echo "" ;;
  esac
}

required_sections() {
  case "$1" in
    01_ROADMAP.md|03_SETUP_ALL_PLATFORMS.md|04_FOUNDATIONS.md|05_AUTOMATION_FILES_EXCEL.md|06_SQL.md|07_SOLARWINDS_ORION.md|08_DASHBOARDS.md|09_QUALITY_TOOLING.md|10_CAPSTONE_PROJECTS.md)
      cat <<'SECTIONS'
Who this is for
What you will build
Prerequisites
Step-by-step lab pack
Expected output
Break/fix drills
Troubleshooting
Mastery check
Learning-style options (Play/Build/Dissect/Teach-back)
SECTIONS
      ;;
    02_GLOSSARY.md)
      cat <<'SECTIONS'
Core programming terms
Environment and packaging terms
Quality terms
SQL and data terms
SolarWinds and monitoring terms
SECTIONS
      ;;
    11_CHECKLISTS.md)
      cat <<'SECTIONS'
Project startup checklist
Pre-run checklist
Post-run validation checklist
Incident triage checklist
Release and handoff checklist
Dashboard UX checklist (non-technical users)
SME conversation prep checklist
Screenshot and checkpoint checklist
SECTIONS
      ;;
    *)
      ;;
  esac
}

# File existence and home-link checks.
for file in "${expected_files[@]}"; do
  path="$ROOT_DIR/$file"
  if [[ ! -f "$path" ]]; then
    echo "missing root doc: $file"
    fail=1
    continue
  fi

  home_line="$(sed -n '2p' "$path")"
  if [[ "$home_line" != "Home: [README](./README.md)" ]]; then
    echo "bad home line: $file"
    fail=1
  fi

  # Ensure Next is the final heading.
  last_heading="$(rg '^## ' "$path" | tail -n1 || true)"
  if [[ "$last_heading" != "## Next" ]]; then
    echo "last heading is not ## Next: $file"
    fail=1
  fi

done

# Next-chain checks.
for file in "${expected_files[@]}"; do
  path="$ROOT_DIR/$file"
  [[ -f "$path" ]] || continue

  next_header_line="$(rg -n '^## Next$' "$path" | tail -n1 | cut -d: -f1 || true)"
  if [[ -z "$next_header_line" ]]; then
    echo "missing ## Next: $file"
    fail=1
    continue
  fi

  next_target="$(tail -n +$((next_header_line + 1)) "$path" | rg -n '^(Go to|Return to) \[[^]]+\]\(\./[^)]+\)' | head -n1 | sed -E 's#.*\(\./([^)]+)\).*#\1#' || true)"
  expected_target="$(expected_next "$file")"

  if [[ -z "$next_target" ]]; then
    echo "missing next link after ## Next: $file"
    fail=1
    continue
  fi

  if [[ "$next_target" != "$expected_target" ]]; then
    echo "bad next target in $file: expected $expected_target got $next_target"
    fail=1
  fi

done

# Source-section checks for root docs except README.
for file in "${expected_files[@]}"; do
  [[ "$file" == "README.md" ]] && continue
  path="$ROOT_DIR/$file"
  [[ -f "$path" ]] || continue

  if ! rg -n '^## Primary Sources$' "$path" >/dev/null; then
    echo "missing Primary Sources: $file"
    fail=1
  fi
  if ! rg -n '^## Optional Resources$' "$path" >/dev/null; then
    echo "missing Optional Resources: $file"
    fail=1
  fi

done

# Section contract checks for 01-11.
for file in "${expected_files[@]}"; do
  path="$ROOT_DIR/$file"
  [[ -f "$path" ]] || continue

  while IFS= read -r section; do
    [[ -z "$section" ]] && continue
    if ! rg -F -n "## $section" "$path" >/dev/null; then
      echo "missing section '$section' in $file"
      fail=1
    fi
  done < <(required_sections "$file")
done

# Stale README reference check.
if rg -n --glob '*.md' --glob '!PythonBootcamp/**' '00_README\.md' "$ROOT_DIR" >/dev/null; then
  echo "stale 00_README.md references found"
  fail=1
fi

if [[ "$fail" -ne 0 ]]; then
  echo "root doc contract check failed"
  exit 1
fi

echo "root doc contract verified"
