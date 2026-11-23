# Implementer map

**Scaffolded, not implemented.** The files below exist as stubs with a one-line responsibility; `static/` is empty. This page adds only what the product plan and technical specification leave open: where the code goes and where the contracts are frozen. It does not repeat their rules. Tickets #12 to #15 fill these files and must correct this page to match what they build.

Sources: [PRD](PRD.md), [technical specification](TECHNICAL_SPEC.md).

## Layout (scaffolded; contracts frozen by ticket #2)

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

## Limit definitions

The caps themselves are in the technical specification; these definitions say what is counted, so tests and implementers agree.

- **Characters**: the length of the source text, checked before parsing.
- **Depth**: the parse-tree depth that bounds recursion. A literal or the symbol `x` is depth 1; every operator, unary, power or parenthesized-group node adds one level above its deepest child. Parentheses count, so 31 nested parentheses around `1` have depth 32 (accepted) and 32 have depth 33 (`limit`). A left-associative chain of 33 terms such as `1+1+...+1` also has depth 33.
- **Nodes**: every tree node, including parenthesized groups.
- Depth and nodes are checked while the tree is built, so deeply nested or unclosed input such as 1,000 opening parentheses returns the depth `limit` before any recursion limit is reachable.
- **Spans**: a diagnostic caused by the source text has an input span. Request-level failures (rejected Host or Origin, malformed JSON, oversized body, unknown route) have a class and a message and no span.
- **Plotting** is the separate module `plotting.py`; the plot operation in `operations.py` calls it. Plot work is capped separately from normalization.

## Where a request goes

Browser cell, `POST` to a compute route, `service` guards the request, `parser` builds the typed tree, `operations` call `algebra`, the response is rendered as text by `static/app.js`. Save goes browser, `service`, `store`, and the response names the new revision.
