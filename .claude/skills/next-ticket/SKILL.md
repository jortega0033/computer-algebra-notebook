---
name: next-ticket
description: Take the next ready ticket of epic #1 up to a ready pull request. Only the owner starts it; starting it is the go signal.
argument-hint: "[issue number]"
disable-model-invocation: true
---

# Next ticket

The owner runs this to start ticket work: `/next-ticket` for the next ready ticket, or `/next-ticket <issue number>` for one named ticket. Nothing starts it automatically and there is no scheduler. One ticket per run. It never merges and never starts another run by itself.

Read [`CLAUDE.md`](../../../CLAUDE.md) first (section "Delivery workflow"), then follow the playbook [`implement-ticket`](../implement-ticket/SKILL.md) for the ticket itself. This file only picks the ticket and drives the pull request.

Epic: [#1](https://github.com/jortega0033/computer-algebra-notebook/issues/1). Its table gives the dependency order. Labels: `status:ready`, `status:blocked`, `status:in-progress`, `needs-decision`, `tracking`.

Big tickets are split into sub-issues of 1 to 4 hours, one pull request each. A ticket labelled `tracking`, or with open sub-issues, is a container and is never picked.

## Steps

1. **Refresh the queue.** `gh issue list --label "status:blocked" --state open`. For each, read its "Prerequisites and dependencies" and the native "blocked by" links. If every blocker is closed, relabel it `status:ready` (remove `status:blocked`). Change no other label. Then check parents: a parent whose sub-issues are all closed is closed with a comment.
2. **Pick the ticket.** With an issue number, use that ticket and check it is open, not `status:in-progress`, not `needs-decision`, and all blockers are closed; otherwise stop and say why. If the number is a `tracking` parent, refuse it and list its open sub-issues. Without one, take the first `status:ready` leaf ticket (never a `tracking` parent) in the epic's order (the order of the parents in the epic's table, then the order of the sub-issues inside each parent) that is neither `status:in-progress` nor `needs-decision`. If there is none, stop and report the queue.
3. **Claim it.** Label the issue `status:in-progress` (remove `status:ready`) and comment that work started.
4. **Branch in a fresh worktree inside the project** from an up-to-date `main`: `git fetch origin`, then `git worktree add .claude/worktrees/<number> -b ticket-<number>-<short-slug> origin/main` (the folder is ignored by Git), then `cd .claude/worktrees/<number>`. Run every later command from there, including `gh pr create` and `gh pr ready`. Do not put the worktree outside the project folder: Claude Code resets the working directory of a Bash command to the project folder when the `cd` target is outside it, so the session would stay on clean `main`, the gate hook (which reads the changed files from the working directory of the hook event) would see no code changes and let `gh pr create` and `gh pr ready` through without Code Reviewer and Reality Checker, and every edit outside the project would ask for permission. After the `cd`, run `git branch --show-current`; if it does not print `ticket-<number>-<short-slug>`, stop and say so.
5. **Run the playbook** [`implement-ticket`](../implement-ticket/SKILL.md): local checks, then Code Reviewer, then Reality Checker, in that order, on the full diff and the recorded local evidence. Code Reviewer and Reality Checker have no shell: before calling them, write the diff and the evidence to `.claude/state/review/` in the ticket worktree (`git diff --stat origin/main...HEAD`, `git diff origin/main...HEAD`, the check outputs) and name those files in the request.
6. **Draft pull request.** Only after both gates passed: `gh pr create --draft`, with the template in `.github/pull_request_template.md` (`Closes #<number>`, evidence, agent roles run). If this is the last open sub-issue of a parent, the body also says `Closes #<parent>`. Acceptance steps that need a person (marked manual in the ticket) are done as far as an agent can, with evidence, and the rest is listed under "Owner checks". The gate hook allows it because both gates ran after the last code edit.
7. **CI, without polling.** After `gh pr create --draft` and `git push`, bind the pull request to the session if the app offers it, then end the turn with the line "Draft pull request #N is waiting for CI". Do not loop, sleep or watch. When the session is woken (a CI event, or the owner says "continue"), run `gh pr checks <pr>` once: still running, end the turn again with the same line; red, fix. If a check fails, fix, re-run local checks and both gates, push, and check again. Compare any failure with the latest run on `main` and say whether the change could have caused it.
8. **Ready.** When CI is green, `gh pr ready <pr>` (the hook checks the gates again) and comment on the issue with the pull request and the CI run link. Green CI is a condition for marking ready, checked here, not by Reality Checker.
9. **Stop.** Do not merge, tag, release or start the next ticket. Say which ticket is next in the queue.

If anything blocks the ticket (an open owner decision with no default, a spec that disagrees with the ticket, a gate that cannot run), stop, comment on the issue, label it `needs-decision` if it needs the owner, and leave the pull request as a draft.
