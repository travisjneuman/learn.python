#!/usr/bin/env bash
set -euo pipefail

# Smoke checker for the learning projects ladder.
# Default mode runs one representative project per level.
# --full mode runs every project in every level.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR"
FULL_MODE=0

usage() {
  cat <<'USAGE'
Usage:
  ./run_smoke_checks.sh [--full] [--keep-artifacts]

Options:
  --full            Run every project (all levels).
  --keep-artifacts  Keep generated output_summary.json and __pycache__ artifacts.
  -h, --help        Show this help.
USAGE
}

KEEP_ARTIFACTS=0
for arg in "$@"; do
  case "$arg" in
    --full) FULL_MODE=1 ;;
    --keep-artifacts) KEEP_ARTIFACTS=1 ;;
    -h|--help) usage; exit 0 ;;
    *)
      echo "Unknown argument: $arg" >&2
      usage
      exit 2
      ;;
  esac
done

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 is required but not found in PATH." >&2
  exit 1
fi

if [[ ! -d "$ROOT_DIR/level-0" || ! -d "$ROOT_DIR/level-10" ]]; then
  echo "ERROR: expected levels level-0 through level-10 under: $ROOT_DIR" >&2
  exit 1
fi

echo "[info] projects root: $ROOT_DIR"
echo "[info] full mode: $FULL_MODE"

echo "[check] validating level folders and project counts"
for level in $(seq 0 10); do
  level_dir="$ROOT_DIR/level-$level"
  if [[ ! -d "$level_dir" ]]; then
    echo "ERROR: missing directory $level_dir" >&2
    exit 1
  fi
  project_count=$(find "$level_dir" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
  if [[ "$project_count" != "15" ]]; then
    echo "ERROR: expected 15 projects in level-$level, found $project_count" >&2
    exit 1
  fi
  echo "  - level-$level ok (15 projects)"
done

echo "[check] compiling all python files"
py_files=$(find "$ROOT_DIR" -type f -name '*.py' | sort)
if [[ -z "$py_files" ]]; then
  echo "ERROR: no python files found under $ROOT_DIR" >&2
  exit 1
fi
while IFS= read -r f; do
  python3 -m py_compile "$f"
done <<< "$py_files"

echo "[check] selecting projects to run"
selected_projects=()
if [[ "$FULL_MODE" -eq 1 ]]; then
  # Only select direct project directories (level-X/project-name).
  while IFS= read -r d; do
    selected_projects+=("$d")
  done < <(find "$ROOT_DIR"/level-* -mindepth 1 -maxdepth 1 -type d | sort)
else
  for level in $(seq 0 10); do
    first_project=$(find "$ROOT_DIR/level-$level" -mindepth 1 -maxdepth 1 -type d | sort | head -n 1)
    if [[ -z "$first_project" ]]; then
      echo "ERROR: no projects found in level-$level" >&2
      exit 1
    fi
    selected_projects+=("$first_project")
  done
fi

total=${#selected_projects[@]}
passed=0
failed=0

for proj in "${selected_projects[@]}"; do
  rel_path="${proj#${ROOT_DIR}/}"
  echo "[run] $rel_path"

  cmd=(python3 project.py --input data/sample_input.txt --output data/output_summary.json)
  if [[ "$rel_path" == level-[7-9]/* || "$rel_path" == level-10/* ]]; then
    cmd+=(--run-id smoke-check)
  fi

  if (cd "$proj" && "${cmd[@]}" >/dev/null); then
    passed=$((passed+1))
  else
    failed=$((failed+1))
    echo "  -> FAIL: $rel_path" >&2
  fi
done

echo "[summary] total=$total passed=$passed failed=$failed"

if [[ "$KEEP_ARTIFACTS" -eq 0 ]]; then
  echo "[cleanup] removing generated artifacts"
  find "$ROOT_DIR" -type f -name 'output_summary.json' -delete
  find "$ROOT_DIR" -type d -name '__pycache__' -prune -exec rm -rf {} +
  find "$ROOT_DIR" -type f -name '*.pyc' -delete
fi

if [[ "$failed" -gt 0 ]]; then
  exit 1
fi

echo "[done] smoke checks passed"
