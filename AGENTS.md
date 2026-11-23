# AGENTS.md

The full repository instructions are in [CLAUDE.md](CLAUDE.md). This file repeats only what an agent needs before it reads that.

The repository is a scaffold: the package layout, the entry point and smoke tests exist, but no product behaviour. The run command is planned (ticket #14). Do not report it as passing before then.

## Test commands

```
python -m unittest
```

Run it from the repository root. Python 3.12 or newer, standard library only. `python -m algebra_notebook --help` prints the usage. There is no lint step, no build step and no package manifest. Do not add pip or npm dependencies.

## Run (planned: ticket #14)

```
python -m algebra_notebook --data-dir ./notebook-data --port 8765
```

The server binds `127.0.0.1` only.

## Ticket work

To implement a GitHub issue, follow [.claude/skills/implement-ticket/SKILL.md](.claude/skills/implement-ticket/SKILL.md) and the section "Ticket implementation: agent roles run automatically" in [CLAUDE.md](CLAUDE.md). The role files in `.claude/agents/` each start with a section "In this repository" that holds the project rules for that role. An agent that cannot delegate to those roles does the steps itself and says so in the pull request. The review gate and the acceptance gate apply to every ticket, and the agent that wrote the change cannot pass them: stop, say that the gates could not run, and leave the run for the owner. Only the owner merges.

## Loop conventions

- The loop runs at L1: report-only, started by hand. It proposes; it does not label, comment, close, edit source, push or merge.
- No scheduler and no scheduled workflow is installed. Do not add one without the owner's approval.
- See [LOOP.md](LOOP.md) for the manual command and the human gates.

## Delivery

The owner starts ticket work with `/next-ticket`. Gates, CI, permissions and templates are described in the "Delivery workflow" section of [CLAUDE.md](CLAUDE.md). UI rules: [docs/ui-quality.md](docs/ui-quality.md). Owner decisions: [docs/owner-decisions.md](docs/owner-decisions.md).
