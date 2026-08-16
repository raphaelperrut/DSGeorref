# ISSUE-0798 — ADR overlap targeted repair evidence

## Candidate and repair boundary

The repair commit containing this report is layered directly on rejected
candidate `4fef80156ae97423b38afc703f416f98ae976488`. The rejected candidate was
not amended, reset or rebased.

This repair changes only the ADR overlap validator, its focused mandatory-test
coverage and this implementation evidence. It does not implement ISSUE-0802 or
ISSUE-0803 and does not revisit the findings that targeted QA already passed.

## Accurate QA history

Targeted QA rejected `4fef80156ae97423b38afc703f416f98ae976488`
with one remaining HIGH. Lifecycle authority, ISM approval/history, canonical
Sprint roots and TaskEnvelope/scope were independently reported as PASS and are
not claimed as work performed by this repair.

The remaining HIGH demonstrated that a materially overlapping ADR decision
could be paraphrased and accepted when the caller supplied an empty or
incomplete `overlapping_adr_ids` collection. The prior implementation report's
claim that material ADR overlap was closed exceeded what QA demonstrated and is
superseded by this history.

## ADR overlap repair

The validator still derives exact decision-clause matches, shared owned
requirements and explicit supersession from governed ADR artifacts. It now also
derives a deterministic similarity signal for paraphrased decision clauses when
the canonical ADR index places both decisions in an intersecting bounded
context. The signal requires at least three shared normalized terms covering at
least half of the shorter clause. Per the existing TEST_STRATEGY rule,
similarity triggers review; it does not itself create a new architectural
decision.

Caller-provided overlap IDs are combined with independently derived candidates
and therefore cannot prove absence of overlap. A derived overlap remains
blocking until the governed ADR metadata and caller supersession claim agree.
An unreadable ADR named by the canonical index now produces
`ADR_AUTHORITY_INVALID` instead of being skipped.

## Regression and targeted validation

The focused regression reproduces the rejected-candidate bypass with a
PostgreSQL/RabbitMQ decision paraphrase and an empty caller overlap collection.
It also exercises an unrelated browser-theme decision and verifies that the
validator does not classify every ADR change as overlap.

- paraphrased overlap rejected: PASS;
- non-overlap accepted: PASS;
- ISSUE-0798 mandatory/adversarial tests: PASS;
- applicable FND regression: PASS;
- independent paraphrased-overlap reproduction: PASS;
- `git diff --check`: PASS.

No scope audit was required because the effective authorized file set did not
change. No repository-wide verification or unrelated QA finding was re-audited
for this targeted repair.
