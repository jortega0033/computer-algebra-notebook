# Design tokens

The visual system is the Pipenzo "Flow look": a black page, Flow-style alpha layers, one accent (Pipenzo yellow `#FECE02`), red only for danger. Dark is the primary design.

## Source and resync

- File: `algebra_notebook/static/tokens.css`, a byte-for-byte copy of `extension/sidepanel/tokens.css` in `jortega0033/clip-to-reel-studio` at commit `a13378ce73e5b27213c9a200fc960ec93afef054` (2026-11-21).
- Resync: copy the file over `algebra_notebook/static/tokens.css`. Nothing else. Never edit the copy; change the source instead.
- The header comment of the file holds the contrast rules. The tokens are already contrast-checked.

## Rule

New UI uses these tokens. No new colour literals in CSS or JavaScript. Yellow only on the primary action and the current-step marker. Text never sits on a bare alpha layer; use a solid surface token.

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
