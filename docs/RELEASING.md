# Releasing

There is no release yet and no ticket in epic #1 publishes one. Only the owner releases.

## What a release is here

A tagged commit on `main` with the notebook runnable from a clean checkout: `python -m unittest` is green and the clean-checkout list in `docs/verification.md` (introduced by ticket #7) has been followed. There is no package to publish and no build step.

## Steps (owner only)

1. Confirm CI is green on `main` for Linux and Windows, Python 3.12 and 3.13.
2. Run `python -m unittest` and the clean-checkout list from a fresh clone. Record the output.
3. Move the `Unreleased` entries in `CHANGELOG.md` under a new version heading with the date, in a pull request, and merge it.
4. Tag the merge commit `vX.Y.Z` and push the tag.
5. Create the GitHub release from the tag with the changelog section as notes.

Agents never tag, release or publish. Choosing a licence is a separate owner decision (D10) and is not part of a release.
