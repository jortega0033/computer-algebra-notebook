# CLAUDE.md

Instructions for Claude Code and other coding agents working in this repository.

**Status: planning only.** There is no application code, no test suite and no manifest yet. Every command below is planned and marked with the ticket that introduces it. Do not report a command as passing until the ticket that introduces it has merged and you have run it.

## Product

An offline notebook for exact algebra in one real variable. A learner or developer types an expression into a browser cell, picks Simplify, Evaluate, Differentiate, Solve or Plot, and gets an exact result together with the x values it excludes. Notebooks are saved as append-only revisions in a local SQLite file, reopened after a restart, and protected from silent stale overwrites. The service listens on loopback only and makes no external requests.

## Source of truth

| Topic | Document |
|---|---|
| Scope, grammar, acceptance, fixtures, batch order | [docs/PRD.md](docs/PRD.md) |
| Runtime contract, exact algebra, plotting, persistence, fixtures | [docs/TECHNICAL_SPEC.md](docs/TECHNICAL_SPEC.md) |
| Module map and contract freeze points (planned) | [docs/architecture.md](docs/architecture.md) |
| Ticket order and acceptance | epic [#1](https://github.com/jortega0033/computer-algebra-notebook/issues/1) and its children |

If a document and a ticket disagree, stop and say so in the issue; do not pick silently. The fixtures in the technical spec are expected results, not observed ones. When a fixture first runs, record what the implementation actually printed.

## Stack and constraints

- CPython 3.12 or newer, standard library only. Exact arithmetic with `fractions.Fraction` and `int`. No pip or npm dependency in the runtime, no build step, no framework. SymPy is allowed only as an optional, pinned, offline checker for staged verification, never in the runtime and never fed raw learner input.
- SQLite through the standard `sqlite3` module for notebooks and revisions.
- Local HTML, CSS and browser JavaScript, no bundler, no CDN. Assets and fixtures ship in the repository.
- Bind to `127.0.0.1` only. Zero external requests. Writes need a same-origin check. Request size, input size and compute work are all capped. Storage paths are chosen by the app, never taken from a request.
- Input is data. It is parsed with a grammar into a typed tree. Never `eval`, `exec`, `compile` or `ast.literal_eval` learner input. Labels, results and errors reach the page as text (`textContent`), never as HTML.
- Starting caps (documented defaults, see the technical spec): 1,024 characters, 256 nodes, depth 32, polynomial degree 24, 2,048 bits per intermediate integer, exponent 0 to 12, 513 plot samples.
- Platforms: develop on Windows, verify on Linux in CI. Use `pathlib`, no shell scripts in the product, no POSIX-only calls.
- Everything written in this repository is in English. User-facing copy is plain and specific.

## Commands (all planned)

Run from the repository root. Use `python3` where `python` is not Python 3 (Linux).

| Purpose | Command | Status |
|---|---|---|
| Run the test suite (standard `unittest`, no extras) | `python -m unittest` | planned: introduced by ticket #2 |
| Start the service on loopback | `python -m algebra_notebook --data-dir ./notebook-data --port 8765` | planned: introduced by ticket #2 |
| Open the bundled demo | click "Open demo" in the page at `http://127.0.0.1:8765/` | planned: introduced by ticket #2, extended by ticket #7 |
| Clean-checkout check list | documented in `docs/verification.md` | planned: introduced by ticket #7 |

There is no lint, format or build step. Do not add one without an owner decision.

## Module boundaries (planned, see docs/architecture.md)

Dependencies point downward only; a lower module never imports a higher one.

1. `service` (HTTP, request guards, static files) and `static/` (browser UI) are the only layers that touch the network or the page.
2. `operations` (simplify, evaluate, differentiate, solve, and the plot operation) and `plotting` (exact-grid sampling, discontinuity classes, series, which `operations` calls) take a typed tree and return a structured result or one diagnostic.
3. `algebra` (rational polynomials, reduced rational expressions, excluded-value set, canonical formatting) is pure and exact.
4. `parser` (tokens, grammar, typed tree, spans, limits) is pure and does no algebra.
5. `store` (notebooks, cells, revisions, compare-and-set head) knows nothing about algebra.

Invariants that apply to every ticket:

- Exact until display: floats appear only for plot coordinates, after exact evaluation, with non-finite values guarded.
- The excluded x values always travel with a result. Cancelling a common factor never drops an exclusion.
- Failure is a typed diagnostic with a class (syntax, unsupported, domain, limit), a message and, when the failure comes from the input text, an input span. Request-level failures (rejected Host or Origin, malformed JSON, oversized body, unknown route) carry a class and message but no span. No stack trace reaches a response or the page.
- Limits are checked before allocation where practical.
- A save names the revision it is based on. A stale save returns a conflict and changes nothing.
- Output is canonical and deterministic: reduced fractions, positive denominators, stable ordering.

## Git workflow

- `main` is the default branch and is protected. Never commit to it and never force-push.
- One ticket, one branch, one pull request. Branch name `ticket-<issue number>-<short-slug>`, created from an up-to-date `main` in a worktree inside the project: `git worktree add .claude/worktrees/<issue number> -b <branch> origin/main`, then `cd` into it and run every later command, including `gh pr create` and `gh pr ready`, from there. A worktree outside the project folder is not allowed: the session working directory would stay on clean `main` and the gate hook would not see the changed files.
- Small commits in English, imperative mood. Do not commit `.env`, a notebook data directory or any `*.sqlite*`/`*.db` file.
- The pull request body starts with `Closes #<number>` and lists the evidence below. Agents open pull requests; only the owner merges.
- Do not publish, tag, release or deploy.

## Evidence before a ticket is called done

Say "done" only after all of these exist, and put them in the pull request:

1. Every acceptance criterion of the ticket, each tied to a test name or a recorded manual step.
2. The exact commands you ran (at least `python -m unittest` once it exists) and their observed output. Never report a result you did not see.
3. For any UI change, a manual run in Chrome of the documented flow with what you saw (typed input, visible result, excluded values, errors), plus the keyboard path for any new control.
4. For a fixture from the technical spec, the value the implementation printed next to the expected one.
5. Code Reviewer, then Reality Checker, on the full diff and the recorded evidence, with their verdicts. Reality Checker checks that the documented checks were run and passed and that CI is configured to run them.
6. CI green on the pull request, which is opened as a draft after the gates, before it is marked ready for review.
7. For any UI change, the changed screens checked against [docs/ui-quality.md](docs/ui-quality.md), and user-facing copy and pull request text run through the `unslop` skill.

Anything that could not be run is listed as not run, with the reason.

## Ticket implementation: agent roles run automatically

When asked to implement, continue or finish a GitHub issue, follow the playbook in [`.claude/skills/implement-ticket/SKILL.md`](.claude/skills/implement-ticket/SKILL.md). Claude Code loads it on its own for ticket work; `/implement-ticket <issue number>` starts it by hand.

Delegate to the project subagents in `.claude/agents/` without waiting to be asked:

- **Before coding:** Software Architect, as its description says.
- **While coding:** the implementing role that matches the files being changed.
- **After coding:** each specialist reviewer whose trigger matches the change.
- **On every ticket, before it is called done:** Code Reviewer, then Reality Checker.
- The session that wrote a change does not count as its reviewer.
- List the roles that ran and their verdicts in the pull request description under "Agent roles run".

Each role's `description` ends with a "Use proactively ..." sentence, which is what makes Claude Code delegate to it without being told. Each role file starts with a section "In this repository" written for this project (stack, planned files, commands, checklist, what does not apply); that section and this file override the generic upstream text below it. The five reviewer roles (Software Architect, Application Security Engineer, Accessibility Auditor, Code Reviewer, Reality Checker) are limited to `Read, Grep, Glob`, so the caller gives them the diff, the acceptance criteria and the recorded command output. Role provenance is in [`.claude/agency-agents/README.md`](.claude/agency-agents/README.md).

## Delivery workflow

- **Start:** the owner runs `/next-ticket`, the normal entry that claims the ticket and sets its labels (driver: [`.claude/skills/next-ticket/SKILL.md`](.claude/skills/next-ticket/SKILL.md)); there is no scheduler and nothing starts ticket work by itself. The playbook is [`implement-ticket`](.claude/skills/implement-ticket/SKILL.md).
- **Order:** local checks, then Code Reviewer and Reality Checker, then `gh pr create --draft`, then CI on the draft, then `gh pr ready` once CI is green and a comment on the issue with the CI run link.
- **Review gate hook:** [`.claude/hooks/role_gate.py`](.claude/hooks/role_gate.py) blocks `gh pr create` and `gh pr ready` until both gate roles ran after the last code edit (documentation-only changes pass). `ROLE_GATE=off` in the environment Claude Code is started from switches it off for that session; only the owner does that.
- **Permissions:** [`.claude/settings.json`](.claude/settings.json). Documented commands are allowed; force pushes, pushes to `main`, `gh pr merge`, releases and reads of `.env` are denied; edits to CI, agent configuration and Loop files ask first.
- **CI:** [`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs `python -m unittest` and the gate self-test on Linux and Windows with Python 3.12 and 3.13. Until ticket #2 creates `algebra_notebook/__main__.py`, a temporary guard skips the test command; ticket #2 removes it. Every required check must be green before a pull request is marked ready.
- **Templates and labels:** [pull request template](.github/pull_request_template.md), [ticket template](.github/ISSUE_TEMPLATE/implementation-ticket.md). Ticket labels: `status:ready`, `status:blocked`, `status:in-progress`, `needs-decision`.
- **Changelog:** every ticket pull request adds a line under `Unreleased` in [CHANGELOG.md](CHANGELOG.md).
- **UI and writing quality:** [docs/ui-quality.md](docs/ui-quality.md) (ten binding rules); skills `ui-ux-pro-max` and `unslop` in `.claude/skills/`.
- **Decisions:** [docs/owner-decisions.md](docs/owner-decisions.md) records what the owner decided. An agent that finds a decision blocking a ticket stops and says so.
- **Merging and releasing:** only the owner merges and releases ([docs/RELEASING.md](docs/RELEASING.md)). Security reports: [SECURITY.md](SECURITY.md).
