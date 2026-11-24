# Computer Algebra Notebook

A planned offline project. The repository contains the product plan, technical specification, implementation backlog and an empty code scaffold (`algebra_notebook/`, `tests/`). No product feature is implemented.

## Program goal

Build a computer algebra system from nothing: exact arithmetic, symbolic integration, equation solving, Gröbner bases, calculus and proofs, in a notebook where every step can be checked by a small independent kernel.

The program is planned ([#28](https://github.com/jortega0033/computer-algebra-notebook/issues/28)). Phase 1 is the current epic [#1](https://github.com/jortega0033/computer-algebra-notebook/issues/1) and the only phase with tickets.

**Score.** Share of a pinned public integration test suite solved and verified by differentiation, per problem family.

| Phase | Content | Hours (rough) | Issue |
|---|---|---|---|
| 1 | The current epic and its tickets | 58 to 84 | [#1](https://github.com/jortega0033/computer-algebra-notebook/issues/1) |
| 2 | Algebra core | 140 to 240 | [#29](https://github.com/jortega0033/computer-algebra-notebook/issues/29) |
| 3 | Calculus | 180 to 320 | [#30](https://github.com/jortega0033/computer-algebra-notebook/issues/30) |
| 4 | Solving | 150 to 260 | [#31](https://github.com/jortega0033/computer-algebra-notebook/issues/31) |
| 5 | Functions and language | 130 to 220 | [#32](https://github.com/jortega0033/computer-algebra-notebook/issues/32) |
| 6 | Checked steps | 130 to 230 | [#33](https://github.com/jortega0033/computer-algebra-notebook/issues/33) |

About 790 to 1350 engineer hours in total: rough estimates, not measurements. The numbers in the score and the finish lines are targets until a run shows them. Only phase 1 has tickets to work; the sub-issues of a later phase are written when it starts. No single session is expected to reach the end.

## Plan

- [Full product plan and acceptance criteria](docs/PRD.md)
- [Technical specification and verification fixtures](docs/TECHNICAL_SPEC.md)
- [Implementation epic](https://github.com/jortega0033/computer-algebra-notebook/issues/1)

## Current status

The fixtures describe expected results for future checks. `python -m unittest` runs smoke tests only (every module imports, `--help` works). No working baseline is claimed. Required runtime versions and offline dependencies must be checked before the first build.

## Licensing

A license for this project has not been selected. Any upstream reference or adapted code must retain its applicable notices; see the plan.
