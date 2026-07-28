# STORY-0223 / ISSUE-0333 — Expor consulta, download e visualização: persistência e exportação escalável de resultados por imagem/lote, geometrias, manifestos e checksums

- **Tipo:** `História implementável`
- **Estado:** `Planned`
- **Épico pai:** `EPIC-037`
- **Sprint:** `SPRINT-010`
- **Domínio:** `REP`
- **Bounded Context:** `BC-012 — Resultados, Diagnósticos e Exportação`
- **Papel executor:** `Frontend`
- **TaskEnvelope:** `.codex/tasks/TASK-0223.json`

## História de usuário

Como revisor e auditor, preciso expor consulta, download e visualização para “persistência e exportação escalável de resultados por imagem/lote, geometrias, manifestos e checksums”, para que o resultado do épico seja implementável, verificável e integrável sem violar seus contratos.

## Resultado verificável

Expor consulta, download e visualização para a capacidade **persistência e exportação escalável de resultados por imagem/lote, geometrias, manifestos e checksums**, com saída versionada, testes e evidência no commit candidato.

## Escopo

- `src/frontend/src/contexts/results_reporting/features/persistencia-e-exportacao-escalavel-de-resultados-por/**`
## Fora de escopo

- Alterar ADR, contrato compartilhado ou regra de produto sem issue de decisão aprovada.
- Ampliar o escopo para outro épico ou introduzir dependência não declarada.
- Declarar gate aprovado sem evidência independente.

## Requisitos

`REQ-BEX-001`, `REQ-EPIC-037`, `REQ-QUAL-002`, `REQ-QUAL-003`, `REQ-RMR-003`

## ADRs e contratos

- `ADR-018`
- `ADR-046`
- `ADR-039`
- `ADR-048`
- `ADR-041`
- `ADR-050`
- `ADR-053`
- `ADR-026`
- `contracts/README.md`
- `contracts/http/openapi.yaml`

## Dependências


`STORY-0220`

## Critérios de aceitação

- [ ] O resultado de “persistência e exportação escalável de resultados por imagem/lote, geometrias, manifestos e checksums” é observável por contrato, interface, artifact ou evidência executável.
- [ ] Os requisitos REQ-BEX-001, REQ-EPIC-037, REQ-QUAL-002, REQ-QUAL-003, REQ-RMR-003 possuem evidência explícita no commit candidato.
- [ ] Estados de erro e caminhos fail-closed aplicáveis são testados, sem fallback silencioso.
- [ ] API, CLI ou UI preserva idempotência, autorização e Problem Details aplicáveis.

## Testes obrigatórios

- `test_batch_execution_decision_01`
- `test_success_failure_name_relative_path_exports`
- `test_quality_profile_metric_threshold_gate_lineage`
- `test_input_output_deformation_profile_and_heatmap`
- `test_epic_037_superficie`

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

Leia `AGENTS.md`, `.codex/roles/ROLE-005-frontend.md`, este documento, o épico `EPIC-037` e o TaskEnvelope `TASK-0223`. Trabalhe somente nos paths permitidos. Implemente o menor incremento que satisfaça todos os critérios, execute os testes, registre evidências e interrompa quando qualquer condição de parada ocorrer.


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

- **Contexto owner:** `BC-012` — Resultados, Diagnósticos e Exportação.
- **Impacto no modelo:** `LOCAL_MODEL`.
- **Upstreams permitidos:** `BC-002, BC-003, BC-004, BC-006, BC-007, BC-008, BC-010, BC-011, BC-013`.
- **Regra de integração:** DTO, evento, port ou ACL publicado; entidade, repository, ORM model e state machine não atravessam o boundary.
- **Package de produção:** context-first conforme `DDD-090-CONTEXT-OWNERSHIP-AND-CODE-LAYOUT.md`.
- **Resultado:** `PASS`.

## Revisão de Requisitos — Fase B

- **Resultado:** `PASS`
- **Critérios rastreados:** `AC-ISSUE-0333-01, AC-ISSUE-0333-02, AC-ISSUE-0333-03, AC-ISSUE-0333-04`
- **Base de requisitos:** `MIXED`
- **ADRs governantes:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-014`, `ADR-039`, `ADR-046`, `ADR-050`
- **Conflito:** `Nenhum`
- **Redundância funcional:** `Nenhuma`
- **Requisito faltante:** `Não`
- **Requisito impossível:** `Não`
- **Dependência circular:** `Não`
- **Matriz canônica:** `docs/07-assurance/ACCEPTANCE_CRITERION_TRACEABILITY.csv`


## Revisão de ADRs — Fase D

- **Resultado:** `PASS`
- **ADRs aplicáveis:** `ADR-002`, `ADR-003`, `ADR-004`, `ADR-005`, `ADR-006`, `ADR-007`, `ADR-008`, `ADR-010`, `ADR-011`, `ADR-012`, `ADR-014`, `ADR-016`, `ADR-025`, `ADR-039`, `ADR-046`, `ADR-050`
- **Decisão em aberto:** `Nenhuma`
- **Regra:** implementar somente os boundaries listados; divergência ou lacuna interrompe a tarefa.


## Specification Review — Fase E

- **Especificações aplicáveis:** `SPEC-001`, `SPEC-004`, `SPEC-005`
- **Status:** `PASS`
- A história deve parar se texto, schema, exemplo ou versão aplicável estiver ausente ou contraditório.

## Sprint Review — Fase F

| Dimensão | Aplicabilidade | Resultado |
|---|---|---|
| Dependências | 1 predecessores explícitos | PASS |
| Arquivos | 1 write scopes; deny scopes declarados | PASS |
| API | APPLICABLE | PASS |
| Banco | APPLICABLE | PASS |
| Frontend | APPLICABLE | PASS |
| Geo | NOT_APPLICABLE | PASS |
| IA | NOT_APPLICABLE | PASS |
| Testes | 5 testes obrigatórios | PASS |
| Artefatos | PRODUCT_AND_EVIDENCE | PASS |
| Critérios | 4 critérios com IDs estáveis | PASS |
| Review | Arquiteto, QA, Reviewer; mesmo commit candidato | PASS |

- **Matriz canônica:** `docs/07-assurance/PHASE-F-ISSUE-DELIVERY-REVIEW.csv`
- **Relatório da sprint:** `docs/07-assurance/phase-f/SPRINT-010-REVIEW.md`
- **Baseline:** `SAR-v2.9-PHASE-F`
- **Resultado:** `PASS`
## CTO Review — Fase G

- **Resultado:** `PASS`
- **Risk tier:** `CRITICAL`
- **Controles aplicáveis:** `CTO-001, CTO-002, CTO-003, CTO-004, CTO-005, CTO-006, CTO-008, CTO-009, CTO-010, CTO-011, CTO-012, CTO-013, CTO-014, CTO-015`
- **Gate de produção:** `SECURITY_AND_PRIVACY_GATES`
- **Regra:** implementação não pode publicar claim de custo, escala, latência, GPU, RPO/RTO ou segurança sem a evidência listada no TaskEnvelope.
