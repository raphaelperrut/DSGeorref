# STORY-0003 / ISSUE-0113 — Automatizar validações e controles: governança de decisões arquiteturais e manutenção da baseline normativa

- **Tipo:** `História implementável`
- **Estado:** `Done`
- **Épico pai:** `EPIC-001`
- **Sprint:** `SPRINT-001`
- **Domínio:** `FND`
- **Bounded Context:** `BC-001 — Governança de Engenharia e Entrega`
- **Papel executor:** `DevOps`
- **TaskEnvelope:** `.codex/tasks/TASK-0003.json`

## História de usuário

Como mantenedor de engenharia, preciso automatizar validações e controles para “governança de decisões arquiteturais e manutenção da baseline normativa”, para que o resultado do épico seja implementável, verificável e integrável sem violar seus contratos.

## Resultado verificável

Automatizar validações e controles para a capacidade **governança de decisões arquiteturais e manutenção da baseline normativa**, com validator e workflow versionados, execução read-only determinística, diagnóstico acionável e evidence DevOps no commit candidato.

## Escopo

- `tools/quality/contexts/engineering_governance/governanca-de-decisoes-arquiteturais-e-manutencao-da-b/**`
- `.github/workflows/governanca-de-decisoes-arquiteturais-e-manutencao-da-b.yaml`
- `evidence/operations/epic-001/story-0003/**`
## Fora de escopo

- Alterar ADR, contrato compartilhado ou regra de produto sem issue de decisão aprovada.
- Ampliar o escopo para outro épico ou introduzir dependência não declarada.
- Declarar gate aprovado sem evidência independente.

## Requisitos

Nenhum requisito exclusivo; valida integração do épico.

## ADRs e contratos

- Nenhuma ADR exclusiva; aplicar as referências do épico pai.
- `contracts/README.md`

## Dependências


`STORY-0001`

## Critérios de aceitação

- [ ] O validator versionado avalia os contratos aplicáveis com saída determinística, read-only e diagnóstico acionável.
- [ ] O workflow executa o validator e preserva status e diagnóstico suficientes para a validação QA no commit candidato.
- [ ] A automação não altera ADRs, contratos congelados ou estado do produto e suporta dry-run quando qualquer ação potencialmente destrutiva for aplicável.
- [ ] A evidence DevOps registra saída do validator, execução do workflow, arquivos alterados e justificativa de escopo.

## Testes obrigatórios

- `test_epic_001_contrato`

## Evidências obrigatórias

- Resultado dos testes no commit candidato.
- Lista de arquivos alterados e justificativa de escopo.
- Handoff com limitações, riscos residuais e impacto em contratos.
- Aprovação independente aplicável ao mesmo commit.

## Condição de conclusão no fluxo

Esta lane pode concluir quando validator, workflow, diagnóstico e evidence DevOps estiverem satisfeitos. O fluxo de delivery permanece bloqueado para `STORY-0004` até `STORY-0759` validar o mesmo commit candidato final.

## Condições de parada

- Decisão material de produto ou arquitetura não resolvida.
- Contrato necessário ausente, contraditório ou não versionado.
- Colisão de write scope com lane ativa.
- Critério de aceitação sem teste ou evidência objetiva.

## Prompt de execução Codex

Leia `AGENTS.md`, `.codex/roles/ROLE-009-devops.md`, este documento, o épico `EPIC-001` e o TaskEnvelope `TASK-0003`. Trabalhe somente nos paths permitidos. Implemente o menor incremento que satisfaça todos os critérios, execute a validação contratual, registre evidence DevOps e entregue o mesmo commit candidato para `STORY-0759`. Interrompa quando qualquer condição de parada ocorrer.


## Revisão SAR

- **Estado arquitetural:** `RESOLVED`
- **Decisão tecnológica necessária antes de iniciar:** `Nenhuma`
- **Atributos de qualidade dominantes:** `operabilidade`, `disponibilidade`, `supply chain`
- **Autoridade de dados:** PostgreSQL/PostGIS para estado; filesystem gerenciado para binários publicados; broker/telemetria são derivados.
- **Contrato de entrada:** referências e schemas listados no TaskEnvelope.
- **Contrato de saída:** artifact, código, schema, teste ou evidência versionada no commit candidato.
- **Migration/rollback:** obrigatório quando a história altera schema, estado persistido, artifact ou deployment; caso contrário `não aplicável` deve ser justificado no handoff.
- **Observabilidade:** falhas e transições relevantes devem emitir signal/event/audit sem cardinalidade ilimitada.
- **Gate de completude:** nenhum heading obrigatório vazio, placeholder, ID obsoleto ou dependência implícita.

`EVIDENCE_BOUND` não representa decisão arquitetural em aberto: indica parâmetro quantitativo cujo valor é promovido pelo Benchmark Profile declarado.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Impacto no modelo:** `NONE`.
- **Upstreams permitidos:** `Nenhum`.
- **Regra de integração:** DTO, evento, port ou ACL publicado; entidade, repository, ORM model e state machine não atravessam o boundary.
- **Package de produção:** context-first conforme `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0113-01, AC-ISSUE-0113-02, AC-ISSUE-0113-03, AC-ISSUE-0113-04`
- **Base de requisitos:** `DERIVED_CONTROL`
- **ADRs governantes:** `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-033`, `ADR-034`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-009`, `ADR-033`, `ADR-034`
- **Decisão em aberto:** `Nenhuma`
- **Regra:** implementar somente os boundaries listados; divergência ou lacuna interrompe a tarefa.


## Specification Review — Fase E

- **Especificações aplicáveis:** `SPEC-001`, `SPEC-004`
- **Status:** `PASS`
- A história deve parar se texto, schema, exemplo ou versão aplicável estiver ausente ou contraditório.

## Sprint Review — Fase F

| Dimensão | Aplicabilidade | Resultado |
|---|---|---|
| Dependências | 1 predecessores explícitos | PASS |
| Arquivos | 3 write scopes; deny scopes declarados | PASS |
| API | NOT_APPLICABLE | PASS |
| Banco | NOT_APPLICABLE | PASS |
| Frontend | NOT_APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | NOT_APPLICABLE | PASS |
| Testes | 1 validação contratual obrigatória | PASS |
| Artefatos | EVIDENCE_ONLY | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | QA, Reviewer; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-001-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `CRITICAL`
- **Controles aplicáveis:** `CTO-002, CTO-003, CTO-004, CTO-006, CTO-012, CTO-013, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
- **Regra:** implementação não pode publicar claim de custo, escala, latência, GPU, RPO/RTO ou segurança sem a evidência listada no TaskEnvelope.
