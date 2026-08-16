# Comece aqui

## Ordem de contexto mínimo

1. `docs/01-product/PRD.md`
2. `docs/02-architecture/MODULE_CATALOG.md` e o módulo atribuído
3. relatório da Fase A em `docs/07-assurance/PHASE-A-ARCHITECTURE-REVIEW-REPORT.md`
4. sprint e backlog em `docs/06-delivery/sprints/` e `sprint-backlogs/`
5. épico pai
6. história/issue filha
7. TaskEnvelope em `.codex/tasks/`
8. requisitos, ADRs e contratos referenciados
9. `AGENTS.md` aplicável ao path de escrita

## Inventário ativo

- 376 requisitos
- 22 ADRs
- 18 módulos
- 12 sprints
- 110 épicos
- 759 histórias implementáveis
- 869 issues
- 759 tarefas Codex

## Regra de execução

Nenhum agente escolhe trabalho por conta própria. O Tech Lead atribui uma história cujo grafo esteja liberado e cujo write scope não colida. QA e Reviewer validam o mesmo commit candidato de forma independente.


## Fechamento da Fase A (2.6.0)

Arquitetura aprovada, ações AR-ACT-001 a AR-ACT-004 encerradas, 22 ADRs aceitas e entrada na Fase B autorizada.

## Fase B — Requirements Review (2.6.0)

Revisão concluída e aprovada: 12 sprints, 869 issues, 376 requisitos, 22 ADRs e todos os critérios de aceite reconciliados. Zero conflito, requisito impossível ou ciclo bloqueante permanece aberto.
## Fase G — CTO Review

A due diligence técnica final está em `docs/07-assurance/PHASE-G-CTO-REVIEW-REPORT.md`. Custos, capacidade, locks, dependências, saída de tecnologias, SLOs, recuperação, segurança, LGPD e rollback possuem contracts e gates executáveis.
