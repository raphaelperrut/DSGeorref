# STORY-0684 / ISSUE-0794 — Consolidar slices e liberar integração: governança contínua do backlog e decomposição de épicos em histórias implementáveis

- **Tipo:** `História implementável`
- **Estado:** `Planned`
- **Épico pai:** `EPIC-110`
- **Sprint:** `SPRINT-001`
- **Domínio:** `FND`
- **Bounded Context:** `BC-001 — Governança de Engenharia e Entrega`
- **Papel executor:** `Tech Lead`
- **TaskEnvelope:** `.codex/tasks/TASK-0684.json`

## História de usuário

Como mantenedor de engenharia, preciso materializar a fundação executável para “governança contínua do backlog e decomposição de épicos em histórias implementáveis”, para que o resultado do épico seja implementável, verificável e integrável sem violar seus contratos.

## Resultado verificável


Consolidar todos os slices de requisitos, verificar compatibilidade dos outputs e liberar o nó de integração downstream.

## Escopo

- `tools/governance/governanca-continua-do-backlog-e-decomposicao-de-epico/consolidacao/**`
- `docs/03-engineering/contexts/engineering_governance/governanca-continua-do-backlog-e-decomposicao-de-epico/consolidacao/**`
## Fora de escopo

- Alterar ADR, contrato compartilhado ou regra de produto sem issue de decisão aprovada.
- Ampliar o escopo para outro épico ou introduzir dependência não declarada.
- Declarar gate aprovado sem evidência independente.

## Requisitos


Nenhum requisito de produto próprio. Os requisitos originais foram atribuídos aos slices explícitos listados em dependências.

## ADRs e contratos

- Nenhuma ADR exclusiva; aplicar as referências do épico pai.
- `contracts/README.md`

## Dependências



`STORY-0754`, `STORY-0755`, `STORY-0756`, `STORY-0757`, `STORY-0758`

## Critérios de aceitação


- [ ] Todos os slices vinculados estão concluídos no mesmo baseline candidato.
- [ ] Cobertura requisito→história permanece integral e sem duplicação normativa.
- [ ] Contratos e outputs dos slices integram sem colisão ou implementação redundante.
- [ ] Reviewer registra riscos residuais e libera dependentes.

## Testes obrigatórios


- `test_story_0684_slice_consolidation`

## Evidências obrigatórias

- Resultado dos testes no commit candidato.
- Lista de arquivos alterados e justificativa de escopo.
- Handoff com limitações, riscos residuais e impacto em contratos.
- Aprovação independente aplicável ao mesmo commit.

## Condições de parada

- Decisão material de produto ou arquitetura não resolvida.
- Contrato necessário ausente, contraditório ou não versionado.
- Colisão de write scope com lane ativa.
- Critério de aceitação sem teste ou evidência objetiva.

## Prompt de execução Codex

Leia `AGENTS.md`, `.codex/roles/ROLE-003-tech-lead.md`, este documento, o épico `EPIC-110` e o TaskEnvelope `TASK-0684`. Trabalhe somente nos paths permitidos. Implemente o menor incremento que satisfaça todos os critérios, execute os testes, registre evidências e interrompa quando qualquer condição de parada ocorrer.


## Revisão SAR

- **Estado arquitetural:** `RESOLVED`
- **Decisão tecnológica necessária antes de iniciar:** `Nenhuma`
- **Atributos de qualidade dominantes:** `integrabilidade`, `rastreabilidade`, `manutenibilidade`
- **Autoridade de dados:** PostgreSQL/PostGIS para estado; filesystem gerenciado para binários publicados; broker/telemetria são derivados.
- **Contrato de entrada:** referências e schemas listados no TaskEnvelope.
- **Contrato de saída:** artifact, código, schema, teste ou evidência versionada no commit candidato.
- **Migration/rollback:** obrigatório quando a história altera schema, estado persistido, artifact ou deployment; caso contrário `não aplicável` deve ser justificado no handoff.
- **Observabilidade:** falhas e transições relevantes devem emitir signal/event/audit sem cardinalidade ilimitada.
- **Gate de completude:** nenhum heading obrigatório vazio, placeholder, ID obsoleto ou dependência implícita.

`EVIDENCE_BOUND` não representa decisão arquitetural em aberto: indica parâmetro quantitativo cujo valor é promovido pelo Benchmark Profile declarado.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-001` — Governança de Engenharia e Entrega.
- **Impacto no modelo:** `LOCAL_MODEL`.
- **Upstreams permitidos:** `Nenhum`.
- **Regra de integração:** DTO, evento, port ou ACL publicado; entidade, repository, ORM model e state machine não atravessam o boundary.
- **Package de produção:** context-first conforme `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0794-01, AC-ISSUE-0794-02, AC-ISSUE-0794-03, AC-ISSUE-0794-04`
- **Base de requisitos:** `DERIVED_CONTROL`
- **ADRs governantes:** `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-006`, `ADR-007`, `ADR-008`
- **Decisão em aberto:** `Nenhuma`
- **Regra:** implementar somente os boundaries listados; divergência ou lacuna interrompe a tarefa.


## Specification Review — Fase E

- **Especificações aplicáveis:** `SPEC-001`, `SPEC-004`
- **Status:** `PASS`
- A história deve parar se texto, schema, exemplo ou versão aplicável estiver ausente ou contraditório.

## Sprint Review — Fase F

| Dimensão | Aplicabilidade | Resultado |
|---|---|---|
| Dependências | 5 predecessores explícitos | PASS |
| Arquivos | 2 write scopes; deny scopes declarados | PASS |
| API | NOT_APPLICABLE | PASS |
| Banco | NOT_APPLICABLE | PASS |
| Frontend | NOT_APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | NOT_APPLICABLE | PASS |
| Testes | 1 testes obrigatórios | PASS |
| Artefatos | EVIDENCE_ONLY | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | QA, Reviewer; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-001-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `MEDIUM`
- **Controles aplicáveis:** `CTO-003, CTO-004, CTO-006, CTO-012, CTO-013, CTO-015`
- **Gate de produção:** `IMPLEMENTATION_AUTHORIZATION`
- **Regra:** implementação não pode publicar claim de custo, escala, latência, GPU, RPO/RTO ou segurança sem a evidência listada no TaskEnvelope.
