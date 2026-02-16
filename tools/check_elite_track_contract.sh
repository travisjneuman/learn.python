#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ELITE_DIR="$ROOT_DIR/projects/elite-track"

fail=0

if [[ ! -f "$ELITE_DIR/README.md" ]]; then
  echo "missing elite track index: projects/elite-track/README.md"
  exit 1
fi

if [[ "$(sed -n '2p' "$ELITE_DIR/README.md")" != "Home: [README](../../README.md)" ]]; then
  echo "bad elite track home link"
  fail=1
fi

expected_projects=(
  "01-algorithms-complexity-lab"
  "02-concurrent-job-system"
  "03-distributed-cache-simulator"
  "04-secure-auth-gateway"
  "05-performance-profiler-workbench"
  "06-event-driven-architecture-lab"
  "07-observability-slo-platform"
  "08-policy-compliance-engine"
  "09-open-source-maintainer-simulator"
  "10-staff-engineer-capstone"
)

for slug in "${expected_projects[@]}"; do
  if ! rg -F -- "- [$slug](./$slug/README.md)" "$ELITE_DIR/README.md" >/dev/null; then
    echo "missing elite index link: $slug"
    fail=1
  fi

  project_dir="$ELITE_DIR/$slug"
  readme="$project_dir/README.md"
  script="$project_dir/project.py"
  test_file="$project_dir/tests/test_project.py"
  input_file="$project_dir/data/sample_input.txt"

  for p in "$readme" "$script" "$test_file" "$input_file"; do
    if [[ ! -f "$p" ]]; then
      echo "missing elite file: ${p#$ROOT_DIR/}"
      fail=1
    fi
  done

  if [[ -f "$readme" ]]; then
    if [[ "$(sed -n '2p' "$readme")" != "Home: [README](../../../README.md)" ]]; then
      echo "bad elite project home link: ${readme#$ROOT_DIR/}"
      fail=1
    fi

    required_headings=(
      "## Run (copy/paste)"
      "## Expected terminal output"
      "## Expected artifacts"
      "## Alter it (required)"
      "## Break it (required)"
      "## Fix it (required)"
      "## Explain it (teach-back)"
      "## Mastery check"
      "## Next"
    )

    for heading in "${required_headings[@]}"; do
      if ! rg -F -n "$heading" "$readme" >/dev/null; then
        echo "missing heading '$heading' in ${readme#$ROOT_DIR/}"
        fail=1
      fi
    done

    if ! rg -F -n "Use \`<repo-root>\` as the folder containing this repository's \`README.md\`." "$readme" >/dev/null; then
      echo "missing <repo-root> note in ${readme#$ROOT_DIR/}"
      fail=1
    fi
  fi

  if [[ -f "$script" ]]; then
    first_non_empty="$(awk 'NF {print; exit}' "$script")"
    if [[ "$first_non_empty" != '"""'* ]]; then
      echo "missing module docstring at top: ${script#$ROOT_DIR/}"
      fail=1
    fi

    comment_lines="$(awk '/^\s*#/ {n++} END{print n+0}' "$script")"
    if [[ "$comment_lines" -lt 6 ]]; then
      echo "too few comment lines in ${script#$ROOT_DIR/}: $comment_lines (min 6)"
      fail=1
    fi
  fi

  if [[ -f "$test_file" ]]; then
    first_non_empty="$(awk 'NF {print; exit}' "$test_file")"
    if [[ "$first_non_empty" != '"""'* ]]; then
      echo "missing test module docstring at top: ${test_file#$ROOT_DIR/}"
      fail=1
    fi
  fi

done

if [[ "$fail" -ne 0 ]]; then
  echo "elite track contract check failed"
  exit 1
fi

echo "elite track contract verified"
