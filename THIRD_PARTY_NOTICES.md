# Third-party dependency notices

Stage A builds a frontend containing direct runtime npm dependencies. Development
and validation tools remain outside the application bundle. Upstream distributions
remain governed by their own licenses. A release candidate must generate and
verify a complete SBOM and all applicable redistribution notices before the
publication gate can pass. This direct-dependency reference table does not replace
upstream copyright/license texts required for redistribution.

| Ecosystem | Package | Version | License expression | Scope |
|---|---|---:|---|---|
| Python | PyYAML | 6.0.3 | MIT | validation |
| Python | jsonschema | 4.26.0 | MIT | validation |
| Python | cryptography | 50.0.2 | Apache-2.0 OR BSD-3-Clause | validation |
| Python | celery | 5.7.0 | BSD-3-Clause | validation |
| Python | psycopg[binary] | 3.3.8 | LGPL-3.0-only | validation |
| Python | pytest | 9.2.0 | MIT | validation |
| Python | ruff | 0.17.4 | MIT | validation |
| Python | mypy | 2.4.1 | MIT | validation |
| npm | @playwright/test | 1.62.1 | Apache-2.0 | development |
| npm | @testing-library/dom | 10.4.1 | MIT | development |
| npm | @types/node | 24.13.3 | MIT | development |
| npm | jsdom | 30.0.1 | MIT | development |
| npm | typescript | 6.0.3 | Apache-2.0 | development |
| npm | vitest | 4.1.12 | MIT | development |
| npm | react | 19.2.4 | MIT | runtime |
| npm | react-dom | 19.2.4 | MIT | runtime |
| npm | @hey-api/openapi-ts | 0.97.3 | MIT | development |
| npm | @oasdiff-js/oasdiff-js | 1.0.0 | Apache-2.0 | development |
| npm | @types/react | 19.2.14 | MIT | development |
| npm | @types/react-dom | 19.2.3 | MIT | development |
| npm | vite | 8.1.6 | MIT | development |
| npm | yaml | 2.8.3 | ISC | development |

The generated OpenAPI client includes the Fetch runtime from @hey-api/openapi-ts 0.97.3. The local compatibility patch modifies templates from that release. Both retain Hey API's upstream copyright and [MIT license](LICENSES/MIT.txt).

The machine-readable source of this table and its input manifests is
`docs/03-engineering/contexts/engineering_governance/license-citation-cff-contribuicao-dco-cla-e-gate-de-pu/dependency-inventory.json`.
