# STORY-0759 / ISSUE-0869 — Validar automação fail-closed e idempotente: governança de decisões arquiteturais e manutenção da baseline normativa

- **Tipo:** `História implementável`
- **Estado:** `Planned`
- **Épico pai:** `EPIC-001`
- **Sprint:** `SPRINT-001`
- **Domínio:** `FND`
- **Bounded Context:** `BC-001 — Governança de Engenharia e Entrega`
- **Papel executor:** `QA`
- **TaskEnvelope:** `.codex/tasks/TASK-0759.json`

## História de usuário

Como responsável por qualidade, preciso validar a automação entregue por `STORY-0003` no mesmo commit candidato, para demonstrar que seus controles são fail-closed, idempotentes e verificáveis sem ampliar o write scope da lane DevOps.

## Resultado verificável

O teste `test_epic_001_automacao` passa contra o mesmo commit candidato final de `STORY-0003`, com evidência QA independente para os caminhos fail-closed e para a idempotência.

## Escopo

- `tests/fnd/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/test_automation.py`
- `evidence/qa/epic-001/story-0759/**`

## Fora de escopo

- Implementar ou alterar o validator e o workflow entregues por `STORY-0003`.
- Alterar contratos, schemas, examples, ADRs, código em `src/**` ou evidence DevOps.
- Validar commit diferente daquele submetido pela lane DevOps e pelo Reviewer.

## Requisitos

Nenhum requisito exclusivo; valida os controles derivados materializados por `STORY-0003`.

## ADRs e contratos

- Nenhuma ADR exclusiva; aplicar as referências do épico pai e de `STORY-0003`.
- `contracts/README.md`

## Dependências

`STORY-0003`

## Critérios de aceitação

- [ ] `test_epic_001_automacao` passa contra o mesmo commit candidato final produzido por `STORY-0003`.
- [ ] Estados de erro e caminhos fail-closed aplicáveis são exercitados sem fallback silencioso.
- [ ] Execuções repetidas demonstram idempotência e ausência de mutação indevida.
- [ ] A evidence QA registra resultados, diagnóstico, commit candidato e aprovação independente do Reviewer.

## Testes obrigatórios

- `test_epic_001_automacao`

## Evidências obrigatórias

- `evidence/qa/epic-001/story-0759/`
- Resultado do teste no mesmo commit candidato final de `STORY-0003`.
- Handoff QA com caminhos fail-closed, idempotência e riscos residuais.
- Aprovação independente do Reviewer no mesmo commit candidato.

## Condição de conclusão no fluxo

`STORY-0003` pode concluir sua lane de implementação quando suas obrigações DevOps estiverem satisfeitas, mas o próximo consumidor `STORY-0004` permanece bloqueado até esta Story validar o mesmo commit candidato final.

## Condições de parada

- O commit candidato difere daquele produzido por `STORY-0003`.
- O teste obrigatório ou seu contrato está ausente ou contraditório.
- O write scope exige alteração em path pertencente à lane DevOps.
- A aceitação não pode ser demonstrada por teste ou evidência QA objetiva.

## Prompt de execução Codex

Leia `AGENTS.md`, `.codex/roles/ROLE-008-qa.md`, este documento, o épico `EPIC-001` e o TaskEnvelope `TASK-0759`. Trabalhe somente nos paths permitidos, valide o mesmo commit candidato final de `STORY-0003`, execute o teste obrigatório, registre evidence QA e interrompa quando qualquer condição de parada ocorrer.

## Revisão SAR

- **Estado arquitetural:** `RESOLVED`
- **Decisão tecnológica necessária antes de iniciar:** `Nenhuma`
- **Atributos de qualidade dominantes:** `testabilidade`, `rastreabilidade`, `confiabilidade`
- **Autoridade de dados:** PostgreSQL/PostGIS para estado; filesystem gerenciado para binários publicados; broker/telemetria são derivados.
- **Contrato de entrada:** commit candidato final e interfaces materializadas por `STORY-0003`.
- **Contrato de saída:** teste e evidence QA versionados no mesmo commit candidato.
- **Migration/rollback:** `não aplicável`; esta Story não altera schema nem estado persistido.
- **Observabilidade:** falhas devem preservar o diagnóstico acionável produzido pela automação.
- **Gate de completude:** nenhum critério pode ser aprovado contra commit diferente da lane DevOps.

## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Impacto no modelo:** `NONE`.
- **Upstreams permitidos:** `Nenhum`.
- **Regra de integração:** a validação consome somente interfaces publicadas pela lane DevOps.
- **Package de produção:** `não aplicável`; nenhum código de produção é autorizado.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0869-01, AC-ISSUE-0869-02, AC-ISSUE-0869-03, AC-ISSUE-0869-04`
- **Base de requisitos:** `DERIVED_CONTROL`
- **ADRs governantes:** `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-033`, `ADR-034`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`; os critérios de validação foram transferidos de `STORY-0003` por decisão do Owner.
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`

## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-033`, `ADR-034`
- **Decisão em aberto:** `Nenhuma`
- **Regra:** validar somente os boundaries publicados por `STORY-0003`; divergência ou lacuna interrompe a tarefa.

## Specification Review — Fase E

- **Especificações aplicáveis:** `SPEC-001`, `SPEC-004`
- **Status:** `PASS`
- A Story deve parar se texto, schema, exemplo ou versão aplicável estiver ausente ou contraditório.

## Sprint Review — Fase F

| Dimensão | Aplicabilidade | Resultado |
|---|---|---|
| Dependências | 1 predecessor explícito | PASS |
| Arquivos | 2 write scopes mínimos; deny scopes declarados | PASS |
| API | NOT_APPLICABLE | PASS |
| Banco | NOT_APPLICABLE | PASS |
| Frontend | NOT_APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | NOT_APPLICABLE | PASS |
| Testes | 1 teste obrigatório | PASS |
| Artefatos | EVIDENCE_ONLY | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | Reviewer independente; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-001-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`

## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `CRITICAL`
- **Controles aplicáveis:** `CTO-002, CTO-003, CTO-004, CTO-006, CTO-012, CTO-013, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
- **Regra:** nenhum resultado QA autoriza claim de segurança ou produção sem a evidence listada no TaskEnvelope.
