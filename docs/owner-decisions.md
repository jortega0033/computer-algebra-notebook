# Owner decisions

A dated record of the decisions the owner made for this repository, so the rules do not depend on anyone's memory of a conversation. Changing any entry needs the owner. An agent that finds a decision blocking a ticket stops and says so.

Entries 1 to 12 are dated 2026-11-22; entries 13 and 14 are dated 2026-11-23.

| # | Decision | Implemented in |
|---|---|---|
| 1 | The instructions, tooling and playbook live on the default branch. | `CLAUDE.md`, `AGENTS.md`, `.claude/` and `.github/` on `main` once the preparation pull request is merged |
| 2 | Persona agents run automatically during ticket work and carry instructions tailored to this project. | `.claude/agents/*.md` ("Use proactively" in each `description`, section "In this repository"), [`implement-ticket`](../.claude/skills/implement-ticket/SKILL.md) |
| 3 | Every open ticket is about app implementation. Tooling is installed, not ticketed. | Epic #1 and its children; the one CI guard removal sits inside ticket #2 |
| 4 | Agents may take a ticket up to a ready pull request. Only the owner merges and releases. | `CLAUDE.md` (Git workflow, Delivery workflow), [`next-ticket`](../.claude/skills/next-ticket/SKILL.md), `.claude/settings.json` (`gh pr merge` and releases denied), [`RELEASING.md`](RELEASING.md) |
| 5 | No scheduler. Ticket work starts only on the owner's go signal, because the repository is used to train AI models. `/next-ticket` is the normal entry (it claims the ticket and sets the labels); `implement-ticket` can also start from a direct user request, but then claiming and labelling the issue is up to the user. | `next-ticket` (`disable-model-invocation: true`), `LOOP.md` |
| 6 | A review gate hook blocks opening or readying a pull request until the gate roles (Code Reviewer, Reality Checker) have run after the last code edit. | `.claude/hooks/role_gate.py` and the hooks in `.claude/settings.json`; switch it off for a session with `ROLE_GATE=off` in the environment Claude Code is started from |
| 7 | Loop Engineering stays at L1, report-only and unscheduled. | `LOOP.md`, `loop-constraints.md` |
| 8 | Continuous integration runs on Linux and Windows; the default branch requires a pull request and green checks. | `.github/workflows/ci.yml`; branch protection is set on GitHub by the orchestrator after the merge |
| 9 | Permission rules: documented commands are allowed; force pushes, pushes to the default branch, merges, releases and reads of secrets are denied; edits to CI, agent configuration and Loop files ask first. | `.claude/settings.json` |
| 10 | Open decisions on tickets are settled with the ticket's stated default. | See the list below |
| 11 | Rust (where present) is verified in CI only. | Not applicable: this repository has no Rust. |
| 12 | The ten UI rules in `docs/ui-quality.md` are binding, and the `ui-ux-pro-max` and `unslop` skills are installed in the repository and used for UI work and for copy. | [`ui-quality.md`](ui-quality.md), `.claude/skills/ui-ux-pro-max/`, `.claude/skills/unslop/` |
| 13 | Visual system: Pipenzo Flow look tokens ([docs/design-tokens.md](design-tokens.md)). SDLC kit version: jortega0033/sdlc-kit v1.0.0. (2026-11-23) | `algebra_notebook/static/tokens.css`, [`design-tokens.md`](design-tokens.md) |
| 14 | Accent, focus, themes and linking rules for the design tokens (2026-11-23). D1 Current selection: the yellow accent is used for the primary action, the current-step marker and the current selection (UI rule 8). Decided by the owner on 2026-11-23. How (recommended by the orchestrator, adopted under the owner's delegation of the same day): a selection uses a solid --primary fill with --on-primary text (not only a yellow border, which has about 1.5:1 against white on light), plus a second sign that is not colour (weight, icon or text) and the existing aria attribute. Never a tint with a same-hue border and never a thick one-sided border. D2 Focus ring: --focus is a focus indicator, exempt from the accent limit, including where it is yellow in dark. A ticket that says the focus style stays unchanged means the rule on main after the token pull request. Recommended by the orchestrator, adopted under the owner's delegation of 2026-11-23. D3 Themes: contrast and no-colour-alone checks cover both the light and the dark block of tokens.css. Recommended by the orchestrator, adopted under the owner's delegation of 2026-11-23. D4 Linking: a ticket that creates a page or its static allowlist links tokens.css before any other stylesheet and serves it (allowlist and its test). Recommended by the orchestrator, adopted under the owner's delegation of 2026-11-23. D5 release-dependency-planner: while a plan is open only one yellow primary button shows; "New plan" (#new-plan) becomes neutral, in ticket #11. Recommended by the orchestrator, adopted under the owner's delegation of 2026-11-23. | [`design-tokens.md`](design-tokens.md) (D1 to D3); D4 and D5 apply in ticket work |

## Entry 10: decisions settled with the ticket default

This page is the record. The ticket plan copies the list into the "Open owner decisions" section of epic [#1](https://github.com/jortega0033/computer-algebra-notebook/issues/1) when it is applied to GitHub; until then the live epic body still has the older text. "E21-7" and "E21-9" are plan IDs of tickets whose issue numbers GitHub assigns when they are created.

| Id | Question | Default taken | Applies to |
|---|---|---|---|
| D1 | Minimum Python | 3.12 (CPython; CI runs 3.12 and 3.13) | #2 |
| D2 | Browser target and browser verification | Current stable Chrome; verified by a documented manual flow plus HTTP-level tests; no browser automation dependency | #2, #7 |
| D3 | SQLite transaction strategy | One short connection per write, `BEGIN IMMEDIATE`, head compare and revision insert in one transaction, default rollback journal, `synchronous=FULL`, `PRAGMA user_version` as schema version | #2, #6 |
| D4 | Package and module names | `algebra_notebook` with the layout in `docs/architecture.md` | #2 |
| D5 | Meaning of "localized errors" | Located at the input span, in English; no translation | #2, E21-7 |
| D6 | Optional SymPy cross-check | Not included in this batch; the hand-calculated fixtures are the oracle | #7 (recorded as not run) |
| D7 | Persist derived results | No; recompute on reopen | #6 |
| D8 | Diagnostic class of caps and unsupported forms | `limit` for exponent above 12, node cap and similar; `unsupported` for irrational quadratic roots and non-affine divisors; `domain` for division by constant zero | E21-7, #3, #4 |
| D9 | Writes without an Origin header | Rejected | #2, E21-9 |
| D10 | Licence | Not selected; no ticket adds a licence file; the owner decides separately and it blocks no ticket | none (blocks no ticket) |
