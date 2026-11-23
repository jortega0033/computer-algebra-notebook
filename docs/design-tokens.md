# Design tokens

The visual system is the Pipenzo "Flow look": a black page, Flow-style alpha layers, one accent (Pipenzo yellow `#FECE02`), red only for danger. The accent marks the primary action, the current step and the current selection. Dark is the primary design.

## Source and resync

- File: `algebra_notebook/static/tokens.css`, a byte-for-byte copy of `extension/sidepanel/tokens.css` in `jortega0033/clip-to-reel-studio` at commit `a13378ce73e5b27213c9a200fc960ec93afef054` (2026-11-21).
- Resync: copy the file over `algebra_notebook/static/tokens.css`. Nothing else. Never edit the copy; change the source instead.
- The header comment of the file holds the contrast rules. The tokens are already contrast-checked.
- The header comment of `tokens.css` is narrower than this document: its yellow rule lists only the primary button, the current-step node, the turn chip and two dots, and it does not mention the current selection or the focus ring. This document takes precedence, because the copy must stay identical to the source and so the comment cannot be edited here.

## Rule

New UI uses these tokens. No new colour literals in CSS or JavaScript. Yellow only on the primary action, the current-step marker and the current selection (rule 8 of [ui-quality.md](ui-quality.md)); the focus ring is a separate case (14-D2). Text never sits on a bare alpha layer; use a solid surface token.

How this maps to this app, next to rule 8 of [ui-quality.md](ui-quality.md):

- `--primary` (yellow) only on the primary action, the current-step marker and the current selection. What the notebook's current-step marker is has not been decided by the owner: open, do not choose it in a ticket.
- 14-D1, current selection. The owner decided on 2026-11-23 that the yellow accent is used for the primary action, the current-step marker and the current selection. How it is drawn was recommended by the orchestrator and adopted under the owner's delegation of the same day: a selection is a solid `--primary` fill with `--on-primary` text, not only a yellow border (a yellow border has about 1.5:1 against white on light). It carries a second sign that is not colour (weight, an icon or text) and the existing aria attribute (the one the control already uses). For example `aria-selected`, `aria-current` or `aria-pressed`; no page exists yet, so the ticket that adds the control chooses the fitting one. Never a tint with a same-hue border and never a thick one-sided border.
- 14-D2, focus ring. `--focus` is a focus indicator and is exempt from the accent limit, including where it is yellow in dark. A ticket that says the focus style stays unchanged means the rule on main after the token pull request. This was recommended by the orchestrator and adopted under the owner's delegation of 2026-11-23.
- 14-D3, themes. Contrast and no-colour-alone checks cover both the light block and the dark block of `tokens.css`. This was recommended by the orchestrator and adopted under the owner's delegation of 2026-11-23.
- `--state-selected` is a neutral layer and is not used to mark the current selection; a selection uses the solid `--primary` fill of 14-D1. Its inline comment in `tokens.css` ("selected row / segment fill") gives way to this document, as the header comment does.
- Status of the page: there is no page yet. `algebra_notebook/static/` holds only the tokens; the page starts in ticket #15. Screens built in ticket work follow 14-D1 to 14-D3 from the start; this document does not claim any screen exists or follows them today.
- The labels 14-D1 to 14-D5 are the ids of owner decision 14 in [owner-decisions.md](owner-decisions.md). They are separate from the ids D1 to D10 in its Entry 10 table.

## Linking and serving

- 14-D4: a ticket that creates a page or its static allowlist links `tokens.css` before any other stylesheet and serves it (allowlist and its test). Recommended by the orchestrator, adopted under the owner's delegation of 2026-11-23.
- `index.html` (ticket #15, not built yet) must link `static/tokens.css` with `<link rel="stylesheet">` before `app.css`.
- The static-file allowlist (#10, #14, not built yet) must include `tokens.css`, and its test must cover it.
- The static-asset scan (#10, #15, not built yet) must cover it. The file holds no http(s) URL, no `style=`, no `.style.` and no `cssText`, so it meets those checks.

## Fonts

This repository ships no `fonts.css` and no font files, although the header of `tokens.css` mentions them. `--font` and `--font-display` resolve to local system fonts. Never load a web font from a CDN or Google Fonts; that breaks the offline and no-external-request rules and the #10 scan. Bundling font files needs an owner decision.

## Light and dark

The `:root` block is the light theme. A `prefers-color-scheme: dark` block overrides it, so the operating system colour scheme decides. There is no manual switch.

## Token names by role

- Surfaces: `--bg`, `--bg-raised`, `--surface`, `--bg-sunken`, `--hero-bg`, `--hero-border`, `--hero-chip-border`, `--ink`, `--ink-border`, `--grad-canvas`
- Text: `--fg`, `--muted`, `--faint`, `--on-hero`, `--on-hero-muted`, `--on-ink`, `--on-ink-muted`, `--on-media`, `--on-primary`
- Lines and controls: `--border`, `--hairline`, `--control-border`, `--input-border`, `--focus`, `--ring-accent`
- Accent: `--primary`, `--primary-press`, `--primary-edge`
- Status: `--success`, `--ok`, `--ok-bg`, `--warn-fg`, `--warn-bg`, `--danger`, `--danger-bg`, `--info`
- Layers and states: `--glass`, `--glass-strong`, `--glass-border`, `--glass-highlight`, `--glass-video`, `--glass-video-border`, `--scrim`, `--ink-hover`, `--state-hover`, `--state-selected`, `--btn-secondary`, `--btn-secondary-border`
- Shadows and gradients: `--shadow-1`, `--shadow-2`, `--shadow-3`, `--shadow-float`, `--shadow-on-video`, `--shadow-on-video-lg`, `--hero-shadow`, `--blur`, `--grad-scrim-bottom`, `--grad-ink`
- Type: `--font`, `--font-display`, `--mono`
- Space and radius: `--space-1` to `--space-7`, `--radius-control`, `--radius-card`, `--radius-media`, `--radius-hero`, `--radius-chip`, `--radius-pill`
- Motion: `--dur-1` to `--dur-4`, `--ease-out`, `--ease-in-out`

Rules 3 and 4 of [ui-quality.md](ui-quality.md) still apply: the glass, blur and shadow tokens exist in the file but are not a licence to use them on every card.

## Reading a token in JavaScript

```js
getComputedStyle(document.documentElement).getPropertyValue('--primary').trim()
```

The plot SVG should take stroke and fill from classes in `app.css` that use `var(--token)`; use the call above only where a colour must be set from code.
