# STORY-0204 / ISSUE-0314 — Consolidar slices e liberar integração: painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos

- **Tipo:** `História implementável`
- **Estado:** `Planned`
- **Épico pai:** `EPIC-034`
- **Sprint:** `SPRINT-009`
- **Domínio:** `WEB`
- **Bounded Context:** `BC-016 — Experiência e Orientação do Operador`
- **Papel executor:** `Frontend`
- **TaskEnvelope:** `.codex/tasks/TASK-0204.json`

## História de usuário

Como operador geoespacial, preciso integrar contratos e cliente tipado para “painel de qualidade do lote, busca server-side, filtros salvos, triagem, deformação e retry/revisão de subconjuntos”, para que o resultado do épico seja implementável, verificável e integrável sem violar seus contratos.

## Resultado verificável


Consolidar todos os slices de requisitos, verificar compatibilidade dos outputs e liberar o nó de integração downstream.

## Escopo

- `src/frontend/src/contexts/operator_experience/features/painel-de-qualidade-do-lote-busca-server-side-filtros/consolidacao/**`
## Fora de escopo

- Alterar ADR, contrato compartilhado ou regra de produto sem issue de decisão aprovada.
- Ampliar o escopo para outro épico ou introduzir dependência não declarada.
- Declarar gate aprovado sem evidência independente.

## Requisitos


Nenhum requisito de produto próprio. Os requisitos originais foram atribuídos aos slices explícitos listados em dependências.

## ADRs e contratos

- `ADR-046`
- `ADR-039`
- `ADR-048`
- `contracts/README.md`
- `contracts/http/openapi.yaml`

## Dependências



`STORY-0741`, `STORY-0742`

## Critérios de aceitação


- [ ] Todos os slices vinculados estão concluídos no mesmo baseline candidato.
- [ ] Cobertura requisito→história permanece integral e sem duplicação normativa.
- [ ] Contratos e outputs dos slices integram sem colisão ou implementação redundante.
- [ ] Reviewer registra riscos residuais e libera dependentes.

## Testes obrigatórios


- `test_story_0204_slice_consolidation`

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

Leia `AGENTS.md`, `.codex/roles/ROLE-005-frontend.md`, este documento, o épico `EPIC-034` e o TaskEnvelope `TASK-0204`. Trabalhe somente nos paths permitidos. Implemente o menor incremento que satisfaça todos os critérios, execute os testes, registre evidências e interrompa quando qualquer condição de parada ocorrer.


## Revisão SAR

- **Estado arquitetural:** `RESOLVED`
- **Decisão tecnológica necessária antes de iniciar:** `Nenhuma`
- **Atributos de qualidade dominantes:** `usabilidade`, `acessibilidade`, `segurança Web`
- **Autoridade de dados:** PostgreSQL/PostGIS para estado; filesystem gerenciado para binários publicados; broker/telemetria são derivados.
- **Contrato de entrada:** referências e schemas listados no TaskEnvelope.
- **Contrato de saída:** artifact, código, schema, teste ou evidência versionada no commit candidato.
- **Migration/rollback:** obrigatório quando a história altera schema, estado persistido, artifact ou deployment; caso contrário `não aplicável` deve ser justificado no handoff.
- **Observabilidade:** falhas e transições relevantes devem emitir signal/event/audit sem cardinalidade ilimitada.
- **Gate de completude:** nenhum heading obrigatório vazio, placeholder, ID obsoleto ou dependência implícita.

`EVIDENCE_BOUND` não representa decisão arquitetural em aberto: indica parâmetro quantitativo cujo valor é promovido pelo Benchmark Profile declarado.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-016` — Experiência e Orientação do Operador.
- **Impacto no modelo:** `LOCAL_MODEL`.
- **Upstreams permitidos:** `BC-002, BC-003, BC-012, BC-013, BC-014`.
- **Regra de integração:** DTO, evento, port ou ACL publicado; entidade, repository, ORM model e state machine não atravessam o boundary.
- **Package de produção:** context-first conforme `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0314-01, AC-ISSUE-0314-02, AC-ISSUE-0314-03, AC-ISSUE-0314-04`
- **Base de requisitos:** `DERIVED_CONTROL`
- **ADRs governantes:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-014`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-014`
- **Decisão em aberto:** `Nenhuma`
- **Regra:** implementar somente os boundaries listados; divergência ou lacuna interrompe a tarefa.


## Specification Review — Fase E

- **Especificações aplicáveis:** `SPEC-001`, `SPEC-004`
- **Status:** `PASS`
- A história deve parar se texto, schema, exemplo ou versão aplicável estiver ausente ou contraditório.

## Sprint Review — Fase F

| Dimensão | Aplicabilidade | Resultado |
|---|---|---|
| Dependências | 2 predecessores explícitos | PASS |
| Arquivos | 1 write scopes; deny scopes declarados | PASS |
| API | NOT_APPLICABLE | PASS |
| Banco | NOT_APPLICABLE | PASS |
| Frontend | APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | NOT_APPLICABLE | PASS |
| Testes | 1 testes obrigatórios | PASS |
| Artefatos | EVIDENCE_ONLY | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | QA, Reviewer; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-009-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `MEDIUM`
- **Controles aplicáveis:** `CTO-001, CTO-003, CTO-004, CTO-005, CTO-006, CTO-008, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `IMPLEMENTATION_AUTHORIZATION`
- **Regra:** implementação não pode publicar claim de custo, escala, latência, GPU, RPO/RTO ou segurança sem a evidência listada no TaskEnvelope.
