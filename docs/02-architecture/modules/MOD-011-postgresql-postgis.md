# MOD-011 — PostgreSQL/PostGIS

- **Componente arquitetural:** `COMP-011`
- **Camada:** `Persistência e transporte`
- **Domínios de entrega:** `DAT`, `PLT`, `JOB`
- **ADRs owners:** `ADR-018`, `ADR-026`

## Responsabilidade

System of record para estado, geometrias, jobs, audit, lineage e outbox.

## Submódulos esperados

- `domain`: regras e tipos sem dependência de framework, quando aplicável.
- `application`: casos de uso, ports, Unit of Work e políticas.
- `adapters`: HTTP, CLI, persistence, provider ou runtime.
- `contracts`: schemas públicos, eventos e manifests versionados.
- `tests`: unitários, integração, contrato, segurança e evidência científica aplicável.

## Boundaries

### Responsabilidade exclusiva

System of record para estado, geometrias, jobs, audit, lineage e outbox.

### Interfaces fornecidas

- Não fornece interface direta fora de seu boundary; participa por contratos compartilhados.

### Interfaces consumidas

- Consome `UoW/system of record` de `domain`.
- Consome `estado/checkpoints/outbox` de `workers`.

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
- **Contexts servidos:** `BC-002`, `BC-003`, `BC-004`, `BC-005`, `BC-006`, `BC-007`, `BC-008`, `BC-009`, `BC-010`, `BC-011`, `BC-012`, `BC-013`, `BC-014`, `BC-015`.
- **Regra:** adapters traduzem contratos; não concentram modelo de domínio nem acessam tabelas de múltiplos contexts sem ports.
- **Resultado:** `PASS`.

## Entrega

- **Épicos vinculados:** `EPIC-008`, `EPIC-009`, `EPIC-010`, `EPIC-011`, `EPIC-012`, `EPIC-013`, `EPIC-014`, `EPIC-015`, `EPIC-016`, `EPIC-017`, `EPIC-018`, `EPIC-019`, `EPIC-049`, `EPIC-061`, `EPIC-065`, `EPIC-066`, `EPIC-067`, `EPIC-068`, `EPIC-069`, `EPIC-071`, `EPIC-073`, `EPIC-074`, `EPIC-082`, `EPIC-104`, `EPIC-105`
- **Histórias vinculadas:** 157
- A lista integral está em `MODULE_INDEX.csv` e `STORY_INDEX.csv`.

## Escopo de código previsto

- `src/data/**`
- Paths exatos são sempre reduzidos pelo TaskEnvelope da história.
