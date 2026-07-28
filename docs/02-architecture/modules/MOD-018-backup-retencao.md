# MOD-018 — Backup + Retenção

- **Componente arquitetural:** `COMP-018`
- **Camada:** `Capacidades transversais`
- **Domínios de entrega:** `DAT`, `OPS`
- **ADRs owners:** `ADR-027`

## Responsabilidade

BackupSet coordenado, restore drills, retention e GC reference-aware.

## Submódulos esperados

- `domain`: regras e tipos sem dependência de framework, quando aplicável.
- `application`: casos de uso, ports, Unit of Work e políticas.
- `adapters`: HTTP, CLI, persistence, provider ou runtime.
- `contracts`: schemas públicos, eventos e manifests versionados.
- `tests`: unitários, integração, contrato, segurança e evidência científica aplicável.

## Boundaries

### Responsabilidade exclusiva

BackupSet coordenado, restore drills, retention e GC reference-aware.

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
- **Contexts servidos:** `BC-013`, `BC-014`.
- **Regra:** adapters traduzem contratos; não concentram modelo de domínio nem acessam tabelas de múltiplos contexts sem ports.
- **Resultado:** `PASS`.

## Entrega

- **Épicos vinculados:** `EPIC-012`, `EPIC-013`, `EPIC-039`, `EPIC-040`, `EPIC-049`, `EPIC-061`, `EPIC-071`, `EPIC-072`, `EPIC-073`, `EPIC-074`, `EPIC-075`, `EPIC-077`, `EPIC-079`, `EPIC-083`, `EPIC-105`
- **Histórias vinculadas:** 90
- A lista integral está em `MODULE_INDEX.csv` e `STORY_INDEX.csv`.

## Escopo de código previsto

- `src/data/**`
- Paths exatos são sempre reduzidos pelo TaskEnvelope da história.
