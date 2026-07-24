# agent-scripts/

Conformity-checking tools that make the root `AGENTS.md` rules verifiable instead of
aspirational. Agents run these during and at the end of a task; humans can too.

## Boundaries

- Scripts with logic are **Python, stdlib only** — no third-party imports, so they run
  before any environment exists. Thin git wrappers are bash.
- Each script does one job, prints `WARN`/`FAIL` lines, and exits non-zero only on
  hard violations. Keep them small and independent; `check_all.sh` is the only
  orchestrator.
- These scripts are review aids, not a substitute for judgment. A clean run does not
  mean the change is good; a `WARN` is a prompt to think, not necessarily to act.

## Tools

- `check_all.sh` — run every check; use before finishing a task.
- `check_sizes.py` — file line counts and line lengths vs the root thresholds table.
- `check_templates.py` — no inline JS/CSS in templates (htmx attributes allowed).
- `check_requirements.py` — `requirements.in` / `requirements.txt` exist and are in sync.
- `check_stack.py` — no npm/Node artifacts; `.venv` present.
- `agents_md_status.py` — fails on any non-excluded directory missing an `AGENTS.md`
  (owns the exclusion list); with `--for <files>`, lists the AGENTS.md files to
  review for a set of changed paths. Never looks outside the repo root.
- `changed_files.sh` — git changed/added/removed files; `--names` emits a bare list
  to pipe into the other checks.

## When adding a script

Update this file's Tools list in the same change, follow the same WARN/FAIL and
exit-code convention, and keep thresholds in one place — `check_sizes.py` owns the
size table; don't duplicate it elsewhere.
