# MOD-012 — Filesystem gerenciado

- **Componente arquitetural:** `COMP-012`
- **Camada:** `Persistência e transporte`
- **Domínios de entrega:** `DAT`, `GEO`, `REP`
- **ADRs owners:** `ADR-018`, `ADR-041`, `ADR-027`

## Responsabilidade

Originais e ArtifactSets imutáveis, publicação atômica e checksums.

## Submódulos esperados

- `domain`: regras e tipos sem dependência de framework, quando aplicável.
- `application`: casos de uso, ports, Unit of Work e políticas.
- `adapters`: HTTP, CLI, persistence, provider ou runtime.
- `contracts`: schemas públicos, eventos e manifests versionados.
- `tests`: unitários, integração, contrato, segurança e evidência científica aplicável.

## Boundaries

### Responsabilidade exclusiva

Originais e ArtifactSets imutáveis, publicação atômica e checksums.

### Interfaces fornecidas

- Não fornece interface direta fora de seu boundary; participa por contratos compartilhados.

### Interfaces consumidas

- Consome `ArtifactSets/inputs` de `domain`.

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
- **Contexts servidos:** `BC-013`.
- **Regra:** adapters traduzem contratos; não concentram modelo de domínio nem acessam tabelas de múltiplos contexts sem ports.
- **Resultado:** `PASS`.

## Entrega

- **Épicos vinculados:** `EPIC-012`, `EPIC-013`, `EPIC-021`, `EPIC-022`, `EPIC-023`, `EPIC-024`, `EPIC-025`, `EPIC-026`, `EPIC-027`, `EPIC-028`, `EPIC-029`, `EPIC-030`, `EPIC-037`, `EPIC-038`, `EPIC-044`, `EPIC-045`, `EPIC-046`, `EPIC-047`, `EPIC-048`, `EPIC-049`, `EPIC-050`, `EPIC-051`, `EPIC-052`, `EPIC-053`, `EPIC-054`, `EPIC-055`, `EPIC-056`, `EPIC-057`, `EPIC-058`, `EPIC-059`, `EPIC-060`, `EPIC-061`, `EPIC-063`, `EPIC-070`, `EPIC-071`, `EPIC-073`, `EPIC-074`, `EPIC-093`, `EPIC-094`, `EPIC-095`, `EPIC-096`, `EPIC-097`, `EPIC-098`, `EPIC-099`, `EPIC-100`, `EPIC-101`, `EPIC-102`, `EPIC-103`, `EPIC-105`
- **Histórias vinculadas:** 332
- A lista integral está em `MODULE_INDEX.csv` e `STORY_INDEX.csv`.

## Escopo de código previsto

- `src/data/**`
- Paths exatos são sempre reduzidos pelo TaskEnvelope da história.
