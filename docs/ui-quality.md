# UI quality rules

These ten rules are binding for every screen and every piece of user-facing copy in this repository. Rules 1 and 2 were stated by the owner; rules 3 to 10 were proposed and approved on 2026-11-22. See [owner-decisions.md](owner-decisions.md), entry 12.

1. No thick accent border on one side of a card, callout, alert, list item or quote (for example `border-left: 4px solid <accent>`). Use spacing, type weight, an icon or a full hairline border instead.
2. No soft tinted background with a thin border of the same hue as the default way to mark a status, tag, callout or card. One neutral surface and one clear signal (text, icon or a solid chip) is enough.
3. No gradient text and no purple-to-blue gradient as a default accent.
4. No blur or glass panels, and no drop shadow plus large radius on every card.
5. No emoji used as icons or bullets, and no sparkle marks.
6. No pill or badge on things that are not states. No all-caps, letter-spaced micro labels as section decoration.
7. No centred hero with a slogan in an application screen. Screens open on the user's task (here: the cell, the operation buttons and the result).
8. One accent colour, used for the primary action and the current selection. Status colours only for status.
9. Dense, aligned layouts on a consistent spacing scale. No card grid where a table or a list is the right form (the plot's text table is a table).
10. User-facing copy is plain and specific: no filler, no exclamation marks, and the same word for the same thing everywhere.

## How the rules are applied

- Rule 8 is read with the Rule section of [design-tokens.md](design-tokens.md) and owner decision 14 in [owner-decisions.md](owner-decisions.md): the accent also marks the current step, and `--focus` is a focus indicator, exempt from the accent limit.
- Colours, spacing, radii and type come from the tokens in `algebra_notebook/static/tokens.css`; see [design-tokens.md](design-tokens.md). New UI adds no colour literals.

- A UI ticket starts with the `ui-ux-pro-max` skill (design-system search for the product type; run `python .claude/skills/ui-ux-pro-max/scripts/search.py` as its `SKILL.md` describes) and ends with a check of the changed screens against this page. Record the check in the pull request.
- User-facing copy, documentation and pull request text go through the `unslop` skill before the pull request is opened.
- Frontend Developer, Accessibility Auditor and Code Reviewer name this page in their checklists. Enforcement is by the review gate (Code Reviewer on every ticket), not by a script. Rule 1 can be linted; rule 2 cannot be detected reliably from CSS.
- This repository ships plain HTML, CSS and browser JavaScript with no framework and no CDN (see `CLAUDE.md`). The stack-specific advice in the skill's data does not override that.
