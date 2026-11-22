# Agency Agents roles used in this repository

The Markdown files in `.claude/agents/` whose names start with `engineering-`, `security-` or `testing-` are copies of role definitions from Agency Agents. They are project-local Claude Code subagents. The file `loop-verifier.md` in the same folder is not from Agency Agents; it belongs to the Loop Engineering setup described in [`LOOP.md`](../../LOOP.md).

## Source and licence

- Upstream: https://github.com/msitarzewski/agency-agents
- Pinned revision: `8ae6164602c95ca78828b148b9052460ee426885` (upstream `main`, committed 2026-11-09)
- Licence: MIT, "Copyright (c) 2025 AgentLand Contributors". The upstream licence text at the pinned revision is kept unchanged in [`LICENSE`](LICENSE) next to this file (SHA-256 `9a45258434d5cedf0af73c9ad4771373701225038d246c49219026c33677f66f`). It covers only the copied role files, not the rest of this repository.
- Fetched with `gh api -H "Accept: application/vnd.github.raw" "repos/msitarzewski/agency-agents/contents/<path>?ref=<revision>"`.

## Installed roles

"Upstream SHA-256" is the hash of the file as fetched at the pinned revision. Reviewer roles have one added frontmatter line, `tools: Read, Grep, Glob`, so they cannot edit files or run commands. Nothing else in any file was changed by the first install.

| File in `.claude/agents/` | `name:` | Upstream path | Upstream SHA-256 | Local change |
|---|---|---|---|---|
| `engineering-software-architect.md` | Software Architect | `engineering/engineering-software-architect.md` | `b85121691776147bacde26673e68fbbacd6a7f0816d1ca8e203c264d25ce1d30` | added `tools: Read, Grep, Glob` |
| `engineering-code-reviewer.md` | Code Reviewer | `engineering/engineering-code-reviewer.md` | `7509fcc3ea1dda46511b2801996305bf3d4a125576f9655ff0b63df25602f446` | added `tools: Read, Grep, Glob` |
| `security-appsec-engineer.md` | Application Security Engineer | `security/security-appsec-engineer.md` | `a19f0bda46f4adca5737365dbc3c7ed93e9d93b71349536d92ff055dcf4e3b83` | added `tools: Read, Grep, Glob` |
| `testing-accessibility-auditor.md` | Accessibility Auditor | `testing/testing-accessibility-auditor.md` | `362935907af23839775b9c6162f38c0c5a740542ab4350cb5c5b5a0d9f9a4268` | added `tools: Read, Grep, Glob` |
| `testing-reality-checker.md` | Reality Checker | `testing/testing-reality-checker.md` | `6d32fcdb114233e13902ec6372d50293b120e85d490b5e81d372c29808f988a1` | added `tools: Read, Grep, Glob` |
| `engineering-backend-architect.md` | Backend Architect | `engineering/engineering-backend-architect.md` | `ac717bde4848d7663fff8a3c7edc711fd119256de6a7ce38c036619372f42c99` | none |
| `engineering-frontend-developer.md` | Frontend Developer | `engineering/engineering-frontend-developer.md` | `1ae4cc10b2e0163bd3ed921ad54080b865cd02e591becd8919b64b73fab06dad` | none |
| `testing-api-tester.md` | API Tester | `testing/testing-api-tester.md` | `ab91de9188d48bd9c417282c33673a37b066215e90e08c0f1b270d036084e3bb` | none |

## Why these roles

| Role | Use in this repository |
|---|---|
| Software Architect (read-only) | Review a ticket's design against the module map in [`docs/architecture.md`](../../docs/architecture.md) before code is written: where the parser, the exact algebra, the plot sampler and the revision store sit, and which contract each ticket freezes. |
| Code Reviewer (read-only) | Review a diff for correctness, missed edge cases and broken rules (exact arithmetic, excluded values kept, typed diagnostics, limits before allocation, compare-and-set on save). |
| Application Security Engineer (read-only) | Review the places where untrusted text meets the interpreter, the page or the database: the grammar and its caps, request guards, same-origin writes, text-only rendering, app-owned storage paths. |
| Accessibility Auditor (read-only) | Review keyboard operation, focus, labels and the text table that accompanies every plot. |
| Reality Checker (read-only) | Compare claimed evidence with what was actually run before a ticket or the epic is called done. |
| Backend Architect | Implement Python work: parser, algebra, operations, plotting, store, service. |
| Frontend Developer | Implement the browser page, cell editor, result panel and SVG plot in `algebra_notebook/static/`. |
| API Tester | Write the HTTP-level `unittest` cases for the compute and save routes. |

