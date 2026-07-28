# DSGeorref — Software Architecture Repository v3.0

Baseline consolidada após as Fases A–E. O repositório contém arquitetura, requisitos, DDD, 57 ADRs definitivas, contratos, especificações executáveis, roadmap, histórias e TaskEnvelopes para Codex.

## Estado

- Arquitetura, requisitos, DDD, ADRs e especificações: aprovados.
- Runtime primário: CPython 3.12.13.
- Implementação: `BLOCKED_EXTERNAL` até o registro formal de autorização.
- Especificações congeladas: Prompt Bundle, Edit Case Registry, AIBackend, Template e Artifact.

## Entrada

Comece em `docs/02-architecture/sar/SAR-000-START-HERE.md`. Para a Fase E, leia `docs/02-architecture/specifications/README.md` e `docs/07-assurance/PHASE-E-SPECIFICATION-REVIEW-REPORT.md`.

## Validação

Execute `make verify`. O target inclui Architecture, Requirements, DDD, ADR, Specification Review e fitness functions Python.


## Fase F

A revisão sprint por sprint está em `docs/07-assurance/PHASE-F-SPRINT-REVIEW-REPORT.md`, com matriz de 868 issues e relatórios individuais para as 12 sprints.
## Fase G — CTO Review

A due diligence técnica final está em `docs/07-assurance/PHASE-G-CTO-REVIEW-REPORT.md`. Custos, capacidade, locks, dependências, saída de tecnologias, SLOs, recuperação, segurança, LGPD e rollback possuem contracts e gates executáveis.
