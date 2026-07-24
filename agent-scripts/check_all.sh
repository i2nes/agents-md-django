#!/usr/bin/env bash
# Run every conformity check against the repo. Intended before finishing a task.
#
# Usage:
#   check_all.sh [repo_root]    # default: the repo containing this script
#
# Exit code: 0 if every check passed, 1 if any check failed.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="${1:-$(dirname "$SCRIPT_DIR")}"
STATUS=0

run() {
    echo "── $1 ──"
    python3 "$SCRIPT_DIR/$1" "${@:2}" || STATUS=1
    echo
}

run check_sizes.py "$ROOT"
run check_templates.py "$ROOT"
run check_requirements.py "$ROOT"
run check_stack.py "$ROOT"
run agents_md_status.py "$ROOT"

if [[ $STATUS -eq 0 ]]; then
    echo "check_all: all checks passed"
else
    echo "check_all: FAILURES above — fix them or ask the user"
fi
exit $STATUS
