# MOD-003 — HTTP API

- **Componente arquitetural:** `COMP-003`
- **Camada:** `Interfaces e superfícies`
- **Domínios de entrega:** `FND`, `PLT`, `JOB`, `REP`
- **ADRs owners:** `ADR-002`, `ADR-028`

## Responsabilidade

Comandos e consultas REST, OpenAPI, SSE e polling de reconciliação.

## Submódulos esperados

- `domain`: regras e tipos sem dependência de framework, quando aplicável.
- `application`: casos de uso, ports, Unit of Work e políticas.
- `adapters`: HTTP, CLI, persistence, provider ou runtime.
- `contracts`: schemas públicos, eventos e manifests versionados.
- `tests`: unitários, integração, contrato, segurança e evidência científica aplicável.

## Boundaries

### Responsabilidade exclusiva

Comandos e consultas REST, OpenAPI, SSE e polling de reconciliação.

### Interfaces fornecidas

- Fornece `adapta contratos` para `domain`.
- Fornece `federação opcional` para `oidc`.

### Interfaces consumidas

- Consome `REST/SSE/polling` de `web`.

### Autoridade de dados

- Não cria fonte de verdade paralela. Estado de domínio e execução é autoritativo no PostgreSQL/PostGIS; binários publicados são autoritativos no filesystem gerenciado.
- Caches, SSE, filas, logs e views são derivados e reconciliáveis.

### Dependências proibidas

- UI, CLI ou worker não implementam regra de negócio exclusiva.
- Nenhum módulo acessa path arbitrário, secret, payload interno do broker ou tabela de outro boundary sem port/contrato aprovado.
- Dependência circular entre módulos é proibida; shared code exige responsabilidade explícita.

### Contratos e qualidade

- Contratos públicos: `contracts/` e `docs/02-architecture/sar/SAR-070-CONTRACT-VIEW.md`.
- Qualidades obrigatórias: integridade, auditabilidade, reprodutibilidade, segurança, observabilidade e recuperação conforme `SAR-030-QUALITY-ATTRIBUTE-SCENARIOS.md`.
- Mudança de boundary requer ADR; mudança local compatível segue Application Profile e issue.


## Domain-Driven Design — Fase C

- **Natureza:** componente/módulo técnico; não é bounded context.
- **Contexts servidos:** `BC-002`, `BC-003`, `BC-004`, `BC-005`, `BC-006`, `BC-007`, `BC-008`, `BC-009`, `BC-010`, `BC-011`, `BC-012`, `BC-013`, `BC-014`, `BC-015`, `BC-016`.
- **Regra:** adapters traduzem contratos; não concentram modelo de domínio nem acessam tabelas de múltiplos contexts sem ports.
- **Resultado:** `PASS`.

## Entrega

- **Épicos vinculados:** `EPIC-001`, `EPIC-002`, `EPIC-003`, `EPIC-004`, `EPIC-005`, `EPIC-006`, `EPIC-007`, `EPIC-008`, `EPIC-009`, `EPIC-010`, `EPIC-011`, `EPIC-014`, `EPIC-015`, `EPIC-016`, `EPIC-017`, `EPIC-018`, `EPIC-019`, `EPIC-037`, `EPIC-038`, `EPIC-065`, `EPIC-066`, `EPIC-067`, `EPIC-068`, `EPIC-069`, `EPIC-070`, `EPIC-082`, `EPIC-086`, `EPIC-090`, `EPIC-091`, `EPIC-092`, `EPIC-104`, `EPIC-110`
- **Histórias vinculadas:** 187
- A lista integral está em `MODULE_INDEX.csv` e `STORY_INDEX.csv`.

## Escopo de código previsto

- `src/foundation/**`
- Paths exatos são sempre reduzidos pelo TaskEnvelope da história.
