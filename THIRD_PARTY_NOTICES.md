# Third-party dependency notices

The 0.0.0 foundation does not bundle third-party code for redistribution.
The following direct dependencies are used only to develop or validate the
repository. Their upstream distributions remain governed by their own
licenses. A release candidate must generate and verify a complete SBOM and
all applicable redistribution notices before the publication gate can pass.

| Ecosystem | Package | Version | License expression | Scope |
|---|---|---:|---|---|
| Python | PyYAML | 6.0.3 | MIT | validation |
| Python | jsonschema | 4.26.0 | MIT | validation |
| Python | cryptography | 50.0.1 | Apache-2.0 OR BSD-3-Clause | validation |
| Python | celery | 5.6.3 | BSD-3-Clause | validation |
| Python | psycopg[binary] | 3.3.5 | LGPL-3.0-only | validation |
| Python | pytest | 9.1.1 | MIT | validation |
| Python | ruff | 0.16.7 | MIT | validation |
| Python | mypy | 2.3.1 | MIT | validation |
| npm | @playwright/test | 1.62.1 | Apache-2.0 | development |
| npm | @testing-library/dom | 10.4.1 | MIT | development |
| npm | @types/node | 24.13.3 | MIT | development |
| npm | jsdom | 30.0.1 | MIT | development |
| npm | typescript | 6.0.3 | Apache-2.0 | development |
| npm | vitest | 4.1.11 | MIT | development |

The machine-readable source of this table and its input manifests is
`docs/03-engineering/contexts/engineering_governance/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/dependency-inventory.json`.
