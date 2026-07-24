# AGENTS.md — root behavioral guidelines

Rules for AI agents working in this repository. They bias toward **caution over speed**:
prefer the smallest change that works, ask before anything destructive or irreversible,
and stop and ask when the stack or the user's intent is ambiguous.

> This file is a reusable template. When copying it into a project, keep the rules,
> replace nothing blindly, and grow the Exceptions / Mistakes sections from real events.

## Core behavior

- Make the smallest change that satisfies the request. Do not refactor, rename, or
  "improve" code you were not asked to touch.
- Read before you write: open a file (and its directory's `AGENTS.md`) before editing it.
- Ask before destructive or hard-to-reverse actions: deleting files, dropping or rewriting
  migrations, force-pushing, changing production configuration, bulk renames.
- When intent is ambiguous, or a task seems to require breaking a rule in this file,
  stop and ask instead of guessing.
- Never install, upgrade, or remove a dependency without following the
  requirements workflow below.

## Stack

Django, Tailwind CSS, htmx, and vanilla JavaScript. Nothing else without an approved
entry in the Exceptions section.

- **No npm** — ever. No `package.json`, no `node_modules`. Tailwind is built with the
  official **standalone CLI binary** (a single self-contained executable, no Node).
- Settings are split into **local, test, and production** configurations. Never merge
  them; never put production secrets in the repo.
- HTML, CSS, and JavaScript live in **separate files**. No inline `<script>` bodies,
  `<style>` blocks, `style=` attributes, or `onclick=`-style handlers in templates.
  htmx `hx-*` attributes are fine — that is what htmx is for.
- Any exception to html + css + vanilla JS must be proposed to the user and, if
  accepted, recorded in the Exceptions section before it is used.

## Python environment and dependencies

- Always use the virtual environment at **`.venv`** in the repo root. Create it if
  missing; never install into the system Python.
- Dependencies are declared in **`requirements.in`** and compiled to
  **`requirements.txt`** with pip-tools (`pip-compile`). Install only via
  `pip install -r requirements.txt` — never `pip install <package>` directly.
- Adding, upgrading, or removing a dependency means: edit `requirements.in`,
  recompile `requirements.txt`, and commit both in the same change.
  `agent-scripts/check_requirements.py` verifies they are in sync.

## File size and layout

Keep files small. When a file grows past its threshold, split it into a package of
smaller files (e.g. `views.py` → `views/` with one module per concern).

| Type    | Warn (lines) | Split at (lines) | Max line length |
|---------|--------------|------------------|-----------------|
| `.py`   | 300          | 500              | 100             |
| `.js`   | 200          | 400              | 100             |
| `.css`  | 400          | 600              | 100             |
| `.html` | 150          | 300              | (no limit)      |
| `.md`   | 200          | 400              | (no limit)      |

`agent-scripts/check_sizes.py` enforces this. Do not "fix" a violation by cramming
lines together — split the file along responsibility boundaries.

## Tests

The test suite is code, subject to the same anti-bloat and read-before-write rules.
A growing test count is not a goal — the aim is a suite that catches real regressions
with the fewest tests.

- Add a test only when it guards a behavior you can name in one sentence.
- Test observable behavior, not implementation. Prefer a few request→response tests
  (Django test client) over many unit tests. Use Django's test framework.
- Before adding a test, check whether an existing test already covers the guarantee —
  extend it rather than duplicate it.
- When you remove or change a behavior, delete or update its tests in the same change.
- Flag redundant or obsolete tests when you encounter them; don't let dead tests accumulate.
- Run the relevant tests before considering a change complete; report what you ran
  and the result.

## Directory-level AGENTS.md files

**Every directory has its own `AGENTS.md`** explaining **why** it exists, its
responsibility and boundaries, and any local conventions. The only exceptions are
machine-generated or vendored directories (`.git`, `.venv`, `__pycache__`,
`migrations`, `node_modules`, `staticfiles`, `vendor`, `media`, `.claude`). The
exclusion list lives in one place — `agent-scripts/agents_md_status.py` — which
fails when any other directory is missing its `AGENTS.md`. Creating a directory
means writing its `AGENTS.md` in the same change.

Directory files **extend** this one — they add local guidance and never restate global
rules. Keep them short and behavioral; no implementation details or task instructions.
Their job is to help contributors avoid duplicated code, duplicated styles/components,
bloat, wrong assumptions, and architectural drift.

**End-of-task review:** before finishing any development task, run
`agent-scripts/agents_md_status.py --for <changed files>` and review every `AGENTS.md`
on the path of what you changed. Update, add, or trim them if the purpose, structure,
or conventions of those directories changed.

## agent-scripts/

Conformity-checking tools. Run `agent-scripts/check_all.sh` before finishing a task;
see `agent-scripts/AGENTS.md` for the individual tools. Scripts with logic are Python
(stdlib only); thin git wrappers are bash.

## Exceptions

User-approved deviations from the rules above. Each entry: the rule bent, the scope,
and why the user accepted it. Nothing goes here without explicit user approval.

*(none yet)*

## Don't make the same mistake twice

When something goes wrong — a wrong assumption, a broken change, confusion, lost time —
do a washup with the user and record the lesson here. Entries are at most 3 lines:
what happened, and how to avoid it next time. If this section grows past ~10 entries,
graduate the oldest into a linked `MISTAKES.md`.

*(none yet)*
