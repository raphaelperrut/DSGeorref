# STORY-0457 / ISSUE-0567 — Definir modelo, invariantes e contratos de dados: RetentionPolicy por classe/estado/dependência, holds e preview de impacto

- **Tipo:** `História implementável`
- **Estado:** `Planned`
- **Épico pai:** `EPIC-073`
- **Sprint:** `SPRINT-011`
- **Domínio:** `DAT`
- **Bounded Context:** `BC-013 — Artifacts, Proveniência e Lifecycle`
- **Papel executor:** `Arquiteto`
- **TaskEnvelope:** `.codex/tasks/TASK-0457.json`

## História de usuário

Como operador geoespacial, preciso definir modelo, invariantes e contratos de dados para “RetentionPolicy por classe/estado/dependência, holds e preview de impacto”, para que o resultado do épico seja implementável, verificável e integrável sem violar seus contratos.

## Resultado verificável

Definir modelo, invariantes e contratos de dados para a capacidade **RetentionPolicy por classe/estado/dependência, holds e preview de impacto**, com saída versionada, testes e evidência no commit candidato.

## Escopo

- `contracts/contexts/artifact_provenance/dat/retentionpolicy-por-classe-estado-dependencia-holds-e/**`
- `docs/02-architecture/design-reviews/retentionpolicy-por-classe-estado-dependencia-holds-e/**`
## Fora de escopo

- Alterar ADR, contrato compartilhado ou regra de produto sem issue de decisão aprovada.
- Ampliar o escopo para outro épico ou introduzir dependência não declarada.
- Declarar gate aprovado sem evidência independente.

## Requisitos

`REQ-RET-001`

## ADRs e contratos

- `ADR-039`
- `ADR-027`
- `contracts/README.md`
- `contracts/http/openapi.yaml`

## Dependências


`STORY-0301`, `STORY-0384`

## Critérios de aceitação

- [ ] O resultado de “RetentionPolicy por classe/estado/dependência, holds e preview de impacto” é observável por contrato, interface, artifact ou evidência executável.
- [ ] Os requisitos REQ-RET-001 possuem evidência explícita no commit candidato.
- [ ] Estados de erro e caminhos fail-closed aplicáveis são testados, sem fallback silencioso.
- [ ] Schemas, estados, compatibilidade e autoridade de dados estão versionados e revisados pelo Arquiteto.

## Testes obrigatórios

- `test_retention_policy_protected_lineage_hold_dry_run`
- `test_epic_073_contrato`

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

Leia `AGENTS.md`, `.codex/roles/ROLE-002-arquiteto.md`, este documento, o épico `EPIC-073` e o TaskEnvelope `TASK-0457`. Trabalhe somente nos paths permitidos. Implemente o menor incremento que satisfaça todos os critérios, execute os testes, registre evidências e interrompa quando qualquer condição de parada ocorrer.


## Revisão SAR

- **Estado arquitetural:** `RESOLVED`
- **Decisão tecnológica necessária antes de iniciar:** `Nenhuma`
- **Atributos de qualidade dominantes:** `modificabilidade`, `compatibilidade`, `integridade`
- **Autoridade de dados:** PostgreSQL/PostGIS para estado; filesystem gerenciado para binários publicados; broker/telemetria são derivados.
- **Contrato de entrada:** referências e schemas listados no TaskEnvelope.
- **Contrato de saída:** artifact, código, schema, teste ou evidência versionada no commit candidato.
- **Migration/rollback:** obrigatório quando a história altera schema, estado persistido, artifact ou deployment; caso contrário `não aplicável` deve ser justificado no handoff.
- **Observabilidade:** falhas e transições relevantes devem emitir signal/event/audit sem cardinalidade ilimitada.
- **Gate de completude:** nenhum heading obrigatório vazio, placeholder, ID obsoleto ou dependência implícita.

`EVIDENCE_BOUND` não representa decisão arquitetural em aberto: indica parâmetro quantitativo cujo valor é promovido pelo Benchmark Profile declarado.


## Domain-Driven Design — Fase C

- **Contexto owner:** `BC-013` — Artifacts, Proveniência e Lifecycle.
- **Impacto no modelo:** `PUBLIC_CONTRACT`.
- **Upstreams permitidos:** `BC-002, BC-003, BC-005, BC-006, BC-007, BC-008, BC-009, BC-011`.
- **Regra de integração:** DTO, evento, port ou ACL publicado; entidade, repository, ORM model e state machine não atravessam o boundary.
- **Package de produção:** context-first conforme `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0567-01, AC-ISSUE-0567-02, AC-ISSUE-0567-03, AC-ISSUE-0567-04`
- **Base de requisitos:** `MIXED`
- **ADRs governantes:** `ADR-003`, `ADR-004`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-016`
- **Decisão em aberto:** `Nenhuma`
- **Regra:** implementar somente os boundaries listados; divergência ou lacuna interrompe a tarefa.


## Specification Review — Fase E

- **Especificações aplicáveis:** `SPEC-001`, `SPEC-004`, `SPEC-005`
- **Status:** `PASS`
- A história deve parar se texto, schema, exemplo ou versão aplicável estiver ausente ou contraditório.

## Sprint Review — Fase F

| Dimensão | Aplicabilidade | Resultado |
|---|---|---|
| Dependências | 2 predecessores explícitos | PASS |
| Arquivos | 2 write scopes; deny scopes declarados | PASS |
| API | APPLICABLE | PASS |
| Banco | APPLICABLE | PASS |
| Frontend | NOT_APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | NOT_APPLICABLE | PASS |
| Testes | 2 testes obrigatórios | PASS |
| Artefatos | PRODUCT_AND_EVIDENCE | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | Arquiteto, Reviewer; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-011-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `HIGH`
- **Controles aplicáveis:** `CTO-001, CTO-002, CTO-003, CTO-004, CTO-005, CTO-006, CTO-008, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `BENCHMARK_AND_OPERATIONS_GATES`
- **Regra:** implementação não pode publicar claim de custo, escala, latência, GPU, RPO/RTO ou segurança sem a evidência listada no TaskEnvelope.
