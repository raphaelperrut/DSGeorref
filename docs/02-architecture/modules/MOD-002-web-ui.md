# MOD-002 — Web UI

- **Componente arquitetural:** `COMP-002`
- **Camada:** `Interfaces e superfícies`
- **Domínios de entrega:** `WEB`, `REV`, `EDU`
- **ADRs owners:** `ADR-002`, `ADR-028`, `ADR-048`

## Responsabilidade

Experiência guiada, workspace cartográfico, triagem e revisão.

## Submódulos esperados

- `domain`: regras e tipos sem dependência de framework, quando aplicável.
- `application`: casos de uso, ports, Unit of Work e políticas.
- `adapters`: HTTP, CLI, persistence, provider ou runtime.
- `contracts`: schemas públicos, eventos e manifests versionados.
- `tests`: unitários, integração, contrato, segurança e evidência científica aplicável.

## Boundaries

### Responsabilidade exclusiva

Experiência guiada, workspace cartográfico, triagem e revisão.

### Interfaces fornecidas

- Fornece `REST/SSE/polling` para `api`.

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
- **Contexts servidos:** `BC-016`.
- **Regra:** adapters traduzem contratos; não concentram modelo de domínio nem acessam tabelas de múltiplos contexts sem ports.
- **Resultado:** `PASS`.

## Entrega

- **Épicos vinculados:** `EPIC-031`, `EPIC-032`, `EPIC-033`, `EPIC-034`, `EPIC-035`, `EPIC-036`, `EPIC-062`, `EPIC-064`, `EPIC-084`
- **Histórias vinculadas:** 53
- A lista integral está em `MODULE_INDEX.csv` e `STORY_INDEX.csv`.

## Escopo de código previsto

- `src/web/**`
- Paths exatos são sempre reduzidos pelo TaskEnvelope da história.
