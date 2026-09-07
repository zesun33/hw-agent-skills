#!/usr/bin/env bash
# verify.sh — verification suite for hw-agent-skills.
#
# Mirrors the strict engineering standard from hw-agent-tooling.
# Each gate is independent and exits non-zero on failure.
#
# Usage:
#   ./scripts/verify.sh              # full verification
#   ./scripts/verify.sh --gate N     # run only gate N

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

GATE=""
for arg in "$@"; do
  case "$arg" in
    --gate) shift; GATE="${1:-}" ;;
    --gate=*) GATE="${arg#--gate=}" ;;
    -h|--help)
      cat <<'EOF'
verify.sh — hw-agent-skills verification suite
  --gate N       Run only the given gate (1..5)
                   1  spec lock & package integrity
                   2  skill schema & frontmatter validation
                   3  unit tests
                   4  cursor .mdc rules sync
                   5  docs verification
EOF
      exit 0
      ;;
  esac
done

pass() { echo -e "\033[0;32m[PASS]\033[0m Gate $1: $2"; }
fail() { echo -e "\033[0;31m[FAIL]\033[0m Gate $1: $2"; exit 1; }

run_gate_1() {
  echo "--- Gate 1: Spec Lock & Package Integrity ---"
  test -f package.json || fail 1 "package.json missing"
  test -f LICENSE || fail 1 "LICENSE missing"
  pass 1 "Package files present and locked"
}

run_gate_2() {
  echo "--- Gate 2: Skill Schema & Frontmatter Validation ---"
  python3 scripts/validate_skills.py || fail 2 "Skill frontmatter validation failed"
  pass 2 "All 8 skills validated with proper YAML frontmatter"
}

run_gate_3() {
  echo "--- Gate 3: Unit Tests ---"
  python3 -m unittest discover tests || fail 3 "Unit tests failed"
  pass 3 "Unit test suite passed"
}

run_gate_4() {
  echo "--- Gate 4: Cursor .mdc Rules Sync ---"
  python3 scripts/export_cursor_rules.py || fail 4 "Cursor rule export failed"
  test -f .cursor/rules/rtl-reviewer.mdc || fail 4 "rtl-reviewer.mdc missing"
  test -f .cursor/rules/kernel-roofline-explainer.mdc || fail 4 "kernel-roofline-explainer.mdc missing"
  pass 4 "Cursor .mdc rules synchronized"
}

run_gate_5() {
  echo "--- Gate 5: Docs Verification ---"
  test -f README.md || fail 5 "README.md missing"
  grep -q "rtl-reviewer" README.md || fail 5 "README missing rtl-reviewer"
  grep -q "kernel-roofline-explainer" README.md || fail 5 "README missing kernel-roofline-explainer"
  pass 5 "Documentation complete"
}

case "${GATE}" in
  1) run_gate_1 ;;
  2) run_gate_2 ;;
  3) run_gate_3 ;;
  4) run_gate_4 ;;
  5) run_gate_5 ;;
  "")
    run_gate_1
    run_gate_2
    run_gate_3
    run_gate_4
    run_gate_5
    echo ""
    echo -e "\033[0;32m=== All Gates Cleared: hw-agent-skills Verified ===\033[0m"
    ;;
  *)
    fail "?" "Unknown gate: ${GATE}"
    ;;
esac
