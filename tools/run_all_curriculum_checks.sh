#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FULL=0

if [[ "${1:-}" == "--full" ]]; then
  FULL=1
fi

cd "$ROOT_DIR"

echo "[1/9] markdown links"
./tools/check_markdown_links.sh

echo "[2/9] root doc contract"
./tools/check_root_doc_contract.sh

echo "[3/9] level index contract"
./tools/check_level_index_contract.sh

echo "[4/9] project README contract"
./tools/check_project_readme_contract.sh

echo "[5/9] project python comment/docstring contract"
./tools/check_project_python_comment_contract.sh

echo "[6/9] portable path contract"
./tools/check_portable_paths.sh

echo "[7/9] elite track contract"
./tools/check_elite_track_contract.sh

echo "[8/9] core project smoke checks"
if [[ "$FULL" -eq 1 ]]; then
  ./projects/run_smoke_checks.sh --full
else
  ./projects/run_smoke_checks.sh
fi

echo "[9/9] elite project smoke checks"
if [[ "$FULL" -eq 1 ]]; then
  ./projects/run_elite_smoke_checks.sh --full
else
  ./projects/run_elite_smoke_checks.sh
fi

echo "all curriculum checks passed"