Most of these roles are written for larger stacks (frameworks, cloud services, Playwright, PostgreSQL, scanners). In this repository the rules in [`CLAUDE.md`](../../CLAUDE.md) win: CPython standard library only, SQLite, native HTML, CSS and JavaScript, `unittest`, no pip or npm dependencies, no external requests.

Roles that were considered and left out: Codebase Onboarding Engineer (there is no code to trace yet), Database Optimizer and Database Reliability Engineer (one small SQLite store with an append-only table; Software Architect and Backend Architect cover it), Test Automation Engineer and Performance Benchmarker (their methods need tools this repository does not allow; browser checks are manual and recorded, timings are recorded by the integration ticket), Technical Writer.

## Name collision with user-level agents

A developer who has installed Agency Agents in `~/.claude/agents/` already has agents with the same `name:` values. Claude Code gives the project-level definition precedence, so inside this repository the copies here are used, including the read-only tool limits. The upstream names were kept on purpose so that the roles stay recognisable and can be compared with upstream.

A Claude Code session that was already running when these files were added keeps the definitions it loaded at start. Start a new session to pick up the project copies.

## Updating

Fetch the same paths at a newer revision, re-apply the `tools:` line to the five reviewer roles, and update the revision and hashes in this file in the same commit.

## Local change: automatic delegation (2026-11-22)

One sentence beginning "Use proactively" was appended to the `description:` line of every Agency Agents role in `.claude/agents/` (not to `loop-verifier`). Claude Code uses that field to decide when to delegate, so the roles now run during ticket work without being named. 
A section headed "In this repository" was then inserted directly after the frontmatter of every Agency Agents role (not into `loop-verifier`), before the upstream text. It is project-specific text written for this repository, not upstream text: the planned stack and hard rules, the planned files the role owns or reviews, the planned commands (each marked as planned until ticket #2 merges), a checklist with its sources, the parts of the generic text that do not apply here, and what the role hands back. It ends with the sentence "This section and CLAUDE.md override the generic text below wherever they differ." Because there is no code yet, every file, module and command it names is a plan and must be corrected by the first ticket that makes it real.

This supersedes any statement above that a role file is unmodified or that the `tools:` line is the only local change. To compare a role with the pinned upstream file, remove the "Use proactively" sentence (in Backend Architect, Frontend Developer, API Tester and Reality Checker also the full stop that was added in front of it, because the upstream description has none), the section "In this repository" together with the blank line after it, and the `tools:` line where one was added; the result should have the upstream SHA-256 listed in the table above.

The steps at which each role runs are in `.claude/skills/implement-ticket/SKILL.md`.

Checked on 2026-11-22: with the three removals above, each of the eight files has the upstream SHA-256 listed in the table. Loading check, 2026-11-22, Claude Code 2.1.323, from the prep worktree root: `claude -p "List every project subagent in .claude/agents with its name and tools, say whether each starts with a section titled In this repository, and list the project skills." --model haiku` listed nine project subagents. Software Architect, Code Reviewer, Accessibility Auditor, Reality Checker, Application Security Engineer and loop-verifier showed `Read, Grep, Glob`; Frontend Developer, Backend Architect and API Tester showed no `tools:` field (default tools). Eight of nine start with "In this repository" (loop-verifier does not, by design). Skills listed: implement-ticket, next-ticket, issue-triage, loop-budget, loop-constraints, loop-intake, unslop, ui-ux-pro-max. The run printed a warning that the workspace was not trusted, so it ignored the 23 `permissions.allow` entries in `.claude/settings.json`; that does not affect agent or skill listing. Hooks were not exercised by this run.
