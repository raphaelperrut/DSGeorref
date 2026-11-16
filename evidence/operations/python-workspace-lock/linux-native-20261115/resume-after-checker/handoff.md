# TASK-0773 execution candidate
Current operational result: results.json in this directory. The parent directory's
stage1 result/failure files are preserved historical evidence from the checker stop;
none of those bytes were changed. preserved-before.sha256 and preserved-final-check.txt
bind the exact original manifest, lock and all prior execution evidence.
Checker fix from approved 94ab889c32f5d21f74c5353fa1489c9247b76743 was integrated
through current main e2123eb4ac178103b1169ced32c2b680d3d320fb using normal merge
f38ae67dfbdacad8a371247c54054a1d715da5cf, retaining all prior evidence commits.
The four checker files are identical to main and are not candidate-owned changes.
Graph and supplement authority and bootstrap digests remain in the preserved
execution-state.json. No graph, pin, wheel artifact, VM_LOCAL or BP-003 changes.
Only the independent second checkout generated a lock, from no lock and an empty
resolver cache; the first lock was never regenerated. Both locks have the required
bd70e02748e7f09b5ca7fd544862f3b7d1deec30365a65c66552795839ce5cf2 SHA-256.
Frozen runtime inventory: 37 packages. Full dev/test and offline inventory: 54.
Inventory reconciliation, active marker/extra audit and artifact identities pass.
Offline install used a new virtual environment and the complete first-install cache
(4110 files recorded by digest), with uv --offline enforcing no network fallback.
make verify is FAIL due solely to missing pnpm after all Python quality steps pass.
See make-verify-classification.md for scope and limitations. Twenty pertinent tests
and the runtime crypto/psycopg smoke pass. No PostgreSQL test, benchmark, API image,
TLS configuration or production readiness is claimed.
The second checkout shares the merged source tree and exact approved manifest with
the eventual candidate; the candidate adds evidence and the first lock only.
Independent QA and Reviewer must assess the final local candidate SHA and the make
verify limitation; the executor does not approve its own candidate. No publication.
Rollback: revert only candidate pyproject.toml and uv.lock; preserve evidence.
The container, backup /tmp/task0773-state, independent checkout, cache and environments
are retained for inspection. A local Git bundle is exported for handoff.
