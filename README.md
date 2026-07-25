# agents-md-django

A reusable [`AGENTS.md`](AGENTS.md) starter for Django projects, plus the small
scripts that make its rules checkable instead of aspirational.

`AGENTS.md` is a convention for giving AI coding agents (Claude Code, Codex,
Copilot, Cursor, …) standing instructions about a repository. Most such files
are wish lists — this one ships with tooling, so an agent can *verify* it
followed the rules before calling a task done.

## What's in the box

- **[`AGENTS.md`](AGENTS.md)** — behavioral guidelines biased toward caution
  over speed: smallest change that works, read before write, ask before
  anything destructive, never guess when intent is ambiguous.
- **[`agent-scripts/`](agent-scripts/)** — stdlib-only Python checkers (plus two
  thin bash wrappers) that enforce the rules. No dependencies, so they run
  before any environment exists.

## The opinions

The template assumes a deliberately boring stack, chosen to keep an
agent-maintained codebase small and inspectable:

- **Django** with settings split into local / test / production.
- **Tailwind CSS via the standalone CLI** — no npm, no `package.json`,
  no `node_modules`, ever.
- **htmx + vanilla JavaScript** — HTML, CSS, and JS in separate files; no
  inline scripts, style blocks, or `onclick=` handlers in templates.
- **pip-tools** — dependencies declared in `requirements.in`, compiled to
  `requirements.txt`, installed only from the compiled file into `.venv`.
- **File size limits** — files that grow past a threshold get split along
  responsibility boundaries, not crammed together.
- **An `AGENTS.md` in every directory** — each one says *why* the directory
  exists and what its boundaries are, extending (never restating) the root file.
- **Lean tests** — a few request→response tests over many unit tests; a test
  exists only if it guards a behavior you can name in one sentence.

Disagree with an opinion? Edit the template — it's yours after you copy it.
The structure (rules + checkers + an Exceptions section + a mistakes log) is
the part worth keeping.

## The scripts

| Script | Checks |
|---|---|
| `check_all.sh` | Runs everything below; use before finishing a task. |
| `check_sizes.py` | File line counts and line lengths vs the thresholds table. |
| `check_templates.py` | No inline JS/CSS in templates (htmx `hx-*` allowed). |
| `check_requirements.py` | `requirements.in` / `requirements.txt` exist and are in sync. |
| `check_stack.py` | No npm/Node artifacts anywhere; `.venv` present. |
| `agents_md_status.py` | Every non-excluded directory has an `AGENTS.md`; `--for <files>` lists which ones to review for a change. |
| `changed_files.sh` | Changed/added/removed files; `--names` for a bare list to pipe into other checks. |

Every checker prints `WARN`/`FAIL` lines and exits non-zero only on hard
violations. A `WARN` is a prompt to think, not necessarily to act.

```console
$ agent-scripts/check_all.sh
── check_sizes.py ──
── check_templates.py ──
── check_requirements.py ──
── check_stack.py ──
── agents_md_status.py ──
check_all: all checks passed
```

## Using it in your project

1. Copy `AGENTS.md` and `agent-scripts/` into your repo root.
2. Adjust the stack rules and size thresholds to taste (the size table lives in
   `check_sizes.py`; the directory exclusion list in `agents_md_status.py`).
3. Write an `AGENTS.md` for each existing directory —
   `agent-scripts/agents_md_status.py` will list the missing ones.
4. Tell your agent to run `agent-scripts/check_all.sh` before finishing any
   task (the root `AGENTS.md` already instructs it to).

Two sections of `AGENTS.md` are meant to grow with the project:

- **Exceptions** — user-approved deviations from the rules, recorded before
  they're used. Nothing lands there without explicit approval.
- **Don't make the same mistake twice** — a short washup log: what went wrong,
  how to avoid it next time.
