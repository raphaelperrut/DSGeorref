# MOD-017 — Instalação + Supply Chain

- **Componente arquitetural:** `COMP-017`
- **Camada:** `Capacidades transversais`
- **Domínios de entrega:** `FND`, `OPS`, `SEC`, `REL`, `PUB`
- **ADRs owners:** `ADR-034`, `ADR-026`

## Responsabilidade

OCI/Compose, TLS, secrets, SBOM, assinaturas, upgrades e rollback.

## Submódulos esperados

- `domain`: regras e tipos sem dependência de framework, quando aplicável.
- `application`: casos de uso, ports, Unit of Work e políticas.
- `adapters`: HTTP, CLI, persistence, provider ou runtime.
- `contracts`: schemas públicos, eventos e manifests versionados.
- `tests`: unitários, integração, contrato, segurança e evidência científica aplicável.

## Boundaries

### Responsabilidade exclusiva

OCI/Compose, TLS, secrets, SBOM, assinaturas, upgrades e rollback.

### Interfaces fornecidas

- Não fornece interface direta fora de seu boundary; participa por contratos compartilhados.

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
- **Contexts servidos:** `BC-015`.
- **Regra:** adapters traduzem contratos; não concentram modelo de domínio nem acessam tabelas de múltiplos contexts sem ports.
- **Resultado:** `PASS`.

## Entrega

- **Épicos vinculados:** `EPIC-001`, `EPIC-002`, `EPIC-003`, `EPIC-004`, `EPIC-005`, `EPIC-006`, `EPIC-007`, `EPIC-039`, `EPIC-040`, `EPIC-041`, `EPIC-042`, `EPIC-043`, `EPIC-072`, `EPIC-075`, `EPIC-076`, `EPIC-077`, `EPIC-078`, `EPIC-079`, `EPIC-080`, `EPIC-081`, `EPIC-083`, `EPIC-085`, `EPIC-086`, `EPIC-087`, `EPIC-089`, `EPIC-090`, `EPIC-091`, `EPIC-092`, `EPIC-106`, `EPIC-107`, `EPIC-108`, `EPIC-109`, `EPIC-110`
- **Histórias vinculadas:** 184
- A lista integral está em `MODULE_INDEX.csv` e `STORY_INDEX.csv`.

## Escopo de código previsto

- `src/foundation/**`
- Paths exatos são sempre reduzidos pelo TaskEnvelope da história.
