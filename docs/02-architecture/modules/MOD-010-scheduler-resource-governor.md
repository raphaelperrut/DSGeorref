# MOD-010 — Scheduler + Resource Governor

- **Componente arquitetural:** `COMP-010`
- **Camada:** `Execução e orquestração`
- **Domínios de entrega:** `JOB`, `OPS`
- **ADRs owners:** `ADR-039`, `ADR-054`

## Responsabilidade

Fairness, backpressure, leases, fencing, quotas e budgets de CPU/RAM/GPU/disco.

## Submódulos esperados

- `domain`: regras e tipos sem dependência de framework, quando aplicável.
- `application`: casos de uso, ports, Unit of Work e políticas.
- `adapters`: HTTP, CLI, persistence, provider ou runtime.
- `contracts`: schemas públicos, eventos e manifests versionados.
- `tests`: unitários, integração, contrato, segurança e evidência científica aplicável.

## Boundaries

### Responsabilidade exclusiva

Fairness, backpressure, leases, fencing, quotas e budgets de CPU/RAM/GPU/disco.

### Interfaces fornecidas

- Fornece `admission/fairness/resources` para `workers`.

### Interfaces consumidas

- Não consome interface direta de outro módulo no modelo de contexto.

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
- **Contexts servidos:** `BC-010`.
- **Regra:** adapters traduzem contratos; não concentram modelo de domínio nem acessam tabelas de múltiplos contexts sem ports.
- **Resultado:** `PASS`.

## Entrega

- **Épicos vinculados:** `EPIC-014`, `EPIC-015`, `EPIC-016`, `EPIC-017`, `EPIC-018`, `EPIC-019`, `EPIC-039`, `EPIC-040`, `EPIC-065`, `EPIC-066`, `EPIC-067`, `EPIC-068`, `EPIC-069`, `EPIC-072`, `EPIC-075`, `EPIC-077`, `EPIC-079`, `EPIC-083`, `EPIC-104`
- **Histórias vinculadas:** 126
- A lista integral está em `MODULE_INDEX.csv` e `STORY_INDEX.csv`.

## Escopo de código previsto

- `src/jobs/**`
- Paths exatos são sempre reduzidos pelo TaskEnvelope da história.
