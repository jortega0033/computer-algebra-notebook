---
name: next-ticket
description: Take the next ready ticket of epic #1 up to a ready pull request. Only the owner starts it; starting it is the go signal.
argument-hint: "[issue number]"
disable-model-invocation: true
---

# Next ticket

The owner runs this to start ticket work: `/next-ticket` for the next ready ticket, or `/next-ticket <issue number>` for one named ticket. Nothing starts it automatically and there is no scheduler. One ticket per run. It never merges and never starts another run by itself.

Read [`CLAUDE.md`](../../../CLAUDE.md) first (section "Delivery workflow"), then follow the playbook [`implement-ticket`](../implement-ticket/SKILL.md) for the ticket itself. This file only picks the ticket and drives the pull request.

Epic: [#1](https://github.com/jortega0033/computer-algebra-notebook/issues/1). Its table gives the dependency order. Labels: `status:ready`, `status:blocked`, `status:in-progress`, `needs-decision`.

## Steps

1. **Refresh the queue.** `gh issue list --label "status:blocked" --state open`. For each, read its "Prerequisites and dependencies" and the native "blocked by" links. If every blocker is closed, relabel it `status:ready` (remove `status:blocked`). Change no other label.
2. **Pick the ticket.** With an issue number, use that ticket and check it is open, not `status:in-progress`, not `needs-decision`, and all blockers are closed; otherwise stop and say why. Without one, take the first `status:ready` child of epic #1 in the epic's dependency order that is neither `status:in-progress` nor `needs-decision`. If there is none, stop and report the queue.
3. **Claim it.** Label the issue `status:in-progress` (remove `status:ready`) and comment that work started.
4. **Branch in a fresh worktree** from an up-to-date `main`: `git fetch origin`, then `git worktree add ../computer-algebra-notebook-ticket-<number> -b ticket-<number>-<short-slug> origin/main`. Work only inside that worktree.
5. **Run the playbook** [`implement-ticket`](../implement-ticket/SKILL.md): local checks, then Code Reviewer, then Reality Checker, in that order, on the full diff and the recorded local evidence.
6. **Draft pull request.** Only after both gates passed: `gh pr create --draft`, with the template in `.github/pull_request_template.md` (`Closes #<number>`, evidence, agent roles run). The gate hook allows it because both gates ran after the last code edit.
7. **CI.** `gh pr checks <pr> --watch` once. If a check fails, fix, re-run local checks and both gates, push, and check again. Compare any failure with the latest run on `main` and say whether the change could have caused it.
8. **Ready.** When CI is green, `gh pr ready <pr>` (the hook checks the gates again) and comment on the issue with the pull request and the CI run link. Green CI is a condition for marking ready, checked here, not by Reality Checker.
9. **Stop.** Do not merge, tag, release or start the next ticket. Say which ticket is next in the queue.

If anything blocks the ticket (an open owner decision with no default, a spec that disagrees with the ticket, a gate that cannot run), stop, comment on the issue, label it `needs-decision` if it needs the owner, and leave the pull request as a draft.
