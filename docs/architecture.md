# Implementer map

**Planned, not implemented.** This page adds only what the product plan and technical specification leave open: where the code goes and where the contracts are frozen. It does not repeat their rules. Ticket #2 creates the first files and must correct this page to match what exists.

Sources: [PRD](PRD.md), [technical specification](TECHNICAL_SPEC.md).

## Layout (proposed default, fixed by ticket #2)

```text
algebra_notebook/
  __main__.py        command line: --data-dir, --port (loopback only)
  parser.py          tokens, grammar, typed tree, spans, limits
  algebra.py         rational polynomials, reduced P/Q, excluded values, canonical text
  operations.py      simplify, evaluate, differentiate, solve
  plotting.py        exact-grid sampling, discontinuity classes, series
  diagnostics.py     the four diagnostic classes and their JSON form
  store.py           SQLite notebooks, cells, append-only revisions, compare-and-set head
  service.py         loopback HTTP, request guards, JSON routes, static files
  static/            index.html, app.css, app.js (text-only rendering, SVG plot)
tests/               unittest modules, fixtures as data in tests/fixtures/
```

Dependencies point down the list: `service` may import everything; `store` imports nothing from the algebra modules; `parser` imports nothing but `diagnostics`.

## Contracts frozen by ticket #2

Ticket #2 writes these into this page as examples taken from running code, and later tickets extend them without breaking them:

- **Compute request**: operation name, source text, options (for example the x value for Evaluate, the bounds for Plot).
- **Compute response**: either a result with its excluded x values, or exactly one diagnostic (class, message, input span). Never both.
- **Cell**: stable cell ID, position, source, operation, options.
- **Notebook save**: base revision plus the full ordered cell list; the response is the new revision or a conflict.

Ticket #3 freezes the canonical result and domain shape that tickets #4, #5 and the stale-result ticket build on.

## Where a request goes

Browser cell, `POST` to a compute route, `service` guards the request, `parser` builds the typed tree, `operations` call `algebra`, the response is rendered as text by `static/app.js`. Save goes browser, `service`, `store`, and the response names the new revision.
