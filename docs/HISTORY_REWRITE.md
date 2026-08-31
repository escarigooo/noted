# History rewrite notice

Noted's Git history was rewritten on 2026-08-31 before public release. The
rewrite removed generated invoice PDFs, realistic legacy fixture identities,
an approximately 93 MB image archive, duplicate legacy source trees, and every
historical image or font that was not approved for redistribution. The current
synthetic fixture and the assets listed in `ASSET_PROVENANCE.md` were restored
after the cleanup. A personal author email was also replaced with the
repository owner's GitHub `noreply` address.

## Coordination rule

Any clone made before this rewrite must be discarded and cloned again. Do not
merge a branch based on the old history: that would make the removed objects
reachable again. A necessary unpublished change must instead be exported as a
patch and applied to a fresh clone.

The pre-rewrite `main` tip was `9b69a2f8c0692b54cff0e906f1799f5b1a22a6c7`.
The first changed commit reported by `git-filter-repo` was
`16288a7c01d4fd2b0b56835b4df10e1f9c5f4e5c`. Pull requests #1, #8, #9, and
#10 referenced the old history. The repository must remain private until the
GitHub-hosted pull-request refs and cached views have been handled.

## Validation performed

- compared the restored tree with the reviewed pre-rewrite tree;
- checked every reachable path and the largest reachable Git objects;
- scanned the complete rewritten history with Gitleaks;
- ran Ruff and the full pytest suite;
- verified the production container build and GitHub Actions after publication
  of the rewritten branch.

The verified offline recovery bundle is retained only for emergency recovery
and must never be pushed to a Git remote.
