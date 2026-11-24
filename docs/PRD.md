# Computer Algebra Notebook

> This document specifies phase 1 of the program in [#28](https://github.com/jortega0033/computer-algebra-notebook/issues/28). Hour figures in it are early estimates for that phase; its open tickets add up to 58 to 84 hours (2026-11-24). Work that it defers is planned in the later phases only where the program names it.

Engineering plan for an original offline notebook. Product status is from scratch. The epic contains six future tickets and an estimated **14–22 engineering hours**.

## Product requirements

A learner or developer can enter an expression, inspect the exact result and its domain, compare related calculations across cells, and reopen a notebook later. The main workflow is to simplify a rational expression, differentiate it, and plot the result over a chosen interval. The result panel always shows excluded input values alongside the simplified expression.

**First working slice.** Start a local service, enter a fraction or a polynomial in one browser cell, and compute an exact value with a clear input error when needed. Open a bundled demo through an explicit action. Later slices add domain-preserving simplification, derivatives, equation solving, plots, and saved revisions.

**Success.** From a clean checkout, run the bundled notebook offline. Verify the independently calculated outcomes and plots below. Save the notebook, restart the service, and reopen the same cell order and inputs. Try an unsupported expression and confirm that its diagnostic points to the input span, leaves the previous saved revision intact, and never displays a stale result as current.

**Scope.** The epic covers one real variable, exact rational coefficients, bounded polynomial and rational operations, first derivatives, equations of degree at most two with rational roots, and local plot previews. General integration, transcendental functions, irrational root approximation, units, cross-cell variables, uploaded executable notebooks, and remote services are future work.

## Technical design

### Runtime and input contract

Use CPython 3.12 standard library for exact arithmetic and storage, SQLite for revisions, and local HTML, CSS, and browser JavaScript for the editor and plot. Bind to loopback. Ship all assets and original fixtures with the project. The implementation must use a grammar and typed expression tree. Parse input as data. Render labels and errors as text. Enforce same-origin writes, size limits, and app-owned storage paths.

- Accept decimal integer literals, finite decimal fractions with digits on both sides of the point, the symbol x, parentheses, unary minus or plus, and binary addition, subtraction, multiplication, division, and power. Decimal literals become exact rationals. Multiplication is explicit. Powers accept one integer literal from 0 through 12. Parenthesize nested powers. A power binds before a leading unary sign, so −x^2 means −(x^2). Multiplication and division share a precedence level and associate left to right, as do addition and subtraction. The defined formal polynomial convention is that a supported expression raised to power zero equals one on that expression’s original domain.
- Reject additional variable names, function calls, implicit multiplication, chained equality, exponent syntax, and text outside the grammar. Only the Solve operation accepts one top-level equality. Use separate diagnostic classes for invalid syntax, unsupported math, domain errors, and computation limits. A validation error points to the original token span. Set initial input limits of 1,024 characters, 256 nodes, depth 32, polynomial degree 24, and 2,048 bits per intermediate integer. Apply limits before allocation where practical and cap normalization and plot work separately. Treat caps as documented starting defaults.
- Provide explicit Simplify, Evaluate, Differentiate, Solve, and Plot operations. Each cell holds its own source and options, with no dependency on other cells. An Evaluate input x value and plot bounds accept exact rational literals. Structured responses include the result and domain, or one actionable diagnostic without a stack trace.

### Exact algebra, domain, and equality

Represent a polynomial as degree-ordered rational coefficients. Represent a rational expression as a reduced pair P/Q, with a monic nonzero Q, and the exact rational excluded x values inherited from the original syntax. Union child exclusions for each operation. Division adds the zeros of the reduced divisor numerator. In the supported profile this numerator must be a nonzero constant or affine polynomial. A constant zero divisor yields a domain error. A divisor numerator of higher degree yields an unsupported diagnostic. This rule allows products of affine denominator factors formed by multiplying intermediate rational expressions. Cancel polynomial GCD factors after tracking exclusions. Reducing a zero numerator to a zero polynomial retains its exclusions.

Use exact polynomial derivatives and the quotient rule. The result inherits the source exclusions. Solve by subtracting the expressions, working with the reduced numerator, and verifying every exact candidate in both original expressions. Apply rational quadratic roots only when the nonnegative discriminant is a rational square. A negative discriminant yields no real solution. A positive nonsquare discriminant yields an explicit unsupported-root result. Report an identically zero numerator as all real values in the declared domain. Sort and deduplicate exact candidates. Canonical output uses reduced positive-denominator fractions and stable leading-degree ordering. Keep exact values in results, with optional decimal previews labeled as approximations.

### Plotting and persistence

Use a browser SVG plot for mathematical curves and an accompanying text table. Sample up to 513 x values on an exact rational grid between the requested endpoints. Split line segments at every known domain boundary, even if a grid point does not land there. For a cancelled factor, display an open marker at the finite reduced value. For a residual denominator root, show a gap with a pole indicator and no marker. Never treat a clipped point or empty sample as an ordinary zero. Render coordinates in floating point only after exact evaluation and guard non-finite conversion. Derive accessibility labels from the same plot response.

Persist stable notebook and cell IDs, explicit cell ordering, raw source, operation, and options. Use an append-only revision record and transactional head update. Each save includes the prior revision and returns a new revision. A stale save returns a conflict and leaves the committed notebook untouched. Retain unsaved text and show a reload or copy action on conflict. Persist derived results only if the format includes the exact input digest and algebra engine version. A simpler first release recomputes on reopen. Ignore late compute responses after the cell input changes. Keep unsaved edits visible and separate from the last saved revision.

## Deterministic fixtures and verification

These are reasoned expectations for original fixtures. Capture observed outputs when implementation runs.

| Fixture | Expected result |
|---|---|
| Evaluate 0.1 + 0.2 | Exact 3/10, with no excluded x values |
| Simplify (x^2 − 1)/(x − 1) | x + 1 with x = 1 excluded. Evaluate at x = 2 gives 3. Evaluate at x = 1 reports undefined |
| Differentiate (x^2 − 1)/(x − 1) | Constant 1 with x = 1 still excluded |
| Solve (x^2 − 1)/(x − 1) = 2 | No solutions. The only candidate x = 1 is excluded |
| Solve x^2 − 5*x + 6 = 0 | Exact roots 2 and 3, in ascending order |
| Solve x^2 = 2 | Unsupported irrational roots, with no false no-solution result |
| Plot (x^2 − 1)/(x − 1) on [0, 3] | Two segments and an open marker at (1, 2), including with sample grids that skip x = 1 |
| Plot 1/(x − 1) on [0, 3] | Two segments with a pole at x = 1 and no finite open marker |

Build the reference fixture text using the implemented ASCII minus operator. The typography above uses the mathematical minus glyph for readability. Tests also cover 1/0, 1/(x^2 − 2), a second variable, a function call, an exponent above the cap, and malformed input spans. For the nested division 1/((x^2 − 1)/(x − 1)), expect 1/(x + 1) with both −1 and 1 excluded. The points come from the zero divisor and the inherited denominator restriction, respectively.

Use independent exact substitutions into the original expression for recorded solutions. Verify polynomial derivatives analytically against hand-calculated fixtures and generated low-degree coefficient vectors. Spot-check rational derivative quotients against independent exact expansions. Compare optional SymPy results for an explicitly staged version by constructing symbolic objects from validated fixtures. Keep SymPy out of the runtime and pass it no raw learner input. The original hand-calculated fixture suite has no third-party dependency. [SymPy calculus](https://docs.sympy.org/latest/tutorials/intro-tutorial/calculus.html) · [SymPy parser documentation](https://docs.sympy.org/latest/modules/parsing.html)

## Epic E21 · Preserve exact algebra and its domain in a reusable notebook

A developer or learner can compute, inspect, plot, and save a sequence of supported algebra operations locally. Release when all mandatory fixtures pass from an offline clean checkout, the saved notebook restores after restart, restricted expressions return bounded diagnostics, and two editors cannot silently overwrite a saved revision.

| Ticket | Scope | Depends on | Estimate |
|---|---|---|---:|
| E21-1 | Safe parser and exact first notebook cell | — | 2–3 h |
| E21-2 | Canonical rational simplification and domains | E21-1 | 3–5 h |
| E21-3 | Differentiation and equation solving | E21-2 | 3–4 h |
| E21-4 | Plot gaps, limits, and accessible table | E21-2 | 2–3 h |
| E21-5 | Notebook storage and revision conflict flow | E21-1 | 2–4 h |
| E21-6 | Offline integration and reference checks | E21-3, E21-4, E21-5 | 2–3 h |

**Batch order.** Freeze the request, response, and cell contracts in E21-1. Run E21-2 and E21-5 in parallel, with separate owners for the algebra engine and storage. After E21-2 freezes its canonical result and domain shape, run E21-3 and E21-4 in parallel. E21-6 integrates the lanes and runs the release checks. The estimates include implementation, tests, and integration.

### E21-1 · Safe parser and exact first notebook cell

Build the grammar, typed tree, diagnostic spans, bounds, loopback entry point, and single-cell flow. Acceptance requires 0.1 + 0.2 to produce 3/10 in the browser, unary power precedence to match the grammar, and malformed syntax or unknown names to display localized errors. An input over the exponent or node cap must stop with a specific diagnostic. Verify with parser table tests and the documented offline Chrome flow.

### E21-2 · Canonical rational simplification and domains

Implement polynomial arithmetic, rational normalization, operation-specific domain accumulation, and canonical formatting. Acceptance requires the cancellation fixture to simplify correctly while preserving x = 1 as an exclusion, even when multiplied by zero. Validate undefined and unsupported divisors independently. Verify with exact rational substitutions at included values, reparse checks for emitted expressions within the grammar profile, and separate tests of result-domain metadata.

### E21-3 · Differentiation and equation solving

Implement exact first derivatives and degree-limited real solving. Acceptance requires the derivative, cancellation-equation, integer-root, and nonsquare-discriminant cases above, a repeated root returned once, and a rational identity that reports its complete domain. Verify every successful candidate with the original input evaluator and compare the polynomial derivative set with independently generated expected coefficients.

### E21-4 · Plot gaps, limits, and accessible table

Build bounded exact-grid sampling, discontinuity classification, segmented curves, and a local textual representation. Acceptance requires both discontinuity fixtures to split independently of grid alignment, one finite open marker for the removable hole, and no marker for the pole. Invalid bounds and oversized requests return specific diagnostics. Verify the structured series and keyboard access in an offline browser.

### E21-5 · Notebook storage and revision conflict flow

Implement durable notebooks, cell order, revision head checks, and browser save/reopen. Acceptance requires an authored three-cell notebook to restore exact sources and order after restart. The second of two writes to the same base revision receives a conflict and retains editable unsaved input. Verify stored revision counts, both writer results, and deterministic recomputation after reopen.

### E21-6 · Offline integration and reference checks

Assemble the guided demo and documented clean-checkout checks. Run the mandatory fixtures in both direct service tests and the browser flow. Verify recovery after invalid input, stable canonical results across repeat runs, exact notebook reopen, and zero external requests. Report regression results and any platform or optional-oracle checks that could not run. Record reproducible operation timings before setting performance targets.

## Open implementation checks

Confirm the target Python and browser versions, baseline SQLite transaction strategy, and browser verification tooling before the first build. Verify the numeric work caps against generated fixtures as the engine develops. Any optional independent checker must be available offline and pinned before it is included in release verification.

[Official project inspiration](https://docs.google.com/document/d/1R5MyfVvn033KoXZXgXP65qRAXnhcjtVvO_VF7IxUZaA/edit?tab=t.ef9a30wzb1z5)
