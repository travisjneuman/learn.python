#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR/elite-track"
FULL_MODE=0
KEEP_ARTIFACTS=0

usage() {
  cat <<'USAGE'
Usage:
  ./run_elite_smoke_checks.sh [--full] [--keep-artifacts]

Options:
  --full            Run all elite projects.
  --keep-artifacts  Keep generated output_summary.json and cache artifacts.
  -h, --help        Show this help.
USAGE
}

for arg in "$@"; do
  case "$arg" in
    --full) FULL_MODE=1 ;;
    --keep-artifacts) KEEP_ARTIFACTS=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $arg" >&2; usage; exit 2 ;;
  esac
done

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 is required but not found in PATH." >&2
  exit 1
fi

if [[ ! -d "$ROOT_DIR" ]]; then
  echo "ERROR: missing elite-track directory at $ROOT_DIR" >&2
  exit 1
fi

echo "[info] elite root: $ROOT_DIR"
echo "[info] full mode: $FULL_MODE"

echo "[check] compiling elite python files"
py_files=$(find "$ROOT_DIR" -type f -name '*.py' | sort)
python3 -m py_compile $py_files

selected_projects=()
if [[ "$FULL_MODE" -eq 1 ]]; then
  while IFS= read -r d; do
    selected_projects+=("$d")
  done < <(find "$ROOT_DIR" -mindepth 1 -maxdepth 1 -type d | sort)
else
  while IFS= read -r d; do
    selected_projects+=("$d")
  done < <(find "$ROOT_DIR" -mindepth 1 -maxdepth 1 -type d | sort | head -n 3)
fi

total=${#selected_projects[@]}
passed=0
failed=0

for proj in "${selected_projects[@]}"; do
  rel_path="${proj#${SCRIPT_DIR}/}"
  echo "[run] $rel_path"
  if (cd "$proj" && python3 project.py --input data/sample_input.txt --output data/output_summary.json --run-id elite-smoke >/dev/null); then
    passed=$((passed+1))
  else
    failed=$((failed+1))
    echo "  -> FAIL: $rel_path" >&2
  fi
done

echo "[summary] total=$total passed=$passed failed=$failed"

if [[ "$KEEP_ARTIFACTS" -eq 0 ]]; then
  find "$ROOT_DIR" -type f -name 'output_summary.json' -delete
  find "$ROOT_DIR" -type d -name '__pycache__' -prune -exec rm -rf {} +
  find "$ROOT_DIR" -type f -name '*.pyc' -delete
fi

if [[ "$failed" -gt 0 ]]; then
  exit 1
fi

echo "[done] elite smoke checks passed"
